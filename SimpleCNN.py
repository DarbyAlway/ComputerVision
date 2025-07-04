import torch 
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

class SimpleCNN(nn.Module):
    def __init__(self):
        # image 28*28
        self.conv1 = nn.Conv2d(1,16,kernel_size = 3,padding=1)#  28x28 -> 28x28
        self.pool = nn.MaxPool2d(2,2) # 28x28 -> 14x14
        self.conv2 = nn.Conv2d(16,32,kernel_size = 3,padding=1) # 14x14 -> 14x14
        self.fc1 = nn.Linear(32*7*7,128)
        self.fc2 = nn.Linear(128,10) # 10 classes for MNIST

    def forward(self,x):
        x = self.pool(torch.relu(self.conv1(x)))
        x = self.pool(torch.relu(self.conv2(x)))
        x = x.view(x.size(0),-1) # flatten
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

transform = transforms.ToTensor()

train_dataset = datasets.MNIST(root='./data', train=True, download=True, transform=transform)
test_dataset = datasets.MNIST(root='./data', train=False, download=True, transform=transform)

train_loader = DataLoader(train_dataset,batch_size = 32,shuffle = True)
test_loader = DataLoader(test_dataset,batch_size = 32,shuffle = False)

device = torch.device("cpu")
model = SimpleCNN().to(device)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

for epoch in range(5):
    model.train()
    running_loss = 0.0
    for images, labels in train_loader:
        images, labels = images.to(device), labels.to(device)
        
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item()
    print(f'Epoch [{epoch+1}/5], Loss: {running_loss/len(train_loader):.4f}')
model.eval()
correct = 0
total = 0
with torch.no_grad():
    for images, labels in test_loader:
        images, labels = images.to(device), labels.to(device)
        outputs = model(images)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

accuracy = 100 * correct / total
print(f'Accuracy of the model on the test images: {accuracy:.2f}%')
print('Finished Training')