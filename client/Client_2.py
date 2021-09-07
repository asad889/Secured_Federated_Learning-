from data_preprocessing import *
import torch

client_2 = {}
n = list(users_split[1])
Load_2 = Data_division(data_file,n)
print("***********************************")
print("Splitting Data between clients")
print("***********************************")
client_2['dataset']     = torch.utils.data.DataLoader(Load_2)  #reading data file from the dataset
print("***********************************")

model_2 = torch.load("Global_model.pt")

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

torch.manual_seed(args.torch_seed)
client_2['model'] = Net()
client_2['model'].load_state_dict(model_2)
client_2['optim'] = optim.SGD(client_2['model'].parameters(), lr=args.lr)
client_2['model'].train()
loss_func = torch.nn.CrossEntropyLoss()  # apply log-softmax()

for epoch in range(1, args.epochs + 1):
    for (batch_idx, batch) in enumerate(client_2['dataset']):
        X = batch['predictors']  # inputs
        Y = batch['targets']
        client_2['optim'].zero_grad()
        output = client_2['model'](X)
        loss_val = loss_func(output, Y)  # avg loss in batch
        loss_val.backward()
        client_2['optim'].step()
        print('client Train Epoch: {} [{}/{}         ({:.0f}%)]\tLoss: {:.6f}'.format(
                         epoch, batch_idx , len(client_2['dataset']) ,
                              100. * batch_idx / len(client_2['dataset']), loss_val))
                              
client_2_model=client_2['model'] 
print(client_2_model.state_dict())
torch.save(client_2_model.state_dict(),"fedavg_2.pt")
