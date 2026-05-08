from pypdf import PdfReader

import markdown
from bs4 import BeautifulSoup


from pathlib import Path


from knowledge_base.utils import chunk_text


class KnowledgeIngestor:
    def __init__(self, knowledge_base):
        self.knowledge_base = knowledge_base

        self.pdf_loader = PDFLoader()
        self.md_loader = MarkdownLoader()

    def ingest_directory(self, directory: str):
        documents = []

        for path in Path(directory).rglob("*"):

            if path.suffix == ".pdf":
                text = self.pdf_loader.load(str(path))

            elif path.suffix in [".md", ".markdown"]:
                text = self.md_loader.load(str(path))

            else:
                continue

            chunks = chunk_text(text)

            for chunk in chunks:
                documents.append({
                    "text": chunk,
                    "metadata": {
                        "source": str(path)
                    }
                })

        self.knowledge_base.add_documents(documents)

class PDFLoader:
    def load(self, path: str) -> str:
        reader = PdfReader(path)

        text = []

        for page in reader.pages:
            extracted = page.extract_text()

            if extracted:
                text.append(extracted)

        return "\n".join(text)



class MarkdownLoader:
    def load(self, path: str) -> str:
        with open(path, "r", encoding="utf-8") as f:
            md = f.read()

        html = markdown.markdown(md)

        soup = BeautifulSoup(html, "html.parser")

        return soup.get_text()