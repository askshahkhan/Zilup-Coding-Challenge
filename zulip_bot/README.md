# Zulip Bot Coding Challenge

This project automates sending and summarizing messages in a Zulip chat stream using Selenium and OpenAI, with a modern Streamlit UI for workflow control and output display.

## Features

- Automates login and posts message to topic in Zulip using Selenium (web-scraping tool).
- Retrieves and summarizes recent messages using OpenAI GPT-3.5 Turbo.
- Estimates and displays OpenAI API token usage and cost.
- Interactive Streamlit UI to run the workflow and view results.
- Option to run Chrome in headless mode or with live display.
- Error handling for alomst every task to increase robustness of code 

## Output

- The bot saves results to `output/output.json` including:
  - Last 5 messages (if there's less than 5, last few messages)
  - Summary of messages
  - OpenAI token usage and cost
  - Timings for each workflow step
- **If there is no OpenAI API key set, the summary and openai_usage fields will not be present in the output JSON, and the user will see a warning in the Streamlit UI.**


## Setup

1. **Clone the repository**  
   ```bash
   git clone <your-repo-url>
   cd Detect_Auto_Take_Coding_Challenge/zulip_bot
   ```

2. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**  
   - Copy `.env` and fill in your Zulip credentials and OpenAI API key:
     ```
     ZULIP_URL=<your-zulip-login-url>
     ZULIP_EMAIL=<your-zulip-email>
     ZULIP_PASSWORD=<your-zulip-password>
     OPENAI_API_KEY=<your-openai-api-key>
     ```

## Usage

1. **Run the Streamlit app**  
   ```bash
   streamlit run src/main.py
   ```

2. **Choose display mode**  
   - Select whether to see the Chrome window or run headless.

3. **Run the workflow**  
   - Click the "Run Zulip Bot Workflow 🚀" button.
   - Watch status updates and view the JSON output in the browser.

## Notes

- Requires Chrome and ChromeDriver installed.
- Make sure your OpenAI API key has sufficient quota.
- For troubleshooting, check Streamlit UI for error messages.

## Documentation

- [OpenAI API](https://platform.openai.com/docs/)
- [os (Python stdlib)](https://docs.python.org/3/library/os.html)
- [time (Python stdlib)](https://docs.python.org/3/library/time.html)
- [json (Python stdlib)](https://docs.python.org/3/library/json.html)
- [random (Python stdlib)](https://docs.python.org/3/library/random.html)
- [Selenium for Python](https://selenium-python.readthedocs.io/)
- [expected_conditions](https://www.selenium.dev/selenium/docs/api/py/webdriver_support/selenium.webdriver.support.expected_conditions.html)
- [webdriver.common.by](https://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.common.by)
- [Streamlit](https://docs.streamlit.io/)
- [python-dotenv (PyPI)](https://pypi.org/project/python-dotenv/)

## Future Automations

- Add sender name next to each message for better traceability
- Structure messages into a tree in memory: channels → topics → messages
    - Implement **topic search** using DFS (Depth First Search) that works even without specifying channel name
- More error handling for DOM (html document handling)
- Use message embeddings to cluster similar topics across different channels.
    - Vector Search using Elastic 
    - RAG: Returns relevant topics/messages using vector similarity 
    - Group related messages into threads (suing embeddings) even if users didn’t use the same topic or replied directly.
    - Topic Auto-Naming: predicting relevant topic title from messages (users don't need to input one manually).
    - RAG: Training a bot on all past chats to act as a *"know it all secretary"*


