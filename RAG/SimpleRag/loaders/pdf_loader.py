from langchain_community.document_loaders import PyPDFLoader
def load_pdf(file_path: str):
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    return documents

# pdf - 10
# Page-1. Page-2. page-3.     Page-10