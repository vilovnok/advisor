# from sentence_transformers import SentenceTransformer
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from huggingface_hub import login

login(token='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')

e5 = HuggingFaceEmbeddings(model_name = 'intfloat/e5-mistral-7b-instruct', encode_kwargs = {'normalize_embeddings': True})