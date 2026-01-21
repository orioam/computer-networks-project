# 📡 TCP Multithreaded Server
![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat&logo=python)
![Network](https://img.shields.io/badge/Protocol-TCP%2FIP-orange)
![Status](https://img.shields.io/badge/Status-Active-success)

## 👥 Members
Ori Amsalem, Ofek Drori

## 📘 Overview
The **Server** acts as the central hub of the chat system. It utilizes **multi-threading** to handle multiple client connections simultaneously, ensuring efficient message routing and real-time user management without blocking.

## ⚙️ Key Features
* **Multi-Client Support:** Handles multiple concurrent connections using Python `threading`.
* **Custom Protocol:** Uses a robust message parsing system (based on `|` separators) for command and data handling.
* **Live Logging:** Real-time console output for connection events, errors, and traffic monitoring.
* **Safety:** Implements error handling to prevent server crashes on client disconnects.

## 🛠️ Tech Stack
| Component | Technology |
|-----------|------------|
| **Core** | Python `socket` API |
| **Concurrency** | `threading` module |
| **Port** | `5555` (Default) |

## 🚀 How to Run
1.  Navigate to the server directory.
2.  Execute the script:
    ```bash
    python server.py
    ```
3.  The server will start listening on `0.0.0.0:5555`.