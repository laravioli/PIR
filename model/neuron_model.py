import torch
from torch import nn, optim
import torch.nn.functional as F

from model_util import *


class FNN(nn.Module):
    def __init__(self, size=3):
        super(FNN, self).__init__()
        self.fc1 = nn.Linear(34 * size, 500)
        self.fc2 = nn.Linear(500, 200)
        self.fc3 = nn.Linear(200, 34)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x


class CNN_v1(nn.Module):
    def __init__(self):
        super(CNN_v1, self).__init__()

        self.convlayer1 = nn.Sequential(
            nn.Conv2d(1, 50, 3, padding=1),
            nn.BatchNorm2d(50),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=(2, 1)),
        )

        self.convlayer2 = nn.Sequential(
            nn.Conv2d(50, 150, 3),
            nn.BatchNorm2d(150),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=(3, 1)),
        )

        self.fc1 = nn.Linear(150 * 5, 400)
        self.drop = nn.Dropout2d(0.25)
        self.fc2 = nn.Linear(400, 200)
        self.fc3 = nn.Linear(200, 34)

    def forward(self, x):
        x = self.convlayer1(x)
        x = self.convlayer2(x)
        x = x.view(-1, 150 * 5)
        x = self.fc1(x)
        x = self.drop(x)
        x = self.fc2(x)
        x = self.fc3(x)

        return x


class CNN_v2(nn.Module):
    def __init__(self):
        super(CNN_v2, self).__init__()

        self.convlayer1 = nn.Sequential(
            nn.Conv2d(1, 100, 3, padding=2),
            nn.BatchNorm2d(100),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=(1, 3), stride=1),
        )

        self.convlayer2 = nn.Sequential(
            nn.Conv2d(100, 200, 3, padding=1),
            nn.BatchNorm2d(200),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=3, stride=1),
        )

        self.fc1 = nn.Linear(200 * 34, 800)
        self.drop = nn.Dropout2d(0.25)
        self.fc2 = nn.Linear(800, 200)
        self.fc3 = nn.Linear(200, 34)

    def forward(self, x):
        x = self.convlayer1(x)
        x = self.convlayer2(x)
        x = x.view(-1, 200 * 34)
        x = self.fc1(x)
        x = self.drop(x)
        x = self.fc2(x)
        x = self.fc3(x)

        return x

    """
Laboratory for CNN shape
"""


print("conv1 :", conv_output_shape((34, 3), 3, pad=2), 36 * 5 * 100)
print("maxpool2d :", conv_output_shape((36, 5), (1, 3), stride=1), 36 * 3 * 100)
print("conv2 :", conv_output_shape((36, 3), 3, pad=1), 36 * 3 * 200)
print("maxpool2d :", conv_output_shape((36, 3), 3, stride=(1, 1)), 34 * 200)
