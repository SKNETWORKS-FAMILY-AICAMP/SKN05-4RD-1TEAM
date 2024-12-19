from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
import os

# 환경 변수 로드
load_dotenv()

# 환경 변수 값 확인
print("OPENAI_API_KEY:", os.getenv("OPENAI_API_KEY"))

def initialize_qa_chain():
    """
    Chroma 벡터 저장소 및 QA 체인 초기화
    """
    # 환경 변수에서 OpenAI API 키 가져오기
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY가 설정되지 않았습니다. .env 파일을 확인해주세요.")

    # OpenAIEmbeddings 및 ChatOpenAI에 API 키 전달
    vector_store = Chroma(
        persist_directory="./chroma_db",
        embedding_function=OpenAIEmbeddings(openai_api_key=openai_api_key)
    )
    qa_chain = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(model_name="gpt-4", openai_api_key=openai_api_key),
        retriever=vector_store.as_retriever()
    )
    return qa_chain
