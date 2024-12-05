import os
import torch
from PIL import Image
import numpy as np

class SeicaImageSave:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),
                "filename": ("STRING", {"default": "image"}),
                "output_path": ("STRING", {"default": "outputs"}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("save_path",)
    FUNCTION = "save_images"
    CATEGORY = "Seica/Image"

    def save_images(self, images, filename, output_path):
        os.makedirs(output_path, exist_ok=True)
        results = []

        for i, image in enumerate(images):
            if isinstance(image, torch.Tensor):
                image = image.squeeze().cpu().numpy()
                image = (image * 255).astype(np.uint8)
                if image.ndim == 3:
                    image = image.transpose(1, 2, 0)
                image = Image.fromarray(image)
            elif not isinstance(image, Image.Image):
                raise ValueError(f"Unsupported image type: {type(image)}")

            save_name = f"{filename}_{i}.png" if images.shape[0] > 1 else f"{filename}.png"
            save_path = os.path.join(output_path, save_name)
            image.save(save_path)
            results.append(save_path)

        return (", ".join(results),)

    @classmethod
    def IS_CHANGED(s, images, filename, output_path):
        return True

NODE_CLASS_MAPPINGS = {
    "SeicaImageSave": SeicaImageSave
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SeicaImageSave": "Seica Image Save"
}