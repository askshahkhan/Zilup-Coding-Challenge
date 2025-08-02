import time
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class ZulipBot:
    """
    Automates interactions with the Zulip web interface using Selenium.
    Supports login, navigation, message sending, retrieval, and saving output.
    """
    def __init__(self, browser_manager, url, email, password):
        """
        Initializes the ZulipBot with browser manager and Zulip credentials.
        """
        self.driver = browser_manager.driver
        self.wait = browser_manager.wait
        self.url = url
        self.email = email
        self.password = password

    def login(self):
        """
        Logs in to Zulip using provided credentials.
        Waits for the compose textarea to confirm successful login.
        """
        start = time.time()
        print("🌐 Navigating to Zulip login page...")
        self.driver.get(self.url)

        email_input = self.wait.until(EC.presence_of_element_located((By.ID, "id_username")))
        email_input.send_keys(self.email)

        password_input = self.wait.until(EC.presence_of_element_located((By.ID, "id_password")))
        password_input.send_keys(self.password)

        login_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        login_button.click()

        self.wait.until(EC.presence_of_element_located((By.ID, "compose-textarea")))
        print(f"✅ Logged in! (took {time.time() - start:.2f}s)")

    def navigate_to_topic(self, stream_partial_href="#narrow/channel/512718-general", topic_name="test-topic"):
        """
        Navigates to the specified Zulip stream and topic.
        Clicks the compose reply button to prepare for sending a message.
        """
        start = time.time()
        print(f"➡️ Navigating to stream and topic '{topic_name}'...")

        stream_link = self.wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            f'a[href*="{stream_partial_href}"]'
        )))
        stream_link.click()
        time.sleep(1)

        topic_link = self.wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            f'li.topic-list-item[data-topic-name="{topic_name}"] > a.topic-box'
        )))
        topic_link.click()
        print(f"✅ Clicked on topic '{topic_name}'")

        compose_button = self.wait.until(EC.element_to_be_clickable((By.ID, "left_bar_compose_reply_button_big")))
        compose_button.click()
        print(f"✅ Compose reply button clicked (took {time.time() - start:.2f}s)")

    def send_message(self, message):
        """
        Sends a message to the currently selected Zulip topic.
        """
        start = time.time()
        print(f"💬 Typing message: {message}")
        textarea = self.wait.until(EC.presence_of_element_located((By.ID, "compose-textarea")))
        self.driver.execute_script("arguments[0].value = arguments[1];", textarea, message)

        send_button = self.wait.until(EC.element_to_be_clickable((By.ID, "compose-send-button")))
        send_button.click()

        self.wait.until(lambda d: d.find_elements(By.CSS_SELECTOR, ".message_row") and
                        d.find_elements(By.CSS_SELECTOR, ".message_row")[-1].find_element(By.CSS_SELECTOR, "a.message-time").text.strip() != "")
        print(f"✅ Message sent! (took {time.time() - start:.2f}s)")

    def get_last_messages(self, count=5):
        """
        Retrieves the last `count` messages from the current Zulip topic.
        Returns a list of dictionaries with message content and timestamp.
        """
        print(f"📥 Retrieving last {count} messages...")
        messages_data = []
        start = time.time()

        message_rows = self.driver.find_elements(By.CSS_SELECTOR, ".message_row")
        if not message_rows:
            print("⚠️ No messages found.")
            return messages_data

        last_msgs = message_rows[-count:]
        for idx, msg in enumerate(last_msgs, 1):
            try:
                content = msg.find_element(By.CSS_SELECTOR, ".message_content").text.strip()
                timestamp = msg.find_element(By.CSS_SELECTOR, "a.message-time").text.strip()
                # print(f"{idx}. [{timestamp}] {content}")
                messages_data.append({"content": content, "timestamp": timestamp})
            except Exception as e:
                print(f"{idx}. ⚠️ Failed to extract message: {e}")

        print(f"📦 Messages retrieved in {time.time() - start:.2f}s.")
        return messages_data

    def save_messages_to_json(self, output, filename="../output/output.json"):
        """
        Saves the provided output dictionary to a JSON file.
        """
        try:
            start = time.time()
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(output, f, ensure_ascii=False, indent=4)
            print(f"💾 Messages saved to {filename} (took {time.time() - start:.2f}s)")
        except Exception as e:
            print(f"❌ Failed to save messages to JSON: {e}")
