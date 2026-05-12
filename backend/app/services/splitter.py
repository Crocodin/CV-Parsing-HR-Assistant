import re

class Splitter:
    def __init__(self):
        self.KEY_HEADINGS = ['Summary', 'Education', 'Experience', 'Skills', 'Projects', 'Certifications', 'Awards', 'Achievements', 'Publications']

    def contains_heading(self, text: str) -> bool:
        for heading in self.KEY_HEADINGS:
            # r is to make sure the text is treated as a row string
            # we don't take the hole line because the extractor doesn't always extract the new line
            if re.search(r'\w* ?' + re.escape(heading) + r' ?\w*', text, re.IGNORECASE):
                return True
        return False
    
    def split_into_sections(self, text: str) -> list[dict[str, str]]:
        section = []
        current_section = None

        for line in text.splitlines():
            if self.contains_heading(line):
                if current_section is None:
                    current_section = {'heading': line.strip(), 'content': ''}
                else:
                    section.append(current_section)
                    current_section = {'heading': line.strip(), 'content': ''}
            elif current_section is not None:
                current_section['content'] += line + '\n'
        
        if current_section:
            section.append(current_section)

        return section

splitter = Splitter()