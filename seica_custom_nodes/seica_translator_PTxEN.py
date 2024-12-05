from deep_translator import GoogleTranslator

class TranslatePromptNode:
    def __init__(self):
        self.translator = None
        
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

    def init_translator(self):
        if self.translator is None:
            self.translator = GoogleTranslator(source='pt', target='en')

    def traduzir(self, texto_pt):
        self.init_translator()
        
        try:
            # Traduz o texto
            texto_en = self.translator.translate(texto_pt)
            return (texto_en,)
        except Exception as e:
            print(f"Erro na tradução: {str(e)}")
            return (texto_pt,)  # Retorna o texto original em caso de erro

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
