from flask import Flask, request, render_template, jsonify
import google.generativeai as genai
from PIL import Image
import io

app = Flask(__name__)

# Configure Gemini API
genai.configure(api_key="AIzaSyBq5EZFCV19CJY__Ovbv_bdCFTrFZTyR1E")
model = genai.GenerativeModel("models/gemini-1.5-pro-latest")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/describe-once", methods=["POST"])
def describe_once():
    image_bytes = request.files['image'].read()
    try:
        response = model.generate_content([
            {"text": "Describe what is happening in this image in one short sentence."},
            {"mime_type": "image/jpeg", "data": image_bytes}
        ])
        return jsonify({"result": response.text})
    except Exception as e:
        return jsonify({"result": f"Error: {str(e)}"})

@app.route("/voice-query", methods=["POST"])
def voice_query():
    if 'image' not in request.files or 'query' not in request.form:
        return jsonify({"result": "Missing image or query."})

    image_bytes = request.files['image'].read()
    query = request.form['query']

    try:
        response = model.generate_content([
            {"text": query},
            {"mime_type": "image/jpeg", "data": image_bytes}
        ])
        return jsonify({"result": response.text})
    except Exception as e:
        return jsonify({"result": f"Error: {str(e)}"})
    
@app.route("/random-page")
def random_page():
    return render_template("random-page.html")


if __name__ == "__main__":
    app.run(debug=True)
