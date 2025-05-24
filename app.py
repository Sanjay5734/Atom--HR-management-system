import os
import json
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_core.messages import HumanMessage
from chatbot import graph  # <-- Your chatbot logic

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route("/chat", methods=["POST"])
def chat_api():
    data = request.get_json()
    user_input = data.get("query", "")

    if not user_input:
        return jsonify({"error": "Empty query"}), 400

    try:
        config = {"thread_id": "123"}  # static for now
        stream = graph.stream(
            {"messages": [HumanMessage(content=user_input)]},
            config,
            stream_mode="values"
        )

        final_response = ""
        for step in stream:
            for msg in step["messages"]:
                if hasattr(msg, "content"):
                    final_response = msg.content

        return jsonify({"answer": final_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
