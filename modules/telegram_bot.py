import requests
import streamlit as st

def send_telegram_message(message_text):
    """
    Envia uma mensagem para o Telegram via Bot.
    Requer st.secrets configurado com [telegram] BOT_TOKEN e CHAT_ID.
    """
    bot_token = st.secrets.get("telegram", {}).get("BOT_TOKEN")
    chat_id = st.secrets.get("telegram", {}).get("CHAT_ID")

    if not bot_token or not chat_id:
        st.error("Credenciais do Telegram não configuradas nos Secrets.")
        return False
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message_text,
        'parse_mode': 'Markdown'
    }
    
    try:
        response = requests.post(url, json=payload)
        return response.json().get("ok", False)
    except Exception as e:
        st.error(f"Erro ao enviar a mensagem: {e}")
        return False