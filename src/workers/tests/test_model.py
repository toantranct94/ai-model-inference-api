import os

import pytest
import torch
from app.ai.model import InferenceModel
from PIL import Image


class TestInferenceModel:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.model = InferenceModel()
        self.checkpoint_path = (
            './app/ai/checkpoints/EfficientNet_B0_NS_320.pth'
        )
        self.image_path = './tests/test_image.jpeg'
        self.image = Image.open(self.image_path).convert('RGB')

    def test_model_creation(self):
        assert isinstance(self.model, InferenceModel)

    def test_load_checkpoint(self):
        self.model.load_checkpoint(self.checkpoint_path)
        assert self.model is not None
        assert os.path.exists(self.checkpoint_path), (
            "Checkpoint file does not exist"
        )

    def test_preprocess_image(self):
        preprocessed_image = InferenceModel.preprocess_image(self.image)
        assert isinstance(preprocessed_image, torch.Tensor)

    def test_inference_image(self):
        self.model.load_checkpoint(self.checkpoint_path)
        preprocessed_image = InferenceModel.preprocess_image(self.image)
        label = self.model(preprocessed_image)
        assert isinstance(preprocessed_image, torch.Tensor)
        assert label is not None
