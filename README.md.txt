# Server Monitor – Cross-Platform Metrics Collector (Linux + Windows)

A lightweight, agent-based server monitoring system designed to demonstrate skills in **server administration**, **automation**, **remote execution**, and **GitHub project structure**.

This project includes:
- A **central Flask-based Aggregator API**
- Cross-platform **Linux and Windows agents**
- Secure submission using **Basic Auth**
- Collects metrics such as CPU, memory, disk, uptime, and network usage
- Runs on any VM (AWS, On-Prem, Proxmox, VMware, etc.)
- Produces logs you can visualize, analyze, or ship to Grafana later

This is intentionally simple, readable, and practical — ideal for showcasing fundamentals in monitoring and automation.

---

## 📁 Project Structure

```
server-monitor/
│
├── aggregator/             # Central API server that receives metrics
│   ├── app.py              # Flask API endpoint (/metrics)
│   ├── config.py           # API credentials + settings
│   ├── basic_auth.py       # Auth helper
│   └── logs/               # Stored JSON metrics from agents
│
├── scrapers/               # Host-side collectors (agents)
│   ├── linux_agent.py      # Linux metrics collector (SSH, cron, systemd)
│   └── windows_agent.py    # Windows metrics collector (PowerShell, Task Scheduler)
│
├── README.md               # Documentation
├── .gitignore              # Ignore compiled files, secrets, OS clutter
└── requirements.txt        # Python dependencies
```

---

## 🚀 How It Works

### 1. The **Aggregator** runs on ANY server.
It exposes a single endpoint:

```
POST /metrics
```

Agents send JSON describing system health:

```json
{
  "hostname": "web01",
  "cpu_percent": 37,
  "memory_percent": 62,
  "disk_percent": 71,
  "uptime": "3 days, 4:12",
  "timestamp": "2025-01-11T15:23:02Z"
}
```

The aggregator:
- Validates Basic Auth
- Stores each entry as a JSON file in `/aggregator/logs/`
- Prints logs to console for demo purposes

---

### 2. The **Linux Agent** collects:
- CPU %
- Memory %
- Disk %
- Load average
- Uptime

It can run on:
- Ubuntu
- Debian
- RedHat / CentOS
- Amazon Linux

Schedule via cron or systemd.

---

### 3. The **Windows Agent** collects:
- CPU %
- Memory %
- Disk %
- Uptime
- Network throughput

Uses native PowerShell (`Get-Counter`, `Get-WmiObject`).

Schedule via Windows Task Scheduler.

---

## 🔐 Authentication

The Aggregator uses **Basic Auth** with credentials stored in:

```
aggregator/config.py
```

Example:

```python
USERNAME = "admin"
PASSWORD = "supersecret"
```

Agents must send the same credentials in their POST request.

---

## 📦 Installation

### 1. Clone the Repo

```bash
git clone https://github.com/<your-username>/server-monitor.git
cd server-monitor
```

---

## 🖥️ Aggregator Setup

### Install dependencies:

```bash
pip install -r requirements.txt
```

### Run the API:

```bash
cd aggregator
python app.py
```

Default port: `5000`

You will see:

```
Aggregator running on http://0.0.0.0:5000
```

---

## 🐧 Linux Agent Setup

Edit the top of `linux_agent.py` to point to your aggregator:

```python
AGGREGATOR_URL = "http://YOUR-SERVER-IP:5000/metrics"
USERNAME = "admin"
PASSWORD = "supersecret"
```

Run manually:

```bash
python3 linux_agent.py
```

To run every 5 minutes (cron):

```
*/5 * * * * /usr/bin/python3 /path/to/linux_agent.py
```

---

## 🪟 Windows Agent Setup

Edit the config section in:

```
scrapers/windows_agent.ps1
```

Run manually:

```powershell
powershell.exe -File windows_agent.ps1
```

Schedule with Task Scheduler to run every 5 minutes.

---

## 📊 Viewing the Data

The aggregator writes logs to:

```
aggregator/logs/
```

Each file contains metrics from one agent run:

```
web01_2025-01-10T20-12-33.json
```

You can optionally:
- ship logs into Grafana/Loki,
- parse with pandas,
- visualize in PowerBI,
- or display them via a simple HTML dashboard (future expansion).

---

## 🎯 Why This Project Matters

This demonstrates:

### ✔ Server Administration  
Linux + Windows metrics, system services, scheduled tasks.

### ✔ Automation  
Agent scripts run on a schedule and communicate automatically.

### ✔ Monitoring Fundamentals  
CPU, memory, disk, uptime, network.

### ✔ Networking + Security  
REST API, Basic Auth, JSON payloads.

### ✔ Python Development  
API (Flask), agents (Linux + PowerShell), structured repo.

### ✔ Git & GitHub  
Professional project layout, documentation, version control.

Ideal for sharing on LinkedIn or including in a portfolio.

---

## 📌 Future Enhancements (Optional)

- TLS (HTTPS) for secure transport  
- SQLite database instead of JSON files  
- Grafana dashboard  
- Auto-discovery of hosts  
- Alerting thresholds (email, Slack, Teams)

---

## 📣 Share Your Demo on LinkedIn

Ideas:

- Show a screenshot of logs appearing in real time  
- Show Task Scheduler + cron entries  
- Explain the architecture  
- Add a GIF of the aggregator receiving data  
- Link to the repo  

---

## 📝 License
MIT License.

