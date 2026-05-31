#tweet_fetcher.py
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

DISASTER_KEYWORDS = [
    "earthquake", "flood", "cyclone", "storm", "landslide",
    "fire", "explosion", "accident", "collapse", "disaster",
    "tsunami", "rescue", "emergency", "evacuation",
    "injured", "dead", "missing", "rain", "heavy rain", "covid"
]


def is_disaster_post(text):
    text_lower = text.lower()
    return any(word in text_lower for word in DISASTER_KEYWORDS)


def remove_dates(text):
    text = re.sub(r"\(\d{1,2}[./-]\d{1,2}[./-]\d{2,4}\)", "", text)
    text = re.sub(r"\b\d{1,2}[./-]\d{1,2}[./-]\d{2,4}\b", "", text)
    text = re.sub(r"\b\d{4}-\d{2}-\d{2}\b", "", text)
    return text.strip()


def get_latest_post(username):
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    wait = WebDriverWait(driver, 15)

    try:
        url = f"https://x.com/{username}"
        driver.get(url)

        wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//article[@data-testid="tweet"]')
            )
        )

        driver.execute_script("window.scrollBy(0,600);")
        time.sleep(3)

        posts = driver.find_elements(By.XPATH, '//article[@data-testid="tweet"]')

        for post in posts:
            is_pinned = False
            social_context = post.find_elements(By.XPATH, './/div[@data-testid="socialContext"]')

            for context in social_context:
                if "Pinned" in context.text:
                    is_pinned = True
                    break

            if is_pinned:
                continue

            try:
                raw_text = post.find_element(By.XPATH, './/div[@data-testid="tweetText"]').text
                text = remove_dates(raw_text)

                if text and is_disaster_post(text):
                    return text

            except Exception:
                continue

        return None

    except Exception as e:
        print("Error while fetching tweet:", e)
        return None

    finally:
        driver.quit()