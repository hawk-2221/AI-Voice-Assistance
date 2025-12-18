import google.generativeai as genai
import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# 👇 Set your Gemini API key here
os.environ["GOOGLE_API_KEY"] = "AIzaSyD8n6vVOKhSGDTzkbnFIOQOBiuASPQ-nHQ"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

model = genai.GenerativeModel("models/gemini-flash-latest")

# store conversation
conversation_history = []

def voice_assistance(user_input):
    global conversation_history

    prompt = f"""
    You are an AI assistant talking to a user.
    User said: '{user_input}'
    Give a short, clear, and helpful response.
    """

    try:
        response = model.generate_content(prompt).text
    except Exception as e:
        response = "Error: could not connect to AI service."
        print(e)

    # save both user + ai message
    conversation_history.append({
        'user': user_input,
        'ai': response
    })

    return response


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process_voice', methods=['POST'])
def process_voice():
    user_input = request.json.get("user_input", "")
    response = voice_assistance(user_input)
    return jsonify({'response': response, 'conversation_history': conversation_history})


if __name__ == '__main__':
    # debug=True so Flask reloads automatically
    app.run(debug=True)
