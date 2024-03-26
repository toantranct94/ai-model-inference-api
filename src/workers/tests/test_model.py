import os

import pytest
import torch
from PIL import Image

from app.ai import ModelFactory
from app.ai.models import ONNXInferenceModel, TorchInferenceModel

MODEL_PARAMS = [
    (
        'pytorch',
        TorchInferenceModel,
        './app/ai/checkpoints/EfficientNet_B0_NS_320.pth'),
    (
        'onnx',
        ONNXInferenceModel,
        './app/ai/checkpoints/EfficientNet_B0_NS_320.onnx')
]


@pytest.mark.parametrize(
    'model_type,model_class,checkpoint_path', MODEL_PARAMS
)
class TestInferenceModel:
    @pytest.fixture(autouse=True)
    def setup(self, model_type, model_class, checkpoint_path):
        self.model_type = model_type
        self.model_class = model_class
        self.checkpoint_path = checkpoint_path
        self.model = ModelFactory.create_model(model_type)
        self.image_path = './tests/test_image.jpeg'
        self.image = Image.open(self.image_path).convert('RGB')

    def test_model_creation(self):
        model = ModelFactory.create_model(self.model_type)
        assert isinstance(model, self.model_class)

    def test_load_checkpoint(self):
        if self.model_type == 'pytorch':
            self.model.load_checkpoint(self.checkpoint_path)
        assert self.model is not None
        assert os.path.exists(self.checkpoint_path), (
            "Checkpoint file does not exist"
        )

    def test_preprocess_image(self):
        preprocessed_image = self.model.preprocess_image(self.image)
        assert isinstance(preprocessed_image, torch.Tensor)

    def test_inference_image(self):
        if self.model_type == 'pytorch':
            self.model.load_checkpoint(self.checkpoint_path)
        preprocessed_image = self.model.preprocess_image(self.image)
        label = self.model.forward(preprocessed_image)
        assert isinstance(preprocessed_image, torch.Tensor)
        assert label is not None
