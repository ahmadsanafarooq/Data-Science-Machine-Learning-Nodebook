import streamlit as st
import whisper
from transformers import pipeline
import tempfile
import os
from fpdf import FPDF
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.set_page_config(page_title="Voice-to-Summary Assistant", layout="centered")
st.title("🎙️ Voice-to-Summary Meeting Assistant")
st.write("Upload a meeting audio file to get transcription, summary, action items, and key topics.")

@st.cache_resource
def load_whisper():
    return whisper.load_model("small")

@st.cache_resource
def load_summarizer():
    return pipeline("summarization", model="facebook/bart-large-cnn")

whisper_model = load_whisper()
summarizer = load_summarizer()

uploaded_file = st.file_uploader("Upload an audio file (.mp3 or .wav)", type=["mp3", "wav"])

if uploaded_file is not None:
    st.audio(uploaded_file)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    st.info("Transcribing audio... This may take a minute.")
    transcription = whisper_model.transcribe(tmp_path)["text"]

    st.success("Transcription Complete ✅")

    # 🔍 Search input
    st.subheader("🔤 Transcribed Text")
    search_term = st.text_input("Search in Transcript", "")
    
    def highlight_text(text, term):
        pattern = re.compile(re.escape(term), re.IGNORECASE)
        return pattern.sub(f"**:orange[\\g<0>]**", text)

    if search_term.strip():
        st.markdown(highlight_text(transcription, search_term), unsafe_allow_html=True)
    else:
        st.write(transcription)

    # 🧠 Summary
    st.info("Summarizing...")
    summary_output = summarizer(transcription[:1024], max_length=150, min_length=50, do_sample=False)[0]["summary_text"]
    st.success("Summary Generated ✅")
    st.subheader("🧠 Summary of Meeting")
    st.write(summary_output)

    # ✅ Action Items
    st.info("Extracting Action Items...")
    prompt_text = f"Extract all action items and decisions from this meeting transcript:\n{transcription[:1024]}"
    action_items = summarizer(prompt_text, max_length=100, min_length=30, do_sample=False)[0]["summary_text"]
    st.success("Action Items Extracted ✅")
    st.subheader("✅ Action Items")
    st.write(action_items)

    # ☁️ Word Cloud
    st.subheader("☁️ Word Cloud of Transcript")
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(transcription)
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)

    # 📄 Save to TXT
    txt_content = (
        f"Meeting Summary:\n{summary_output}\n\n"
        f"Action Items:\n{action_items}\n\n"
        f"Transcript:\n{transcription}"
    )
    st.download_button("⬇️ Download as .txt", txt_content, file_name="meeting_summary.txt")

    # 📄 Save to PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt_content)

    pdf_path = os.path.join(tempfile.gettempdir(), "meeting_summary.pdf")
    pdf.output(pdf_path)

    with open(pdf_path, "rb") as f:
        st.download_button("⬇️ Download as .pdf", f, file_name="meeting_summary.pdf")

    os.remove(tmp_path)
    os.remove(pdf_path)