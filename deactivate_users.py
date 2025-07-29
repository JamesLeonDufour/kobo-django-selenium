import time
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException

# === CONFIGURATION ===
CONFIG = {
    'base_url': 'https://KPI', # 👈 Kobotoolbox URL
    'cookie_name': 'kobonaut', 
    'cookie_value': '',  # 👈 Paste your cookie value here
    'mode': 'deactivate',  # 'activate' or 'deactivate'
    'admin_user_path': '/admin/kobo_auth/user/',
    'headless': False,
    'wait_timeout': 10
}

CSV_FILE = "users.csv"       # Must contain a 'user_id' column
TXT_LOG_FILE = "user_update_log.txt"
CSV_LOG_FILE = f"user_update_log_{CONFIG['base_url'].replace('https://', '').replace('.', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

# === INIT CSV LOG ===
csv_log = []

# === LOGGING ===
def log_action(user_id, action, status, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{timestamp} - {message}"
    print(line)
    with open(TXT_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")
    csv_log.append({
        "timestamp": timestamp,
        "user_id": user_id,
        "action": action,
        "status": status,
        "message": message
    })

# === BROWSER SETUP ===
def load_browser_with_manual_cookie(config):
    options = Options()
    if config.get("headless", False):
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(f"{config['base_url']}/admin/")
        log_action("", "", "info", f"Visited {config['base_url']}/admin/ to set cookie.")
        driver.add_cookie({
            'name': config['cookie_name'],
            'value': config['cookie_value'],
            'domain': config['base_url'].replace('https://', '').split('/')[0],
            'path': '/',
        })
        log_action("", "", "info", "Cookie added. Refreshing page.")
        driver.get(f"{config['base_url']}/admin/")
        WebDriverWait(driver, config['wait_timeout']).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        log_action("", "", "info", "Browser loaded and cookie applied successfully.")
    except Exception as e:
        log_action("", "", "error", f"❌ Error during browser setup: {e}")
        driver.quit()
        raise
    return driver

# === USER PROCESSING ===
def process_user_by_id(driver, config, user_id):
    url = f"{config['base_url']}{config['admin_user_path']}{user_id}/change/"
    wait = WebDriverWait(driver, config['wait_timeout'])
    try:
        log_action(user_id, config['mode'], "info", f"Attempting to process user at {url}")
        driver.get(url)

        checkbox = wait.until(EC.element_to_be_clickable((By.ID, "id_is_active")))
        is_checked = checkbox.is_selected()

        action_performed = None
        if config['mode'] == "deactivate":
            if is_checked:
                checkbox.click()
                action_performed = "deactivated"
            else:
                log_action(user_id, "deactivate", "skip", "User already inactive.")
        elif config['mode'] == "activate":
            if not is_checked:
                checkbox.click()
                action_performed = "activated"
            else:
                log_action(user_id, "activate", "skip", "User already active.")

        if action_performed:
            save_button = wait.until(EC.element_to_be_clickable((By.NAME, "_save")))
            save_button.click()
            log_action(user_id, config['mode'], "success", f"✅ User {user_id} {action_performed}.")

    except TimeoutException:
        log_action(user_id, config['mode'], "timeout", "❌ Timed out waiting for elements.")
    except NoSuchElementException:
        log_action(user_id, config['mode'], "not_found", "❌ User not found or page structure changed.")
    except ElementClickInterceptedException:
        log_action(user_id, config['mode'], "click_error", "❌ Element click intercepted.")
    except Exception as e:
        log_action(user_id, config['mode'], "error", f"❌ Unexpected error: {e}")

# === MAIN ===
def main():
    try:
        df = pd.read_csv(CSV_FILE)
        if "user_id" not in df.columns:
            log_action("", "", "error", "CSV must contain a 'user_id' column.")
            return

        driver = load_browser_with_manual_cookie(CONFIG)

        for user_id in df["user_id"]:
            process_user_by_id(driver, CONFIG, str(user_id).strip())

        driver.quit()

        # Write CSV log
        pd.DataFrame(csv_log).to_csv(CSV_LOG_FILE, index=False, encoding="utf-8")
        print(f"\n🎉 Done! Logs saved to: {TXT_LOG_FILE} and {CSV_LOG_FILE}")
        log_action("", "", "done", "Script finished successfully.")

    except FileNotFoundError:
        log_action("", "", "error", f"CSV file '{CSV_FILE}' not found.")
    except Exception as e:
        log_action("", "", "fatal", f"Unhandled error: {e}")
        if 'driver' in locals() and driver:
            driver.quit()

if __name__ == "__main__":
    main()
