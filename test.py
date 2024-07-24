from languagechange.benchmark import SemEval2020Task1



semeval_en = SemEval2020Task1('EN')

corpus1 = semeval_en.corpus1_lemma

from languagechange.models.representation.static import StaticModel, CountModel,PPMI,SVD
from languagechange.models.representation.alignment import OrthogonalProcrustes

count_encoder1 = CountModel(corpus1, window_size=10, savepath='count_matrix1')
count_encoder1.encode()


"""
svd_encoder1 = SVD(count_encoder, dimensionality=25, gamma=0.1, savepath='svd1_count_matrix')
#svd_encoder1.encode()
#PPMI_encoder = PPMI(count_encoder, 5, 0.1, 'ppmi_matrix')
#PPMI_encoder.encode()
#svd_encoder = SVD(count_encoder, dimensionality=25, gamma=0.1, savepath='svd_count_matrix')
#svd_encoder.encode()
#count_encoder.load()
#svd_encoder.load()
#print(svd_encoder['hello'])
#print(svd_encoder['hello'].shape)
#print(svd_encoder.matrix().shape)

corpus2 = semeval_en.corpus2_lemma
count_encoder2 = CountModel(corpus2, 5, 'count_matrix2')
#count_encoder2.encode()
svd_encoder2 = SVD(count_encoder2, dimensionality=25, gamma=0.1, savepath='svd2_count_matrix')
#svd_encoder2.encode()


alignment = OrthogonalProcrustes('aligned1','aligned2')
#alignment.align(svd_encoder1, svd_encoder2)


aligned1 = StaticModel('aligned1')
aligned2 = StaticModel('aligned2')
aligned1.load()
aligned2.load()

print(aligned1['word'])

print(aligned2['word'])
"""
"""
target_words = list(semeval_en.binary_task.keys())
print([str(t) for t in target_words])

from languagechange.models.representation.contextualized import BERT

bert = BERT('bert-base-uncased', device='cpu')

usages = corpus1.search(target_words)
print(usages.keys())

print(len(usages['graft_nn']))
vectors = bert.encode(usages['graft_nn'])
print(vectors.shape)
"""