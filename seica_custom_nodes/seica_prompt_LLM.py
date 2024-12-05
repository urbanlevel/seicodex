import json
import requests
from typing import Dict, Any

class SeicaPromptGenerator:
    def __init__(self):
        self.local_url = "http://localhost:1234/v1/chat/completions"
        
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "keyword1": ("STRING", {"default": ""}),
                "keyword2": ("STRING", {"default": ""}),
                "keyword3": ("STRING", {"default": ""}),
                "prompt_length": ("INT", {
                    "default": 50,
                    "min": 20,
                    "max": 200,
                    "step": 5,
                    "display": "slider"
                }),
                "temperature": ("FLOAT", {
                    "default": 0.7,
                    "min": 0.1,
                    "max": 2.0,
                    "step": 0.1,
                    "display": "slider"
                }),
                "style": (["descriptive", "artistic", "technical", "atmospheric", "photographic"], {"default": "photographic"}),
                "focus": (["general", "foreground", "background", "details", "sharp"], {"default": "general"})
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

    def generate_prompt(self, keyword1: str, keyword2: str, keyword3: str, 
                       prompt_length: int, temperature: float, 
                       style: str, focus: str, seed: int = -1) -> tuple[str, str]:
        
        # Define o estilo do prompt baseado na seleção
        style_instructions = {
            "descriptive": "Create a clear and detailed description focusing on visual elements",
            "artistic": "Create a poetic and expressive description with artistic flair",
            "technical": "Create a precise and technical description with specific details",
            "atmospheric": "Create a mood-focused description emphasizing atmosphere and feeling",
            "photographic": "Create a photographic realistic description emphasizing natural elements with detail"
        }
        
        # Define o foco do prompt
        focus_instructions = {
            "general": "balanced description of all elements",
            "foreground": "emphasis on main subject and foreground elements",
            "background": "emphasis on setting and background elements",
            "details": "emphasis on specific details and textures",
            "sharp": "emphasis on specific sharp details of the elements"
        }

        # Monta o sistema e prompt do usuário
        system_message = f"""You are a creative writing assistant specializing in image prompts.
Generate a prompt of approximately {prompt_length} words based on the given keywords.
Style: {style_instructions[style]}
Focus: {focus_instructions[focus]}"""
        
        user_message = f"""Create an image prompt using these keywords: {keyword1}, {keyword2}, and {keyword3}.
Make it suitable for image generation. Include relevant style tags at the end."""

        # Prepara o payload para a API
        payload = {
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            "temperature": temperature,
            "max_tokens": int(prompt_length * 2.5),  # Buffer para garantir texto completo
        }
        
        # Adiciona seed se fornecida
        if seed != -1:
            payload["seed"] = seed

        try:
            # Faz a requisição para o LM Studio
            response = requests.post(
                self.local_url,
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                full_text = result["choices"][0]["message"]["content"].strip()
                
                # Separa o prompt principal das tags de estilo
                parts = full_text.split("Tags:", 1)
                main_prompt = parts[0].strip()
                style_tags = parts[1].strip() if len(parts) > 1 else "No tags generated"
                
                return (main_prompt, style_tags)
            else:
                return ("Error: Failed to generate prompt. Check if LM Studio server is running.", "Error")
                
        except Exception as e:
            return (f"Error: {str(e)}", "Error")

    def IS_CHANGED(self, **kwargs) -> float:
        # Garante que o nó seja executado sempre que os parâmetros mudarem
        return float("nan")

# Registra o nó no ComfyUI
NODE_CLASS_MAPPINGS = {
    "SeicaPromptGenerator": SeicaPromptGenerator
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SeicaPromptGenerator": "Seica Prompt Generator"
}
