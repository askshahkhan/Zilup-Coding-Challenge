import random
import streamlit as st
from config import ZULIP_URL, ZULIP_EMAIL, ZULIP_PASSWORD
from browser_manager import BrowserManager
from zulip_bot import ZulipBot
from summarize import summarize_messages
import time
import json
import os

st.set_page_config(page_title="Zulip Bot Status", layout="centered")
st.title("🤖 Zulip Bot Status")

status_lines = st.empty()

def update_status(lines):
    """
    Updates the Streamlit status window with the current list of status messages.
    Each message is separated by a blank line for readability.
    """
    status_lines.markdown("\n\n".join(lines))

def run_bot_workflow(headless):
    """
    Executes the Zulip bot workflow:
    - Logs in to Zulip
    - Navigates to the specified topic
    - Sends a random message
    - Retrieves and summarizes the last 5 messages
    - Saves results and timings to a JSON file
    - Updates the Streamlit UI with status and output
    The workflow can run in headless or visible Chrome mode.
    """
    status = []
    update_status(status)
    browser_manager = BrowserManager(headless=headless)
    bot = ZulipBot(browser_manager, ZULIP_URL, ZULIP_EMAIL, ZULIP_PASSWORD)

    timings = {}

    try:
        total_start = time.time()

        # Login
        t0 = time.time()
        status.append("🌐 Navigating to Zulip login page...")
        update_status(status)
        bot.login()
        timings["login"] = round(time.time() - t0, 2)
        status.append(f"✅ Logged in! (took {timings['login']}s)")
        update_status(status)

        # Navigate to topic
        t0 = time.time()
        status.append("➡️ Navigating to stream and topic 'test-topic'...")
        update_status(status)
        bot.navigate_to_topic()
        timings["navigate_to_topic"] = round(time.time() - t0, 2)
        status.append("✅ Clicked on topic 'test-topic'")
        status.append(f"✅ Compose reply button clicked (took {timings['navigate_to_topic']}s)")
        update_status(status)

        # Send message
        random_msgs = [
            "Hey there! Just testing the Zulip bot",
            "Automated message from Selenium script",
            "Random check-in: everything looks good!",
            "Selenium test: message delivery in progress"
        ]
        msg = random.choice(random_msgs)

        t0 = time.time()
        status.append(f"💬 Typing message: {msg}")
        update_status(status)
        bot.send_message(msg)
        timings["send_message"] = round(time.time() - t0, 2)
        status.append(f"✅ Message sent! (took {timings['send_message']}s)")
        update_status(status)

        # Get last messages
        t0 = time.time()
        status.append("📥 Retrieving last 5 messages...")
        update_status(status)
        last_msgs = bot.get_last_messages()
        timings["get_last_messages"] = round(time.time() - t0, 2)
        for idx, msg_obj in enumerate(last_msgs, 1):
            status.append(f"{idx}. [{msg_obj['timestamp']}] {msg_obj['content']}")
        status.append(f"📦 Messages retrieved in {timings['get_last_messages']}s.")
        update_status(status)

        # Summarize messages only if OpenAI API key is set
        t0 = time.time()
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if openai_api_key:
            summary_result = summarize_messages(last_msgs)
            timings["summarize_messages"] = round(time.time() - t0, 2)
            output = {
                "messages": last_msgs,
                "summary": summary_result["summary"],
                "openai_usage": summary_result["openai_usage"],
                "timings": timings
            }
        else:
            output = {
                "messages": last_msgs,
                "timings": timings
            }
            status.append("⚠️ No OpenAI API key found. Skipping summarization.")
            update_status(status)

        # Save messages
        t0 = time.time()
        bot.save_messages_to_json(output)
        timings["save_messages_to_json"] = round(time.time() - t0, 2)
        status.append(f"💾 Messages saved to ../output/output.json (took {timings['save_messages_to_json']}s)")
        total_time = round(time.time() - total_start, 2)
        status.append(f"✅ Total execution time: {total_time}s")
        update_status(status)

        st.subheader("JSON Output")
        st.code(json.dumps(output, indent=4), language="json")

        st.success("Done! You may close this window.")
    except Exception as e:
        status.append(f"❌ Fatal error in execution: {e}")
        update_status(status)
        st.error("Fatal error occurred.")
    finally:
        browser_manager.quit()

# --- Streamlit UI for workflow selection ---
st.write("Would you like to see the Chrome window while the bot runs?")
chrome_mode = st.radio(
    "Choose display mode:",
    ("Show Chrome Window (see actions live)", "Run Headless (no Chrome window)")
)

if st.button("Run Zulip Bot Workflow 🚀"):
    if chrome_mode == "Show Chrome Window (see actions live)":
        run_bot_workflow(headless=False)
    else:
        run_bot_workflow(headless=True)