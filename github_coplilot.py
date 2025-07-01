import streamlit as st
import random

st.title('숫자 맞추기 게임 (1~100)')

# 세션 상태에 정답과 시도 횟수 저장
def init_state():
    if 'answer' not in st.session_state:
        st.session_state['answer'] = random.randint(1, 100)
    if 'tries' not in st.session_state:
        st.session_state['tries'] = 0
    if 'game_over' not in st.session_state:
        st.session_state['game_over'] = False

init_state()

if st.session_state['game_over']:
    st.success(f"축하합니다! {st.session_state['tries']}번 만에 맞췄어요!")
    if st.button('다시 시작'):
        st.session_state['answer'] = random.randint(1, 100)
        st.session_state['tries'] = 0
        st.session_state['game_over'] = False
else:
    guess = st.number_input('1~100 사이의 숫자를 입력하세요', min_value=1, max_value=100, step=1)
    if st.button('제출'):
        st.session_state['tries'] += 1
        if guess < st.session_state['answer']:
            st.info('더 큰 숫자입니다!')
        elif guess > st.session_state['answer']:
            st.info('더 작은 숫자입니다!')
        else:
            st.session_state['game_over'] = True
            st.success(f"정답! {st.session_state['tries']}번 만에 맞췄어요!")

st.write(f"시도 횟수: {st.session_state['tries']}")
