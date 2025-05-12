import os
from flask import Flask
from Chatbot.routes import chatbot
from graph_rag_recommender.routes import recommender

app = Flask(__name__)
app.register_blueprint(chatbot, url_prefix="/chatbot")
app.register_blueprint(recommender, url_prefix="/recommend")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
