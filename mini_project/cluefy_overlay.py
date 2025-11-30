import tkinter as tk
from tkinter import ttk
import google.generativeai as genai
import threading
import speech_recognition as sr
from PIL import Image, ImageTk, ImageDraw
import io

# Configure Gemini API
genai.configure(api_key="YOUR_API_KEY_HERE")
model = genai.GenerativeModel('gemini-2.0-flash-exp')

class TransparentOverlay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Cluefy")
        
        # Window configuration
        self.root.attributes('-alpha', 0.95)
        self.root.attributes('-topmost', True)
        self.root.overrideredirect(True)
        
        # Colors
        self.bg_color = '#1a1a1a'
        self.text_color = '#ffffff'
        self.accent_color = 'rgb(254, 113, 113)'
        self.gray_color = '#808080'
        
        # Window size and position
        window_width = 400
        window_height = 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = screen_width - window_width - 20
        y = 50
        
        self.root.geometry(f'{window_width}x{window_height}+{x}+{y}')
        self.root.configure(bg=self.bg_color)
        
        # Make draggable
        self.root.bind('<Button-1>', self.start_move)
        self.root.bind('<B1-Motion>', self.do_move)
        
        self.setup_ui()
        self.recognizer = sr.Recognizer()
        self.is_listening = False
        
    def start_move(self, event):
        self.x = event.x
        self.y = event.y
        
    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")
        
    def create_circle_image(self, size, color):
        """Create a circular image for buttons"""
        image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        draw.ellipse((0, 0, size-1, size-1), fill=color)
        return ImageTk.PhotoImage(image)
        
    def setup_ui(self):
        # Header with close button
        header_frame = tk.Frame(self.root, bg=self.bg_color, height=40)
        header_frame.pack(fill='x', padx=10, pady=(10, 0))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="CLUEFY",
            font=('Arial', 16, 'bold'),
            bg=self.bg_color,
            fg=self.text_color
        )
        title_label.pack(side='left', pady=5)
        
        close_btn = tk.Button(
            header_frame,
            text="×",
            font=('Arial', 20),
            bg=self.bg_color,
            fg='#fe7171',
            bd=0,
            command=self.root.quit,
            cursor='hand2',
            activebackground=self.bg_color,
            activeforeground='#ff5555'
        )
        close_btn.pack(side='right', pady=5)
        
        # Chat display area
        chat_frame = tk.Frame(self.root, bg=self.bg_color)
        chat_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.chat_display = tk.Text(
            chat_frame,
            bg='#2a2a2a',
            fg=self.text_color,
            font=('Arial', 11),
            wrap='word',
            bd=0,
            padx=10,
            pady=10,
            state='disabled'
        )
        self.chat_display.pack(fill='both', expand=True)
        
        # Configure text tags
        self.chat_display.tag_config('user', foreground='#fe7171', font=('Arial', 11, 'bold'))
        self.chat_display.tag_config('ai', foreground='#ffffff', font=('Arial', 11))
        self.chat_display.tag_config('system', foreground=self.gray_color, font=('Arial', 9, 'italic'))
        
        # Input area
        input_frame = tk.Frame(self.root, bg=self.bg_color)
        input_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        # Text input
        self.input_field = tk.Entry(
            input_frame,
            bg='#2a2a2a',
            fg=self.text_color,
            font=('Arial', 11),
            bd=0,
            insertbackground=self.text_color
        )
        self.input_field.pack(side='left', fill='x', expand=True, ipady=8, padx=(0, 5))
        self.input_field.bind('<Return>', lambda e: self.send_message())
        
        # Microphone button
        mic_btn = tk.Button(
            input_frame,
            text="🎤",
            font=('Arial', 16),
            bg='#fe7171',
            fg=self.text_color,
            bd=0,
            width=3,
            cursor='hand2',
            activebackground='#ff5555',
            command=self.toggle_voice_input
        )
        mic_btn.pack(side='left', ipady=5)
        
        # Send button
        send_btn = tk.Button(
            input_frame,
            text="→",
            font=('Arial', 14, 'bold'),
            bg=self.gray_color,
            fg=self.text_color,
            bd=0,
            width=3,
            cursor='hand2',
            activebackground='#666666',
            command=self.send_message
        )
        send_btn.pack(side='left', padx=(5, 0), ipady=5)
        
    def add_message(self, message, tag):
        """Add message to chat display"""
        self.chat_display.config(state='normal')
        self.chat_display.insert('end', message + '\n\n', tag)
        self.chat_display.see('end')
        self.chat_display.config(state='disabled')
        
    def send_message(self):
        """Send text message to AI"""
        message = self.input_field.get().strip()
        if not message:
            return
            
        self.input_field.delete(0, 'end')
        self.add_message(f"You: {message}", 'user')
        
        # Get AI response in background
        threading.Thread(target=self.get_ai_response, args=(message,), daemon=True).start()
        
    def get_ai_response(self, message):
        """Get response from Gemini AI"""
        try:
            self.add_message("Thinking...", 'system')
            response = model.generate_content(message)
            
            # Remove "Thinking..." message
            self.chat_display.config(state='normal')
            self.chat_display.delete('end-3l', 'end-2l')
            self.chat_display.config(state='disabled')
            
            self.add_message(f"AI: {response.text}", 'ai')
        except Exception as e:
            self.add_message(f"Error: {str(e)}", 'system')
            
    def toggle_voice_input(self):
        """Toggle voice input"""
        if self.is_listening:
            return
            
        self.is_listening = True
        self.add_message("Listening...", 'system')
        threading.Thread(target=self.listen_voice, daemon=True).start()
        
    def listen_voice(self):
        """Listen to voice input and convert to text"""
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
            # Remove "Listening..." message
            self.chat_display.config(state='normal')
            self.chat_display.delete('end-2l', 'end-1l')
            self.chat_display.config(state='disabled')
            
            # Recognize speech
            text = self.recognizer.recognize_google(audio)
            self.input_field.delete(0, 'end')
            self.input_field.insert(0, text)
            self.add_message(f"You (voice): {text}", 'user')
            
            # Auto-send
            threading.Thread(target=self.get_ai_response, args=(text,), daemon=True).start()
            
        except sr.WaitTimeoutError:
            self.chat_display.config(state='normal')
            self.chat_display.delete('end-2l', 'end-1l')
            self.chat_display.config(state='disabled')
            self.add_message("No speech detected", 'system')
        except sr.UnknownValueError:
            self.add_message("Could not understand audio", 'system')
        except Exception as e:
            self.add_message(f"Error: {str(e)}", 'system')
        finally:
            self.is_listening = False
            
    def run(self):
        """Start the application"""
        self.add_message("Welcome to Cluefy! Ask me anything.", 'system')
        self.root.mainloop()

if __name__ == "__main__":
    app = TransparentOverlay()
    app.run()
