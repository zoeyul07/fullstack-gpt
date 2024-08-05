#데이터가 바뀔 때 마다 파이썬 파일 전체가 위엣서부터 아래까지 전부 다시 실행된다.

import streamlit as st

#ai 부터 받은 모든것을 넣을 수 있따.
#st.write()

st.set_page_config(
  page_title="FullstackGPT Home",
  page_icon="🤖"
)

st.markdown(
  """
# Hello!

Welcome to my FullstackGPT portfolio!
Here are the apps I made:

- [ ] [DocumentGPT](/DocumentGPT)
- [ ] [PrivateGPT](/PrivateGPT)
- [ ] [QuizGPT](/QuizGPT)
- [ ] [SiteGPT](/SiteGPT)
- [ ] [MeetingGPT](/MeetingGPT)
- [ ] [InvestorGPT](/InvestorGPT)
"""
)