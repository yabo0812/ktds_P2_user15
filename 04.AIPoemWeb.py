import openai
import os
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
import time

# 환경변수 로드
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.azure_endpoint = os.getenv("AZUER_ENDPOINT")
openai.api_type = os.getenv("OPENAI_API_TYPE")
openai.api_version = os.getenv("OPENAI_API_VERSION")

subject = st.text_input("시의 주제를 입력하세요: ")
centent = st.text_area("시의 내용을 입력하세요: ")

button_clicked = st.button("시 생성") ## 버튼이 클릭된 상태값이 들어감

if button_clicked:
    with st.spinner("Wait for it...", show_time=True):
        #time.sleep(5)
        
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
        st.write(response.choices[0].message.content)
    st.success("시 생성 완료!")