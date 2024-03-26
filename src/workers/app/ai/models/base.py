from abc import ABC, abstractmethod

from PIL import Image
from torch.autograd import Variable

from .functions import ImageTransform


class Model(ABC):
    @abstractmethod
    def forward(self, x: Variable):
        raise NotImplementedError()

    def preprocess_image(self, image: Image.Image):
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
