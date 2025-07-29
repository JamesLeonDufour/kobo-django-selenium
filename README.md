
# KoboToolbox User Activation/Deactivation Script

This Python script automates the activation or deactivation of user accounts in the KoboToolbox Django admin panel by simulating browser actions via Selenium.

---

## 🔧 Features

- Activate or deactivate users by ID via the admin panel
- Uses your active session cookie to authenticate (no login needed)
- Logs activity to both `.txt` and `.csv` files
- Supports headless mode for automation

---

## 📁 Requirements

- Python 3.8+
- Google Chrome (latest stable version)
- [ChromeDriver](https://sites.google.com/chromium.org/driver/) matching your Chrome version
- Python packages:
  ```bash
  pip install selenium pandas
  ```

---

## 📂 Files

- `deactivate_users.py`: The main script
- `users.csv`: A CSV with a `user_id` column
- `user_update_log.txt`: Log file with full details (timestamp, actions)
- `user_update_log_{server_name}_{timestamp}.csv`: One-line-per-user summary

---

## 📋 users.csv Format

```csv
user_id
5
25
8
```

---

## ⚙️ Configuration

In `script.py`, edit the `CONFIG` dictionary:

```python
CONFIG = {
    'base_url': 'https://KPI',               # Your KoboToolbox URL
    'cookie_name': 'kobonaut',               # Your session cookie name (typically kobonaut)
    'cookie_value': '<your_cookie_here>',    # Paste your browser cookie here
    'mode': 'deactivate',                    # activate or deactivate users
    'admin_user_path': '/admin/kobo_auth/user/',
    'headless': False,                       # Set to True for headless browser
    'wait_timeout': 10                       # Seconds to wait for elements
}
```

To get your session cookie:
1. Open the KoboToolbox admin panel in Chrome.
2. Press F12 to open Developer Tools → Application → Cookies.
3. Find the cookie named `kobonaut` and copy its value.

---

## ▶️ Running the Script

```bash
python deactivate_users.py
```

The script will:
- Load the cookie into a fresh Chrome session.
- Loop through all user IDs from `users.csv`.
- Activate or deactivate users depending on the `mode`.
- Log results to both `.txt` and `.csv`.

---

## ✅ Example Output

```txt
2025-07-28 23:09:42 - Browser loaded and cookie applied successfully.
2025-07-28 23:09:43 - Attempting to process user 5...
2025-07-28 23:09:44 - ✅ User 5 deactivated.
```

---

## 🧪 Notes

- The script assumes you have Django admin rights.
- If MFA or additional prompts block access, the cookie must reflect an active session.
- Errors are logged with reasons (timeout, element not found, etc.).

---

## 📄 License

MIT License – Use freely and adapt for your needs.
