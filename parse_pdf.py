import pymupdf.layout
import pymupdf4llm
import pathlib

pathlib.Path("md_files").mkdir(parents=True, exist_ok=True) # make dir if not exists already
pathlib.Path("pdfs").mkdir(parents=True, exist_ok=True) # again, same idea here

def getFileCount(currentdir):
    count = 0
    for file in pathlib.Path(str(currentdir)).iterdir():
        if file.is_file():
            count += 1
    return count


def parse_pdf_to_markdown(file_path: str):
    md_text = pymupdf4llm.to_markdown(file_path)

    pdf_name = pathlib.Path(file_path).stem #get just filename

    subdir = pathlib.Path(f"md_files/{pdf_name}")
    subdir.mkdir(parents=True, exist_ok=True)

    next_file_num = getFileCount(subdir) + 1

    pathlib.Path(f"{subdir}/mdfile{next_file_num}.md").write_bytes(md_text.encode())