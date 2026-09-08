import streamlit as st

# ==========================================
# CONFIGURAÇÃO DE ACESSO
# ==========================================

USUARIO = "editorplanilhas"
SENHA = "@Blm1975"


def login():

    st.title("🔐 B3 DIVIDEND RADAR")

    st.markdown(
        """
        Informe suas credenciais para acessar o sistema.
        """
    )

    usuario = st.text_input(
        "Usuário"
    )

    senha = st.text_input(
        "Senha",
        type="password"
    )

    if st.button("Entrar"):

        if (
            usuario == USUARIO
            and senha == SENHA
        ):

            st.session_state.logado = True
            st.session_state.usuario = usuario

            st.success(
                "Login realizado com sucesso"
            )

            st.rerun()

        else:

            st.error(
                "Usuário ou senha inválidos."
            )

    st.stop()


def verificar_login():

    if "logado" not in st.session_state:
        st.session_state.logado = False

    if not st.session_state.logado:
        login()


def logout():

    if st.sidebar.button(
        "🚪 Sair",
        use_container_width=True
    ):

        st.session_state.clear()

        st.rerun()