import timm


class Model:
    def __init__(
        self,
        name: str = 'tf_efficientnet_b0_ns',
        pretrained: bool = True,
        drop_rate: float = 0.2
    ):
        self.model_instance = timm.create_model(
            name, pretrained=pretrained, drop_rate=drop_rate)


model = timm.create_model(
        'tf_efficientnet_b0_ns', pretrained=True, drop_rate=0.2)
