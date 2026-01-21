# 📡 Part 1: Traffic Analysis & Encapsulation

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat&logo=python)
![Wireshark](https://img.shields.io/badge/Tool-Wireshark-blueviolet?style=flat&logo=wireshark)
![Jupyter](https://img.shields.io/badge/Environment-Jupyter-orange?style=flat&logo=jupyter)
![Pandas](https://img.shields.io/badge/Library-Pandas-150458?style=flat&logo=pandas)

## 📋 Table of Contents

1. [Project Overview](#1-project-overview)
2. [Workflow & Methodology](#2-workflow--methodology)
3. [Data Structure (CSV)](#3-data-structure-csv)
4. [Packet Analysis (Wireshark)](#4-packet-analysis-wireshark)
5. [Execution Guide](#5-execution-guide)

---

## 1. Project Overview

**Phase 1** of the project focuses on the fundamental concepts of the TCP/IP model: **Encapsulation** and **Protocol Analysis**.
The objective was to simulate the generation of application-layer data, process it programmatically, and then analyze real network traffic to observe how data is packaged and transmitted across the network.

**Key Learning Outcomes:**
* **Encapsulation Logic:** Understanding how data is wrapped with headers (TCP/UDP, IP, Ethernet) as it moves down the stack.
* **Traffic Capture:** Gaining proficiency with **Wireshark** for sniffing and dissecting packets.
* **Data Correlation:** Mapping logical data entries (CSV) to actual captured packets (`.pcap`).

---

## 2. Workflow & Methodology

The project was executed in three main stages:

### 🔹 Stage 1: Data Generation
We created a structured dataset (`CSV`) representing "pure" Application Layer messages (e.g., HTTP GET requests, DNS queries). This serves as the simulated input for the network stack.

### 🔹 Stage 2: Simulation (Jupyter Notebook)
Using **Python (Pandas)**, we processed the raw CSV data. The script simulates the operating system's role by parsing these messages and preparing them for transmission logic.

### 🔹 Stage 3: Live Capture & Analysis
We generated real network traffic matching our dataset and captured it using **Wireshark**. We then dissected the packets to verify header fields, flags, and payload integrity.

---

## 3. Data Structure (CSV)

The input file contains application-layer messages designed to simulate various network protocols.

**File Format:** `groupXX_protocol_input.csv`

| Field | Description | Example |
| :--- | :--- | :--- |
| `msg_id` | Unique identifier for the message | `1` |
| `app_protocol` | The Application Layer protocol | `HTTP` / `DNS` |
| `src_app` | Source entity | `client_browser` |
| `dst_app` | Destination entity | `web_server` |
| `message` | The raw payload/content | `GET /index.html` |
| `timestamp` | Simulation time offset | `0.015` |

---

## 4. Packet Analysis (Wireshark)

We performed a deep dive into the captured traffic (`.pcap` file) to decode the encapsulation layers.

### 🔍 TCP/IP Layer Breakdown

| Layer | Protocol | Key Fields Analyzed |
| :--- | :--- | :--- |
| **Layer 4** | **TCP** | `Source Port`, `Dest Port`, `Sequence Number`, `Flags (SYN, ACK, PSH)` |
| **Layer 3** | **IP** | `Source IP`, `Dest IP`, `TTL`, `Protocol ID` |
| **Layer 2** | **Ethernet** | `MAC Address`, `EtherType` |

### 🛠 Wireshark Filters Used

To isolate relevant traffic, the following filters were applied:

* **HTTP Traffic:** `http && tcp.port == 80`
* **DNS Queries:** `dns && udp.port == 53`
* **Specific Conversation:** `ip.addr == [TARGET_IP]`

---

## 5. Execution Guide

### Prerequisites
* **Python 3.x** with `pandas` installed.
* **Jupyter Notebook** environment.
* **Wireshark** installed on the host machine.

### How to Run

**1. Generate/Load Data:**
Ensure the input CSV file is placed in the project directory.

**2. Run the Notebook:**
Open the `.ipynb` file in Jupyter and execute the cells sequentially to process the data and visualize the encapsulation logic.

**3. Capture Traffic:**
1.  Open Wireshark.
2.  Select the active network interface (e.g., Wi-Fi or Ethernet).
3.  Start capture.
4.  Generate traffic (e.g., open a browser for HTTP).
5.  Stop capture and save as `.pcap`.

---