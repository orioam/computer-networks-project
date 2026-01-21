import socket
import threading
import sys
import time

# --- הגדרות שרת ---
HOST = '0.0.0.0'
PORT = 5555
MAX_CLIENTS = 10
SEPARATOR = "|"  # מפריד הפרוטוקול שלנו

# משתנים גלובליים
clients = {}  # מילון: { username: client_socket }
server_running = True

def log(tag, message):
    timestamp = time.strftime("%H:%M:%S", time.localtime())
    print(f"[{timestamp}] [{tag}] {message}")

def broadcast_user_list():
    """ שולח לכל הלקוחות את רשימת המחוברים המעודכנת """
    users_list = ",".join(clients.keys())
    msg = f"USERS{SEPARATOR}{users_list}"
    for user_sock in clients.values():
        try:
            user_sock.send(msg.encode('utf-8'))
        except:
            pass

def handle_client(conn, addr):
    """ טיפול בלקוח בודד ב-Thread נפרד """
    username = ""
    try:
        # 1. שלב ההתחברות וקבלת השם
        username = conn.recv(1024).decode('utf-8').strip()
        
        # בדיקות תקינות
        if username in clients:
            conn.send(f"ERROR{SEPARATOR}Username already taken.".encode('utf-8'))
            conn.close()
            return
        if len(clients) >= MAX_CLIENTS:
            conn.send(f"ERROR{SEPARATOR}Server is full.".encode('utf-8'))
            conn.close()
            return
            
        # הרשמה מוצלחת
        clients[username] = conn
        conn.send(f"WELCOME{SEPARATOR}Connected successfully!".encode('utf-8'))
        log("AUTH", f"User '{username}' connected from {addr}")
        
        # עדכון כל המשתמשים שמישהו חדש הצטרף
        broadcast_user_list()

        # 2. לולאת קבלת הודעות
        while server_running:
            data = conn.recv(2048).decode('utf-8')
            if not data:
                break
            
            # פירוק ההודעה לפי הפרוטוקול: TARGET|MESSAGE
            parts = data.split(SEPARATOR, 1)
            if len(parts) == 2:
                target_user, content = parts
                
                # שליחת הודעה פרטית
                if target_user in clients:
                    # הפורמט שנשלח למקבל: MSG|SENDER_NAME|CONTENT
                    msg_to_send = f"MSG{SEPARATOR}{username}{SEPARATOR}{content}"
                    clients[target_user].send(msg_to_send.encode('utf-8'))
                    log("CHAT", f"{username} -> {target_user}: {content}")
                else:
                    # החזרת שגיאה לשולח
                    err_msg = f"SYSTEM{SEPARATOR}User '{target_user}' is not online."
                    conn.send(err_msg.encode('utf-8'))

    except ConnectionResetError:
        log("WARN", f"Connection lost with {addr}")
    except Exception as e:
        log("ERROR", f"Exception with user '{username}': {e}")
    finally:
        # ניתוק מסודר
        if username in clients:
            del clients[username]
            broadcast_user_list() # עדכון רשימה לכולם
            log("DISCONNECT", f"User '{username}' removed.")
        conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(MAX_CLIENTS)
    
    log("INIT", f"Server running on {HOST}:{PORT}")
    log("INFO", "Waiting for connections...")

    while server_running:
        try:
            conn, addr = server.accept()
            # new thread to every new client
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.daemon = True # ייסגר אוטומטית כשהתוכנית הראשית תיסגר
            thread.start()
        except KeyboardInterrupt:
            break
            
    server.close()

if __name__ == "__main__":
    start_server()