class SeicaLatentSwitch:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "latent_1": ("LATENT",),
                "latent_2": ("LATENT",),
                "select_latent_1": ("BOOLEAN", {"default": True}),
            }
        }

    CATEGORY = "Seica/Switch"
    RETURN_TYPES = ("LATENT",)
    FUNCTION = "switch_latent"

    def switch_latent(self, latent_1, latent_2, select_latent_1):
        if select_latent_1:
            return (latent_1,)
        else:
            return (latent_2,)

class SeicaStringSwitch:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string_1": ("STRING", {"multiline": True}),
                "string_2": ("STRING", {"multiline": True}),
                "select_string_1": ("BOOLEAN", {"default": True}),
            }
        }

    CATEGORY = "Seica/Switch"
    RETURN_TYPES = ("STRING",)
    FUNCTION = "switch_string"

    def switch_string(self, string_1, string_2, select_string_1):
        if select_string_1:
            return (string_1,)
        else:
            return (string_2,)

NODE_CLASS_MAPPINGS = {
    "SeicaLatentSwitch": SeicaLatentSwitch,
    "SeicaStringSwitch": SeicaStringSwitch
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SeicaLatentSwitch": "Seica Latent Switch",
    "SeicaStringSwitch": "Seica String Switch"
}