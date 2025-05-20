from flask import Flask, render_template, request
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
import os

app = Flask(__name__)
model = tf.keras.models.load_model(r"E:\DS Material\CNN\model.h5")

inv_map = {
    0: 'bacterial_leaf_blight',
    1: 'bacterial_leaf_streak',
    2: 'bacterial_panicle_blight',
    3: 'blast',
    4: 'brown_spot',
    5: 'dead_heart',
    6: 'downy_mildew',
    7: 'hispa',
    8: 'normal',
    9: 'tungro'
}

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        img_file = request.files["file"]
        if img_file:
            img_path = os.path.join("static", img_file.filename)
            img_file.save(img_path)

            img = image.load_img(img_path, target_size=(64, 64))
            x = image.img_to_array(img) / 255.0
            x = np.expand_dims(x, axis=0)
            pred = model.predict(x)
            result = inv_map[np.argmax(pred)]

            return render_template("index.html", result=result, img_path=img_path)

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
