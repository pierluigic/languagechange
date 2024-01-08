import torch
import numpy as np
from collections import defaultdict
from typing import Tuple, List, Union, Any
from languagechange.usages import TargetUsage
from languagechange.representation import ContextualizedModel
from transformers import AutoTokenizer, AutoModel
from WordTransformer import WordTransformer, InputExample

class ContextualizedEmbeddings():
    def __str__(self):
        return 'ContextualizedEmbeddings({\n    features: ' + f'{self.column_names}' + f',\n    num_rows: {self.num_rows}' + '\n})'

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def from_usages(target_usages: List[TargetUsage], raw_embedding: np.array):
        columns = defaultdict(list)

        for i, target_usage in enumerate(target_usages):
            columns['token'].append(target_usage.token)
            columns['target'].append(target_usage.target)
            columns['context'].append(target_usage.context)
            columns['start'].append(target_usage.start)
            columns['end'].append(target_usage.end)
            columns['embedding'].append(raw_embedding[i])

        embs = ContextualizedEmbeddings.from_dict(columns)
        return embs.with_format("np")

class XL_LEXEME(ContextualizedModel):

    def __init__(self, pretrained_model: str = 'pierluigic/xl-lexeme',
                 device: str = 'cuda',
                 n_extra_tokens: int = 0):
        super().__init__(device=device, n_extra_tokens=n_extra_tokens)

        self._model = WordTransformer(pretrained_model, device=device)

    def encode(self, target_usages: Union[TargetUsage, List[TargetUsage]],
               batch_size: int = 8) -> np.array:
        super(XL_LEXEME, self).encode(target_usages=target_usages, batch_size=batch_size)
        if isinstance(target_usages, TargetUsage):
            target_usages = [target_usages]

        examples = list()

        for target_usage in target_usages:
            start, end = target_usage.offsets.split(':')
            start, end = int(start), int(end)
            examples.append(InputExample(texts=target_usage.context, positions=[start, end]))

        raw_embeddings = self._model.encode(examples, batch_size=batch_size, device=self._device)
        return ContextualizedEmbeddings.from_usages(target_usages, raw_embeddings)

class BERT(ContextualizedModel):
    def __init__(self, pretrained_model: str,
                 device: str = 'cuda',
                 n_extra_tokens: int = 2):
        super().__init__(device=device, n_extra_tokens=n_extra_tokens)

        self._tokenizer = AutoTokenizer.from_pretrained(pretrained_model)
        self._model = AutoModel.from_pretrained(pretrained_model)
        self._token_type_ids = True

    def split_context(self, target_usage: TargetUsage) -> Tuple[List[str],
                                                                List[str],
                                                                List[str]]:
        start, end = target_usage.offsets.split(':')
        start, end = int(start), int(end)

        right_context = target_usage.context[:start]
        token_occurrence = target_usage.context[start:end]
        left_context = target_usage.context[end:]

        left_tokens = self._tokenizer.tokenize(right_context, return_tensors='pt')
        target_tokens = self._tokenizer.tokenize(token_occurrence, return_tensors='pt')
        right_tokens = self._tokenizer.tokenize(left_context, return_tensors='pt')

        return left_tokens, target_tokens, right_tokens

    def center_usage(self,
                     left_tokens: List[str],
                     target_tokens: List[str],
                     right_tokens: List[str]) -> Tuple[List[str],
                                                       List[str],
                                                       List[str]]:

        max_seq_len = self._tokenizer.model_max_length - self._n_extra_tokens

        overflow_left = len(left_tokens) - int((max_seq_len - len(target_tokens)) / 2)
        overflow_right = len(right_tokens) - int((max_seq_len - len(target_tokens)) / 2)

        if overflow_left > 0 and overflow_right > 0:
            left_tokens = left_tokens[overflow_left:]
            right_tokens = right_tokens[:len(right_tokens) - overflow_right]

        elif overflow_left > 0 and overflow_right <= 0:
            left_tokens = left_tokens[overflow_left:]

        else:
            right_tokens = right_tokens[:len(right_tokens) - overflow_right]

        return left_tokens, target_tokens, right_tokens

    def add_special_tokens(self, left_tokens: List[str],
                           target_tokens: List[str],  # for additional extensions
                           right_tokens: List[str]) -> Tuple[List[str],
                                                             List[str],
                                                             List[str]]:

        left_tokens = [self._tokenizer.cls_token] + left_tokens
        right_tokens = right_tokens + [self._tokenizer.sep_token]
        return left_tokens, target_tokens, right_tokens

    def process_input_tokens(self,
                             tokens: List[str]) -> dict[str, Union[list[int], Any]]:
        max_seq_len = self._tokenizer.model_max_length

        input_ids_ = self._tokenizer.convert_tokens_to_ids(tokens)
        attention_mask_ = [1] * len(input_ids_)

        offset_len = max_seq_len - len(input_ids_)
        input_ids_ += [self._tokenizer.convert_tokens_to_ids(self._tokenizer.pad_token)] * offset_len
        attention_mask_ += [0] * offset_len

        token_type_ids_ = [0] * len(input_ids_)

        processed_input = {'input_ids': input_ids_,
                           'token_type_ids': token_type_ids_,
                           'attention_mask': attention_mask_}
        if self._token_type_ids:
            del processed_input['token_type_ids']

        return processed_input

    def batch_encode(self, target_usages: List[TargetUsage]) -> np.array:
        target_embeddings = list()
        examples = defaultdict(list)
        target_offsets = defaultdict(list)

        for target_usage in target_usages:
            left_tokens, target_tokens, right_tokens = self.split_context(target_usage)
            left_tokens, target_tokens, right_tokens = self.center_usage(left_tokens,
                                                                         target_tokens,
                                                                         right_tokens)
            left_tokens, target_tokens, right_tokens = self.add_special_tokens(left_tokens,
                                                                               target_tokens,
                                                                               right_tokens)

            # start and end in terms of tokens
            start, end = len(left_tokens), len(left_tokens) + len(target_tokens)
            target_offsets['start'].append(start)
            target_offsets['end'].append(end)

            tokens = left_tokens + target_tokens + right_tokens
            processed_input = self.process_input_tokens(tokens)

            for k, v in processed_input.items():
                examples[k].append(v)

        for k in examples:
            examples[k] = torch.tensor(examples[k]).to(self._device)

        output = self._model(**examples)

        embeddings = output.last_hidden_state
        for i in range(embeddings.size(0)):
            start, end = target_offsets['start'][i], target_offsets['end'][i]
            target_embedding = embeddings[i, start:end, :].mean(axis=0)
            target_embeddings.append(target_embedding.detach().numpy())

        return np.array(target_embeddings)

    def encode(self, target_usages: Union[TargetUsage, List[TargetUsage]],
               batch_size: int = 8) -> np.array:
        super(BERT, self).encode(target_usages=target_usages, batch_size=batch_size)

        if isinstance(target_usages, TargetUsage):
            target_usages = [target_usages]

        target_embeddings = list()

        num_usages = len(target_usages)
        for i in range(0, num_usages, batch_size):
            batch_target_usages = target_usages[i: min(i + num_usages, batch_size)]
            target_embeddings.append(self.batch_encode(batch_target_usages))

        raw_embeddings = np.concat(target_embeddings, axis=0)

        return ContextualizedEmbeddings.from_usages(target_usages, raw_embeddings)

class RoBERTa(BERT):
    def __init__(self, pretrained_model: str,
                 device: str = 'cuda',
                 n_extra_tokens: int = 2):
        super().__init__(pretrained_model=pretrained_model, device=device, n_extra_tokens=n_extra_tokens)

        self._token_type_ids = False