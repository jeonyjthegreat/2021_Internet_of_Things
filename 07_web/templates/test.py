import torch
import torchvision
import torchvision.transforms as transforms
import torch.utils.data as data
import torchvision.datasets as datasets
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import time

from google.colab import drive
drive.mount('/content/drive')

trans = transforms.Compose( 
    [transforms.Resize((777, 777)),
    transforms.RandomHorizontalFlip(0.5), 
     transforms.RandomRotation(30),
     transforms.ToTensor()])

train_dataset = torchvision.datasets.ImageFolder(root = '/content/drive/Shareddrives/전공up X/recyclable_materials/train',transform=trans)
test_dataset = torchvision.datasets.ImageFolder(root = '/content/drive/Shareddrives/전공up X/recyclable_materials/test',transform=trans)
val_dataset = torchvision.datasets.ImageFolder(root = '/content/drive/Shareddrives/전공up X/recyclable_materials/val',transform=trans)
#can_dataset = torchvision.datasets.ImageFolder(root = '/content/drive/Shareddrives/전공up X/recyclable_materials/can',transform=trans)
#glass_dataset = torchvision.datasets.ImageFolder(root = '/content/drive/Shareddrives/전공up X/recyclable_materials/glass',transform=trans)
#paper_dataset = torchvision.datasets.ImageFolder(root = '/content/drive/Shareddrives/전공up X/recyclable_materials/paper',transform=trans)
#plastic_dataset = torchvision.datasets.ImageFolder(root = '/content/drive/Shareddrives/전공up X/recyclable_materials/plastic',transform=trans)
#plastic_bag_dataset = torchvision.datasets.ImageFolder(root = '/content/drive/Shareddrives/전공up X/recyclable_materials/plastic_bag',transform=trans)
#styrofoam_dataset = torchvision.datasets.ImageFolder(root = '/content/drive/Shareddrives/전공up X/recyclable_materials/styrofoam',transform=trans)

classes = test_dataset.classes
dic_classes ={}
for i in range(len(classes)):
  dic_classes[i] = classes[i]

print(dic_classes)  

trainloader = torch.utils.data.DataLoader(train_dataset, batch_size=16, shuffle=True)
valloader = torch.utils.data.DataLoader(val_dataset, batch_size=16, shuffle=True)
testloader = torch.utils.data.DataLoader(test_dataset, batch_size=16, shuffle=True)
'''glassloader = torch.utils.data.DataLoader(glass_dataset, batch_size=16, shuffle=True)
paperloader = torch.utils.data.DataLoader(paper_dataset, batch_size=16, shuffle=True)
plasticloader = torch.utils.data.DataLoader(plastic_dataset, batch_size=16, shuffle=True)
plastic_bagloader = torch.utils.data.DataLoader(plastic_bag_dataset, batch_size=16, shuffle=True)
styrofoamloader = torch.utils.data.DataLoader(styrofoam_dataset, batch_size=16, shuffle=True)'''

class CNN(torch.nn.Module):
  def __init__(self):
    super(CNN, self).__init__()

    self.layer1 = nn.Sequential(
        nn.Conv2d(3,5, kernel_size=3, stride=1),
        nn.ReLU())
    self.pool = nn.MaxPool2d(kernel_size = 2, stride=2)
    self.layer2 = nn.Sequential(
        nn.Conv2d(5, 2, kernel_size=5, stride=3),
        nn.ReLU())
    self.avg = nn.AdaptiveAvgPool2d(7)
    self.fc = nn.Linear(7*7*2, 6)
    
  def forward(self, x):
    out = self.layer1(x)
    out = self.pool(out)
    out = self.layer2(out)
    out = self.avg(out)
    out = out.reshape(out.shape[0], -1)
    out = self.fc(out)
    return out

net = CNN().cuda()
criterion = nn.CrossEntropyLoss().cuda()
optimizer = optim.Adam(net.parameters(), lr = 0.01)

def calculate_accuracy(y_pred, y):
  top_pred = y_pred.argmax(1, keepdim = True)
  correct = top_pred.eq(y.view_as(top_pred)).sum()
  acc = correct.float() / y.shape [0]
  return acc

def train(model, iterator, optimizer, criterion):
    
    epoch_loss = 0
    epoch_acc = 0
    
    model.train()
    
    for (x, y) in iterator:
        
        x = x.cuda()
        y = y.cuda()
        
        optimizer.zero_grad()
                
        y_pred = model(x)
        
        loss = criterion(y_pred, y)
        
        acc = calculate_accuracy(y_pred, y) 
        
        loss.backward()
        
        optimizer.step()
        
        epoch_loss += loss.item()
        epoch_acc += acc.item()
        
    return epoch_loss / len(iterator), epoch_acc / len(iterator)

def epoch_time(start_time, end_time):
    elapsed_time = end_time - start_time
    elapsed_mins = int(elapsed_time/60)
    elapsed_secs = int(elapsed_time -(elapsed_mins*60))
    return elapsed_mins, elapsed_secs

def evaluate(model, iterator, criterion):
    
    epoch_loss = 0
    epoch_acc = 0
    
    model.eval()
    
    with torch.no_grad():
        
        for (x, y) in iterator:

            x = x.cuda()
            y = y.cuda()

            y_pred = model(x)

            loss = criterion(y_pred, y)

            acc = calculate_accuracy(y_pred, y)

            epoch_loss += loss.item()
            epoch_acc += acc.item()
        
    return epoch_loss / len(iterator), epoch_acc / len(iterator)

EPOCHS = 100

best_valid_loss = float('inf')

for epoch in range(EPOCHS):

    if (epoch+1) % 10 ==1:
        start_time = time.monotonic()

    train_loss, train_acc = train(net, trainloader, optimizer, criterion)
    valid_loss, valid_acc = evaluate(net, valloader, criterion)

    if valid_loss < best_valid_loss:
        best_valid_loss = valid_loss
        torch.save(net.state_dict(), 'best_model.pt')

    if (epoch+1) % 10 ==0:
        end_time = time.monotonic()

        epoch_mins, epoch_secs = epoch_time(start_time, end_time)

        print(f'Epoch: {epoch+1:02} | Epoch Time: {epoch_mins}m {epoch_secs}s')
        print(f'\tTrain Loss: {train_loss:.3f} | Train Acc: {train_acc*100:.2f}%')
        print(f'\t Val. Loss: {valid_loss:.3f} |  Val. Acc: {valid_acc*100:.2f}%')

net.load_state_dict(torch.load('best_model.pt'))
test_loss, test_acc = evaluate(net, testloader, criterion)
print(f'Test Loss: {test_loss:.3f} l Test Acc: {test_acc*100:.2f}%')