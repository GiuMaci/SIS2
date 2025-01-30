from transformers import BertModel, BertTokenizer
from sentence_transformers import SentenceTransformer
import torch
import numpy as np
import gensim.downloader as api


class Embeddings:
    def __init__(self, model_name="glove"):
        """
        Initializes the embedding model.
        :param model_name: 'glove' for GloVe, 'sbert' for SBERT
        """
        self.model_name = model_name

        if model_name == "glove":
            print("Loading GloVe embeddings...")
            self.model = api.load("glove-twitter-25")
        elif model_name == "sbert":
            print("Loading SBERT model...")
            self.model = SentenceTransformer("paraphrase-MiniLM-L6-v2")
        else:
            raise ValueError("Invalid model name. Choose 'glove' or 'sbert'.")

    def embed(self, text):
        """
        Generates an embedding for the input text.
        :param text: The input text string
        :return: Embedding vector
        """
        text = text.lower()

        if self.model_name == "glove":
            return self._embed_glove(text)
        elif self.model_name == "sbert":
            return self._embed_sbert(text)

    def _embed_glove(self, text):
        """Embeds text using GloVe (averaging word vectors)."""
        words = text.split()
        embeddings = [self.model[word] for word in words if word in self.model]

        if embeddings:
            return np.mean(embeddings, axis=0)  # Average word embeddings
        else:
            return np.zeros(self.model.vector_size)  # Return zero vector if no words found

    def _embed_sbert(self, text):
        """Embeds text using SBERT."""
        return self.model.encode(text)  # Get SBERT embedding
