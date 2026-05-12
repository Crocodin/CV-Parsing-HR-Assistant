import pdfplumber
import docx2txt
from io import BytesIO

# the CVExtractor class has aditional methods to extract via path in case we will need it later, but the main method is extract_text which will determine the file type and extract accordingly.
class CVExtractor:
    @staticmethod
    def extract_pdf(file_bytes: bytes) -> str:
        with pdfplumber.open(BytesIO(file_bytes)) as pdf:
            text = ''
            for page in pdf.pages:
                text += page.extract_text()
        return text
    
    @staticmethod
    def extract_pdf_from_path(file_path: str) -> str:
        with pdfplumber.open(file_path) as pdf:
            text = ''
            for page in pdf.pages:
                text += page.extract_text()
        return text
    
    @staticmethod
    def extract_docx(file_bytes: bytes) -> str:
        return docx2txt.process(BytesIO(file_bytes))
    
    @staticmethod
    def extract_docx_from_path(file_path: str) -> str:
        return docx2txt.process(file_path)
    
    @staticmethod
    def what_is_file_type(file_bytes: bytes) -> str:
        starting_bytes = file_bytes[:5]
        if starting_bytes == b'%PDF-':
            return 'pdf'
        # docx files are fundeamentally zip files, so they start with 'PK' (Phil Katz)
        return 'docx' if starting_bytes[:2] == b'PK' else 'unknown'
    
    @staticmethod
    def extract_text(file_bytes: bytes) -> str:
        file_type = CVExtractor.what_is_file_type(file_bytes)
        if file_type == 'pdf':
            return CVExtractor.extract_pdf(file_bytes)
        elif file_type == 'docx':
            return CVExtractor.extract_docx(file_bytes)
        else:
            raise ValueError("Unsupported file type")