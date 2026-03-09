
from flask import Flask, request
import subprocess, json, os, tempfile

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.json
    with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".json") as f:
        json.dump(update, f)
        temp_path = f.name

    # pass update to php bot
    env = os.environ.copy()
    env["TELEGRAM_UPDATE_FILE"] = temp_path

    subprocess.run(["php", "php-bot/index.php"], env=env)

    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
