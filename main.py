from llm_interface import stream_ai_response
from parse_pdf import parse_pdf_to_markdown
from chunking import chunk_md_file
from vector_store import VectorStore
from retrieval import Retriever
import pathlib
import tqdm
from tkinter import filedialog, Tk
import shutil

def index_pdfs():
    print("1) Indexing pdfs...\n")

    vector_store = VectorStore()

    existing_count = vector_store.get_collection_count()
    if existing_count > 0:
        print(f"Found {existing_count} existing chunks in vector store")
        response = input("Do you want to reindex (clear existing data)? (y/n): ")
        if response.lower() == 'y':
            vector_store.clear_collection()
        else:
            print("-> using existing index.")
            return vector_store

    print("\nConverting PDFs to markdown...")
    md_files = []
    try:
        for file in tqdm.tqdm(list(pathlib.Path("pdfs").iterdir())):
            if file.is_file() and file.suffix == '.pdf':
                parse_pdf_to_markdown(str(file))
                pdf_name = file.stem
                md_dir = pathlib.Path(f"md_files/{pdf_name}")
                if md_dir.exists():
                    for md_file in md_dir.iterdir():
                        if md_file.suffix == '.md':
                            md_files.append((str(md_file), str(file.name)))
    except Exception as e:
        print(f"error parsing PDFs, {e}")
        return None

    print("\n2) Chunking PDFs...")
    total_chunks = 0
    for md_file, pdf_name in tqdm.tqdm(md_files):
        try:
            chunks = chunk_md_file(md_file, chunk_size=500, overlap=50)
            vector_store.add_chunks(chunks, pdf_name)
            total_chunks += len(chunks)
        except Exception as e:
            print(f"\nError processing {md_file}: {e}")

    print(f"\n Indexing complete, total chunks indexed: {total_chunks}")
    return vector_store

def query_pdfs(vector_store: VectorStore):
    print("\n--- RAG Assistant system ---\n")
    print("Ask questions about your PDFs:")
    print("Type 'quit' or 'exit' to stop\n")

    retriever = Retriever(vector_store)

    while True:
        query = input("\nYour question: ").strip()

        if query.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break

        if not query:
            continue

        print("\nSearching PDFs...")
        context = retriever.retrieve_and_format(query, top_k=3)

        print("\nGenerating answer...\n")
        print("Answer: ", end="", flush=True)

        full_query = f"Context from PDFs:\n{context}\n\nQuestion: {query}"

        for chunk in stream_ai_response(
            full_query,
            system_prompt="You are a helpful and smart research assistant. Answer questions based on the provided context from the PDFs. Be accurate and cite sources when possible."
        ):
            print(chunk, end="", flush=True)
        print("\n")

def chat_without_documents():
    print("Chat with the AI assistant:")
    print("Type 'quit' or 'exit' to stop\n")

    while True:
        query = input("\nYou: ").strip()

        if query.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break

        if not query:
            continue

        print("\nAssistant: ", end="", flush=True)

        for chunk in stream_ai_response(
            query,
            system_prompt="You are a helpful and smart assistant."
        ):
            print(chunk, end="", flush=True)
        print("\n")

def get_pdfs():
    root = Tk()
    root.withdraw()
    file_paths = filedialog.askopenfilenames(title="Choose your PDF files",
                                             filetypes=(("PDF files", "*.pdf"), ("All files", "*.*")))
    root.update()
    root.destroy()

    if file_paths:
        dst_path = pathlib.Path("pdfs")
        dst_path.mkdir(parents=True, exist_ok=True)
        for path in file_paths:
            path = pathlib.Path(path)
            shutil.copy(path, dst_path)

def main():
    print("Starting RAG system...")

    decision = input("Do you want to enter files for context? (y/n): ")
    if decision.lower() == "y":
        md = pathlib.Path("md_files")
        pdfs = pathlib.Path("pdfs")

        if md.exists():
            shutil.rmtree(md)
        if pdfs.exists():
            shutil.rmtree(pdfs)

        md.mkdir(parents=True, exist_ok=True)
        pdfs.mkdir(parents=True, exist_ok=True)

        get_pdfs()
        vector_store = index_pdfs()
    else:
        vector_store = None

    if vector_store is None or vector_store.get_collection_count() == 0:
        print("\nNo documents found. Switching to regular chat mode...\n")
        chat_without_documents()
    else:
        query_pdfs(vector_store)

if __name__ == "__main__":
    main()

