from flask import Flask, request, jsonify, render_template_string
import requests
import json

app = Flask(__name__)

# Your Gemini API Key
GEMINI_API_KEY = "AIzaSyAJxFYRAc_lSqN5nHaNu07v1ahM3a2H_xQ"

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Gemini AI Chat</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #007bff, #0056b3);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        .header p {
            opacity: 0.9;
            font-size: 1.1em;
        }
        .chat-container {
            padding: 20px;
            height: 500px;
            overflow-y: auto;
            background: #f8f9fa;
        }
        .message {
            margin: 15px 0;
            padding: 15px 20px;
            border-radius: 25px;
            max-width: 80%;
            line-height: 1.4;
            animation: fadeIn 0.3s ease-in;
        }
        .user-message {
            background: linear-gradient(135deg, #007bff, #0056b3);
            color: white;
            margin-left: auto;
            border-bottom-right-radius: 5px;
        }
        .bot-message {
            background: white;
            color: #333;
            border: 2px solid #e9ecef;
            border-bottom-left-radius: 5px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .input-area {
            padding: 20px;
            background: white;
            border-top: 1px solid #e9ecef;
            display: flex;
            gap: 10px;
        }
        .input-area input {
            flex: 1;
            padding: 15px 20px;
            border: 2px solid #e9ecef;
            border-radius: 25px;
            font-size: 16px;
            outline: none;
            transition: border-color 0.3s;
        }
        .input-area input:focus {
            border-color: #007bff;
        }
        .input-area button {
            padding: 15px 30px;
            background: linear-gradient(135deg, #007bff, #0056b3);
            color: white;
            border: none;
            border-radius: 25px;
            font-size: 16px;
            cursor: pointer;
            transition: transform 0.2s;
        }
        .input-area button:hover {
            transform: translateY(-2px);
        }
        .typing {
            color: #666;
            font-style: italic;
            padding: 10px 20px;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Gemini AI Chat</h1>
            <p>Powered by Google's Gemini 2.5 Flash</p>
        </div>
        
        <div class="chat-container" id="chat">
            <div class="message bot-message">
                Hello! I'm Gemini AI powered by the latest Gemini 2.5 Flash model. How can I help you today?
            </div>
        </div>
        
        <div class="input-area">
            <input type="text" id="userInput" placeholder="Type your message here..." autocomplete="off">
            <button onclick="sendMessage()">Send</button>
        </div>
    </div>

    <script>
        function addMessage(text, isUser) {
            const chat = document.getElementById('chat');
            const messageDiv = document.createElement('div');
            messageDiv.className = isUser ? 'message user-message' : 'message bot-message';
            messageDiv.textContent = text;
            chat.appendChild(messageDiv);
            chat.scrollTop = chat.scrollHeight;
        }

        function showTyping() {
            const chat = document.getElementById('chat');
            const typing = document.createElement('div');
            typing.className = 'typing';
            typing.id = 'typingIndicator';
            typing.textContent = 'Gemini is thinking...';
            chat.appendChild(typing);
            chat.scrollTop = chat.scrollHeight;
        }

        function hideTyping() {
            const typing = document.getElementById('typingIndicator');
            if (typing) typing.remove();
        }

        async function sendMessage() {
            const input = document.getElementById('userInput');
            const message = input.value.trim();
            
            if (!message) return;

            addMessage(message, true);
            input.value = '';
            input.disabled = true;
            
            showTyping();

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: message })
                });

                const data = await response.json();
                hideTyping();
                addMessage(data.response, false);
            } catch (error) {
                hideTyping();
                addMessage('Sorry, there was an error. Please try again.', false);
                console.error('Error:', error);
            }
            
            input.disabled = false;
            input.focus();
        }

        document.getElementById('userInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });

        document.getElementById('userInput').focus();
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'response': 'Please enter a message.'})
        
        # Use the CORRECT model: gemini-2.5-flash
        url = "https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent"
        params = {'key': GEMINI_API_KEY}
        
        headers = {'Content-Type': 'application/json'}
        
        payload = {
            "contents": [{
                "parts": [{"text": user_message}]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 1000
            }
        }
        
        # Make the API request
        response = requests.post(url, params=params, headers=headers, json=payload, timeout=30)
        
        print(f"API Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if 'candidates' in result and result['candidates']:
                ai_response = result['candidates'][0]['content']['parts'][0]['text']
                return jsonify({'response': ai_response})
            else:
                return jsonify({'response': "I couldn't generate a response. Please try again."})
        else:
            error_detail = response.text
            return jsonify({'response': f"API Error {response.status_code}: {error_detail}"})
            
    except requests.exceptions.Timeout:
        return jsonify({'response': "Request timeout. Please try again."})
    except Exception as e:
        return jsonify({'response': f"Connection error: {str(e)}"})

if __name__ == '__main__':
    print("🚀 Starting Gemini AI Chat Server...")
    print("✅ Using Gemini 2.5 Flash (Latest Model)")
    print("📍 Local URL: http://localhost:8080")
    print("📱 Access from browser on your phone")
    print("\nTo make it public, run in another terminal:")
    print("ngrok http 8080")
    print("\nPress Ctrl+C to stop the server")
    app.run(host='0.0.0.0', port=8080, debug=False)
