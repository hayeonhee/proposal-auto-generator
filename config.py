class Config:
    MODEL_NAME = "gemini-2.5-flash"
    FILE_PATH = 'proposal.md'
    
    CHUNK_SIZE = 512  
    
    TEMPERATURE = 0.1
    
    SYSTEM_INSTRUCTION = """
    당신은 문서 기반 AI 어시스턴트입니다. 
    사용자의 질문에 대해 제공된 문서를 바탕으로 정확하고 친절하게 답변해 주세요.
    문서에 없는 내용은 지어내지 말고 '문서에서 정보를 찾을 수 없습니다'라고 말하세요.
    """