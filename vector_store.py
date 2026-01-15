import pathlib
import chromadb
from sentence_transformers import SentenceTransformer


class VectorStore:
    def __init__(self):
        self.save_dir = "./chroma_db"
        pathlib.Path(self.save_dir).mkdir(parents=True, exist_ok=True)

        self.client = chromadb.PersistentClient(path=self.save_dir)
        self.collection = self.client.get_or_create_collection(name="rag_db")

        print("Loading embeddings model")
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2') # open source embedding model
        print("Embeddings model finished loading")


    def create_embeddings(self, texts: list):
        embeddings = self.embedding_model.encode(texts, show_progress_bar=True)
        return embeddings.tolist()


    def add_chunks(self, chunks, source_pdf):
        texts = [chunk['text'] for chunk in chunks]

        embed = self.create_embeddings(texts)

        metadatas = []
        for chunk in chunks:
            metadata = {
                "source_pdf": source_pdf,
                'chunk_id': str(chunk['chunk_id']),
                'token_count': str(chunk["token_count"]),
                'source_file': str(chunk['source_file']),
                'source_name': str(chunk['source_name'])
            }
            metadatas.append(metadata)

        ids = [f"{source_pdf}_chunk_{chunk['chunk_id']}" for chunk in chunks]

        self.collection.add(
            documents=texts,
            embeddings=embed,
            metadatas=metadatas,
            ids=ids
        )
        print(f"added {len(chunks)} to the database")


    def search(self, query, n_results=5):
        query_embed = self.create_embeddings([query])

        results = self.collection.query(
            query_embeddings=query_embed,
            n_results=n_results
        )
        return results

    def get_collection_count(self):
        return self.collection.count()

    def clear_collection(self):
        self.client.delete_collection(self.collection.name)
        self.collection = self.client.get_or_create_collection(
            name=self.collection.name,
        )
        print("database cleared")