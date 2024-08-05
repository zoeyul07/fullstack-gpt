import streamlit as st
from langchain.vectorstores.faiss import FAISS
from langchain.storage import LocalFileStore
from langchain.document_loaders import  UnstructuredFileLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, CacheBackedEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(temperature=0.1)

st.set_page_config(
  page_title="DocumentGPT",
  page_icon="📃"
)

#streamlit이 Input으로 들어오는 파일을 보고 동일하면 이 함수를 재실행시키지 않고 이전에 반환했던것을 반환하게된다.
@st.cache_data(show_spinner="Embedding files...")
def embed_file(file):
  file_content = file.read()
  file_path = f"./.cache/files/{file.name}"
  with open(file_path, "wb") as f:
    f.write(file_content)
  #각각의 파일을 위해 embedding을 cache 한다.
  cache_dir = LocalFileStore(f"./.cache/embeddings/{file.name}")
  splitter = CharacterTextSplitter.from_tiktoken_encoder(
    separator="\n",
    chunk_size=600,
    chunk_overlap=100
  )
  loader = UnstructuredFileLoader(file_path)
  docs = loader.load_and_split(text_splitter=splitter)
  embeddings = OpenAIEmbeddings()
  cached_embeddings = CacheBackedEmbeddings.from_bytes_store(embeddings, cache_dir)
  vectorstore = FAISS.from_documents(docs, cached_embeddings)
  retriever = vectorstore.as_retriever()
  return retriever

def send_message(message, role, save=True):
  with st.chat_message(role):
    st.markdown(message)
  if save:
    st.session_state["messages"].append({"message":message, "role":role})


def paint_history():
  for message in st.session_state["messages"]:
    send_message(message["message"], message["role"], save=False)

def format_document(docs):
  return "\n\n".join(document.page_content for document in docs)

prompt = ChatPromptTemplate.from_messages([
  (
    "system", 
    """
    Answer the question using ONLY the following context. If you don't know the answer just say you don't know. DON'T make anything up.

    Context: {context}
    """
  ),
  ("human", "{question}")
])

st.title("DocumentGPT")

st.markdown(
  """
Welcome!

Use this chatbot to ask question to an AI about your files!

Upload your files on the sidebar.
"""
)

with st.sidebar:
  file = st.file_uploader("Upload a .txt .pdf or .docx file", type=["pdf", "txt", "docx"])

if file:
  retriever = embed_file(file)
  send_message("I'm ready! Ask away!", "ai", save=False)
  paint_history()
  message = st.chat_input("Ask anything about your file")
  if message:
    send_message(message, "human")
    chain = {
      "context": retriever | RunnableLambda(format_document),
      "question": RunnablePassthrough()
    } | prompt | llm

    #하단 코드를 위처럼(chain) 사용할수도 있다.
    
    """ docs = retriever.invoke(message)
    docs = "\n\n".join(document.page_content for document in docs)
    prompt = template.format_messages(context=docs, question=message) """
    

    response = chain.invoke(message)
    send_message(response.content, "ai")
else:
  st.session_state["messages"] = []
