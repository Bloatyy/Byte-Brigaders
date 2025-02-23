from flask import Flask, render_template, request, jsonify
from chatbot import CollegeAdvisor

app = Flask(__name__)
advisor = CollegeAdvisor()

@app.route('/')
def home():
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'Empty message'}), 400
            
        response = advisor.get_response(user_message)
        return jsonify({
            'response': advisor.format_response(response)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)