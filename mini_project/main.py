import tkinter as tk
from tkinter import ttk, font as tkfont, scrolledtext
import google.generativeai as genai
import threading
import speech_recognition as sr
from PIL import Image, ImageTk, ImageDraw
import os
from dotenv import load_dotenv
import subprocess
import re

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.5-flash')


# System prompt for computer expert mode
SYSTEM_PROMPT = """You are a computer expert assistant specializing in macOS and zsh terminal commands. 
When users ask you to perform tasks, respond with the exact terminal command(s) needed.
Format your commands in code blocks using ```bash or just provide the raw command.
Always assume macOS with zsh shell.
Be concise and precise."""

class TransparentOverlay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Terminal Assistant")
        
        # Window configuration
        self.root.attributes('-alpha', 0.97)
        self.root.attributes('-topmost', True)
        self.root.overrideredirect(True)
        
        # Modern minimal color palette
        self.bg_main = '#0a0a0a'
        self.bg_secondary = '#141414'
        self.bg_tertiary = '#1e1e1e'
        self.text_primary = '#ffffff'
        self.text_secondary = '#8a8a8a'
        self.accent = '#fe7171'
        self.accent_hover = '#ff5555'
        self.user_bubble = '#2a2a2a'
        self.ai_bubble = '#1a1a1a'
        self.command_bg = '#0d1117'
        self.success = '#3fb950'
        
        # Window size and position - FIXED 800x400
        window_width = 800
        window_height = 400
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = screen_width - window_width - 30
        y = 40
        
        self.root.geometry(f'{window_width}x{window_height}+{x}+{y}')
        self.root.configure(bg=self.bg_main)
        
        # Make draggable
        self.drag_data = {"x": 0, "y": 0}
        
        self.setup_ui()
        self.recognizer = sr.Recognizer()
        self.is_listening = False
        self.chat_history = []
        
    def start_move(self, event):
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        
    def do_move(self, event):
        deltax = event.x - self.drag_data["x"]
        deltay = event.y - self.drag_data["y"]
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")
        
    def setup_ui(self):
        # Top bar with drag handle and close button
        top_bar = tk.Frame(self.root, bg=self.bg_secondary, height=45)
        top_bar.pack(fill='x')
        top_bar.pack_propagate(False)
        
        # Drag area
        drag_frame = tk.Frame(top_bar, bg=self.bg_secondary)
        drag_frame.pack(fill='both', expand=True)
        drag_frame.bind('<Button-1>', self.start_move)
        drag_frame.bind('<B1-Motion>', self.do_move)
        
        # Title
        title_frame = tk.Frame(drag_frame, bg=self.bg_secondary)
        title_frame.pack(side='left', padx=20)
        
        tk.Label(
            title_frame,
            text="⚡",
            font=('SF Pro Display', 16),
            bg=self.bg_secondary,
            fg=self.accent
        ).pack(side='left', padx=(0, 8))
        
        tk.Label(
            title_frame,
            text="THAKUR KE HAATH",
            font=('SF Pro Display', 13, 'bold'),
            bg=self.bg_secondary,
            fg=self.text_primary
        ).pack(side='left')
        
        # Close button
        close_btn = tk.Label(
            drag_frame,
            text="✕",
            font=('SF Pro Display', 16),
            bg=self.bg_secondary,
            fg=self.text_secondary,
            cursor='hand2',
            padx=12
        )
        close_btn.pack(side='right', padx=10)
        close_btn.bind('<Button-1>', lambda e: self.root.quit())
        close_btn.bind('<Enter>', lambda e: close_btn.config(fg=self.accent))
        close_btn.bind('<Leave>', lambda e: close_btn.config(fg=self.text_secondary))
        
        # Main content area - horizontal split
        content = tk.Frame(self.root, bg=self.bg_main)
        content.pack(fill='both', expand=True)
        
        # Left side - Chat display (60% width)
        chat_container = tk.Frame(content, bg=self.bg_main, width=480)
        chat_container.pack(side='left', fill='both', expand=True, padx=(15, 8), pady=15)
        
        # Chat canvas for custom message bubbles
        self.chat_canvas = tk.Canvas(
            chat_container,
            bg=self.bg_main,
            highlightthickness=0,
            bd=0
        )
        self.chat_scrollbar = tk.Scrollbar(
            chat_container,
            orient='vertical',
            command=self.chat_canvas.yview,
            bg=self.bg_secondary,
            troughcolor=self.bg_main,
            bd=0,
            width=6
        )
        
        self.chat_canvas.configure(yscrollcommand=self.chat_scrollbar.set)
        self.chat_scrollbar.pack(side='right', fill='y')
        self.chat_canvas.pack(side='left', fill='both', expand=True)
        
        # Frame inside canvas for messages
        self.messages_frame = tk.Frame(self.chat_canvas, bg=self.bg_main)
        self.canvas_frame = self.chat_canvas.create_window(
            (0, 0),
            window=self.messages_frame,
            anchor='nw',
            width=460
        )
        
        self.messages_frame.bind('<Configure>', self.on_frame_configure)
        self.chat_canvas.bind('<Configure>', self.on_canvas_configure)
        
        # Right side - Input area (40% width)
        input_container = tk.Frame(content, bg=self.bg_secondary, width=320)
        input_container.pack(side='right', fill='both', padx=(8, 15), pady=15)
        input_container.pack_propagate(False)
        
        # Input section title
        tk.Label(
            input_container,
            text="Send Command",
            font=('SF Pro Display', 11, 'bold'),
            bg=self.bg_secondary,
            fg=self.text_secondary,
            anchor='w'
        ).pack(fill='x', padx=15, pady=(10, 8))
        
        # Text input area with border
        input_wrapper = tk.Frame(
            input_container,
            bg=self.bg_tertiary,
            highlightthickness=1,
            highlightbackground='#2a2a2a'
        )
        input_wrapper.pack(fill='both', expand=True, padx=15, pady=(0, 10))
        
        self.input_text = tk.Text(
            input_wrapper,
            bg=self.bg_tertiary,
            fg=self.text_primary,
            font=('SF Pro Text', 11),
            wrap='word',
            bd=0,
            padx=12,
            pady=12,
            insertbackground=self.accent,
            insertwidth=2,
            height=5,
            spacing1=2,
            spacing3=2
        )
        self.input_text.pack(fill='both', expand=True)
        self.input_text.bind('<Return>', self.on_enter_key)
        self.input_text.bind('<Shift-Return>', lambda e: None)
        self.input_text.bind('<FocusIn>', lambda e: input_wrapper.config(highlightbackground=self.accent))
        self.input_text.bind('<FocusOut>', lambda e: input_wrapper.config(highlightbackground='#2a2a2a'))
        
        # Buttons
        btn_frame = tk.Frame(input_container, bg=self.bg_secondary)
        btn_frame.pack(fill='x', padx=15, pady=(0, 10))
        
        # Voice button
        self.voice_btn = tk.Button(
            btn_frame,
            text="🎤 Voice",
            font=('SF Pro Display', 11, 'bold'),
            bg=self.accent,
            fg='#ffffff',
            activebackground=self.accent_hover,
            activeforeground='#ffffff',
            bd=0,
            cursor='hand2',
            padx=20,
            pady=10,
            command=self.toggle_voice_input
        )
        self.voice_btn.pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        # Send button
        self.send_btn = tk.Button(
            btn_frame,
            text="Send",
            font=('SF Pro Display', 11, 'bold'),
            bg=self.bg_tertiary,
            fg=self.text_primary,
            activebackground='#2a2a2a',
            activeforeground=self.text_primary,
            bd=0,
            cursor='hand2',
            padx=20,
            pady=10,
            command=self.send_message
        )
        self.send_btn.pack(side='right', fill='x', expand=True, padx=(5, 0))
        
        # Welcome message
        self.add_system_message("👋 Ready to assist! Try 'open Firefox' or ask me to run commands.")
        
    def on_frame_configure(self, event=None):
        self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox('all'))
        self.chat_canvas.yview_moveto(1.0)
        
    def on_canvas_configure(self, event):
        self.chat_canvas.itemconfig(self.canvas_frame, width=event.width)
        
    def on_enter_key(self, event):
        if not event.state & 0x1:  # If Shift is not pressed
            self.send_message()
            return 'break'
        
    def add_message_bubble(self, text, msg_type='user'):
        """Add a modern message bubble"""
        bubble_frame = tk.Frame(self.messages_frame, bg=self.bg_main)
        bubble_frame.pack(fill='x', pady=4, padx=5)
        
        if msg_type == 'user':
            # User message - right aligned, coral background
            msg_container = tk.Frame(bubble_frame, bg=self.bg_main)
            msg_container.pack(side='right')
            
            msg_label = tk.Label(
                msg_container,
                text=text,
                font=('SF Pro Text', 10),
                bg=self.accent,
                fg='#ffffff',
                padx=14,
                pady=8,
                justify='left',
                wraplength=300,
                anchor='w'
            )
            msg_label.pack()
            
        elif msg_type == 'ai':
            # AI message - left aligned, dark background
            msg_container = tk.Frame(bubble_frame, bg=self.bg_main)
            msg_container.pack(side='left')
            
            msg_label = tk.Label(
                msg_container,
                text=text,
                font=('SF Pro Text', 10),
                bg=self.ai_bubble,
                fg=self.text_primary,
                padx=14,
                pady=8,
                justify='left',
                wraplength=340,
                anchor='w'
            )
            msg_label.pack()
            
        elif msg_type == 'command':
            # Command - left aligned, monospace, green
            msg_container = tk.Frame(bubble_frame, bg=self.bg_main)
            msg_container.pack(side='left', fill='x', expand=True)
            
            msg_label = tk.Label(
                msg_container,
                text=f"$ {text}",
                font=('JetBrains Mono', 9),
                bg=self.command_bg,
                fg=self.success,
                padx=12,
                pady=6,
                justify='left',
                wraplength=400,
                anchor='w'
            )
            msg_label.pack(fill='x')
            
        elif msg_type == 'output':
            # Output - left aligned, monospace, gray
            msg_container = tk.Frame(bubble_frame, bg=self.bg_main)
            msg_container.pack(side='left', fill='x', expand=True)
            
            msg_label = tk.Label(
                msg_container,
                text=text,
                font=('JetBrains Mono', 8),
                bg=self.command_bg,
                fg=self.text_secondary,
                padx=12,
                pady=6,
                justify='left',
                wraplength=400,
                anchor='w'
            )
            msg_label.pack(fill='x')
            
        self.on_frame_configure()
        
    def add_system_message(self, text):
        """Add a centered system message"""
        bubble_frame = tk.Frame(self.messages_frame, bg=self.bg_main)
        bubble_frame.pack(fill='x', pady=6)
        
        msg_label = tk.Label(
            bubble_frame,
            text=text,
            font=('SF Pro Text', 9, 'italic'),
            bg=self.bg_main,
            fg=self.text_secondary,
            justify='center'
        )
        msg_label.pack()
        
        self.on_frame_configure()
        
    def send_message(self):
        """Send text message to AI"""
        message = self.input_text.get('1.0', 'end-1c').strip()
        if not message:
            return
            
        self.input_text.delete('1.0', 'end')
        self.add_message_bubble(message, 'user')
        
        # Add to chat history
        self.chat_history.append({
            'role': 'user',
            'parts': [message]
        })
        
        # Get AI response in background
        threading.Thread(target=self.get_ai_response, args=(message,), daemon=True).start()
        
    def extract_commands(self, text):
        """Extract shell commands from AI response"""
        # Look for code blocks first
        code_blocks = re.findall(r'```(?:bash|sh|zsh)?\n(.*?)```', text, re.DOTALL)
        if code_blocks:
            commands = []
            for block in code_blocks:
                lines = [line.strip() for line in block.split('\n') if line.strip() and not line.strip().startswith('#')]
                commands.extend(lines)
            return commands
        
        # If no code blocks, look for command-like patterns
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
        
    def execute_command(self, command):
        """Execute shell command and return output"""
        try:
            # For 'open' commands, run in background
            if command.strip().startswith('open'):
                subprocess.Popen(
                    command,
                    shell=True,
                    executable='/bin/zsh',
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                return f"✓ Opened: {command.replace('open ', '')}"
            
            # For other commands, capture output
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
        
    def get_ai_response(self, message):
        """Get response from Gemini AI"""
        try:
            self.add_system_message("⏳ Thinking...")
            
            # Create chat with system prompt
            chat = model.start_chat(history=[
                {'role': 'user', 'parts': [SYSTEM_PROMPT]},
                {'role': 'model', 'parts': ['Understood. I will provide zsh terminal commands for macOS tasks.']}
            ] + self.chat_history[:-1])
            
            response = chat.send_message(message)
            response_text = response.text
            
            # Add AI response to history
            self.chat_history.append({
                'role': 'model',
                'parts': [response_text]
            })
            
            self.add_message_bubble(response_text, 'ai')
            
            # Extract and execute commands
            commands = self.extract_commands(response_text)
            if commands:
                for cmd in commands:
                    if cmd.strip():
                        self.add_message_bubble(cmd, 'command')
                        output = self.execute_command(cmd)
                        if output:
                            self.add_message_bubble(output, 'output')
            
            # Generate speech for AI response
            threading.Thread(target=self.speak_response, args=(response_text,), daemon=True).start()
            
        except Exception as e:
            self.add_system_message(f"✗ Error: {str(e)}")
            
    def speak_response(self, text):
        """Use macOS say command to speak the response"""
        try:
            clean_text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
            clean_text = re.sub(r'[`*_#$]', '', clean_text)
            clean_text = clean_text.strip()
            
            if clean_text:
                subprocess.run(['say', '-v', 'Samantha', clean_text], check=False)
        except Exception as e:
            print(f"Speech error: {e}")
            
    def toggle_voice_input(self):
        """Toggle voice input"""
        if self.is_listening:
            return
            
        self.is_listening = True
        self.add_system_message("🎤 Listening... Speak now!")
        threading.Thread(target=self.listen_voice, daemon=True).start()
        
    def listen_voice(self):
        """Listen to voice input and convert to text"""
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            # Recognize speech
            text = self.recognizer.recognize_google(audio)
            self.input_text.delete('1.0', 'end')
            self.input_text.insert('1.0', text)
            self.add_message_bubble(text, 'user')
            
            # Add to chat history
            self.chat_history.append({
                'role': 'user',
                'parts': [text]
            })
            
            # Auto-send
            threading.Thread(target=self.get_ai_response, args=(text,), daemon=True).start()
            
        except sr.WaitTimeoutError:
            self.add_system_message("⚠ No speech detected")
        except sr.UnknownValueError:
            self.add_system_message("⚠ Could not understand audio")
        except Exception as e:
            self.add_system_message(f"✗ Error: {str(e)}")
        finally:
            self.is_listening = False
            
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = TransparentOverlay()
    app.run()

