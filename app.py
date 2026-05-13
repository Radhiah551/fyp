from flask import Flask, request, jsonify, send_from_directory
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(
    api_key="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"
)

@app.route('/')
def home():
    return send_from_directory('.', 'Peer Collab Hub fixed.html')

@app.route('/ai-support', methods=['POST'])
def ai_support():

    try:

        data = request.json
        message = data.get("message")

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role":"system",
                    "content":"You are a friendly academic peer support AI assistant for university students. Give supportive, short, and helpful study advice."
                },
                {
                    "role":"user",
                    "content":message
                }
            ]
        )

        reply = response.choices[0].message.content

        return jsonify({
            "reply": reply
        })

    except Exception as e:

        return jsonify({
            "reply": f"Error: {str(e)}"
        })

if __name__ == '__main__':
    app.run(debug=True)