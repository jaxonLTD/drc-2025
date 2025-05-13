from main import SlayMax
from flask import Flask, send_file

app = Flask(__name__)
bot = SlayMax()

@app.route("/")
def serve_page():
    return send_file("./index.html")

@app.route("/start", methods=['POST'])
def start_robot():
    print("start robot")
    bot.startLoop()
    return { "status" : "started" }

@app.route("/stop", methods=['POST'])
def stop_robot():
    bot.endLoop()
    return { "status" : "stopped" }

@app.route("/img", methods=['POST', 'GET'])
def send_image():
    return send_file("./img.jpg", mimetype='image/jpeg')

if __name__ == "__main__":
    bot.mainLoop()
    app.run(host='0.0.0.0', port=5000, debug=True)