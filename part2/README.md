# 📡 Computer Networks Project - Part 2: Multithreaded TCP Chat System

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat&logo=python)
![Architecture](https://img.shields.io/badge/Architecture-Client%2FServer-orange)
![Protocol](https://img.shields.io/badge/Protocol-TCP-green)

## 📋 Table of Contents

1. [Project Overview](#1-project-overview)
2. [System Architecture](#2-system-architecture)
3. [Custom Application Protocol](#3-custom-application-protocol)
4. [Implementation Details](#4-implementation-details)
5. [Installation & Usage Guide](#5-installation--usage-guide)
6. [Traffic Analysis (Wireshark)](#6-traffic-analysis-wireshark)

---

## 1. Project Overview

This project implements a fully functional, real-time chat application based on the **TCP/IP** protocol suite.
The goal was to design a distributed system where multiple clients can communicate simultaneously through a central server, simulating real-world network applications.

**Key Features:**

* **Real-Time Communication:** Instant message delivery between users.
* **Concurrency:** Handling multiple clients at once using Multi-threading.
* **GUI:** A user-friendly graphical interface for the client.
* **Robustness:** Handling edge cases like sudden disconnections and duplicate usernames.

---

## 2. System Architecture

The system follows the classic **Client-Server** model:

### 🖥️ The Server (`server.py`)

The server acts as the "switchboard" of the application.

* **Role:** Listens for incoming TCP connections on a specific port.
* **Multithreading:** For every new client that connects, the server spawns a dedicated **Thread**. This allows the main server loop to remain non-blocking and accept new connections continuously.
* **State Management:** Maintains a global, thread-safe dictionary (`clients`) that maps `username` → `socket_object`.

### 👤 The Client (`client.py`)

The client is the end-user application.

* **Role:** Connects to the server, sends user input, and displays incoming messages.
* **Dual-Threaded Design:**
  1. **Main Thread (UI):** Manages the Tkinter GUI loop (rendering windows, buttons, and typing).
  2. **Listener Thread (Network):** Runs in the background (`daemon=True`) and continuously listens for incoming packets. This prevents the interface from freezing while waiting for server responses.

---

## 3. Custom Application Protocol

To enable structured communication over the raw TCP stream, we designed a custom Application Layer protocol.
The protocol uses a text-based format with a delimiter (`|`) to separate the command from the payload.

**Format:** `COMMAND | PARAM1 | PARAM2`

### Protocol Commands

| Direction | Command | Structure | Description |
| :--- | :--- | :--- | :--- |
| **Client → Server** | `Handshake` | `Username` | Sent immediately after connection to register the user. |
| **Server → Client** | `WELCOME` | `WELCOME\|Message` | Confirms successful login. |
| **Server → Client** | `ERROR` | `ERROR\|Reason` | Rejects login (e.g., username taken, server full). |
| **Server → Client** | `USERS` | `USERS\|User1,User2...` | Broadcasts the updated list of online users to all clients. |
| **Client → Server** | `MSG` | `TargetUser\|Content` | Sends a private message to a specific user. |
| **Server → Client** | `MSG` | `MSG\|Sender\|Content` | Delivers the message to the destination client. |

---

## 4. Implementation Details

### Step 1: Server Initialization

The server initiates a TCP socket (`SOCK_STREAM`) and binds it to `0.0.0.0` (all interfaces) on port `5555`. It then enters a listening state, waiting for incoming packets.

### Step 2: Handling Connections

When a client connects:
1. The server accepts the connection and receives a `socket` object.
2. It waits for the first packet (Handshake) containing the `username`.
3. **Validation:** Checks if the username is unique and if the server has space.
4. **Registration:** Adds the user to the `clients` dictionary.
5. **Broadcast:** Sends a `USERS` command to *all* connected clients to update their contact lists.

### Step 3: Message Routing

When Client A sends a message to Client B:
1. Server parses the packet: `Bob|Hello there`.
2. It looks up "Bob" in the `clients` dictionary.
3. It constructs a new packet: `MSG|Alice|Hello there`.
4. It sends the packet specifically to Bob's socket.

### Step 4: Disconnection Handling

If a client closes the app or crashes:
1. The server detects a connection reset or empty byte stream.
2. It removes the user from the `clients` dictionary.
3. It closes the socket to free resources.
4. It broadcasts a new `USERS` list to remaining clients.

---

## 5. Installation & Usage Guide

### Prerequisites

* Python 3.x installed.
* No external libraries required (uses standard `socket`, `threading`, `tkinter`).

### Running the System

**1. Start the Server:**

Open a terminal in the project folder and run:

```bash
python server.py

```

*Expected Output:* `[INIT] Server running on 0.0.0.0:5555`

**2. Start a Client:**

Open a **new** terminal and run:

```bash
python client.py

```
* Enter a username when prompted.
* The main chat window will appear.


**3. Simulate a Chat:**

* Open another terminal and run `client.py` again.
* Login with a **different** name.
* Select the other user from the list and start chatting.
