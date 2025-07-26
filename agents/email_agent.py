import streamlit as st
import openai
from openai import RateLimitError, OpenAIError

# Initialize OpenAI client with your API key from Streamlit secrets
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def generate_email_response(email_text, tone):
    prompt = f"""
You are an AI assistant. Write a reply to the following email using a {tone.lower()} tone:

Email:
{email_text}

Reply:
"""

    try:
        # Attempt to use GPT-4o
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        st.info("✅ Response generated using GPT-4o")
        return response.choices[0].message.content

    except RateLimitError:
        st.warning("⚠️ GPT-4o rate limit hit. Falling back to GPT-3.5-turbo...")

    except OpenAIError as e:
        st.warning(f"⚠️ GPT-4o error: {e}. Falling back to GPT-3.5-turbo...")

    # Fallback: GPT-3.5-turbo
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        st.info("✏️ Response generated using GPT-3.5-turbo")
        return response.choices[0].message.content

    except OpenAIError as e:
        st.error(f"❌ OpenAI API error: {e}")
        return "Error: Could not generate response due to API issues."
