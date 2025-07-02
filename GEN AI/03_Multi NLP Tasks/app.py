import streamlit as st
from transformers import pipeline

st.set_page_config(page_title="Multi-Task NLP Hub", page_icon="🤖")
st.title("🤖 Multi-Task NLP ")
st.write(
    "Choose an NLP task and enter your text below."
)

TASKS = {
    "Sentiment Analysis": {
        "pipeline": "sentiment-analysis",
        "model": "distilbert-base-uncased-finetuned-sst-2-english",
        "description": "Classify text as positive or negative sentiment.",
    },
    "Summarization": {
        "pipeline": "summarization",
        "model": "sshleifer/distilbart-cnn-12-6",
        "description": "Summarize long articles or text passages.",
    },
    "Translation (English → French)": {
        "pipeline": "translation_en_to_fr",
        "model": "Helsinki-NLP/opus-mt-en-fr",
        "description": "Translate English text to French.",
    },
    "Text Generation": {
        "pipeline": "text-generation",
        "model": "gpt2",
        "description": "Generate text based on a prompt.",
    },
}

task = st.selectbox("Choose NLP Task:", list(TASKS.keys()))
st.caption(TASKS[task]["description"])

user_input = st.text_area("Enter your text:", height=150)

@st.cache_resource
def get_pipeline(task_name):
    t = TASKS[task_name]
    if task_name == "Translation (English → French)":
        return pipeline("translation_en_to_fr", model=t["model"])
    else:
        return pipeline(t["pipeline"], model=t["model"])

nlp = get_pipeline(task)

if st.button("Run"):
    if not user_input.strip():
        st.warning("Please enter some text first.")
    else:
        with st.spinner("Processing..."):
            if task == "Summarization":
                # Summarization expects max 1024 tokens, so we truncate for demo
                result = nlp(user_input[:1024], max_length=130, min_length=30, do_sample=False)
                summary = result[0]["summary_text"]
                st.markdown("**Summary:**")
                st.success(summary)
            elif task == "Sentiment Analysis":
                result = nlp(user_input)
                label = result[0]["label"]
                score = result[0]["score"]
                st.markdown(f"**Sentiment:** `{label}`  \n**Confidence:** `{score:.2%}`")
            elif task == "Translation (English → French)":
                result = nlp(user_input)
                translation = result[0]["translation_text"]
                st.markdown("**French Translation:**")
                st.success(translation)
            elif task == "Text Generation":
                # For demo, limit to 50 tokens
                result = nlp(user_input, max_length=50, num_return_sequences=1)
                generated = result[0]["generated_text"]
                st.markdown("**Generated Text:**")
                st.info(generated)