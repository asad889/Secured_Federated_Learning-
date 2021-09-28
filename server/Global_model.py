import pandas as pd     						        #to read the file out from exce
import torch 	 						            #to make tensors
from torch.utils.data import Dataset 					#to upload Data set
import numpy as np                                      #to manipulate data
import torch.nn as nn 							        #for implementing basic neural network
import torch.nn.functional as F                         #for neural network
import torch.optim as optim
import sys
sys.path.append('/home/asadnaveed/PycharmProjects/Secured_Federated_Learning-')

from client.data_preprocessing import *
from client.Client_1 import Client_1
from client.Client_2 import Client_2

data_file = pd.read_csv('/home/asadnaveed/PycharmProjects/Secured_Federated_Learning-/client/data_usage_train_several_server.csv')
users_split_1=users_split[0]
users_split_2=users_split[1]

class Arguments():
	def __init__(self):
		self.dataset_count = 4000
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

torch.manual_seed(0)
global_model = Net()
global_dict = global_model.state_dict()

class Global_model:
	def  __init__(self,model_1,model_2):
		self.model_1 = model_1
		self.model_2 = model_2
	def Intialization(self):

		torch.save(global_model.state_dict(), "Global_model.txt")
		print(global_model.state_dict())
	def aggregation(self):
		model_1 = torch.load(self.model_1)
		model_2 = torch.load(self.model_2)
		samples = (args.dataset_count / args.clients) / args.dataset_count
		client_model = [model_1,model_2]

		for k in global_dict.keys():
			global_dict[k] = torch.stack([client_model[i][k] *samples for i in range(len(client_model))],0).sum(0)
		global_model.load_state_dict(global_dict)
		print("________________________")
		print("parameters from GLOBAL_MODEL")
		print("________________________")
		print(global_model.state_dict())
		torch.save(global_model.state_dict(),"Global_model.txt")
		global_model.state_dict()
f_name_1 = "fedavg_1.txt"
f_name_2 = "fedavg_2.txt"

for round in range(3):
	print("@@@@@@@@")
	print("@@@@@@@@")
	print("round number is")
	print(round)
	print("@@@@@@@@")
	print("@@@@@@@@")
	if round == 0:
		print("INTILIZATION")
		print("--------------")
		print("--------------")
		Gl_md = Global_model(f_name_1, f_name_2)
		Gl_md.Intialization()
		print("--------------")
		print("--------------")

	else:
		print("naveed")
		c = Client_1(users_split_1, data_file)
		c.Training()
		c2 = Client_2(users_split_2, data_file)
		c2.Training()
		Gl_md = Global_model(f_name_1, f_name_2)
		Gl_md.aggregation()





        
        
        
        
        
