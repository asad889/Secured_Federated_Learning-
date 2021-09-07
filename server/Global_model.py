import pandas as pd     						        #to read the file out from exce
import torch 	 						            #to make tensors
from torch.utils.data import Dataset 					#to upload Data set
import numpy as np                                      #to manipulate data
import torch.nn as nn 							        #for implementing basic neural network
import torch.nn.functional as F                         #for neural network
import torch.optim as optim  


model_1 = torch.load("fedavg_1.pt")
model_2 = torch.load("fedavg_2.pt")
print(model_1)
print("--------------")
print(model_2)
print("--------------")
class Arguments():
    def __init__(self):
        self.dataset_count = 4000     					#no. of Data sample
        self.clients = 2
args = Arguments()

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()

        self.fc1 = nn.Linear(7, 10)
        self.fc2 = nn.Linear(10, 10)
        self.fc3 = nn.Linear(10, 6)


    def forward(self, x):
        x = F.relu( self.fc1 (x))
        x = F.relu( self.fc2 (x))
        x = torch.sigmoid(self.fc3 (x))

        return x

samples = (args.dataset_count / args.clients) / args.dataset_count

global_model= Net()

		
global_dict = global_model.state_dict()

client_model = [model_1,model_2]

for k in global_dict.keys():
	global_dict[k] = torch.stack([client_model[i][k] *samples for i in range(len(client_model))],0).sum(0)
global_model.load_state_dict(global_dict)

print(global_model.state_dict())

torch.save(global_model.state_dict(),"Global_model.pt")










        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
