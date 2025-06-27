# 🚀 MANUAL BOT LAUNCH GUIDE

## STEP-BY-STEP LAUNCH INSTRUCTIONS

### 📋 Prerequisites Check

✅ Python 3.8+ installed
✅ All dependencies installed
✅ Windows Command Prompt or PowerShell

---

## 🎯 LAUNCH SEQUENCE

### Step 1: Open Two Command Prompts

- **Terminal 1**: For Backend API Server
- **Terminal 2**: For Dashboard Interface

### Step 2: Start Backend Server (Terminal 1)

```cmd
cd "c:\Users\Hari\Desktop\Crypto bot\backend"
python -m uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

**Expected Output:**

```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8001
```

### Step 3: Start Dashboard (Terminal 2)

```cmd
cd "c:\Users\Hari\Desktop\Crypto bot\dashboard"
python app.py
```

**Expected Output:**

```
Dash is running on http://127.0.0.1:8050/
```

### Step 4: Verify Services

Open browser to:

- **Backend API**: http://localhost:8001/health
- **Dashboard**: http://localhost:8050
- **API Docs**: http://localhost:8001/docs

---

## 🔧 ALTERNATIVE LAUNCH METHODS

### Option A: Use Batch Files

```cmd
cd "c:\Users\Hari\Desktop\Crypto bot"
start_backend.bat
start_dashboard.bat
```

### Option B: Use PowerShell Script

```powershell
cd "c:\Users\Hari\Desktop\Crypto bot"
.\start_system.ps1
```

### Option C: Use Python Launcher

```cmd
cd "c:\Users\Hari\Desktop\Crypto bot"
python launch_bot.py
```

---

## 🌐 ACCESS URLs

Once launched, access your professional trading platform at:

| Service                  | URL                          | Description          |
| ------------------------ | ---------------------------- | -------------------- |
| 📊 **Main Dashboard**    | http://localhost:8050        | Trading interface    |
| 🔌 **Backend API**       | http://localhost:8001        | API server           |
| 📚 **API Documentation** | http://localhost:8001/docs   | Interactive API docs |
| 🔍 **Health Check**      | http://localhost:8001/health | System status        |

---

## 🎯 FEATURES AVAILABLE

### 🤖 AI/ML Trading

- ✅ Transfer Learning System
- ✅ Hybrid Learning Models
- ✅ Online Learning Adaptation
- ✅ ML Compatibility Management

### 📈 Advanced Trading

- ✅ Auto Trading Controls
- ✅ Futures Trading
- ✅ Risk Management
- ✅ Real-time Analytics

### 🛡️ Professional Features

- ✅ Comprehensive P&L Analytics
- ✅ Model Version Management
- ✅ Email Notifications
- ✅ System Health Monitoring

---

## 🚨 TROUBLESHOOTING

### Backend Won't Start

```cmd
# Check if port is busy
netstat -an | findstr ":8001"

# Kill existing Python processes
taskkill /f /im python.exe

# Restart backend
cd "c:\Users\Hari\Desktop\Crypto bot\backend"
python main.py
```

### Dashboard Issues

```cmd
# Check dashboard dependencies
pip install dash plotly dash-bootstrap-components

# Restart dashboard
cd "c:\Users\Hari\Desktop\Crypto bot\dashboard"
python app.py
```

### Port Conflicts

```cmd
# Backend alternative ports
python -m uvicorn main:app --port 8002

# Dashboard alternative ports
python app.py --port 8051
```

---

## ✅ SUCCESS INDICATORS

### Backend Ready

```
✅ "Application startup complete"
✅ "Uvicorn running on http://0.0.0.0:8001"
✅ Health check returns {"status": "healthy"}
```

### Dashboard Ready

```
✅ "Dash is running on http://127.0.0.1:8050/"
✅ Browser opens to trading interface
✅ All components load without errors
```

---

## 🎉 LAUNCH COMPLETE!

Your **Professional Crypto Trading Bot** is now running with:

- 🔥 **100% Backend Integration**
- 🚀 **Advanced AI/ML Features**
- 💎 **Professional-Grade Interface**
- 🛡️ **Enterprise-Level Security**

**Happy Trading!** 🚀💰

---

_For support: Check the comprehensive documentation and status reports in your bot directory_
