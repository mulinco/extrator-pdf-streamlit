import streamlit as st
from modules.telegram_bot import send_telegram_message

def show_tab_contato():
    """
    Renderiza o formulário de contato e relatar bugs.
    """
    st.markdown("<h3 style='text-align: center;'>Encontrou um problema ou tem uma sugestão?</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Use o formulário abaixo para me enviar uma notificação.</p>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        with st.form(key="contact_form"):
            user_email = st.text_input(
                "Seu e-mail (opcional)",
                placeholder="seu.email@exemplo.com"
            )
            message_body = st.text_area(
                "Mensagem",
                placeholder="Descreva o erro ou a sua sugestão...",
                height=200
            )
            submit_button = st.form_submit_button(
                label='Enviar Notificação',
                use_container_width=True
            )

            if submit_button:
                if not message_body.strip():
                    st.warning("Por favor, escreva uma mensagem antes de enviar.")
                else:
                    full_message = f"📨 Novo Relato no App Extrator\n"
                    full_message += f"========================\n"
                    full_message += f"**De:** {user_email if user_email else 'Anônimo'}\n"
                    full_message += f"**Mensagem:**\n{message_body}"
                    
                    with st.spinner("Enviando..."):
                        if send_telegram_message(full_message):
                            st.success("Sua notificação foi enviada com sucesso! Obrigado pelo feedback.")
                        else:
                            st.error("Houve uma falha no envio. Verifique as credenciais ou tente novamente.")