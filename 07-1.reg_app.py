import os
from dotenv import load_dotenv
from openai import AzureOpenAI

def main():
    os.system('cls' if os.name == 'nt' else 'clear')

    # 환경변수 로드
    load_dotenv()
    
    # 환경변수에서 키와 엔드포인트 가져오기
    openai_api_key = os.getenv("OPENAI_API_KEY")
    azuer_endpoint = os.getenv("AZUER_OPENAI_ENDPOINT")
    chat_deployment_name = os.getenv("CHAT_DEPLOYMENT_NAME")
    embedding_deployment_name = os.getenv("EMBEDDING_DEPLOYMENT_NAME")
    search_endpoint = os.getenv("SEARCH_ENDPOINT")
    search_api_key = os.getenv("SEARCH_API_KEY")
    search_index_name = os.getenv("SEARCH_INDEX_NAME")
    openai_api_type = os.getenv("OPENAI_API_TYPE")
    openai_api_version = os.getenv("OPENAI_API_VERSION")

    # OpenAI 클라이언트 초기화
    chat_client = AzureOpenAI(
        api_version=openai_api_version,
        azure_endpoint=azuer_endpoint,
        api_key=openai_api_key
    )

    # 프롬프트 설정
    prompt = [
        {
            "role": "system",
            "content": "You are a travel assistant that provides information on travel service"
        }
    ]

    
    while True:
        input_text = input("Enter your question (or type 'exit' to quit): ")
        if input_text.lower() == 'exit':
            #exit 명령어 입력시 프로그램 종료
            break   
        elif input_text.strip() == "":
            # 공백제거하면 입력한것이 없는 경우
            print("Please enter a valid question.")
            continue

        prompt.append({"role": "user","content": input_text})

        # RAG와 관련있는 추가 파라미터 설정
        rag_params = {
            "data_sources": [
                {
                    "type": "azure_search",
                    "parameters": {
                        "endpoint": search_endpoint,
                        "index_name": search_index_name,
                        "authentication": {
                            "type": "api_key",
                            "key": search_api_key
                        },
                        "query_type": "vector",
                        "embedding_dependency": {
                            "type": "deployment_name",
                            "deployment_name": embedding_deployment_name
                        }
                    }
                }
            ]      
        }	

        # RAG를 사용하여 AI 응답 생성
        response = chat_client.chat.completions.create(
            model=chat_deployment_name,
            messages=prompt,
            extra_body=rag_params,
        )

        completion = response.choices[0].message.content
        print(f"Response: {completion}")

        # AI의 응답을 메세지에 누적
        prompt.append({"role": "assistant", "content": completion})

if __name__ == "__main__":
    main()
    