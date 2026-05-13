import json
import ollama
from warnings import deprecated
import json

from app.config.config import config
from app.services.ollama_promts import HEADER_JSON_STRUCTURE, OLLAMA_PROMPT

class OllamaService:
    def __init__(self):
        self.url = config.OLLAMA_URL
        self.client = ollama.Client(self.url)
        self.model = config.OLLAMA_LLM_MODEL
        self.llm_params = config.OLLAMA_LLM_PARAMS

    def generate_response(self, prompt: str) -> str:
        try:
            response = self.client.generate(model=self.model, prompt=prompt, options=self.llm_params)
            return response.response
        except Exception as e:
            print(f"Error generating response from Ollama: {e}")
            raise
    
    @deprecated("This method is deprecated because we are now generating the JSON from one prompt.")
    # more information about why this method is deprecated can be found in the splitter.py file.
    def prompt_for_header(self, header: str, content: str) -> str:
        MAIN_PROMPT = f"""
            You are a helpful assistant that provides information about the following header: {header}.
            Your task is to generate the best feating JSON for the CV part that is realated to the header {header}.
            YOU WILL ONLY RESPOND WITH THE JSON, DO NOT ADD ANYTHING ELSE!
            YOU WILL RESPECT THE FOLLOWING STRUCTURE OF THE JSON:
            {HEADER_JSON_STRUCTURE[header]}

            THIS IS THE CONTENT OF THE CV PART:
            {content}
            """
        return MAIN_PROMPT
    
    @deprecated("This method is deprecated because we are now generating the JSON from one prompt.")
    # more information about why this method is deprecated can be found in the splitter.py file.
    def generate_json_for_header(self, header: str, content: str) -> str:
        prompt = self.prompt_for_header(header, content)
        json_text =self.generate_response(prompt=prompt)

        try:
            # Try to parse the response as JSON
            json_data = json.loads(json_text)
            return json_data
        
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON from Ollama response: {e}")
            return {"error": "Invalid JSON response from Ollama."}
        
    def generate_json_for_cv(self, content: str) -> dict:
        try:
            response = self.client.generate(model=self.model, system=OLLAMA_PROMPT, prompt=content, options=self.llm_params)

            return json.loads(response.response)
        
        except Exception as e:
            print(f"Error generating JSON for CV: {e}")
            raise
        
ollama_service = OllamaService()
