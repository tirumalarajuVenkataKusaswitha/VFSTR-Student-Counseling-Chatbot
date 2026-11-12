# =========================================================
# 📦 IMPORTS
# =========================================================
import os, json
import streamlit as st
import pandas as pd
from groq import Groq
from streamlit_mic_recorder import mic_recorder

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders.csv_loader import CSVLoader

# =========================================================
# ⚙️ CONFIG
# =========================================================
st.set_page_config(page_title="Vignan AI Counselor", layout="wide")

DATA_PATH = "clg_data"
CHAT_FILE = "chat.json"
EMO_FILE = "emotion.json"

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# =========================================================
# 🎨 UI
# =========================================================
dark = st.sidebar.toggle("🌙 Dark Mode")

bg = "#0f172a" if dark else "#f1f5f9"
card = "#1e293b" if dark else "#ffffff"

st.markdown(f"""
<style>
body {{background:{bg};}}
.card {{
    background:{card};
    padding:15px;
    border-radius:12px;
}}
.header {{
    background: linear-gradient(135deg,#1e3a8a,#2563eb);
    padding:20px;
    border-radius:15px;
    color:white;
    text-align:center;
}}
</style>
""", unsafe_allow_html=True)

# =========================================================
# 🔐 LOGIN
# =========================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in=False

if not st.session_state.logged_in:
    st.markdown('<div class="header"><h1>🎓 AI Counselor Login</h1></div>', unsafe_allow_html=True)

    role=st.selectbox("Role",["Student","Parent","Counselor"])
    user=st.text_input("Username")
    pwd=st.text_input("Password",type="password")

    if st.button("Login"):
        if role in ["Student","Parent"] and user==pwd:
            st.session_state.update({"logged_in":True,"role":role,"user":user})
        elif role=="Counselor" and user.startswith("EMP") and user==pwd:
            st.session_state.update({"logged_in":True,"role":role,"user":user})
        else:
            st.error("Invalid login")
    st.stop()

# =========================================================
# 💾 STORAGE
# =========================================================
def load_data(f):
    return json.load(open(f)) if os.path.exists(f) else []

def save_data(f,d):
    json.dump(d,open(f,"w"),indent=2)

chat=load_data(CHAT_FILE)
emo=load_data(EMO_FILE)

# =========================================================
# 📚 RAG (SMART + TAGGED)
# =========================================================
@st.cache_resource
def build_db():
    docs=[]
    splitter=RecursiveCharacterTextSplitter(chunk_size=800,chunk_overlap=150)
    emb=HuggingFaceEmbeddings()

    FILE_TAGS={
        "attendance.pdf":"attendance subjects percentage",
        "Fees_and_Financial.pdf":"fees payment",
        "Examination.pdf":"exam rules",
        "emotion.pdf":"mental health",
        "stress.pdf":"stress help",
        "career_guidance.csv":"career jobs"
    }

    for file in os.listdir(DATA_PATH):
        path=os.path.join(DATA_PATH,file)

        if file.endswith(".pdf"):
            loader=PyPDFLoader(path)
            pages=loader.load()

            for p in pages:
                chunks=splitter.split_text(p.page_content)
                for c in chunks:
                    docs.append(Document(
                        page_content=c,
                        metadata={"source":file,"tag":FILE_TAGS.get(file,"")}
                    ))

        elif file.endswith(".csv"):
            csv_docs=CSVLoader(file_path=path).load()
            for d in csv_docs:
                d.metadata={"source":file,"tag":FILE_TAGS.get(file,"")}
            docs.extend(csv_docs)

    return FAISS.from_documents(docs,emb).as_retriever(search_kwargs={"k":5})

retriever=build_db()

# =========================================================
# 🧠 RESPONSE (SUBJECT FIX)
# =========================================================
def get_response(query):
    docs=retriever.invoke(query)

    context="\n\n".join([
        f"[{d.metadata['source']}]\n{d.page_content}"
        for d in docs
    ])

    prompt=f"""
You are Vignan AI Counselor.

IMPORTANT:
- Extract real subject names with attendance
- DO NOT write "Subject 1, Subject 2"
- Use actual names from context
- Format like:

Subject Name → 85%

- If not available say "Information not available"

Context:
{context}

Question:
{query}
"""

    res=client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role":"user","content":prompt}],
        temperature=0.3
    )

    return res.choices[0].message.content

# =========================================================
# 😊 EMOTION
# =========================================================
def detect_emotion(t):
    t=t.lower()
    if "stress" in t: return "Stress"
    if "sad" in t: return "Sad"
    if "happy" in t: return "Happy"
    return "Neutral"

# =========================================================
# 📊 DASHBOARD
# =========================================================
st.markdown('<div class="header"><h2>🎓 AI Counselor</h2></div>', unsafe_allow_html=True)

c1,c2,c3,c4=st.columns(4)
c1.metric("Attendance","82%")
c2.metric("CGPA","8.2")
c3.metric("Stress","Moderate")
c4.metric("Status","Active")

# =========================================================
# 💬 CHAT
# =========================================================
if "msgs" not in st.session_state:
    st.session_state.msgs=[]

for m in st.session_state.msgs:
    with st.chat_message(m["role"]):
        st.markdown(f'<div class="card">{m["content"]}</div>',unsafe_allow_html=True)

col1,col2=st.columns([4,1])
with col1:
    inp=st.chat_input("Ask anything...")
with col2:
    audio=mic_recorder(key="mic")

if audio:
    txt=client.audio.transcriptions.create(
        file=("audio.wav",audio["bytes"]),
        model="whisper-large-v3"
    )
    inp=txt.text

# =========================================================
# 🧭 SERVICES
# =========================================================
with st.sidebar:
    st.markdown("## 🧭 Services")

    if st.button("📊 Attendance"):
        inp="Show my attendance with subject names"

    if st.button("📝 Exam Policy"):
        inp="Explain exam rules"

    if st.button("💸 Fees"):
        inp="Fee details"

    if st.button("🚀 Career"):
        inp="Career guidance"

    if st.button("🧠 Stress Help"):
        inp="I feel stressed"

    st.markdown("### 📈 Emotion Graph")
    df=pd.DataFrame(emo)
    if not df.empty:
        st.bar_chart(df["emotion"].value_counts())

# =========================================================
# 🚀 PROCESS
# =========================================================
if inp:
    user=st.session_state.user
    st.session_state.msgs.append({"role":"user","content":inp})

    emotion=detect_emotion(inp)
    emo.append({"user":user,"emotion":emotion})
    save_data(EMO_FILE,emo)

    res=get_response(inp)

    chat.append({"user":user,"q":inp,"a":res})
    save_data(CHAT_FILE,chat)

    st.session_state.msgs.append({"role":"assistant","content":res})

    with st.chat_message("assistant"):
        st.markdown(f'<div class="card">{res}</div>',unsafe_allow_html=True)