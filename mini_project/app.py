from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv
import subprocess
import re
import threading
import webview

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.5-flash')

app = Flask(__name__)
CORS(app)

# System prompt
SYSTEM_PROMPT = """You are a computer expert assistant specializing in macOS and zsh terminal commands. 
When users ask you to perform tasks, respond with the exact terminal command(s) needed.
Format your commands in code blocks using ```bash or just provide the raw command.
Always assume macOS with zsh shell.
Be concise and precise."""

chat_history = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        message = data.get('message', '')
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Add to chat history
        chat_history.append({
            'role': 'user',
            'parts': [message]
        })
        
        # Create chat with system prompt
        chat = model.start_chat(history=[
            {'role': 'user', 'parts': [SYSTEM_PROMPT]},
            {'role': 'model', 'parts': ['Understood. I will provide zsh terminal commands for macOS tasks.']}
        ] + chat_history[:-1])
        
        response = chat.send_message(message)
        response_text = response.text
        
        # Add AI response to history
        chat_history.append({
            'role': 'model',
            'parts': [response_text]
        })
        
        # Extract and execute commands
        commands = extract_commands(response_text)
        command_results = []
        
        for cmd in commands:
            if cmd.strip():
                output = execute_command(cmd)
                command_results.append({
                    'command': cmd,
                    'output': output
                })
        
        # Speak response in background
        threading.Thread(target=speak_response, args=(response_text,), daemon=True).start()
        
        return jsonify({
            'response': response_text,
            'commands': command_results
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def extract_commands(text):
    """Extract shell commands from AI response"""
    code_blocks = re.findall(r'```(?:bash|sh|zsh)?\n(.*?)```', text, re.DOTALL)
    if code_blocks:
        commands = []
        for block in code_blocks:
            lines = [line.strip() for line in block.split('\n') if line.strip() and not line.strip().startswith('#')]
            commands.extend(lines)
        return commands
    
    lines = text.split('\n')
    commands = []
    command_starters = ['open', 'ls', 'cd', 'mkdir', 'rm', 'cp', 'mv', 'cat', 'echo', 'grep', 
                      'find', 'chmod', 'chown', 'sudo', 'brew', 'git', 'python', 'python3', 
                      'pip', 'pip3', 'npm', 'node', 'curl', 'wget', 'kill', 'ps', 'top']
    
    for line in lines:
        line = line.strip()
        if line and any(line.startswith(cmd) for cmd in command_starters):
            commands.append(line)
    
    return commands

def execute_command(command):
    """Execute shell command and return output"""
    try:
        if command.strip().startswith('open'):
            subprocess.Popen(
                command,
                shell=True,
                executable='/bin/zsh',
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            return f"✓ Opened: {command.replace('open ', '')}"
        
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30,
            executable='/bin/zsh',
            cwd=os.path.expanduser('~')
        )
        
        output = result.stdout + result.stderr
        return output.strip() if output.strip() else "✓ Command executed successfully"
    except subprocess.TimeoutExpired:
        return "⚠ Command timed out after 30 seconds"
    except Exception as e:
        return f"✗ Error: {str(e)}"

def speak_response(text):
    """Use macOS say command to speak the response"""
    try:
        clean_text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
        clean_text = re.sub(r'[`*_#$]', '', clean_text)
        clean_text = clean_text.strip()
        
        if clean_text:
            subprocess.run(['say', '-v', 'Samantha', clean_text], check=False)
    except Exception as e:
        print(f"Speech error: {e}")

def start_app():
    """Start Flask app in a frameless window"""
    window = webview.create_window(
        'THAKUR KE HAATH',
        app,
        width=900,
        height=600,
        resizable=True,
        frameless=False,
        easy_drag=True,
        background_color='#0a0a0a'
    )
    webview.start()

if __name__ == '__main__':
    # Start the app with pywebview
    threading.Thread(target=lambda: app.run(debug=False, port=5000, use_reloader=False), daemon=True).start()
    start_app()
