from app.services.ollama import ollama_service
from warnings import deprecated

@deprecated("Because the inconsistency of the extracted text, we are now using Ollama to generate the JSON directly from the extracted text, instead of splitting it into sections and merging it back together.")
# more information about why this class is deprecated can be found in the splitter.py file.
class Merger:
    def make_json(self, sections: list[dict[str, str]]) -> dict:
        json_list = []
        for section in sections:
            header = section['heading']
            content = section['content']
            json_data = ollama_service.generate_json_for_header(header, content)
            json_list.append(json_data)
        
        merged_json = self.merge_jsons(json_list)
        return merged_json

    @staticmethod
    def merge_jsons(json_list):
        merged_json = {}
        for json_data in json_list:
            merged_json.update(json_data)
        return merged_json
    
merger = Merger()