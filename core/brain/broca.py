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


    def continue_conversation(self, conversation_id, user_input):
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
        
        #TODO implement restart conversation?
        if current_step is None or current_step == []:
            return {"status": "failed", "message": "Até mais!"}

        conv_response = {}
        result = self.wernicke.predict(user_input)
        if result is not None:
            tag, score, response = result
            self.temporal_lobe.save_prediction({"tag": tag, "conversation_id": conversation_id, "input": user_input, "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "score": str(score), "response": response, "status": "success"})   

            if current_step['label'] == tag:
                conversation['conversation_flow'].append({"step": str(last_step + 1), "tag": tag, "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "input": user_input, "score": str(score), "response": response})
                self.temporal_lobe.update_conversation(conversation_id, conversation)
                return {"status": "success", "message": response}
            else:
                failback = random.choice(self.temporal_lobe.retrieve_failback(current_step['failback'])['messages'])
                conversation['conversation_flow'].append({"step": str(last_step if last_step != 0 else 1), "tag": current_step['label'], "failback": "true", "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "input": user_input, "response": failback})
                self.temporal_lobe.update_conversation(conversation_id, conversation)
                return {"status": "failed", "message": failback}

        else:
            self.temporal_lobe.save_prediction({"input": user_input, "conversation_id": conversation_id, "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "status": "failed"})

            failback = random.choice(self.temporal_lobe.retrieve_failback(current_step['failback'])['messages'])
            conversation['conversation_flow'].append({"step": str(last_step if last_step != 0 else 1), "tag": current_step['label'], "failback": "true", "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "input": user_input, "response": failback})
            
            self.temporal_lobe.update_conversation(conversation_id, conversation)
            return {"status": "failed", "message": failback}