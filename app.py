from flask import Flask
from Chatbot.routes import chatbot
from graph_rag_recommender.routes import recommend

app = Flask(__name__)
app.register_blueprint(chatbot, url_prefix="/chatbot")
app.register_blueprint(recommend, url_prefix="/recommend")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
