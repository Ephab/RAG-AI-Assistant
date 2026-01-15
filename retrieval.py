class Retriever:
    def __init__(self, vector_store):
        self.vector_store = vector_store

    def retrieve(self, query, top_n=5):
        results = self.vector_store.search(query, n_results=top_n)

        retrieved_chunks = []

        if results['documents'] and len(results['documents']) > 0:
            for i in range(len(results['documents'])):
                chunk = {
                    'text': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'distance': results['distances'][0][i] if 'distances' in results else None
                }
                retrieved_chunks.append(chunk)
        return retrieved_chunks

    def format_context(self, chunks):
        if not chunks:
            return "No relevant context found."

        context_parts = []
        for i, chunk in enumerate(chunks, 1):
            source = chunk['metadata'].get('source_pdf', 'Unknown')
            text = chunk['text']
            context_parts.append(f"[Source {i}: {source}]\n{text}\n")

        return "\n---\n".join(context_parts)

    def retrieve_and_format(self, query: str, top_k: int = 5) -> str:
        chunks = self.retrieve(query, top_k)
        return self.format_context(chunks)