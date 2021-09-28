from client.data_preprocessing import *
import torch


class Client_2:
    def __init__(self, users_split, dataset):
        self.users_split = users_split
        self.dataset = dataset

    def Training(self):
        client = {}
        n = list(self.users_split)
        Load = Data_division(self.dataset, n)
        #print("***********************************")
        #print("Splitting Data between clients")
        #print("***********************************")
        client['dataset'] = torch.utils.data.DataLoader(Load,
                                                        batch_size=args.local_batches)  # reading data file from the dataset
        #print(args.local_batches)
        #print("***********************************")

        model = torch.load("Global_model.txt")

        class Net(nn.Module):
            def __init__(self):
                super(Net, self).__init__()

                self.fc1 = nn.Linear(7, 10)
                self.fc2 = nn.Linear(10, 10)
                self.fc3 = nn.Linear(10, 6)

            def forward(self, x):
                x = F.relu(self.fc1(x))
                x = F.relu(self.fc2(x))
                x = torch.sigmoid(self.fc3(x))

                return x

        torch.manual_seed(args.torch_seed)
        client['model'] = Net()
        client['model'].load_state_dict(model)
        print("--------------------")
        client['optim'] = optim.SGD(client['model'].parameters(), lr=args.lr)
        client['model'].train()
        loss_func = torch.nn.CrossEntropyLoss()  # apply log-softmax()

        for epoch in range(1, args.epochs + 1):

            for (batch_idx, batch) in enumerate(client['dataset']):
                X = batch['predictors']
                Y = batch['targets']

                client['optim'].zero_grad()
                output = client['model'](X)

                loss_val = loss_func(output, Y)  # avg loss in batch
                loss_val.backward()
                client['optim'].step()
                '''print('client Train Epoch: {} [{}/{}         ({:.0f}%)]\tLoss: {:.6f}'.format(
                                 epoch, batch_idx , len(client_1['dataset']) ,
                                      100. * batch_idx / len(client_1['dataset']), loss_val))'''

        client_2_model = client['model']
        print("________________________")
        print("parameters from client_1")
        print("________________________")
        print(client_2_model.state_dict())

        torch.save(client_2_model.state_dict(), "fedavg_2.txt")
        return (client_2_model.state_dict())