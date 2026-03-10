"""Vector store module for Qdrant semantic search over policy documents."""

from functools import lru_cache
from pathlib import Path

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_text_splitters import MarkdownHeaderTextSplitter
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from config import get_settings
from src.schemas import DocSearchResult

EMBEDDING_DIM = 3072  # text-embedding-004 output dimension


class VectorStore:
    """Qdrant-backed vector store for policy document search."""

    def __init__(self, path: str, collection: str, embedding_model: str):
        self.collection = collection
        self._embeddings = GoogleGenerativeAIEmbeddings(model=embedding_model)
        self._client = QdrantClient(path=path)
        self._store = QdrantVectorStore(
            client=self._client,
            collection_name=collection,
            embedding=self._embeddings,
        )

    def _collection_exists(self) -> bool:
        """Return True if the Qdrant collection already has documents."""
        try:
            info = self._client.get_collection(self.collection)
            points_count = info.points_count or 0
            return points_count > 0
        except ValueError:
            return False

    def _create_collection(self) -> None:
        """Create the Qdrant collection if it does not exist."""
        existing = [c.name for c in self._client.get_collections().collections]
        if self.collection not in existing:
            self._client.create_collection(
                collection_name=self.collection,
                vectors_config=VectorParams(
                    size=EMBEDDING_DIM, distance=Distance.COSINE
                ),
            )

    def ensure_indexed(self, docs_dir: Path | None = None) -> None:
        """
        Ensure policy documents are indexed. Indexes on first run only.

        Args:
            docs_dir: Directory containing .md policy files. Defaults to settings.docs_dir.

        """
        if docs_dir is None:
            docs_dir = get_settings().docs_dir

        if self._collection_exists():
            return

        print("Initializing vector store from policy documents...")
        self._create_collection()

        splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=[("#", "h1"), ("##", "h2"), ("###", "h3")],
            strip_headers=False,
        )

        all_chunks = []
        for md_file in sorted(docs_dir.glob("*.md")):
            text = md_file.read_text()
            chunks = splitter.split_text(text)
            for chunk in chunks:
                chunk.metadata["source"] = md_file.name
            all_chunks.extend(chunks)
            print(f" - Chunked {md_file.name} ({len(chunks)} chunks)")

        if not all_chunks:
            print("Warning: No .md files found in docs/")
            return

        self._store.add_documents(all_chunks)
        print(f"Vector store ready. ({len(all_chunks)} total chunks indexed)")

    def similarity_search(self, query: str, k: int = 4) -> list[DocSearchResult]:
        """
        Run semantic similarity search and return typed results.

        Args:
            query: Natural language query string.
            k: Number of results to return.

        Returns:
            List of DocSearchResult with content, source, and score.

        """
        results = self._store.similarity_search_with_score(query, k=k)
        return [
            DocSearchResult(
                content=doc.page_content,
                source=doc.metadata.get("source", "unknown"),
                score=round(float(score), 4),
            )
            for doc, score in results
        ]


@lru_cache
def get_vectorstore() -> VectorStore:
    """
    Get the VectorStore singleton, indexing policy docs on first run.

    Returns:
        VectorStore connected to local Qdrant.

    """
    settings = get_settings()
    vs = VectorStore(
        path=str(settings.qdrant_path),
        collection=settings.qdrant_collection,
        embedding_model=settings.embedding_model,
    )
    vs.ensure_indexed(settings.docs_dir)
    return vs
