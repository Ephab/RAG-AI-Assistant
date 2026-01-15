import pathlib
import tiktoken


def count_tokens(text, model="gpt-3.5-turbo"):
    encoding_model = tiktoken.encoding_for_model(model)
    tokens = encoding_model.encode(text)
    return len(tokens), encoding_model


def chunk_text(text, chunk_size=500, overlap=50):
    if overlap >= chunk_size:
        raise Exception("Overlap must be less than chunk_size")

    chunks = []

    num_tokens, encoder = count_tokens(text)
    tokens = encoder.encode(text)

    start = 0
    end = chunk_size

    chunk_id = 0

    while True:
        next_chunk = tokens[start : end]
        tokens_read = len(next_chunk)

        if tokens_read == 0: # we read an empty slice thus we are finished
            break

        chunk_txt = encoder.decode(next_chunk)

        chunk = {
            'text': chunk_txt,
            'chunk_id': chunk_id,
            'start_token': start,
            'end_token': start + tokens_read,
            'token_count': tokens_read
        }

        chunks.append(chunk)

        step = (chunk_size - overlap)

        chunk_id += 1
        start += step
        end += step

    return chunks


def chunk_md_file(file_path, chunk_size, overlap):
    text = pathlib.Path(file_path).read_text(encoding='utf-8')
    chunks = chunk_text(text, chunk_size=chunk_size, overlap=overlap)

    for chunk in chunks:
        chunk['source_file'] = file_path
        chunk['source_name'] = pathlib.Path(file_path).stem

    return chunks
