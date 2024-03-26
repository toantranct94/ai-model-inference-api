import onnxruntime as ort
import torch
from torch.autograd import Variable

from .base import Model
from .utils import map_prediction_to_class


class ONNXInferenceModel(Model):
    def __init__(
        self,
        model_path: str = './app/ai/checkpoints/EfficientNet_B0_NS_320.onnx'
    ):
        self.model_path = model_path
        self.session = ort.InferenceSession(
            model_path, providers=["CPUExecutionProvider"])

    def forward(self, x: Variable):
        """
        Forward pass of the model.

        Args:
            x (Variable): Input data.

        Returns:
            str: Predicted label.
        """
        input_data = {
            self.session.get_inputs()[0].name: self.to_numpy(x)
        }
        output = self.session.run(None, input_data)
        label = map_prediction_to_class(torch.Tensor(output[0]))
        return label

    def to_numpy(self, tensor: torch.Tensor):
        """
        Converts a PyTorch tensor to a NumPy array.

        Args:
            tensor (torch.Tensor): The input PyTorch tensor.

        Returns:
            numpy.ndarray: The converted NumPy array.
        """
        return tensor.detach().cpu().numpy() if tensor.requires_grad \
            else tensor.cpu().numpy()
