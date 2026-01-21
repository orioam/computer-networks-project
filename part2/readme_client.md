# 💬 Modern Chat GUI Client
![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat&logo=python)
![GUI](https://img.shields.io/badge/Library-Tkinter-green)
![UX](https://img.shields.io/badge/Design-Dark%20Mode-black)

## 📘 Overview
The **Client** is a graphical application designed for real-time communication. It connects to the TCP server and provides a modern, user-friendly interface for chatting with other connected users.

## 🌟 Key Features
* **Modern UI:** Dark-themed interface with a split-view design (Sidebar for users, Main area for chat).
* **Real-Time Updates:** The user list updates automatically when clients join or leave.
* **Stability:** Handles connection errors and server shutdowns gracefully.

## 🛠️ Tech Stack
| Component | Technology |
|-----------|------------|
| **Interface** | `tkinter` (Standard GUI lib) |
| **Network** | Python `socket` API |
| **Concurrency** | Background threads for listening |

## 🚀 How to Run
1.  Ensure the **Server** is running first.
2.  Open a new terminal and run:
    ```bash
    python gui_client.py
    ```
3.  Enter your username and start chatting!
    * *Tip:* You can run multiple instances to simulate a conversation.