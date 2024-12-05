# Estrutura de pastas:
# seica_custom_nodes/
# ├── dadoseica/
# │   └── modelos_dados.json
# └── seica_model_loader.py

# seica_model_loader.py
import os
import json
import folder_paths
from comfy.sd import load_checkpoint_guess_config

class LoadModelWithParams:
    def __init__(self):
        self.loaded_model = None
        self.model_path = None
        self.data_path = os.path.join(os.path.dirname(__file__), "dadoseica", "modelos_dados.json")
        self.default_params = self.load_default_params()
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "ckpt_name": (folder_paths.get_filename_list("checkpoints"), ),
            },
        }
    
    RETURN_TYPES = ("MODEL", "CLIP", "VAE", "INT", "FLOAT", "STRING", "STRING")
    RETURN_NAMES = ("model", "clip", "vae", "steps", "cfg", "sampler_name", "scheduler")
    FUNCTION = "load_with_params"
    CATEGORY = "Seica/loaders"

    def load_default_params(self):
        try:
            with open(self.data_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")
            return {}

    def get_model_params(self, model_name):
        base_name = os.path.splitext(model_name)[0]
        return self.default_params.get(base_name, {
            "steps": 20,
            "cfg": 7.0,
            "sampler_name": "euler",
            "scheduler": "normal"
        })

    def load_with_params(self, ckpt_name):
        # Carrega o modelo usando o LoadCheckpoint padrão
        checkpoint = LoadCheckpoint()
        model, clip, vae = checkpoint.load_checkpoint(ckpt_name)
        
        # Obtém os parâmetros personalizados
        params = self.get_model_params(ckpt_name)
        
        return (
            model, 
            clip, 
            vae,
            params["steps"],
            params["cfg"],
            params["sampler_name"],
            params["scheduler"]
        )
        
NODE_CLASS_MAPPINGS = {
    "SeicaLoadCheckpoint": LoadModelWithParams
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SeicaLoadCheckpoint": "Seica Model with KSampler Params"
}