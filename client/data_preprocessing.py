import pandas as pd     						        #to read the file out from exce
import torch as T	 						            #to make tensors
from torch.utils.data import Dataset 					#to upload Data set
import numpy as np                                      #to manipulate data
import torch.nn as nn 							        #for implementing basic neural network
import torch.nn.functional as F                         #for neural network
import torch.optim as optim                             #optimizer for neural network

print("***********************************")
print("Reading data from excel file")
print("***********************************")
data_file = pd.read_csv('data_usage_train_several_server.csv')  #reading data file from the dataset
print("***********************************")

class Data_division(T.utils.data.Dataset):
    def __init__(self, src_file,data_index):
        all_xy = src_file
        tmp_x = all_xy.iloc[data_index, 1:8].values                      # all rows, cols [0,6)
        tmp_y = all_xy.iloc[data_index, 8].values                        # 1-D required

        self.x_data = \
            T.tensor(tmp_x, dtype=T.float32)
        self.y_data = \
            T.tensor(tmp_y, dtype=T.int64)

    def __len__(self):
        return len(self.x_data)

    def __getitem__(self, idx):
        preds = self.x_data[idx]
        trgts = self.y_data[idx]
        sample = {'predictors' : preds,
                  'targets' : trgts}
        return sample


class Arguments():
    def __init__(self):
        self.dataset_count = 4000    					#no. of Data sample
        self.clients = 2      					#no of clients, we need
        self.rounds = 5						#no.of rounds
        self.epochs = 2
        self.local_batches = 10
        self.lr = 0.01
        self.C = 0.9
        self.drop_rate = 0.1
        self.torch_seed = 0
        self.log_interval = 2
        self.iid = 'iid'
        self.split_size = int(self.dataset_count / self.clients)
args = Arguments()

def data_set_split(data_file, clients):
    rsc_alloc_p_clients = int(data_file/ clients)
    users_dict, indeces = {}, [i for i in range(data_file)]
    for i in range(clients):
        np.random.seed(i)
        users_dict[i] = set(np.random.choice(indeces, rsc_alloc_p_clients, replace=False))
        indeces = list(set(indeces) - users_dict[i])
    return users_dict

users_split = data_set_split(args.dataset_count, args.clients)





