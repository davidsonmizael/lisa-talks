from flask import Flask, request, jsonify

from core.brain import Brain

app = Flask(__name__)

brain = Brain()

@app.route('/chat', methods=['POST'])
def chatBot():
    chat_input = request.form['chat_input']
    result = brain.predict(chat_input)

    if result is not None:
        tag, score, response = result
        return jsonify(status="Success", tag=tag, score=str(score), response=response)
    else:
        return jsonify(status="Failed to predict response")

if __name__ == '__main__':
    app.run(debug=True)