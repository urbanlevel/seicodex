import os
import torch
import numpy as np
from PIL import Image, ImageOps
from PIL.ExifTags import TAGS
import hashlib
from typing import List, Tuple

class SeicaImageLoader:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "ImageID": ("INT", {"default": 0, "min": 0, "max": 10000}),
                "FolderPath": ("STRING", {"default": ""}),
                "RespectSubfolders": (["ON", "OFF"], {"default": "OFF"}),
            },
        }

    RETURN_TYPES = ("STRING", "STRING", "IMAGE")
    RETURN_NAMES = ("TotalImages", "ImageFilename", "Image")
    FUNCTION = "load_image"
    CATEGORY = "Seica/Image"

    def load_image(self, ImageID: int, FolderPath: str, RespectSubfolders: str) -> Tuple[str, str, torch.Tensor]:
        image_files = self.get_image_files(FolderPath, RespectSubfolders == "ON")
        total_images = len(image_files)

        if total_images == 0:
            raise ValueError(f"No images found in the specified folder: {FolderPath}")

        if ImageID >= total_images:
            raise ValueError(f"ImageID {ImageID} is out of range. Total images: {total_images}")

        image_path = image_files[ImageID]
        image_filename = os.path.splitext(os.path.basename(image_path))[0]

        # Load and process the image
        img = Image.open(image_path)
        img = ImageOps.exif_transpose(img)
        img = img.convert("RGB")
        img_np = np.array(img).astype(np.float32) / 255.0
        img_tensor = torch.from_numpy(img_np).permute(2, 0, 1).unsqueeze(0)

        return str(total_images), image_filename, img_tensor

    @staticmethod
    def get_image_files(folder_path: str, respect_subfolders: bool) -> List[str]:
        image_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp')
        image_files = []

        if respect_subfolders:
            for root, _, files in os.walk(folder_path):
                for file in files:
                    if file.lower().endswith(image_extensions):
                        image_files.append(os.path.join(root, file))
        else:
            for file in os.listdir(folder_path):
                if file.lower().endswith(image_extensions):
                    image_files.append(os.path.join(folder_path, file))

        return sorted(image_files)

    @classmethod
    def IS_CHANGED(s, ImageID: int, FolderPath: str, RespectSubfolders: str) -> bool:
        return True

NODE_CLASS_MAPPINGS = {
    "SeicaImageLoader": SeicaImageLoader
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SeicaImageLoader": "Seica Image Loader"
}