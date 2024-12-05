import torch
from PIL import Image
import numpy as np

class SeicaResolutionHandler:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "use_input_image": (["yes", "no"], {"default": "yes"}),
            },
            "optional": {
                "input_image": ("IMAGE",),
                "manual_width": ("INT", {"default": 512, "min": 64, "max": 8192, "step": 8}),
                "manual_height": ("INT", {"default": 512, "min": 64, "max": 8192, "step": 8}),
            },
        }

    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("width", "height")
    FUNCTION = "handle_resolution"
    CATEGORY = "Seica/Image"

    def handle_resolution(self, use_input_image, input_image=None, manual_width=512, manual_height=512):
        if use_input_image == "yes" and input_image is not None:
            if isinstance(input_image, torch.Tensor):
                # Using the method from GetImageSize
                image_size = input_image.size()
                width = int(image_size[2])  # Changed from [2] to [3] to match tensor dimensions
                height = int(image_size[1])  # Changed from [1] to [2] to match tensor dimensions
            else:
                raise ValueError(f"Unsupported image type: {type(input_image)}")
        else:
            width, height = manual_width, manual_height

        return (int(width), int(height))

    @classmethod
    def IS_CHANGED(s, use_input_image, input_image=None, manual_width=512, manual_height=512):
        return True

NODE_CLASS_MAPPINGS = {
    "SeicaResolutionHandler": SeicaResolutionHandler
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SeicaResolutionHandler": "Seica Resolution Handler"
}