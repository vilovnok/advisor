from enum import Enum

class LLMModelType(Enum):
    OLLAMA = "ollama"
    MISTRAL = "mistral"

class EmbedModelType(Enum):
    DEEPVK_USER = "deepvk/USER-bge-m3"
    MiniLM = "sentence-transformers/all-MiniLM-L6-v2"
    BM25 = "Qdrant/bm25"
    BERT = "colbert-ir/colbertv2.0"
