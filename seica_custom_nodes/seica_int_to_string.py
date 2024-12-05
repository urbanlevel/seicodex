class SeicaIntToString:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "integer": ("INT", {
                    "default": 0, 
                    "min": -1000000000,  # Adjust these limits as needed
                    "max": 1000000000,
                    "step": 1
                }),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("string_output",)
    FUNCTION = "convert_to_string"
    CATEGORY = "Seica/Conversion"

    def convert_to_string(self, integer):
        return (str(integer),)

    @classmethod
    def IS_CHANGED(s, integer):
        return True

NODE_CLASS_MAPPINGS = {
    "SeicaIntToString": SeicaIntToString
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SeicaIntToString": "Seica Int to String"
}