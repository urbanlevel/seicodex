import torch
from transformers import MarianMTModel, MarianTokenizer
import os
from huggingface_hub import snapshot_download

class TranslatePromptNode:
    def __init__(self):
        self.model_name = 'Helsinki-NLP/opus-mt-pt-en'
        self.tokenizer = None
        self.model = None
        self.model_path = None
        
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "texto_pt": ("STRING", {
                    "multiline": True,
                    "default": "Descreva sua prompt em português aqui"
                }),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "traduzir"
    CATEGORY = "Seica/prompt"

    def init_model(self):
        if self.tokenizer is None:
            # Define o caminho para salvar o modelo localmente
            cache_dir = os.path.join(os.path.dirname(__file__), "models")
            os.makedirs(cache_dir, exist_ok=True)
            
            try:
                # Tenta baixar o modelo se não existir localmente
                if not os.path.exists(os.path.join(cache_dir, self.model_name.split('/')[-1])):
                    print(f"Baixando modelo de tradução {self.model_name}...")
                    self.model_path = snapshot_download(
                        repo_id=self.model_name,
                        cache_dir=cache_dir,
                        local_dir=os.path.join(cache_dir, self.model_name.split('/')[-1])
                    )
                else:
                    self.model_path = os.path.join(cache_dir, self.model_name.split('/')[-1])
                
                # Carrega o modelo e tokenizer do caminho local
                self.tokenizer = MarianTokenizer.from_pretrained(self.model_path)
                self.model = MarianMTModel.from_pretrained(self.model_path)
                print("Modelo de tradução carregado com sucesso!")
                
            except Exception as e:
                print(f"Erro ao carregar o modelo: {str(e)}")
                raise

    def traduzir(self, texto_pt):
        self.init_model()
        
        # Tokeniza o texto em português
        inputs = self.tokenizer(texto_pt, return_tensors="pt", padding=True)
        
        # Gera a tradução
        translated = self.model.generate(**inputs)
        
        # Decodifica a tradução
        texto_en = self.tokenizer.batch_decode(translated, skip_special_tokens=True)[0]
        
        return (texto_en,)

# Nó para tradução de prompt negativo
class TranslateNegativePromptNode(TranslatePromptNode):
    CATEGORY = "Seica/prompt"
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "texto_pt": ("STRING", {
                    "multiline": True,
                    "default": "Descreva sua prompt negativa em português aqui"
                }),
            },
        }

# Esta função deve ser chamada para registrar os nós no ComfyUI
NODE_CLASS_MAPPINGS = {
    "TranslatePrompt": TranslatePromptNode,
    "TranslateNegativePrompt": TranslateNegativePromptNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TranslatePrompt": "Traduzir Prompt PT-EN",
    "TranslateNegativePrompt": "Traduzir Prompt Negativa PT-EN"
}