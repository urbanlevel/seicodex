import os
from PIL import Image

class SeicaBatchResizer:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_directory": ("STRING", {
                    "multiline": False,
                    "default": "./input_images"
                }),
                "output_directory": ("STRING", {
                    "multiline": False,
                    "default": "./output_images"
                }),
                "target_size": ("INT", {
                    "default": 512,
                    "min": 64,
                    "max": 2048,
                    "step": 64
                }),
                "resize_method": (["smallest_side", "largest_side"],),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "resize_batch"
    OUTPUT_NODE = True
    CATEGORY = "Seica/Image Processing"

    def resize_batch(self, input_directory, output_directory, target_size, resize_method):
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        processed_count = 0
        for filename in os.listdir(input_directory):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                input_path = os.path.join(input_directory, filename)
                output_path = os.path.join(output_directory, filename)
                
                with Image.open(input_path) as img:
                    if resize_method == "smallest_side":
                        ratio = target_size / min(img.size)
                    else:  # largest_side
                        ratio = target_size / max(img.size)
                    
                    new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))
                    resized_img = img.resize(new_size, Image.LANCZOS)
                    resized_img.save(output_path)
                    processed_count += 1

        return (f"Processed {processed_count} images.",)

# Mapeamentos atualizados
NODE_CLASS_MAPPINGS = {
    "SeicaBatchResizer": SeicaBatchResizer
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SeicaBatchResizer": "Seica Batch Resizer"
}