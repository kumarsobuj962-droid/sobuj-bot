import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Sobuj Bot is Running! Boss is Kumarsobuj962"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
