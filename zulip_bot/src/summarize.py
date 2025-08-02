import openai
import os

# Pricing for gpt-3.5-turbo as of 2024-06 (update if needed)
PRICE_PER_1K_PROMPT = 0.0005  # $0.0005 per 1K prompt tokens
PRICE_PER_1K_COMPLETION = 0.0015  # $0.0015 per 1K completion tokens

def summarize_messages(messages):
    """
    Summarizes a list of Zulip chat messages using OpenAI GPT-3.5 Turbo.
    Returns a dictionary with the summary, OpenAI token usage, and estimated cost.
    If an error occurs, returns a summary indicating the error and usage/cost as None.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    try:
        client = openai.OpenAI(api_key=api_key)
        contents = "\n".join([msg["content"] for msg in messages])
        prompt = f"Summarize the following Zulip chat messages:\n{contents}"
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100
        )
        if not response.choices or not hasattr(response.choices[0], "message"):
            raise RuntimeError("OpenAI response missing expected fields.")
        summary = response.choices[0].message.content.strip()

        # Get token usage
        usage = getattr(response, "usage", None)
        if usage:
            prompt_tokens = usage.prompt_tokens
            completion_tokens = usage.completion_tokens
            total_tokens = usage.total_tokens
            cost = (
                (prompt_tokens / 1000) * PRICE_PER_1K_PROMPT +
                (completion_tokens / 1000) * PRICE_PER_1K_COMPLETION
            )
        else:
            prompt_tokens = completion_tokens = total_tokens = None
            cost = None

        return {
            "summary": summary,
            "openai_usage": {
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": total_tokens,
                "cost_usd": round(cost, 6) if cost is not None else None
            }
        }
    except Exception as e:
        return {
            "summary": "Summary unavailable due to error.",
            "openai_usage": {
                "prompt_tokens": None,
                "completion_tokens": None,
                "total_tokens": None,
                "cost_usd": None,
                "error": str(e)
            }
        }