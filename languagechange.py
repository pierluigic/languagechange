import json
import os
from pathlib import Path
from platformdirs import user_cache_dir
import dload

class LanguageChange():

    def __init__(self):
        self.cache_dir = user_cache_dir("languagechange", "Change is Key!")
        self.resources_dir = os.path.join(self.cache_dir, 'resources')
        self.models_dir = os.path.join(self.cache_dir, 'models')
        Path(self.resources_dir).mkdir(parents=True, exist_ok=True)
        Path(self.models_dir).mkdir(parents=True, exist_ok=True)
        self.load_resources_hub()

    def load_resources_hub(self):
        #self.resource_hub = json.load()
        with open('resources_hub.json','r') as f:
            self.resource_hub = json.load(f)

    def download_ui(self):
        j = 0
        list_resources = []

        for resource_type in self.resource_hub:
            print('########################')
            print('###### '+resource_type+' ######')
            print('########################\n')
            for resource_name in self.resource_hub[resource_type]:
                print(resource_name)
                print('---------------------')
                for dataset in self.resource_hub[resource_type][resource_name]:
                    print('\t -'+dataset)
                    for version in self.resource_hub[resource_type][resource_name][dataset]:
                        print(f'\t\t{j}) '+version)
                        list_resources.append([resource_type,resource_name,dataset,version])
                        j = j + 1
                print('\n')

        findchoice = False

        while not findchoice:
            choice = input(f'Select an option (0-{j}), digit -1 to exit: ')
            try:
                choice = int(choice.strip())
                if choice >= -1 and choice <= j:
                    findchoice = True
                else:
                    print(f'Only numbers in the range (0-{j}) are allowed, digit -1 to exit.')
            except:
                print(f'Only numbers in the range (0-{j}) are allowed, digit -1 to exit.')

        if not choice == -1:

            options = {'yes':1,'y':1,'no':0,'n':0}
            confirm = ""

            while not confirm.strip().lower() in {'yes','y','no','n'}:
                choice_resource = '/'.join(list_resources[choice])
                confirm = input(f'You have choice {choice} ({choice_resource}), do you confirm your choice? (yes/y/no/n): ')
            
            confirm = options[confirm]
            if confirm:
                print('Downloading the required resource...')
                self.download(*list_resources[choice])
                print('Completed!')
            else:
                self.download_ui()

    def download(self, resource_type, resource_name, dataset, version):
        try:
            destination_path = os.path.join(self.resources_dir,resource_type,resource_name,dataset,version)
            Path(destination_path).mkdir(parents=True, exist_ok=True)
            dload.save_unzip(self.resource_hub[resource_type][resource_name][dataset][version], destination_path)
        except:
            print('Cannot download the resource.')

    def get_resource(self, resource_type, resource_name, dataset, version):
        path = os.path.join(self.resources_dir,resource_type,resource_name,dataset,version)
        if os.path.exists(path):
            return path
        else:
            self.download(resource_type, resource_name, dataset, version)
            return path

