from .seica_batch_resizer import SeicaBatchResizer
from .seica_image_loader import SeicaImageLoader
from .seica_image_save import SeicaImageSave
from .seica_resolution_handler import SeicaResolutionHandler
from .seica_int_to_string import SeicaIntToString
from .seica_switch import SeicaLatentSwitch, SeicaStringSwitch
from .seica_styler import SeicaStyler, SeicaStylerAdvanced
from .dynamic_prompt.dynamic_prompt_node import DynamicPromptNode
from .seica_ratio import SeicaAspectRatioPH
from .seica_translator_PTxEN import TranslatePromptNode, TranslateNegativePromptNode
from .seica_prompt_LLM import SeicaPromptGenerator
from .seica_prompt_LLM_Plus import SeicaPromptFromTextPlus
from .seica_model_loader import SeicaLoadCheckpoint

NODE_CLASS_MAPPINGS = {
    "SeicaBatchResizer": SeicaBatchResizer,
    "SeicaImageLoader": SeicaImageLoader,
    "SeicaImageSave": SeicaImageSave,
    "SeicaResolutionHandler": SeicaResolutionHandler,
    "SeicaIntToString": SeicaIntToString,
    "SeicaLatentSwitch": SeicaLatentSwitch,
    "SeicaStringSwitch": SeicaStringSwitch,
    "SeicaStyler": SeicaStyler,
    "SeicaStylerAdvanced": SeicaStylerAdvanced,
    "SeicaDynamicPromptNode": DynamicPromptNode,
    "SeicaAspectRatio": SeicaAspectRatioPH,
    "TranslatePrompt": TranslatePromptNode,
    "TranslateNegativePrompt": TranslateNegativePromptNode,
    "SeicaPromptGenerator": SeicaPromptGenerator,
    "SeicaPromptFromTextPlus": SeicaPromptFromTextPlus,
    "SeicaLoadCheckpoint": SeicaLoadCheckpoint,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SeicaBatchResizer": "Seica Batch Resizer",
    "SeicaImageLoader": "Seica Image Loader",
    "SeicaImageSave": "Seica Image Save",
    "SeicaResolutionHandler": "Seica Resolution Handler",
    "SeicaIntToString": "Seica Int to String",
    "SeicaLatentSwitch": "Seica Latent Switch",
    "SeicaStringSwitch": "Seica String Switch",
    "SeicaStyler": "Seica Styler",
    "SeicaStylerAdvanced": "Seica Styler (Advanced)",
    "SeicaDynamicPromptNode": "Seica Dynamic Prompt",
    "SeicaAspectRatio": "Seica Aspect Ratio",
    "TranslatePrompt": "Traduzir Prompt PT-EN",
    "TranslateNegativePrompt": "Traduzir Prompt Negativa PT-EN",
    "SeicaPromptGenerator": "Seica Prompt Generator",
    "SeicaPromptFromTextPlus": "Seica Prompt From Text Plus",
    "SeicaLoadCheckpoint": "Seica Load Checkpoint",
}

##  __all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']