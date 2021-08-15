from flask import Flask, request, jsonify

from core.brain import Brain
from core.connection.mongodb import MongoDB

app = Flask(__name__)

brain = Brain()
mongodb = MongoDB()

@app.route('/chat', methods=['POST'])
def chatBot():
    chat_input = request.form['chat_input']
    result = brain.predict(chat_input)

    if result is not None:
        tag, score, response = result
        mongodb.insert("lisa", "chatbot-userinputs", {"tag": tag, "input": chat_input, "score": str(score), "response": response, "status": "success"})
        return jsonify(status="Success", tag=tag, score=str(score), response=response)
    else:
        mongodb.insert("lisa", "chatbot-userinputs", {"input": chat_input, "status": "failed"})
        return jsonify(status="Failed to predict response")

if __name__ == '__main__':
    app.run(debug=True)