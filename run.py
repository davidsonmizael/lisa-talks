from flask import Flask, request, jsonify

from blueprints import chatbot_blueprint

app = Flask(__name__)
app.register_blueprint(chatbot_blueprint)
if __name__ == '__main__':
    app.run(debug=True)