import torch
from torch import nn, optim
import torch.nn.functional as F

from model_util import *


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

    """
Laboratory for CNN shape
"""


print("conv1 :", conv_output_shape((34, 3), 3, pad=1), 34 * 3 * 50)
print("maxpool2d :", conv_output_shape((34, 3), (2, 1), stride=(2, 1)), 17 * 3 * 50)
print("conv2 :", conv_output_shape((17, 3), 3), 15 * 150)
print("maxpool2d :", conv_output_shape((15, 1), (3, 1), stride=(3, 1)), 5 * 150)
