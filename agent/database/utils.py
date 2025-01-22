import pandas as pd
from pathlib import Path
from typing import List
import torch
from transformers import AutoTokenizer, AutoModel
from agent.utils import EmbedModelType
import torch.nn.functional as F

class Mixin:
    def search_points(self, point_ids: dict, collection_name: str,):
        points = self._client.retrieve(
            collection_name=collection_name,
            ids=point_ids,
        )
        return points
    
    def get_all_files(self):
        """ Получить все файла в директории dataset_dir """

        directory_path = Path(self.dataset_dir)
        return [str(file) for file in directory_path.rglob('*') if file.is_file()]
    
    def combined_df(self, files: List[str]) -> pd.DataFrame:
        """ Комбенируем все csv файлы """

        df_combined = pd.DataFrame()
        
        for file in files:
            df = pd.read_csv(file)
            df_combined = pd.concat([df_combined, df], ignore_index=True)
        
        return df_combined

class ModelEncoder:
    def __init__(self, model_name: EmbedModelType):
        self.model_name = model_name

    def model(self, model_name: EmbedModelType):
        return ModelEncoder(model_name=model_name)
    
    def encode(self, text: str, device='cpu'):
        try:
            if self.model_name == EmbedModelType.E5_LARGE:
                tokenizer = AutoTokenizer.from_pretrained(EmbedModelType.E5_LARGE.value)
                model = AutoModel.from_pretrained(EmbedModelType.E5_LARGE.value)

                batch = tokenizer(text, padding=True, truncation=True, max_length=512, return_tensors="pt")
                with torch.no_grad():
                    outputs = model(**batch)
                embeddings = outputs.last_hidden_state.mean(dim=1)
                embeddings = F.normalize(embeddings, p=2, dim=1)

                return embeddings.tolist()[0]
            
            elif self.model_name == EmbedModelType.TOCHKA:
                tokenizer = AutoTokenizer.from_pretrained(EmbedModelType.TOCHKA.value)
                model = AutoModel.from_pretrained(EmbedModelType.TOCHKA.value, trust_remote_code=True, attn_implementation='sdpa')
                model = model.to(device)
                
                tokenized = tokenizer(text, return_tensors='pt', padding=True, truncation=True)
                tokenized = {key: value.to(device) for key, value in tokenized.items()}
                
                with torch.inference_mode():
                    pooled_output = model(**tokenized).pooler_output
                normalized_embeddings = F.normalize(pooled_output, dim=1)
                
                return normalized_embeddings.tolist()[0]

        except Exception as e:
            print(f"Ошибка при получении эмбеддинга: {e}")
            return None
