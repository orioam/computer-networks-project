import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog
import sys
import subprocess
import random

# --- הגדרות עיצוב (ערכת נושא כהה/כחולה) ---
COLOR_BG = "#1e2124"        # רקע כללי
COLOR_SIDEBAR = "#282b30"   # רקע צד
COLOR_BTN = "#7289da"       # כפתור ראשי (כחול דיסקורד)
COLOR_BTN_HOVER = "#5b6eae"
COLOR_TEXT = "#ffffff"      # טקסט לבן
COLOR_MSG_ME = "#7289da"    # הודעות שלי
COLOR_MSG_OTHER = "#424549" # הודעות של אחרים
FONT_MAIN = ("Segoe UI", 11)
FONT_BOLD = ("Segoe UI", 11, "bold")

# הגדרות רשת
HOST = '127.0.0.1'
PORT = 5555
SEPARATOR = "|"

# --- בוט חכם (Easter Egg) ---
class AutoBot:
    TRIGGERS = {
        "hello": ["System: Greetings.", "System: Online and listening."],
        "joke": ["Why do Java developers wear glasses? Because they don't C#.", "I asked my router for a joke, but it dropped the packet."],
        "status": ["System: All systems nominal.", "System: CPU at optimal temperature."],
        "secret": ["You found the easter egg! 🥚"]
    }
    
    @staticmethod
    def get_response(msg):
        msg = msg.lower()
        for key, responses in AutoBot.TRIGGERS.items():
            if key in msg:
                return random.choice(responses)
        return None

# --- המחלקה הראשית של האפליקציה ---
class ModernChatClient:
    def __init__(self):
        self.sock = None
        self.username = ""
        self.running = True
        self.selected_user = None # עם מי אני מדבר כרגע
        self.chat_history = {}    # היסטוריית שיחות {user: [messages]}
        
        # יצירת חלון ראשי
        self.root = tk.Tk()
        self.root.title("NetChat Pro v2.0")
        self.root.geometry("800x600")
        self.root.configure(bg=COLOR_BG)
        
        # בניית ממשק המשתמש
        self.setup_ui()
        
        # התחלת האזנה לסגירת חלון
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # הצגת מסך התחברות בהתחלה
        self.show_login_dialog()
        
        self.root.mainloop()

    def setup_ui(self):
        """ בניית ה-Layout של החלון: צד ימין צ'אט, צד שמאל משתמשים """
        # --- תפריט צד (רשימת משתמשים) ---
        self.frame_sidebar = tk.Frame(self.root, bg=COLOR_SIDEBAR, width=200)
        self.frame_sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.frame_sidebar.pack_propagate(False) # מונע התכווצות

        tk.Label(self.frame_sidebar, text="ONLINE USERS", bg=COLOR_SIDEBAR, fg="gray", font=("Segoe UI", 9, "bold")).pack(pady=10)
        
        self.user_list_box = tk.Listbox(self.frame_sidebar, bg=COLOR_SIDEBAR, fg=COLOR_TEXT, bd=0, selectbackground=COLOR_BTN, font=FONT_MAIN)
        self.user_list_box.pack(fill=tk.BOTH, expand=True, padx=5)
        self.user_list_box.bind("<<ListboxSelect>>", self.on_user_select)

        # כפתור לפתיחת לקוח חדש (לבדיקות)
        tk.Button(self.frame_sidebar, text="+ New Client", bg="#2c2f33", fg="white", bd=0, command=self.spawn_new_client).pack(side=tk.BOTTOM, fill=tk.X, pady=10, padx=10)

        # --- אזור הצ'אט הראשי ---
        self.frame_chat = tk.Frame(self.root, bg=COLOR_BG)
        self.frame_chat.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # כותרת השיחה
        self.lbl_chat_header = tk.Label(self.frame_chat, text="Select a user to chat", bg=COLOR_BG, fg="gray", font=("Segoe UI", 14))
        self.lbl_chat_header.pack(pady=10)

        # חלון ההודעות
        self.txt_messages = scrolledtext.ScrolledText(self.frame_chat, bg=COLOR_BG, fg=COLOR_TEXT, font=FONT_MAIN, state='disabled', bd=0)
        self.txt_messages.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)
        # עיצוב תגיות טקסט
        self.txt_messages.tag_config('me', foreground="white", background=COLOR_MSG_ME, lmargin1=200, lmargin2=200, rmargin=10, justify='right')
        self.txt_messages.tag_config('other', foreground="white", background=COLOR_MSG_OTHER, lmargin1=10, lmargin2=10, rmargin=200, justify='left')
        self.txt_messages.tag_config('system', foreground="#ffcc00", justify='center')

        # אזור ההקלדה
        self.frame_input = tk.Frame(self.frame_chat, bg=COLOR_BG)
        self.frame_input.pack(fill=tk.X, padx=20, pady=20)

        self.entry_msg = tk.Entry(self.frame_input, bg="#40444b", fg="white", font=FONT_MAIN, bd=0, insertbackground="white")
        self.entry_msg.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8, padx=(0, 10))
        self.entry_msg.bind("<Return>", lambda e: self.send_message())

        btn_send = tk.Button(self.frame_input, text="SEND", bg=COLOR_BTN, fg="white", font=FONT_BOLD, bd=0, command=self.send_message)
        btn_send.pack(side=tk.RIGHT, ipadx=20, ipady=4)

    def show_login_dialog(self):
        """ חלונית קטנה שמבקשת שם משתמש בהתחלה """
        name = simpledialog.askstring("Login", "Enter your username:", parent=self.root)
        if name:
            self.connect_to_server(name)
        else:
            sys.exit() # יציאה אם לא הוכנס שם

    def connect_to_server(self, name):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((HOST, PORT))
            self.sock.send(name.encode('utf-8')) # שלב ההזדהות
            
            # המתנה לתשובה ראשונית מהשרת
            response = self.sock.recv(1024).decode('utf-8')
            
            if response.startswith("WELCOME"):
                self.username = name
                self.root.title(f"NetChat Pro - Logged in as: {name}")
                # התחלת התהליכון שמקשיב להודעות
                threading.Thread(target=self.listen_to_server, daemon=True).start()
            else:
                messagebox.showerror("Error", response)
                self.root.destroy()
        except Exception as e:
            messagebox.showerror("Connection Error", f"Could not connect to server.\n{e}")
            self.root.destroy()

    def listen_to_server(self):
        """ לולאת ההאזנה להודעות נכנסות מהשרת """
        while self.running:
            try:
                data = self.sock.recv(2048).decode('utf-8')
                if not data: break
                
                # טיפול בפרוטוקול
                parts = data.split(SEPARATOR)
                cmd = parts[0]

                if cmd == "USERS":
                    # עדכון רשימת המשתמשים
                    user_str = parts[1]
                    users = user_str.split(",") if user_str else []
                    self.update_user_list(users)
                
                elif cmd == "MSG":
                    # קבלת הודעה פרטית: MSG|SENDER|CONTENT
                    sender = parts[1]
                    content = parts[2]
                    self.add_message_to_history(sender, sender, content)
                    
                    # אם אני כרגע צופה בצ'אט עם השולח, עדכן את המסך
                    if self.selected_user == sender:
                        self.display_message(sender, content, 'other')
                    else:
                        # התראה ויזואלית (אפשר להוסיף צליל)
                        print(f"New message from {sender}")

                elif cmd == "SYSTEM":
                     messagebox.showinfo("System Message", parts[1])

            except Exception as e:
                print(f"Error in listener: {e}")
                break

    def send_message(self):
        msg = self.entry_msg.get().strip()
        if not msg or not self.selected_user: return
        
        # 1. שליחת ההודעה לשרת
        try:
            full_msg = f"{self.selected_user}{SEPARATOR}{msg}"
            self.sock.send(full_msg.encode('utf-8'))
            
            # 2. הצגה במסך שלי ושמירה בהיסטוריה
            self.display_message("Me", msg, 'me')
            self.add_message_to_history(self.selected_user, "Me", msg)
            self.entry_msg.delete(0, tk.END)
            
            # 3. בדיקת בוט (Alice/AutoBot)
            if self.selected_user.lower() == "bot":
                self.handle_bot_response(msg)
                
        except Exception as e:
            messagebox.showerror("Error", "Failed to send message")

    def handle_bot_response(self, user_msg):
        """ לוגיקה מקומית שמדמה בוט אם מדברים אליו """
        reply = AutoBot.get_response(user_msg)
        if reply:
            def delayed_reply():
                self.add_message_to_history("Bot", "Bot", reply)
                if self.selected_user == "Bot":
                    self.display_message("Bot", reply, 'other')
            self.root.after(1000, delayed_reply)

    def on_user_select(self, event):
        selection = self.user_list_box.curselection()
        if not selection: return
        
        target_user = self.user_list_box.get(selection[0])
        
        # אי אפשר לדבר עם עצמך
        if target_user == f"{self.username} (You)": return
        
        self.selected_user = target_user
        self.lbl_chat_header.config(text=f"Chat with {target_user}", fg="white")
        self.load_chat_history(target_user)

    def update_user_list(self, users):
        """ עדכון ה-Listbox בצד שמאל """
        self.user_list_box.delete(0, tk.END)
        
        # הוספת עצמי
        self.user_list_box.insert(tk.END, f"{self.username} (You)")
        self.user_list_box.itemconfig(tk.END, {'fg': '#00ff00'}) # ירוק לעצמי
        
        # הוספת הבוט באופן ידני שתמיד יהיה שם
        self.user_list_box.insert(tk.END, "Bot")
        self.user_list_box.itemconfig(tk.END, {'fg': '#ffff00'})

        # הוספת שאר המשתמשים
        for user in users:
            if user != self.username:
                self.user_list_box.insert(tk.END, user)

    def add_message_to_history(self, partner, sender, text):
        if partner not in self.chat_history:
            self.chat_history[partner] = []
        self.chat_history[partner].append({'sender': sender, 'text': text})

    def load_chat_history(self, partner):
        self.txt_messages.config(state='normal')
        self.txt_messages.delete(1.0, tk.END) # ניקוי מסך
        
        if partner in self.chat_history:
            for msg in self.chat_history[partner]:
                tag = 'me' if msg['sender'] == 'Me' else 'other'
                sender_name = msg['sender'] if tag == 'other' else ''
                final_text = f"{sender_name}\n{msg['text']}\n" if sender_name else f"{msg['text']}\n"
                self.txt_messages.insert(tk.END, final_text, tag)
                self.txt_messages.insert(tk.END, "\n") # רווח
        
        self.txt_messages.yview(tk.END) # גלילה למטה
        self.txt_messages.config(state='disabled')

    def display_message(self, sender, text, tag):
        self.txt_messages.config(state='normal')
        display_text = f"{text}\n" if tag == 'me' else f"{sender}\n{text}\n"
        self.txt_messages.insert(tk.END, display_text, tag)
        self.txt_messages.insert(tk.END, "\n")
        self.txt_messages.yview(tk.END)
        self.txt_messages.config(state='disabled')

    def spawn_new_client(self):
        subprocess.Popen([sys.executable, __file__])

    def on_close(self):
        self.running = False
        if self.sock: self.sock.close()
        self.root.destroy()
        sys.exit()

if __name__ == "__main__":
    ModernChatClient()