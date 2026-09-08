import hashlib
import math
from pathlib import Path

import chromadb

from app.config import CHROMA_PATH


class SimpleEmbedder:
    """
    Small deterministic embedding function used by WeatherGPT RAG.

    It is intentionally lightweight and works completely offline.
    """

    def __init__(self, dimensions=256):
        self.dimensions = dimensions

    def embed(self, text):
        vector = [0.0] * self.dimensions

        words = text.lower().split()

        for word in words:
            digest = hashlib.sha256(
                word.encode("utf-8")
            ).hexdigest()

            index = int(digest[:8], 16) % self.dimensions
            vector[index] += 1.0

        norm = math.sqrt(
            sum(value * value for value in vector)
        )

        if norm > 0:
            vector = [
                value / norm
                for value in vector
            ]

        return vector


class RAGEngine:

    def __init__(self):

        Path(CHROMA_PATH).mkdir(
            parents=True,
            exist_ok=True
        )

        self.embedder = SimpleEmbedder()

        self.client = chromadb.PersistentClient(
            path=CHROMA_PATH
        )

        self.collection = self.client.get_or_create_collection(
            name="weathergpt_knowledge"
        )

        self._seed_documents()

    def _seed_documents(self):

        documents = [

            {
                "id": "rainfall_bands",
                "text": (
                    "IMD rainfall classification includes heavy rainfall "
                    "at 64.5 mm or more, very heavy rainfall at 115.6 mm "
                    "or more, and extremely heavy rainfall at 204.5 mm "
                    "or more in a 24-hour period."
                ),
                "source": "IMD rainfall classification",
                "type": "knowledge",
            },

            {
                "id": "heatwave",
                "text": (
                    "A heatwave can create risks to human health, livestock, "
                    "agriculture, and water availability. During severe heat, "
                    "people should reduce exposure, stay hydrated, and follow "
                    "official local advisories."
                ),
                "source": "WeatherGPT heatwave guidance",
                "type": "knowledge",
            },

            {
                "id": "flood_protocol",
                "text": (
                    "During flooding or severe rainfall, avoid flood-prone "
                    "areas, move to safer elevated locations when necessary, "
                    "protect livestock and equipment, and follow official "
                    "emergency instructions."
                ),
                "source": "WeatherGPT disaster protocol",
                "type": "knowledge",
            },

            {
                "id": "cyclone_protocol",
                "text": (
                    "During cyclone or damaging wind conditions, secure loose "
                    "objects, protect crops and equipment, avoid exposed "
                    "areas, and follow official warnings."
                ),
                "source": "WeatherGPT disaster protocol",
                "type": "knowledge",
            },

            {
                "id": "agronomy",
                "text": (
                    "Farmers should consider rainfall, temperature, humidity, "
                    "wind, soil moisture, crop growth stage, and drainage when "
                    "making weather-sensitive agricultural decisions."
                ),
                "source": "General agronomy guidance",
                "type": "knowledge",
            },
        ]

        existing = self.collection.get()

        existing_ids = set(
            existing.get("ids", [])
        )

        new_documents = [
            document
            for document in documents
            if document["id"] not in existing_ids
        ]

        if not new_documents:
            return

        self.collection.add(
            ids=[
                document["id"]
                for document in new_documents
            ],
            documents=[
                document["text"]
                for document in new_documents
            ],
            embeddings=[
                self.embedder.embed(
                    document["text"]
                )
                for document in new_documents
            ],
            metadatas=[
                {
                    "source": document["source"],
                    "type": document["type"],
                }
                for document in new_documents
            ],
        )

    def add_document(
        self,
        document_id,
        text,
        source,
        document_type="historical_weather",
    ):
        """
        Add a new document to the existing WeatherGPT
        ChromaDB collection.

        This will be used later for historical weather data.
        """

        existing = self.collection.get(
            ids=[document_id]
        )

        if existing.get("ids"):
            return

        self.collection.add(
            ids=[document_id],
            documents=[text],
            embeddings=[
                self.embedder.embed(text)
            ],
            metadatas=[
                {
                    "source": source,
                    "type": document_type,
                }
            ],
        )

    def add_documents(
        self,
        documents,
        source="Historical weather dataset",
        document_type="historical_weather",
    ):
        """
        Add multiple documents to the existing RAG collection.

        Each document must contain:
            {
                "id": "...",
                "text": "..."
            }
        """

        if not documents:
            return

        existing = self.collection.get()

        existing_ids = set(
            existing.get("ids", [])
        )

        new_documents = [
            document
            for document in documents
            if document["id"] not in existing_ids
        ]

        if not new_documents:
            return

        self.collection.add(
            ids=[
                document["id"]
                for document in new_documents
            ],
            documents=[
                document["text"]
                for document in new_documents
            ],
            embeddings=[
                self.embedder.embed(
                    document["text"]
                )
                for document in new_documents
            ],
            metadatas=[
                {
                    "source": document.get(
                        "source",
                        source
                    ),
                    "type": document.get(
                        "type",
                        document_type
                    ),
                }
                for document in new_documents
            ],
        )

    def retrieve_context(
        self,
        query,
        n_results=3
    ):

        query_embedding = self.embedder.embed(
            query
        )

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
        )

        contexts = []

        documents = results.get(
            "documents",
            [[]]
        )[0]

        metadatas = results.get(
            "metadatas",
            [[]]
        )[0]

        for document, metadata in zip(
            documents,
            metadatas
        ):
            contexts.append(
                {
                    "text": document,
                    "source": metadata.get(
                        "source",
                        "knowledge base"
                    ),
                    "type": metadata.get(
                        "type",
                        "knowledge"
                    ),
                }
            )

        return contexts

    def count_documents(self):
        """
        Return the number of documents currently
        stored in the WeatherGPT RAG collection.
        """

        result = self.collection.get()

        return len(
            result.get("ids", [])
        )


rag_engine = RAGEngine()


def retrieve_context(
    query,
    n_results=3
):
    return rag_engine.retrieve_context(
        query,
        n_results
    )
