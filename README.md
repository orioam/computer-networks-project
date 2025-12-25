# 📡 TCP/IP Traffic Analysis & Network Project
![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat&logo=python)
![Wireshark](https://img.shields.io/badge/Tool-Wireshark-red?style=flat&logo=wireshark)
![Status](https://img.shields.io/badge/Status-Phase%201-success)

# Members:
Ori Amsalem, Ofek Drori

## 📘 Project Overview
This project focuses on a practical and in-depth analysis of the **TCP/IP** protocol suite, bridging the gap between theoretical concepts learned in the "Computer Networks" course and real-world application.

The project simulates end-to-end network traffic, starting from data generation at the **Application Layer**, through the encapsulation processes across various layers, to the transmission and analysis of packets in a real network environment.

## 🎯 Project Goals
* **Layer Model Understanding:** Visual and programmatic demonstration of data flow within the TCP/IP model.
* **Traffic Simulation:** Creating traffic scenarios that simulate common network services (HTTP, DNS).
* **Network Analysis:** Using **Wireshark** to decode protocols, troubleshoot issues, and measure performance metrics (Latency, RTT).
* **Network App Development:** Implementing Client-Server architecture using Python Sockets (Phase 2).

---

## 🧰 Tech Stack & Tools
| Category | Tools Used |
|----------|------------|
| **Language** | Python 3.x |
| **Libraries** | Pandas, Socket API |
| **Analysis** | Wireshark, Jupyter Notebook |
| **Protocols** | HTTP, TCP, UDP, IP, Ethernet |

---

## 📂 Project Structure
```text
├── part1_packet_analysis/   # Input CSV files, PCAP captures and Jupyter Notebooks for data 
├── part2_/                  # Python socket server with multiple clients     
└── README.md                # Project documentation