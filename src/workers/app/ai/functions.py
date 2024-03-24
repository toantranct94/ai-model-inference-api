import torch
from torch import nn
from torchvision import transforms


class Swish(nn.Module):
    """
    Swish activation function.
    Swish is a non-linear activation function that applies the
        sigmoid function to the input multiplied by the input itself.
    It has been shown to perform well in deep neural networks,
        providing a smooth and continuous activation.
    """
    def forward(self, x):
        return x * torch.sigmoid(x)


class ImageTransform:
    def __init__(self):
        self.transformation = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(
                [0.485, 0.456, 0.406],
                [0.229, 0.224, 0.225]
            )
        ])

    def __call__(self, image):
        return self.transformation(image).float()
