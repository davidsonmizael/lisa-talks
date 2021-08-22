from flask import Flask, request, jsonify

from core.brain.broca import Broca
from core.brain.temporal_lobe import TemporalLobe
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

broca = Broca()
temporal_lobe = TemporalLobe()

@app.route('/start-conversation', methods=['POST'])
def startConversation():
    user_id = request.form['user_id']
    scope = request.form['scope']
    result = broca.start_conversation(user_id, scope)
    return jsonify(conversation_id=result, user_id=user_id)

@app.route('/continue-conversation', methods=['POST'])
def continueConversation():
    user_input = request.form['chat_input']
    conversation_id = request.form['conversation_id']
    response = broca.continue_conversation(conversation_id, user_input)
    return response


if __name__ == '__main__':
    app.run(debug=True)