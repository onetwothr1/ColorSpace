import pickle
import torch
import torch.nn as nn
from torch.utils.data import DataLoader


'''
data shape
ex) [[3, (50,120,38), (85,200,5)],
     [0, (220,52,135), (200,83,121)],
      ... ]
'''
with open('data.pickle', 'rb') as f:
    data = pickle.load(f)
dataloader = DataLoader(data, batch_size=len(data), shuffle=True)

def train(model, n_epoch, criterion, optimizer, scheduler=None, scale=1, epoch_step=200):
    # save the initial state
    model.show_space(save=True, epoch=0)
    torch.save(model.state_dict(), model.param_dir + f'{model.model_name} epoch 0.pt')

    loss_list = []
    for epoch in range(n_epoch):
        running_loss = 0
        
        for data in dataloader:
            answer, color1, color2 = data
            answer = answer.type(torch.FloatTensor).cuda()
            color1 = color1.type(torch.FloatTensor).cuda()
            color2 = color2.type(torch.FloatTensor).cuda()

            optimizer.zero_grad()

            output1 = model(color1)
            output2 = model(color2)
            dist = nn.functional.pairwise_distance(output1, output2)

            loss = criterion(dist, answer * scale)
            loss = loss.type(torch.FloatTensor)
            loss.backward()

            optimizer.step()

            if scheduler:
              scheduler.step()

            running_loss += loss.item()
        
        epoch_loss = running_loss / len(data)
        loss_list.append(epoch_loss)
        
        if (epoch+1)%epoch_step==0:
          print('Epoch {}  loss: {:.4f}'.format(epoch+1, epoch_loss))
          model.show_space(save=True, epoch=epoch+1)
          torch.save(model.state_dict(), model.param_dir + f'{model.model_name} epoch {epoch+1}.pt')
          with open(model.train_history_dir + 'train history.pickle', 'wb') as f:
            pickle.dump(loss_list, f, pickle.HIGHEST_PROTOCOL)

    print("Successfullly finished.")