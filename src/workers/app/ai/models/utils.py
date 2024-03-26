import yaml
from torch import Tensor, nn

from .functions import Swish

class_mapping = {
    0: "Normal",
    1: "Pneumonia",
    2: "Tuberculosis"
}


def read_config(config_path: str):
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Configuration file {config_path} not found.")
        return None

    return config


def create_layer(layer_type: str, layer_params: dict):
    if layer_type == 'Linear':
        return nn.Linear(**layer_params)
    elif layer_type == 'BatchNorm2d':
        return nn.BatchNorm2d(**layer_params)
    elif layer_type == 'Dropout':
        return nn.Dropout(**layer_params)
    elif layer_type == 'Swish':
        return Swish()
    elif layer_type == 'Softmax':
        return nn.Softmax(**layer_params)
    else:
        raise ValueError(f'Unsupported layer type: {layer_type}')


def map_prediction_to_class(outputs: Tensor):
    prediction = outputs.max(1)[1].item()
    return class_mapping[prediction]
