import os
import sys
from dotenv import load_dotenv
from config import Config
from gemini_service import GeminiService
from logger import ChatLogger

load_dotenv()

class ChatRunner:
    def __init__(self):
        self.gemini = GeminiService()
        self.logger = ChatLogger()
        self.store_name = None

    def start(self):
        print(f"\n📚 '{Config.FILE_PATH}' 파일을 분석 중입니다...")
        
        try:
            self.store_name = self.gemini.create_file_search_store(Config.FILE_PATH)
            print("✅ 분석 완료! 이제 질문해 주세요. (종료하려면 'exit' 또는 'q' 입력)\n")
            
            self._chat_loop()
            
        except Exception as e:
            print(f"❌ 초기화 중 오류 발생: {e}")
        finally:
            # 3. 종료 시 리소스 정리
            if self.store_name:
                print("\n🧹 정리 중...")
                self.gemini.delete_store(self.store_name)
                print("👋 이용해 주셔서 감사합니다.")

    def _chat_loop(self):
        while True:
            try:
                user_input = input("\n🙋 질문: ").strip()
                
                if user_input.lower() in ['exit', 'quit', 'q']:
                    break
                
                if not user_input:
                    continue

                print("🤖 답변 생성 중...", end="\r")

                answer, citations = self.gemini.generate_answer(user_input, self.store_name)
                
                print(f"\n💬 답변: {answer}")
                if citations:
                    print(f"📎 출처: {citations}")
                
                self.logger.log(user_input, answer, citations)
                
            except KeyboardInterrupt:
                break

if __name__ == "__main__":
    if not os.path.exists(Config.FILE_PATH):
        print(f"❌ 오류: '{Config.FILE_PATH}' 파일이 없습니다.")
    else:
        app = ChatRunner()
        app.start()