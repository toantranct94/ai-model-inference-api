from collections import OrderedDict

import timm
import torch
from PIL import Image
from torch import nn
from torch.autograd import Variable

from .functions import ImageTransform
from .utils import create_layer, map_prediction_to_class, read_config


class InferenceModel(nn.Module):
    def __init__(
        self,
        model_name: str = 'efficientnet_b0',
        pretrained: bool = True,
        drop_rate: float = 0.2,
        fc_config_path: str = './app/ai/configs/fully_connected.yaml',
        checkpoint_path: str = (
            './app/ai/checkpoints/EfficientNet_B0_NS_320.pth'
        )
    ):
        super().__init__()

        self.build_model(
            model_name, pretrained, drop_rate, fc_config_path, checkpoint_path)

    def build_model(
        self,
        model_name: str,
        pretrained: bool,
        drop_rate: float,
        fc_config_path: str,
        checkpoint_path: str,
    ):
        """
        Build a model with the specified parameters.

        Args:
            model_name (str): The name of the model architecture.
            pretrained (bool): Whether to use pretrained weights.
            drop_rate (float): The dropout rate for the model.
            fc_config_path (str): The file path to the fully connected layer
                configuration.
            checkpoint_path (str): The file path to the model checkpoint.

        Returns:
            torch.nn.Module: The built model.
        """
        self.model = timm.create_model(
            model_name, pretrained=pretrained, drop_rate=drop_rate)

        self.model.fc = self.build_fully_connected_layers(fc_config_path)

        self.load_checkpoint(checkpoint_path)

    def build_fully_connected_layers(self, config_path: str):
        """
        Builds fully connected layers from a configuration file.

        Args:
            config_path (str): Path to the configuration file.
        """
        config = read_config(config_path)

        if config is None:
            return

        layers = OrderedDict()

        layer_configs = config.get('fc', [])

        if not layer_configs:
            return

        for layer_config in layer_configs:
            layer_type = layer_config.get('type', '')
            layer_name = layer_config.get('name', '')
            layer_params = layer_config.get('params', {})

            layer = create_layer(layer_type, layer_params)
            layers[layer_name] = layer

        fc = nn.Sequential(layers)
        return fc

    def load_checkpoint(self, checkpoint_path: str):
        """
        Loads a checkpoint file and updates the model's state dictionary.

        Args:
            checkpoint_path (str): The path to the checkpoint file.

        Returns:
            None
        """
        checkpoint = torch.load(
            checkpoint_path, map_location=torch.device('cpu'))
        self.model.load_state_dict(checkpoint['model_state_dict'])

    def forward(self, x: Variable):
        """
        Forward pass of the model.

        Args:
            x (Variable): Input data.

        Returns:
            str: Predicted label.
        """
        outputs = self.model(x)
        label = map_prediction_to_class(outputs)
        return label

    @staticmethod
    def preprocess_image(image: Image.Image):
        """
        Preprocesses an image for model inference.

        Args:
            image (str): The data of the image.

        Returns:
            torch.Tensor: The preprocessed image tensor.
        """
        transform = ImageTransform()
        image_tensor = transform(image).float()
        image_tensor = image_tensor.unsqueeze_(0)
        return Variable(image_tensor)
