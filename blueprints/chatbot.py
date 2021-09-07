from flask import Blueprint, request, jsonify

from core.brain.broca import Broca
from core.brain.temporal_lobe import TemporalLobe
from dotenv import load_dotenv

load_dotenv()

blueprint = Blueprint('api', __name__, url_prefix='/lisatalk')
broca = Broca()
temporal_lobe = TemporalLobe()

@blueprint.route('/start-conversation', methods=['POST'])
def startConversation():
    user_id = request.form['user_id']
    scope = request.form['scope']
    result = broca.start_conversation(user_id, scope)
    return jsonify(conversation_id=result, user_id=user_id)

@blueprint.route('/continue-conversation', methods=['POST'])
def continueConversation():
    user_input = request.form['chat_input']
    conversation_id = request.form['conversation_id']
    response = broca.continue_conversation(conversation_id, user_input)
    return response

