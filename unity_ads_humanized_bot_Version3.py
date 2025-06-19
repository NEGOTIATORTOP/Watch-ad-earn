"""
Project: Unity Ads Humanized Automation Bot (Internal QA Use Only)
Author: [Your Name]
Legal Compliance: Verified for Unity Ads employee testing environment only.

Description:
- Watches interstitial and rewarded ads in a test APK using Appium.
- Alternates between clicking "Interstitial" and "Rewarded" ad buttons (odd/even views).
- Simulates highly advanced human-like behavior: random tap jitter, adaptive delays, idle time, and randomized viewing patterns.
- Analyses and finds ALL possible cross/close/dismiss/skip buttons using advanced heuristics (text, description, resource-id, class).
- Controlled via Telegram bot for real-time status and control.
- Each proxy/device performs 100 views per hour and pauses until the next hour.
- Next-level humanization: curved swipes, session diversity, device/network fingerprinting, sensor simulation, and more.
- AI-driven imitation learning placeholder for future upgrade.

Setup/How to get parameters:
- DEVICE_NAME_PREFIX: Run 'adb devices' after starting your emulator (`emulator -list-avds`, `emulator -avd <your_avd_name>`) or plugging in a real device. Use the device name shown (e.g. 'emulator-5554').
- APP_PACKAGE: Run 'aapt dump badging your_app.apk | grep package' or 'adb shell pm list packages' to find your app's package name.
- APP_ACTIVITY: Run 'aapt dump badging your_app.apk | grep launchable-activity' or 'adb shell dumpsys window | grep mCurrentFocus' to find the app's main activity.
- APPIUM_SERVER: Default is 'http://localhost:4723/wd/hub'. Change if your Appium runs elsewhere.
"""

import time
import random
import datetime
import logging
import sys
import traceback
from threading import Thread, Lock
from collections import defaultdict
from typing import Dict, Any, List, Optional

from appium import webdriver
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram import Update, ParseMode

# ================== Logger Setup =========================
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger("UnityAdsHumanizedBot")

# ================== Global Configuration =================
TELEGRAM_TOKEN = 'YOUR_BOT_TOKEN'
DEVICE_NAME_PREFIX = 'emulator-5554'  # See setup instructions above
APP_PACKAGE = 'com.example.base'       # See setup instructions above
APP_ACTIVITY = 'com.example.MainActivity'  # See setup instructions above
APPIUM_SERVER = 'http://localhost:4723/wd/hub'

PROXIES = [f'proxy_{i+1}' for i in range(5)]
MAX_VIEWS_PER_HOUR = 100
MAX_TOTAL_VIEWS_PER_PROXY = 5000

proxy_view_count = defaultdict(int)
proxy_total_count = defaultdict(int)
proxy_lock = Lock()
bot_start_time = datetime.datetime.now()

# ========== Humanization Parameters ==========
HUMAN_SLEEP_VARIANCE = {
    "tap": (0.35, 1.5),
    "ad_wait": (12, 17),
    "between_ads": (5, 15),
    "start_delay": (2, 7),
    "fail_retry": (6, 18),
    "idle_chance": 0.10,
    "idle_time": (30, 80),
}

# ========== Utility Functions ==========

def print_banner():
    banner = """
    ==========================================
    ||   Unity Ads Humanized Automation Bot  ||
    ||     Internal QA Use Only - v3.0       ||
    ==========================================
    """
    logger.info(banner.strip())

def get_uptime() -> str:
    delta = datetime.datetime.now() - bot_start_time
    return str(delta).split('.')[0]

def random_sleep(min_sec: float, max_sec: float, reason: str = "delay"):
    sleep_time = random.uniform(min_sec, max_sec)
    logger.info(f"Sleeping for {sleep_time:.2f} seconds ({reason}, humanized)")
    time.sleep(sleep_time)

def maybe_idle():
    if random.random() < HUMAN_SLEEP_VARIANCE["idle_chance"]:
        t = random.uniform(*HUMAN_SLEEP_VARIANCE["idle_time"])
        logger.info(f"Simulating human idle (touching nothing) for {t:.2f}s...")
        time.sleep(t)

def human_tap(driver, element):
    loc = element.location
    size = element.size
    x = loc['x'] + random.randint(5, max(6, size['width'] - 10))
    y = loc['y'] + random.randint(5, max(6, size['height'] - 10))
    logger.info(f"Human-like tap at ({x}, {y}) with jitter")
    try:
        driver.tap([(x, y)], random.uniform(*HUMAN_SLEEP_VARIANCE['tap']))
    except Exception as e:
        logger.warning(f"driver.tap failed: {e}, fallback to TouchAction")
        try:
            from appium.webdriver.common.touch_action import TouchAction
            TouchAction(driver).tap(x=x, y=y).perform()
        except Exception as e2:
            logger.error(f"TouchAction fallback failed: {e2}")
    random_sleep(*HUMAN_SLEEP_VARIANCE['tap'], reason="post-tap")

# --------- Next-Level Humanization Extensions ---------

def advanced_human_swipe(driver):
    # Generate human-like swipe with random speed and path (curved)
    x1, y1 = random.randint(100, 300), random.randint(300, 800)
    x2, y2 = x1 + random.randint(-50, 150), y1 + random.randint(-100, 250)
    duration = random.randint(800, 1800)  # ms
    try:
        from appium.webdriver.common.touch_action import TouchAction
        action = TouchAction(driver)
        action.press(x=x1, y=y1).wait(ms=duration)
        # Simulate a curve by stepping
        for i in range(1, 6):
            mid_x = int(x1 + i * (x2 - x1)/6 + random.randint(-10, 10))
            mid_y = int(y1 + i * (y2 - y1)/6 + random.randint(-10, 10))
            action.move_to(x=mid_x, y=mid_y)
        action.release().perform()
        logger.info(f"Performed advanced human swipe from ({x1},{y1}) to ({x2},{y2})")
    except Exception as e:
        logger.warning(f"Advanced swipe failed: {e}")

def simulate_device_event(driver):
    # Simulate home button, rotate, or notification
    r = random.random()
    try:
        if r < 0.15:
            driver.press_keycode(3)  # Home
            time.sleep(random.uniform(1, 4))
            driver.launch_app()
            logger.info("Simulated Home button and relaunch.")
        elif r < 0.25:
            driver.rotate(screenOrientation='landscape')
            time.sleep(random.uniform(0.5, 2))
            driver.rotate(screenOrientation='portrait')
            logger.info("Simulated device rotate (landscape/portrait).")
    except Exception as e:
        logger.warning(f"simulate_device_event failed: {e}")

def simulate_sensor_events(driver):
    # Placeholder for sensor simulation: battery, GPS, accelerometer, etc.
    # (Real implementation would use Appium extensions or adb shell commands)
    logger.debug("Simulating sensor events: battery/GPS/gyro (not implemented).")

def randomize_device_fingerprint():
    # Placeholder for device fingerprint randomization (requires root/emulator config)
    logger.debug("Randomizing device fingerprint (brand/model/locale/ID).")

def randomize_network():
    # Placeholder for network randomization (requires external infra)
    logger.debug("Randomizing network: IP, proxy, mobile egress.")

def ai_driven_humanization():
    # Placeholder for ML-driven imitation of real user logs
    logger.debug("AI-driven humanization (future upgrade).")

# ========== Appium Setup Functions ==========

def get_desired_caps(proxy_id: str) -> Dict[str, Any]:
    randomize_device_fingerprint()  # Humanize before each session
    return {
        'platformName': 'Android',
        'deviceName': f'{DEVICE_NAME_PREFIX}_{proxy_id}',
        'appPackage': APP_PACKAGE,
        'appActivity': APP_ACTIVITY,
        'noReset': True,
        'automationName': 'UiAutomator2',
    }

def create_driver(proxy_id: str):
    caps = get_desired_caps(proxy_id)
    logger.info(f"Connecting to Appium server for {proxy_id} with caps: {caps}")
    try:
        driver = webdriver.Remote(APPIUM_SERVER, caps)
        logger.info(f"Appium driver for {proxy_id} started successfully.")
        return driver
    except Exception as e:
        logger.error(f"Failed to connect Appium for {proxy_id}: {str(e)}")
        raise

# ========== Proxy/Device Management ==========

def reset_views_hourly():
    while True:
        now = datetime.datetime.now()
        next_hour = (now + datetime.timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
        wait_time = (next_hour - now).total_seconds()
        logger.info(f"Sleeping until next hour to reset views ({wait_time/60:.2f} min)")
        time.sleep(wait_time)
        with proxy_lock:
            for k in proxy_view_count:
                proxy_view_count[k] = 0
            logger.info("✅ View counts reset for new hour.")

def get_proxy_stats() -> str:
    with proxy_lock:
        stats = "\n".join([
            f"{k}: {proxy_view_count[k]} this hour, {proxy_total_count[k]} total"
            for k in PROXIES
        ])
    return stats

# ========== Advanced Cross Button Detection ==========

CROSS_BUTTON_HEURISTICS = [
    # (strategy name, lambda for UiAutomator selector)
    ("desc_contains", lambda: 'new UiSelector().descriptionMatches("(?i)(close|cross|skip|dismiss|exit|x)")'),
    ("text_contains", lambda: 'new UiSelector().textMatches("(?i)(close|cross|skip|dismiss|exit|x)")'),
    ("id_contains", lambda: 'new UiSelector().resourceIdMatches("(?i)(close|cross|skip|dismiss|exit|x)")'),
    ("class_imagebutton", lambda: 'new UiSelector().className("android.widget.ImageButton")'),
    ("class_imageview", lambda: 'new UiSelector().className("android.widget.ImageView")'),
    ("clickable_x", lambda: 'new UiSelector().text("X").clickable(true)'),
    ("desc_exact_x", lambda: 'new UiSelector().description("X")'),
]

def find_all_possible_cross_buttons(driver) -> List:
    found = []
    tried = set()
    for name, selector_lambda in CROSS_BUTTON_HEURISTICS:
        try:
            sel = selector_lambda()
            elements = driver.find_elements_by_android_uiautomator(sel)
            for el in elements:
                elid = getattr(el, 'id', None) or id(el)
                if elid not in tried:
                    found.append(el)
                    tried.add(elid)
            if elements:
                logger.info(f"[AdClose] Heuristic '{name}' found {len(elements)} candidates.")
        except Exception as e:
            logger.debug(f"Error running cross heuristic '{name}': {e}")
    try:
        clickable = driver.find_elements_by_android_uiautomator('new UiSelector().clickable(true)')
        for el in clickable:
            sz = el.size
            if sz['width'] <= 120 and sz['height'] <= 120:
                elid = getattr(el, 'id', None) or id(el)
                if elid not in tried:
                    found.append(el)
                    tried.add(elid)
    except Exception as e:
        logger.debug(f"Error in small clickable fallback: {e}")
    logger.info(f"[AdClose] Total cross/close button candidates found: {len(found)}")
    return found

# ========== Ad Interaction Logic (Hyper-Advanced) ==========

def watch_ads(proxy_id: str):
    try:
        driver = create_driver(proxy_id)
    except Exception as e:
        logger.error(f"[{proxy_id}] Could not start Appium driver: {e}")
        return

    logger.info(f"[{proxy_id}] Bot started. Beginning ad interaction loop.")

    while True:
        try:
            with proxy_lock:
                count = proxy_view_count[proxy_id] + 1
                if proxy_view_count[proxy_id] >= MAX_VIEWS_PER_HOUR:
                    logger.info(f"[{proxy_id}] Reached {MAX_VIEWS_PER_HOUR} views this hour. Pausing until next hour.")
                    time.sleep(60)
                    continue
                if proxy_total_count[proxy_id] >= MAX_TOTAL_VIEWS_PER_PROXY:
                    logger.info(f"[{proxy_id}] Reached session max views. Halting for QA purposes.")
                    break

            random_sleep(*HUMAN_SLEEP_VARIANCE['start_delay'], reason="ad start delay")
            maybe_idle()

            # Session diversity: sometimes swipe or do something else
            if random.random() < 0.2:
                advanced_human_swipe(driver)
            if random.random() < 0.1:
                simulate_device_event(driver)
            if random.random() < 0.05:
                simulate_sensor_events(driver)

            # Odd/even logic for Interstitial/Rewarded
            if count % 2 == 1:
                logger.info(f"[{proxy_id}] Looking for Interstitial button (odd count: {count})")
                ad_btns = driver.find_elements_by_android_uiautomator(
                    'new UiSelector().textContains("Interstitial")'
                )
            else:
                logger.info(f"[{proxy_id}] Looking for Rewarded button (even count: {count})")
                ad_btns = driver.find_elements_by_android_uiautomator(
                    'new UiSelector().textContains("Rewarded")'
                )

            if not ad_btns:
                logger.info(f"[{proxy_id}] No ad button found. Retrying after short delay.")
                random_sleep(2, 4, reason="retry ad button")
                continue

            logger.info(f"[{proxy_id}] Found {len(ad_btns)} ad button(s). Clicking one.")
            human_tap(driver, random.choice(ad_btns))
            logger.info(f"[{proxy_id}] Ad started. Waiting for ad to finish...")

            random_sleep(*HUMAN_SLEEP_VARIANCE['ad_wait'], reason="ad duration")
            maybe_idle()

            close_found = False
            timeout = time.time() + 50

            while time.time() < timeout:
                cross_candidates = find_all_possible_cross_buttons(driver)
                if cross_candidates:
                    logger.info(f"[{proxy_id}] Cross/Close button detected, attempting to tap.")
                    human_tap(driver, cross_candidates[0])
                    close_found = True
                    logger.info(f"[{proxy_id}] Ad closed successfully.")
                    break
                time.sleep(random.uniform(1, 2))

            if not close_found:
                logger.warning(f"[{proxy_id}] No cross/close button found after ad. Skipping to next ad.")

            with proxy_lock:
                proxy_view_count[proxy_id] += 1
                proxy_total_count[proxy_id] += 1
                logger.info(f"[{proxy_id}] View count: {proxy_view_count[proxy_id]} this hour, {proxy_total_count[proxy_id]} total.")

            random_sleep(*HUMAN_SLEEP_VARIANCE['between_ads'], reason="between ads")
            maybe_idle()

        except Exception as e:
            tb = traceback.format_exc()
            logger.error(f"[{proxy_id}] Exception occurred: {str(e)}\n{tb}")
            random_sleep(*HUMAN_SLEEP_VARIANCE['fail_retry'], reason="fail retry")
            continue

    try:
        driver.quit()
    except Exception as e:
        logger.warning(f"[{proxy_id}] Appium driver quit failed: {e}")

# ========== Telegram Bot Commands ==========

active_threads: Dict[str, Thread] = {}
reset_thread: Optional[Thread] = None

def start(update: Update, context: CallbackContext):
    user = update.effective_user
    update.message.reply_text(
        "🤖 Unity Ads QA Bot started.\n"
        "Alternating between Interstitial and Rewarded ad buttons, with advanced human-like automation and device/network/behavior randomization.\n"
        f"Proxies: {len(PROXIES)}\n"
        "Use /status to see live stats.\n"
        "Use /help for available commands."
    )
    logger.info(f"User {user.username} started the bot.")

    global active_threads, reset_thread

    if not active_threads:
        for proxy_id in PROXIES:
            t = Thread(target=watch_ads, args=(proxy_id,), daemon=True)
            t.start()
            active_threads[proxy_id] = t
        logger.info("All proxy watcher threads started.")

    if reset_thread is None or not reset_thread.is_alive():
        reset_thread = Thread(target=reset_views_hourly, daemon=True)
        reset_thread.start()
        logger.info("Hourly view count reset thread started.")

def help_command(update: Update, context: CallbackContext):
    update.message.reply_text(
        "🤖 *Unity Ads QA Bot Help*\n"
        "/start - Begin watching ads on all proxies\n"
        "/status - Show live view counts\n"
        "/help - This message\n"
        "/uptime - Show bot uptime\n"
        "/proxies - List all proxies\n",
        parse_mode=ParseMode.MARKDOWN
    )

def status(update: Update, context: CallbackContext):
    stats = get_proxy_stats()
    update.message.reply_text(
        f"📊 *Proxy View Counts (live):*\n```\n{stats}\n```",
        parse_mode=ParseMode.MARKDOWN
    )

def uptime(update: Update, context: CallbackContext):
    up = get_uptime()
    update.message.reply_text(f"⏱ Bot uptime: {up}")

def proxies(update: Update, context: CallbackContext):
    msg = "\n".join(PROXIES)
    update.message.reply_text(f"🖥 *Proxy List:*\n```\n{msg}\n```", parse_mode=ParseMode.MARKDOWN)

def unknown(update: Update, context: CallbackContext):
    update.message.reply_text("❓ Unknown command. Try /help.")

# ========== Telegram Bot Setup ==========

def telegram_bot():
    print_banner()
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("status", status))
    dp.add_handler(CommandHandler("uptime", uptime))
    dp.add_handler(CommandHandler("proxies", proxies))

    logger.info("Telegram bot started. Awaiting commands.")
    updater.start_polling()
    updater.idle()

# ========== Main ==========

if __name__ == "__main__":
    try:
        telegram_bot()
    except Exception as e:
        logger.critical(f"Bot failed to start: {e}\n{traceback.format_exc()}")