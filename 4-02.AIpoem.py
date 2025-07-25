import openai
import os
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.azure_endpoint = os.getenv("AZUER_ENDPOINT")
openai.api_type = os.getenv("OPENAI_API_TYPE")
openai.api_version = os.getenv("OPENAI_API_VERSION")

subject = input("시의 주제를 입력하세요: ")
centent = input("시의 내용을 입력하세요: ")

#OpenAI API 호출 예시
response = openai.chat.completions.create(
    model="dev-gpt-4.1-mini",
    temperature=0.8,
    max_tokens=500,
    messages=[
        {"role": "system", "content": "You are a AI Poem generator."},
        {"role": "user", "content": "시의 주제는 "+ subject },
        {"role": "user", "content": "시의 내용은 "+ centent },
        {"role": "user", "content": "이 내용으로 시를 써줘."}
    ]
)

#응답 출력
print(response.choices[0].message.content)