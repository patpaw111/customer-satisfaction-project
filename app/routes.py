from flask import Blueprint, render_template, jsonify
from .camera import video_feed

# Deklarasikan blueprint terlebih dahulu
main = Blueprint('main', __name__)

# Rute untuk halaman utama
@main.route('/')
def index():
    return render_template('index.html')

# Rute untuk video feed
@main.route('/video')
def video():
    return video_feed()

# Rute untuk mendapatkan emosi terakhir
last_emotion = None
is_sitting = False

@main.route('/emotion')
def emotion():
    global last_emotion
    return jsonify(emotion=last_emotion)

# Rute untuk mendapatkan status duduk
@main.route('/status')
def status():
    global is_sitting
    return jsonify(status="Sitting" if is_sitting else "Not Sitting")
