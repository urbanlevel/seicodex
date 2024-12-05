import os
import json
from comfy.sd import load_checkpoint

class SeicaLoadCheckpoint:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model_path": ("STRING", {"default": "", "placeholder": "Caminho para o ficheiro do modelo"})
            }
        }

    RETURN_TYPES = ("MODEL", "CLIP", "VAE", "INT", "FLOAT", "STRING", "STRING")
    RETURN_NAMES = ("Model", "Clip", "VAE", "Steps", "CFG", "Sampler Name", "Scheduler")

    FUNCTION = "load_checkpoint_with_defaults"

    CATEGORY = "Seica/Loaders"

    def load_checkpoint_with_defaults(self, model_path):
        # Caminho para o JSON com os dados
        json_path = os.path.join(os.path.dirname(__file__), "dadoseica", "modelos_dados.json")

        # Carregar o JSON
        try:
            with open(json_path, "r") as file:
                model_defaults = json.load(file)
        except FileNotFoundError:
            raise Exception(f"Ficheiro 'modelos_dados.json' não encontrado em {json_path}.")
        except json.JSONDecodeError:
            raise Exception("Erro ao decodificar o ficheiro JSON.")

        # Extrair valores padrão para o modelo selecionado
        model_name = os.path.basename(model_path)
        defaults = model_defaults.get(model_name, {
            "steps": 20,
            "cfg": 7.0,
            "sampler_name": "Euler a",
            "scheduler": "normal"
        })

        # Carregar o modelo
        model, clip, vae = load_checkpoint(model_path)

        return (
            model, 
            clip, 
            vae, 
            defaults["steps"], 
            defaults["cfg"], 
            defaults["sampler_name"], 
            defaults["scheduler"]
        )

# Registrar o nó
NODE_CLASS_MAPPINGS = {
    "SeicaLoadCheckpoint": SeicaLoadCheckpoint
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "SeicaLoadCheckpoint": "Seica Model W/KSampler Params"
}