#!/usr/bin/env python
from core.brain.wernicke import Wernicke
from core.brain.temporal_lobe import TemporalLobe
from datetime import datetime
import random

"""
Broca is the part of the brain responsible for the speech control
"""
class Broca:

    def __init__(self):
        self.temporal_lobe = TemporalLobe()
        self.wernicke = Wernicke()

    def start_conversation(self, user_id, scope):
        now = datetime.now()
        conversation = {
            "user_id": user_id,
            "start_time": now.strftime("%d/%m/%Y %H:%M:%S"),
            "scope": scope,
            "conversation_flow":[
            ]
        }

        return self.temporal_lobe.save_conversation(conversation)

    def retrieve_conversation(self, conversation_id):
        conversation = self.temporal_lobe.retrieve_conversation(conversation_id)
        if conversation['conversation_flow'] == []:
            last_step = 0   
        else:
            if('failback' in conversation['conversation_flow'][-1]):
                if(conversation['conversation_flow'][-1]['failback'] == 'true' and conversation['conversation_flow'][-1]['step'] == '1'):
                    last_step = 0
            else:
                last_step = int(conversation['conversation_flow'][-1]['step']) 

        current_decisiontree = self.temporal_lobe.retrieve_scope(conversation['scope'])
        current_step = []
        for step in current_decisiontree['flow']:
            if step['step'] == str( last_step + 1):
                current_step = step
        
        return current_decisiontree, conversation, last_step, current_step

    def continue_conversation(self, conversation_id, request):
        current_decisiontree, conversation, last_step, current_step = self.retrieve_conversation(conversation_id)
        step_actions = current_step['actions']

        failed_to_predict = True
        predicted_intent = None
        current_step_no = int(current_step['step'])
        response = {}

        if current_step['type'] == 'input':
            if 'predict-intent' in step_actions:
                user_input = request.form['user_input']
                predicted_intent = self.wernicke.predict(user_input)
        else:
            if current_step['type'] == 'message':
                reply_msg = random.choice(self.temporal_lobe.retrieve_reply(current_step['message'])['messages'])

            if current_step['type'] == 'question':
                reply_msg = random.choice(self.temporal_lobe.retrieve_question(current_step['message'])['messages'])

            conversation['conversation_flow'].append({"step": str(last_step + 1), "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "type": "bot_message", "response": reply_msg})
            self.temporal_lobe.update_conversation(conversation_id, conversation)
            return {"status": "success", "lisa-response": [reply_msg]}

        for action in step_actions:
            if action == 'predict-intent':
                if predicted_intent is not None:
                    tag, score = predicted_intent

                    if tag == step_actions[action] or tag in step_actions[action]:
                        failed_to_predict = False
                        self.temporal_lobe.save_prediction({"tag": tag, "conversation_id": conversation_id, "input": user_input, "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "score": str(score), "status": "success"})   
                    else:
                        failed_to_predict = True
                        self.temporal_lobe.save_prediction({"input": user_input, "predicted": tag, "expected_value": step_actions[action], "conversation_id": conversation_id, "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "status": "failed"})
                        break
                else:
                    failed_to_predict = True
                    self.temporal_lobe.save_prediction({"input": user_input, "expected_value": step_actions[action], "conversation_id": conversation_id, "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "status": "failed"})
                    break

            if action == 'reply-with-message':
                reply_msg = random.choice(self.temporal_lobe.retrieve_reply(step_actions[action])['messages'])
                if 'reply-messages' not in response:
                    response['reply-messages'] = []
                response['reply-messages'].append(reply_msg)
            elif action == 'reply-with-question':
                if 'reply-question' not in response:
                    response['reply-question'] = []
                db_question = self.temporal_lobe.retrieve_question(step_actions[action])
                response['reply-question']['question'] = db_question['question']
                if 'options' in db_question:
                    response['reply-question']['options'] = db_question['options']
            elif action == 'reply-with-condition':
                reply_msg = random.choice(self.temporal_lobe.retrieve_reply(step_actions['reply-with-condition'][tag])['messages'])
                if 'reply-messages' not in response:
                    response['reply-messages'] = []
                response['reply-messages'].append(reply_msg)
            elif action == 'save-reply':
                previous_question = "Unavailable"
                for step in current_decisiontree['flow']:
                    if step['step'] == str(last_step) and step['type'] == 'question':
                        previous_question = step['message']
                self.temporal_lobe.save_user_input({"conversation_id": conversation_id, "user_id": conversation['user_id'], "step": str(current_step_no), "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "previous_question": previous_question ,"user_input": user_input})
            elif action == 'jump-to-step':
                last_step = current_step_no
                current_step_no += 1
                for step in current_decisiontree['flow']:
                    if step['step'] == str(int(current_step['step']) + 1):
                        if step['type'] == 'question':
                            if 'reply-question' not in response:
                                response['reply-question'] = {}
                            db_question = self.temporal_lobe.retrieve_question(step['message'])
                            response['reply-question']['question'] = db_question['question']
                            if 'options' in db_question:
                                response['reply-question']['options'] = db_question['options']

                        if step['type'] == 'message':
                            if 'reply-message' not in response:
                                response['reply-message'] = []
                                response['reply-messages'].append(reply_msg = random.choice(self.temporal_lobe.retrieve_reply(step['message'])['messages']))
                
        if not failed_to_predict or response:
            conversation['conversation_flow'].append({"step": str(current_step_no), "tag": tag, "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "type": "user_input", "input": user_input, "score": str(score), "response": response})
            self.temporal_lobe.update_conversation(conversation_id, conversation)
            return {"status": "success", "lisa-response": response}
        else:
            if 'reply-messages' not in response:
                response['reply-messages'] = []
                response['reply-messages'].append(random.choice(self.temporal_lobe.retrieve_failback(current_step['failback'])['messages']))
            conversation['conversation_flow'].append({"step": str(last_step if last_step != 0 else 1), "tag": current_step['label'], "failback": "true", "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "input": user_input, "response": response})
            self.temporal_lobe.update_conversation(conversation_id, conversation)
            return {"status": "failed", "lisa-response": response}