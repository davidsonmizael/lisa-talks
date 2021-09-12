#!/usr/bin/env python
from core.connection.mongodb import MongoDB
from bson.objectid import ObjectId

"""
Temporal Lobe is the part of the brain responsible for the memory.
"""
class TemporalLobe:

    def __init__(self):
        mongodb = MongoDB()
        mongodb.connect()
        self.db = mongodb.client['lisa']

    def retrieve_intents(self):
        col = self.db.get_collection("chatbot-intents")
        return {'intents': list(col.find({}))}

    def save_conversation(self, conversation):
        col = self.db.get_collection("chatbot-conversations")
        return str(col.insert(conversation))

    def update_conversation(self, conversation_id, conversation):
        col = self.db.get_collection("chatbot-conversations")
        del conversation['_id']
        col.update_one({'_id':ObjectId(conversation_id)}, {"$set": conversation}, upsert=True)

    def save_prediction(self, prediction):
        col = self.db.get_collection("chatbot-userinputs-predictions")
        col.insert(prediction)

    def save_user_input(self, user_input):
        col = self.db.get_collection("userdata-responses")
        col.insert(user_input)

    def retrieve_conversation(self, conversation_id):
        col = self.db.get_collection("chatbot-conversations")
        return col.find_one({"_id": ObjectId(conversation_id)})

    def retrieve_failback(self, failback):
        col = self.db.get_collection("chatbot-messages")
        return col.find_one({"type": "failback", "tag": failback})

    def retrieve_reply(self, tag):
        col = self.db.get_collection("chatbot-messages")
        return col.find_one({"type": "reply", "tag": tag})

    def retrieve_question(self, tag):
        col = self.db.get_collection("chatbot-messages")
        return col.find_one({"type": "question", "tag": tag})

    def retrieve_scope(self, scope):
        col = self.db.get_collection("chatbot-decisiontree")
        return col.find_one({"scope": scope})
    