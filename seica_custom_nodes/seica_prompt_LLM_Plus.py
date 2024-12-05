import json
import requests
from typing import Dict, Any

class SeicaPromptFromTextPlus:
    def __init__(self):
        self.local_url = "http://localhost:1234/v1/chat/completions"
        
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_text": ("STRING", {
                    "default": "", 
                    "multiline": True,
                    "placeholder": "Enter your text here..."
                }),
                "prompt_length": ("INT", {
                    "default": 50,
                    "min": 20,
                    "max": 300,
                    "step": 10,
                    "display": "slider"
                }),
                "temperature": ("FLOAT", {
                    "default": 0.7,
                    "min": 0.1,
                    "max": 2.0,
                    "step": 0.1,
                    "display": "slider"
                }),
                "style": ([
                    "photographic_portrait",
                    "photographic_landscape",
                    "photographic_street",
                    "photographic_fashion",
                    "photographic_product",
                    "photographic_wildlife",
                    "cartoon_pixar",
                    "cartoon_anime",
                    "cartoon_disney",
                    "cartoon_studio_ghibli",
                    "artistic_oil_painting",
                    "artistic_watercolor",
                    "artistic_digital_art",
                    "artistic_concept_art",
                    "cinematic_hollywood",
                    "cinematic_noir",
                    "cinematic_scifi",
                    "cinematic_fantasy"
                ], {"default": "photographic_portrait"}),
                "focus": ([
                    "general_view",
                    "subject_focus",
                    "background_emphasis",
                    "detail_macro",
                    "environmental",
                    "action_motion",
                    "abstract_mood",
                    "minimalist"
                ], {"default": "general_view"}),
                "focal_length": ("INT", {
                    "default": 50,
                    "min": 8,
                    "max": 800,
                    "step": 1,
                    "display": "slider"
                }),
                "focal_perspective": ([
                    "ultra_wide",
                    "wide_angle",
                    "normal",
                    "short_telephoto",
                    "telephoto",
                    "super_telephoto",
                    "macro",
                    "microscopic"
                ], {"default": "normal"}),
                "lighting": ([
                    "natural_daylight",
                    "golden_hour",
                    "blue_hour",
                    "night",
                    "studio_soft",
                    "studio_dramatic",
                    "high_key",
                    "low_key",
                    "neon",
                    "cinematic",
                    "ambient"
                ], {"default": "natural_daylight"})
            },
            "optional": {
                "seed": ("INT", {
                    "default": -1,
                    "min": -1,
                    "max": 2147483647,
                    "step": 1,
                    "display": "number"
                })
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("generated_prompt", "style_tags")
    FUNCTION = "generate_prompt"
    CATEGORY = "Seica/Text"

    def generate_prompt(self, input_text: str, 
                       prompt_length: int, temperature: float, 
                       style: str, focus: str, 
                       focal_length: int, focal_perspective: str,
                       lighting: str, seed: int = -1) -> tuple[str, str]:
        
        # Define o estilo do prompt baseado na seleção
        style_instructions = {
            "photographic_portrait": "Create a professional portrait photography description with attention to subject lighting and expression",
            "photographic_landscape": "Create a dramatic landscape photography description with emphasis on natural beauty and composition",
            "photographic_street": "Create an authentic street photography description capturing urban life and moments",
            "photographic_fashion": "Create a high-end fashion photography description with attention to style and aesthetics",
            "photographic_product": "Create a commercial product photography description with focus on details and presentation",
            "photographic_wildlife": "Create a nature photography description capturing wildlife in their natural habitat",
            "cartoon_pixar": "Create a Pixar-style 3D animation description with characteristic charm and emotion",
            "cartoon_anime": "Create an anime-style description with distinctive Japanese animation features",
            "cartoon_disney": "Create a Disney-style animation description with magical and whimsical elements",
            "cartoon_studio_ghibli": "Create a Studio Ghibli-style description with their distinctive aesthetic and atmosphere",
            "artistic_oil_painting": "Create a description as if painted in oils with rich textures and classical technique",
            "artistic_watercolor": "Create a description as if painted in watercolor with soft edges and transparency",
            "artistic_digital_art": "Create a digital art description with contemporary digital painting techniques",
            "artistic_concept_art": "Create a concept art description with emphasis on world-building and design",
            "cinematic_hollywood": "Create a Hollywood movie-style shot description with dramatic composition",
            "cinematic_noir": "Create a film noir style description with dramatic shadows and mood",
            "cinematic_scifi": "Create a science fiction cinema style description with futuristic elements",
            "cinematic_fantasy": "Create a fantasy cinema style description with magical and otherworldly elements"
        }
        
        # Define o foco do prompt
        focus_instructions = {
            "general_view": "balanced composition of all elements",
            "subject_focus": "strong emphasis on the main subject with background blur",
            "background_emphasis": "focus on environmental context and setting",
            "detail_macro": "extreme close-up focus on intricate details",
            "environmental": "subject in context with equal attention to surroundings",
            "action_motion": "emphasis on movement and dynamic elements",
            "abstract_mood": "focus on creating atmosphere and emotional impact",
            "minimalist": "emphasis on simplicity and negative space"
        }

        # Define instruções de perspectiva focal
        focal_instructions = {
            "ultra_wide": f"Shot with an {focal_length}mm ultra-wide lens, creating an expansive dramatic view",
            "wide_angle": f"Shot with a {focal_length}mm wide-angle lens, capturing a broad perspective",
            "normal": f"Shot with a {focal_length}mm lens, showing natural perspective",
            "short_telephoto": f"Shot with a {focal_length}mm short telephoto lens, ideal for portraits",
            "telephoto": f"Shot with a {focal_length}mm telephoto lens, compressing perspective",
            "super_telephoto": f"Shot with a {focal_length}mm super telephoto lens, for extreme distance",
            "macro": f"Shot with a {focal_length}mm macro lens, revealing minute details",
            "microscopic": f"Shot with a {focal_length}mm microscopic lens, showing extreme detail"
        }

        # Define instruções de iluminação
        lighting_instructions = {
            "natural_daylight": "lit by natural daylight, creating soft, even illumination",
            "golden_hour": "lit by warm, golden sunlight during sunset/sunrise",
            "blue_hour": "lit by cool, blue twilight light",
            "night": "night time lighting with artificial light sources",
            "studio_soft": "soft, diffused studio lighting setup",
            "studio_dramatic": "dramatic studio lighting with strong contrast",
            "high_key": "bright, high-key lighting with minimal shadows",
            "low_key": "dark, low-key lighting with dramatic shadows",
            "neon": "colorful neon lighting with vibrant glow",
            "cinematic": "dramatic cinematic lighting setup",
            "ambient": "natural ambient lighting from the environment"
        }

        # Monta o sistema e prompt do usuário
        system_message = f"""You are a creative writing assistant specializing in image prompts.
Generate a prompt of approximately {prompt_length} words based on the input text.
Style: {style_instructions[style]}
Focus: {focus_instructions[focus]}
Camera Perspective: {focal_instructions[focal_perspective]}
Lighting: {lighting_instructions[lighting]}"""
        
        user_message = f"""Create an image prompt based on this text: "{input_text}"
Transform this into a detailed image generation prompt, incorporating:
- {style.replace('_', ' ').title()} style
- {focal_perspective.replace('_', ' ').title()} perspective at {focal_length}mm
- {lighting.replace('_', ' ').title()} lighting
- {focus.replace('_', ' ').title()} compositional focus
Include relevant style tags at the end, including technical specifications."""

        # Prepara o payload para a API
        payload = {
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            "temperature": temperature,
            "max_tokens": int(prompt_length * 2.5),
        }
        
        if seed != -1:
            payload["seed"] = seed

        try:
            response = requests.post(
                self.local_url,
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                full_text = result["choices"][0]["message"]["content"].strip()
                
                parts = full_text.split("Tags:", 1)
                main_prompt = parts[0].strip()
                style_tags = parts[1].strip() if len(parts) > 1 else "No tags generated"
                
                return (main_prompt, style_tags)
            else:
                return ("Error: Failed to generate prompt. Check if LM Studio server is running.", "Error")
                
        except Exception as e:
            return (f"Error: {str(e)}", "Error")

    def IS_CHANGED(self, **kwargs) -> float:
        return float("nan")

# Registra o nó no ComfyUI
NODE_CLASS_MAPPINGS = {
    "SeicaPromptFromTextPlus": SeicaPromptFromTextPlus
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SeicaPromptFromTextPlus": "Seica Prompt From Text Plus"
}