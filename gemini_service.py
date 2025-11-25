import time
from typing import Tuple
from google import genai
from google.genai import types
from config import Config

class GeminiService:
    
    def __init__(self):
        self.client = genai.Client()

    def create_file_search_store(self, file_path: str) -> str:
        store_name_suffix = f"Chat_{int(time.time())}"
        store = self.client.file_search_stores.create(config={'display_name': store_name_suffix})
        
        chunk_size = Config.CHUNK_SIZE
        overlap_size = int(chunk_size * 0.1)

        operation = self.client.file_search_stores.upload_to_file_search_store(
            file=file_path,
            file_search_store_name=store.name,
            config={
                'display_name': 'Chat Document',
                'chunking_config': {
                    'white_space_config': {
                        'max_tokens_per_chunk': chunk_size,
                        'max_overlap_tokens': overlap_size 
                    }
                }
            }
        )
        
        while not operation.done:
            time.sleep(1)
            operation = self.client.operations.get(operation)
            
        return store.name

    def delete_store(self, store_name: str):
        try:
            self.client.file_search_stores.delete(name=store_name)
        except Exception:
            pass

    def generate_answer(self, question: str, store_name: str) -> Tuple[str, str]:
        full_prompt = f"{Config.SYSTEM_INSTRUCTION}\n\n질문: {question}"
        
        try:
            response = self.client.models.generate_content(
                model=Config.MODEL_NAME,
                contents=full_prompt,
                config=types.GenerateContentConfig(
                    tools=[types.Tool(file_search=types.FileSearch(file_search_store_names=[store_name]))],
                    temperature=Config.TEMPERATURE
                )
            )
            answer = response.text if response.text else "(답변을 생성할 수 없습니다.)"
            citations = self._extract_citations(response)
            return answer, citations
        except Exception as e:
            return f"오류 발생: {e}", "Error"

    def _extract_citations(self, response) -> str:
        if not hasattr(response, 'grounding_metadata') or not response.grounding_metadata.citations:
            return ""
        
        citations = []
        for idx, citation in enumerate(response.grounding_metadata.citations, 1):
            uri = citation.uri if citation.uri else "Unknown"
            citations.append(f"[{idx}] {uri}")
        return ", ".join(citations)