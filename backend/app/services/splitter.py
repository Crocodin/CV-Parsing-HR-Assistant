from warnings import deprecated 
import re

@deprecated(reason="Because the inconsistency of the extracted text, we are now using Ollama to generate the JSON directly from the extracted text, instead of splitting it into sections and merging it back together.")
# if you are reading this code let me explain why I deprecated this class, the idea was to split the extracted text into sections based on the headings, then generate JSON for each section and merge them together, but the problem is that the extracted text is not always consistent, a lot of the times pdfplumber (the library we use to extract text from pdfs) doesn't extract the new lines, so we end up with a big chunk of text without any structure, and that makes it very hard to split it into sections. So for now this class is here for historical reasons.
class Splitter:
    def __init__(self):
        self.KEY_HEADINGS = ['Summary', 'Education', 'Experience', 'Skills', 'Projects', 'Certifications', 'Awards', 'Achievements', 'Publications']

    def contains_heading(self, text: str) -> bool:
        for heading in self.KEY_HEADINGS:
            # r is to make sure the text is treated as a row string
            # we don't take the hole line because the extractor doesn't always extract the new line
            if re.search(r'\w* ?' + re.escape(heading) + r' ?\w*', text, re.IGNORECASE):
                return True, heading
        return False, None
    
    def split_into_sections(self, text: str) -> list[dict[str, str]]:
        section = []
        current_section = None

        for line in text.splitlines():
            is_heading, heading = self.contains_heading(line)
            if is_heading:
                if current_section is None:
                    current_section = {'heading': heading, 'content': ''}
                else:
                    section.append(current_section)
                    current_section = {'heading': heading, 'content': ''}
            elif current_section is not None:
                current_section['content'] += line + '\n'
        
        if current_section:
            section.append(current_section)

        return section

splitter = Splitter()