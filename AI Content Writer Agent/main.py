# content_writer_gui.py
import os
import re
from flask import Flask, render_template, request
from content_writer_agent import generate_blog_post
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

def clean_markdown(text):
    return re.sub(r'(\*\*|##+|\*|__|~~|`{1,3})', '', text)

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    if request.method == 'POST':
        topic = request.form.get('topic')
        if topic:
            result_raw = generate_blog_post(topic)
            result = {
                "blog_post": clean_markdown(result_raw["blog_post"]),
                "seo": clean_markdown(result_raw["seo"])
            }
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
