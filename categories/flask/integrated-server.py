from flask import Flask
import threading
app = Flask(__name__)

@app.route('/')
def ping():
    return 'Axolotl is online!', 200

def run_flask_server():
    app.run(host='0.0.0.0', port=3827)
print("Starting integrated server.")
# Start the Flask server in a separate thread
flask_thread = threading.Thread(target=run_flask_server)
flask_thread.start()
