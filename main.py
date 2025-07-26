import streamlit as st
from agents.email_agent import generate_email_response
from utils.email_sender import send_email

st.set_page_config(page_title="MailMate – Think Less, Send Smart", layout="wide")
st.title("📧 MailMate – Think Less, Send Smart")

# Inputs
email_text = st.text_area("📥 Paste the email content you received:", height=300)
recipient_email = st.text_input("✉️ Recipient Email Address")
tone = st.selectbox("🎯 Select response tone", ["Professional", "Friendly", "Apologetic", "Persuasive"])

# Session state to store generated response
if "generated_response" not in st.session_state:
    st.session_state.generated_response = ""

# Button: Generate
if st.button("🧠 Generate Reply"):
    if not email_text:
        st.warning("Please paste the email content first.")
    else:
        with st.spinner("Generating response..."):
            st.session_state.generated_response = generate_email_response(email_text, tone)
            st.success("Reply generated! You can now edit it below.")

# Editable text area for the generated response
if st.session_state.generated_response:
    edited_response = st.text_area("✍️ Edit the generated reply (optional):", 
                                   value=st.session_state.generated_response, 
                                   height=300, 
                                   key="editable_response")

    # Button: Send
    if st.button("📤 Send Email"):
        if not recipient_email:
            st.warning("Please enter the recipient's email address.")
        else:
            with st.spinner("Sending email..."):
                send_status = send_email(recipient_email, edited_response)
                if send_status:
                    st.success(f"Email sent successfully to {recipient_email}")
                    st.session_state.generated_response = ""  # Clear for next use
                else:
                    st.error("Failed to send the email.")
