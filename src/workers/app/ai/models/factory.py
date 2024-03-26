from .onnx_inference_model import ONNXInferenceModel
from .torch_inference_model import TorchInferenceModel


class ModelFactory:
    @staticmethod
    def create_model(model_type: str = 'onnx'):
        """
        Create an instance of the specified model type.

        Args:
            model_type (str): The type of the model to create.
                Defaults to 'onnx'.

        Returns:
            An instance of the specified model type.

        Raises:
            ValueError: If an invalid model type is provided.
        """
        if model_type == 'onnx':
            return ONNXInferenceModel()
        elif model_type == 'pytorch':
            return TorchInferenceModel()
        else:
            raise ValueError(f"Invalid model type: {model_type}")
