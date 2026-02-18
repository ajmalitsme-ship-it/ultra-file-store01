<h2 align="center">
    ──「 ULTRA FILE STORE PRO 」──
</h2>

<p align="center">
  <img src="https://telegra.ph/file/your-logo.jpg">
</p>

<p align="center">
<a href="#"><img src="https://img.shields.io/badge/Bot-ultra%20Store-blue?style=for-the-badge&logo=telegram" /></a>
<a href="#"><img src="https://img.shields.io/badge/Written%20in-Python-orange?style=for-the-badge&logo=python" /></a>
<a href="#"><img src="https://img.shields.io/badge/License-GPL--3.0-green?style=for-the-badge" /></a>
</p>

---

# 🚀 ultra FILE STORE PRO BOT

A powerful **Telegram File Store Bot** with:

* multi Force-Subscribe system
* Auto delete protection
* Premium users system
* Custom buttons & messages
* URL shortener support
* Multi-admin control
* Secure protected content
* web stream file + web admin panel
Fully customizable and deployable on **VPS, Local, or Heroku**.

---

# ⚙️ DEPLOYMENT METHODS

## 🟣 Deploy on Heroku

Click below and fill variables:

**Deploy →**
https://dashboard.heroku.com/new

---

## 🖥 Deploy on VPS / Local

### 1️⃣ Clone Repo

```bash
git clone https://github.com/yourusername/ajmal-filestore
cd ajmal-filestore
```

### 2️⃣ Install Requirements

```bash
pip3 install -U -r requirements.txt
```

### 3️⃣ Edit Config

Open **config.py** and fill:

```python
API_ID=123456
API_HASH=xxxxx
BOT_TOKEN=xxxxx

OWNER_ID=123456789
MONGO_URI=mongodb://mongo:27017

DB_CHANNEL=-100xxxxxxxxxx

DOMAIN=https://yourdomain.com

ADMIN_USER=admin
ADMIN_PASS=strongpassword
```

### 4️⃣ Run Bot

```bash
python3 main.py
```

---

# ✨ FEATURES

## 🔐 Force Subscribe

Users must join required channel(s) before accessing files.

## 🗑 Auto Delete

Files auto-delete after timer to avoid copyright issues.

## 👑 Premium Users

Grant special access & benefits.

## 📢 Broadcast System

Send messages to all users instantly.

## 🎛 Multi Admin Control

Add/remove admins anytime.

## 🔗 URL Shortener

Earn money using ad-based short links.

## 🧾 Fully Editable Messages

Customize **start, about, fsub, reply** texts easily.

---

# 📜 COMMANDS

### 👤 User

* `/start` – Start bot
* `/profile` – View profile
* `/request` – Send request

### 🛠 Admin

* `/broadcast` – Message all users
* `/users` – User count
* `/ban` – Ban user
* `/unban` – Unban user
* `/addpremium` – Add premium
* `/delpremium` – Remove premium
* `/genlink` – Generate file link
* `/usage` – Link usage stats

---

# 🧩 REQUIRED VARIABLES

```python
FSUBS = [[-1001234567890, True, 10]]
MESSAGES = {
  "START": "Welcome {first} to Ajmal File Store Bot!",
  "ABOUT": "Managed by Ajmal",
}
```

---

# 🛟 SUPPORT

For help & updates:

* Telegram Support Group
* Telegram Update Channel

(Add your links here)

---

# 🤝 CREDITS

* Original Base Developers
* Modified & Managed by **Ajmal**

> GPL-3.0 License — You may modify & share, but must keep credits and open-source license.

---

# ⭐ FINAL NOTE

If you like this project:

**Give a star ⭐ and share with friends.**
