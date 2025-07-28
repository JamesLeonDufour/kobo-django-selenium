# 🔒 KoboToolbox Batch User Activation/Deactivation via Admin Panel

This Python script automates the **activation or deactivation** of KoboToolbox users through the Django admin panel using **Selenium** and a manually supplied **session cookie** (e.g., `kobonaut`). This is especially useful when:
- You **cannot use the API or shell**,
- You’re managing a large number of users,
- MFA is enabled (manual login is required),
- You want to reuse your **logged-in browser session**.

---

## 🚀 Features

- ✅ Activate or deactivate users in bulk via Django Admin
- 🧠 Uses your own session cookie (bypass login)
- 🎭 Supports headless and visible browser modes
- 📝 Logs every action with timestamps and errors
- 🛡️ Graceful error handling with detailed messages

---

## 📦 Requirements

- Python 3.8+
- Google Chrome installed
- [ChromeDriver](https://sites.google.com/chromium.org/driver/) matching your Chrome version
- Python packages:

```bash
pip install selenium pandas
```

---

## 🛠️ Setup

### 1. Get your session cookie from Chrome
- Open DevTools (`F12`) → `Application` tab → `Cookies`
- Copy the value of the `kobonaut` (or `sessionid`) cookie for your domain  
  _(e.g., `https://KPI`)_

### 2. Prepare your CSV file
Save as `users.csv` with the following structure:

```csv
user_id
5
8
12
```

Each value should match the numeric ID from the Django Admin URL:  
`https://yourdomain/admin/kobo_auth/user/<user_id>/change/`

### 3. Edit the script config

In the script file:

```python
CONFIG = {
    'base_url': 'https://KPI',
    'cookie_name': 'kobonaut',  # or 'sessionid'
    'cookie_value': 'your-session-cookie-here',
    'mode': 'deactivate',       # or 'activate'
    'admin_user_path': '/admin/kobo_auth/user/',
    'headless': False,          # True to hide browser
    'wait_timeout': 10
}
```

---

## ▶️ Running the Script

Run the script from your terminal:

```bash
python deactivate_users.py
```

You’ll see the log in the terminal, and it will also be saved to `user_update_log.txt`.

---

## 📓 Example Output

```bash
2025-07-09 15:01:23 - ✅ User 5 deactivated successfully.
2025-07-09 15:01:27 - ✅ User 8 deactivated successfully.

🎉 Done! Log saved to: user_update_log.txt
```

---

## ❗ Notes

- The script navigates to:  
  `https://<your-domain>/admin/kobo_auth/user/<user_id>/change/`
- Make sure the user IDs exist or you'll see "Element not found" errors.
- If MFA is enabled, log in manually in Chrome, copy the cookie, and reuse it.
- Your session may expire after a while — replace the cookie if needed.

---

## 🔐 Disclaimer

This script manipulates Django Admin UI directly.  
Use with caution. It's intended for KoboToolbox superadmins.

---

## 📄 License

MIT License — free to use, modify, or share, but do so responsibly and at your own risk.
