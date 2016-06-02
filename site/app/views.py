from app import app
from . import diacritics_restoration
from flask import request
from flask import render_template
from flask import jsonify

@app.route('/')
def my_form():
    return render_template("index.html")

@app.route('/',methods=['POST'])
def index():
    data = request.form
    lang = data['selectlang']
    new_text,dias = diacritics_restoration.everything(data['text'],lang)
    new_text = new_text.replace('\n','</br>')
    return jsonify({'text': new_text,'dias': dias})
