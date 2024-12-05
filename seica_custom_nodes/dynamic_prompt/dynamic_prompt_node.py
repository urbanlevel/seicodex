import random
import json
import os
from pathlib import Path

class DynamicPromptNode:
    def __init__(self):
        self.output_dir = "dynamic_prompts"
        self.keywords_dir = "keywords"
        # Cria diretórios se não existirem
        Path(self.output_dir).mkdir(exist_ok=True)
        Path(self.keywords_dir).mkdir(exist_ok=True)
        
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "base_prompt": ("STRING", {"multiline": True}),
                "use_files": ("BOOLEAN", {"default": False}),
                "keywords_mode": (["Single File", "Category Files"], {"default": "Single File"}),
                "keywords_file": ("STRING", {"default": "keywords.txt"}),
                "delimiter": ("STRING", {"default": "\""})
            }
        }
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate_prompt"
    CATEGORY = "Seica/prompt"

    def parse_inline_keywords(self, text, delimiter='"'):
        """Extrai e categoriza palavras-chave do texto"""
        keywords_dict = {}
        parts = text.split(delimiter)
        for i in range(1, len(parts), 2):
            if i < len(parts):
                # Divide as palavras da categoria
                words = [w.strip() for w in parts[i].split()]
                # Usa a primeira palavra como identificador da categoria
                category = words[0]
                if category not in keywords_dict:
                    keywords_dict[category] = set()
                keywords_dict[category].update(words)
        return keywords_dict

    def load_single_file(self, file_path):
        """Carrega todas as palavras-chave de um único arquivo"""
        keywords = set()
        if not file_path:
            return keywords
        
        try:
            file_path = os.path.join(self.keywords_dir, file_path)
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    words = line.strip().split()
                    keywords.update(words)
        except Exception as e:
            print(f"Erro ao ler arquivo de palavras-chave: {e}")
        return keywords

    def load_category_files(self):
        """Carrega palavras-chave de múltiplos arquivos por categoria"""
        keywords_dict = {}
        try:
            for file in os.listdir(self.keywords_dir):
                if file.endswith('.txt'):
                    category = file[:-4]  # Remove .txt
                    keywords_dict[category] = set()
                    with open(os.path.join(self.keywords_dir, file), 'r', encoding='utf-8') as f:
                        for line in f:
                            words = line.strip().split()
                            keywords_dict[category].update(words)
        except Exception as e:
            print(f"Erro ao carregar arquivos de categoria: {e}")
        return keywords_dict

    def generate_prompt(self, base_prompt, use_files=False, keywords_mode="Single File", 
                       keywords_file="keywords.txt", delimiter='"'):
        # Extrai categorias e palavras-chave do prompt base
        inline_keywords = self.parse_inline_keywords(base_prompt, delimiter)
        
        # Carrega palavras-chave de arquivos se necessário
        file_keywords = {}
        if use_files:
            if keywords_mode == "Single File":
                # Todas as palavras vão para todas as categorias
                all_words = self.load_single_file(keywords_file)
                for category in inline_keywords:
                    file_keywords[category] = all_words
            else:
                # Carrega palavras específicas por categoria
                file_keywords = self.load_category_files()
        
        # Gera o novo prompt
        new_prompt = base_prompt
        for category, words in inline_keywords.items():
            # Combina palavras do prompt com palavras dos arquivos
            all_words = words.union(file_keywords.get(category, set()))
            if all_words:
                # Substitui cada ocorrência da categoria por uma palavra aleatória
                pattern = f'{delimiter}{category}'
                while pattern in new_prompt:
                    word = random.choice(list(all_words))
                    new_prompt = new_prompt.replace(f'{delimiter}{category}', word, 1)
        
        return (new_prompt,)