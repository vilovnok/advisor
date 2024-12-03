from pymilvus import MilvusClient, model
from pymilvus.model.sparse.bm25.tokenizers import build_default_analyzer
from pymilvus.model.sparse import BM25EmbeddingFunction
from pymilvus.model import SentenceTransformerEmbeddingFunction


client = MilvusClient(uri="http://localhost:19530", timeout=300)



sentence_transformer_ef = SentenceTransformerEmbeddingFunction(
    model_name='all-MiniLM-L6-v2',
    device='cpu'
)

# docs = [
#     "Artificial intelligence was founded as an academic discipline in 1956.",
#     "Alan Turing was the first person to conduct substantial research in AI.",
#     "Born in Maida Vale, London, Turing was raised in southern England.",
# ]

# docs_embeddings = sentence_transformer_ef.encode_documents(docs)

# analyzer = build_default_analyzer(language="en")