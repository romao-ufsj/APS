import streamlit as st
import pandas as pd
import uuid
import os

# Caminho dos arquivos CSV
VACANCIES_FILE = "vagas.csv"
CANDIDATES_FILE = "candidatos.csv"
RECRUITERS_FILE = "recrutadores.csv"

# Banco de dados simulado
vacancies_db = {}
candidates_db = {}
recruiters_db = {}

# Funções auxiliares
def generate_id():
    return str(uuid.uuid4())

# Carregar banco de dados do arquivo CSV
def load_database(file_path):
    if os.path.exists(file_path):
        return pd.read_csv(file_path).to_dict(orient='index')
    return {}

# Salvar banco de dados no arquivo CSV
def save_database(db, file_path):
    df = pd.DataFrame.from_dict(db, orient='index')
    df.to_csv(file_path, index=False)

# Carregar dados iniciais
def load_data():
    global vacancies_db, candidates_db, recruiters_db
    vacancies_db = load_database(VACANCIES_FILE)
    candidates_db = load_database(CANDIDATES_FILE)
    recruiters_db = load_database(RECRUITERS_FILE)

# Salvar dados
def save_data():
    save_database(vacancies_db, VACANCIES_FILE)
    save_database(candidates_db, CANDIDATES_FILE)
    save_database(recruiters_db, RECRUITERS_FILE)

# Página de cadastro
def registration_page():
    st.title("Cadastro")

    user_type = st.selectbox("Selecione o Tipo de Usuário", ["Candidato", "Recrutador"])
    name = st.text_input("Nome")
    email = st.text_input("Email")
    password = st.text_input("Senha", type="password")

    if st.button("Cadastrar"):
        if user_type == "Candidato":
            db = candidates_db
            file = CANDIDATES_FILE
        else:
            db = recruiters_db
            file = RECRUITERS_FILE

        if email in db:
            st.error("Este email já está cadastrado!")
        else:
            db[email] = {
                "name": name,
                "password": password,
                "email": email,
            }
            save_database(db, file)
            st.success(f"{user_type} cadastrado com sucesso! Agora você pode fazer login.")

# Função de autenticação
def authenticate_user(user_type, email, password):
    if user_type == "Candidato":
        db = candidates_db
    elif user_type == "Recrutador":
        db = recruiters_db
    else:
        return None

    user = db.get(email)
    if user and user["password"] == password:
        return user
    return None

# Página de autenticação
def authentication_page():
    st.title("Login")

    user_type = st.selectbox("Selecione o Tipo de Usuário", ["Admin", "Candidato", "Recrutador"])
    email = st.text_input("Email")
    password = st.text_input("Senha", type="password")

    if st.button("Login"):
        if user_type == "Admin":
            st.session_state["authenticated"] = True
            st.session_state["user_type"] = "Admin"
            st.success(f"Bem-vindo Admin!")
            st.experimental_rerun()
        else:
            user = authenticate_user(user_type, email, password)
            if user:
                st.session_state["authenticated"] = True
                st.session_state["user_type"] = user_type
                st.session_state["user_email"] = email
                st.success(f"Bem-vindo {user['name']}!")
                st.experimental_rerun()
            else:
                st.error("Email ou senha inválidos")

# Função de painel do Admin
def admin_dashboard():
    st.title("Painel do Admin")
    st.sidebar.subheader("Ações do Admin")

    action = st.sidebar.selectbox("Escolha uma ação", [
        "Gerenciar Candidatos", 
        "Gerenciar Recrutadores", 
        "Gerenciar Vagas", 
        "Sair"
    ])

    if action == "Gerenciar Candidatos":
        st.subheader("Gerenciamento de Candidatos")
        for email, candidate in candidates_db.items():
            st.write(f"Nome: {candidate['name']}, Email: {candidate['email']}")
            if st.button(f"Excluir {candidate['email']}"):
                del candidates_db[email]
                save_database(candidates_db, CANDIDATES_FILE)
                st.experimental_rerun()

        st.subheader("Adicionar Novo Candidato")
        name = st.text_input("Nome do Candidato")
        email = st.text_input("Email do Candidato")
        password = st.text_input("Senha do Candidato", type="password")
        if st.button("Adicionar Candidato"):
            if email in candidates_db:
                st.error("Este email já está cadastrado!")
            else:
                candidates_db[email] = {
                    "name": name,
                    "password": password,
                    "email": email,
                }
                save_database(candidates_db, CANDIDATES_FILE)
                st.success("Candidato adicionado com sucesso!")

    elif action == "Gerenciar Recrutadores":
        st.subheader("Gerenciamento de Recrutadores")
        for email, recruiter in recruiters_db.items():
            st.write(f"Nome: {recruiter['name']}, Email: {recruiter['email']}")
            if st.button(f"Excluir {recruiter['email']}"):
                del recruiters_db[email]
                save_database(recruiters_db, RECRUITERS_FILE)
                st.experimental_rerun()

        st.subheader("Adicionar Novo Recrutador")
        name = st.text_input("Nome do Recrutador")
        email = st.text_input("Email do Recrutador")
        password = st.text_input("Senha do Recrutador", type="password")
        if st.button("Adicionar Recrutador"):
            if email in recruiters_db:
                st.error("Este email já está cadastrado!")
            else:
                recruiters_db[email] = {
                    "name": name,
                    "password": password,
                    "email": email,
                }
                save_database(recruiters_db, RECRUITERS_FILE)
                st.success("Recrutador adicionado com sucesso!")

    elif action == "Gerenciar Vagas":
        st.subheader("Gerenciamento de Vagas")
        for vac_id, vacancy in vacancies_db.items():
            st.write(f"ID: {vac_id}")
            st.write(f"Empresa: {vacancy['company']}")
            st.write(f"Cargo: {vacancy['position']}")
            st.write(f"Salário: {vacancy['salary']}")
            st.write(f"Email: {vacancy['email']}")
            if st.button(f"Excluir Vaga {vac_id}"):
                del vacancies_db[vac_id]
                save_database(vacancies_db, VACANCIES_FILE)
                st.experimental_rerun()

        # Formulário para adicionar uma nova vaga
        st.subheader("Adicionar Nova Vaga")
        company = st.text_input("Empresa")
        position = st.text_input("Cargo")
        salary = st.number_input("Salário", min_value=0)
        email = st.text_input("Email para Contato")
        if st.button("Submeter Vaga"):
            vac_id = generate_id()
            vacancies_db[vac_id] = {
                "company": company,
                "position": position,
                "salary": salary,
                "email": email,
            }
            save_database(vacancies_db, VACANCIES_FILE)  # Salvar no CSV
            st.success("Vaga adicionada com sucesso!")

    elif action == "Sair":
        st.session_state["authenticated"] = False
        st.experimental_rerun()

# Painel do Candidato
def candidate_dashboard():
    st.title("Painel do Candidato")
    st.subheader("Vagas Disponíveis")

    if not vacancies_db:
        st.write("Não há vagas disponíveis no momento.")
    else:
        for vac_id, vacancy in vacancies_db.items():
            st.write(f"ID: {vac_id}")
            st.write(f"Empresa: {vacancy['company']}")
            st.write(f"Cargo: {vacancy['position']}")
            st.write(f"Salário: {vacancy['salary']}")
            st.write(f"Email para Contato: {vacancy['email']}")
            st.write("---")

    if st.sidebar.button("Sair"):
        st.session_state["authenticated"] = False
        st.experimental_rerun()

# Painel do Recrutador
def recruiter_dashboard():
    st.title("Painel do Recrutador")
    st.subheader("Minhas Vagas")

    recruiter_email = st.session_state.get("user_email")

    # Mostrar vagas do recrutador logado
    my_vacancies = {k: v for k, v in vacancies_db.items() if v['email'] == recruiter_email}

    if not my_vacancies:
        st.write("Você ainda não cadastrou nenhuma vaga.")
    else:
        for vac_id, vacancy in my_vacancies.items():
            st.write(f"ID: {vac_id}")
            st.write(f"Empresa: {vacancy['company']}")
            st.write(f"Cargo: {vacancy['position']}")
            st.write(f"Salário: {vacancy['salary']}")
            st.write("---")

    # Formulário para adicionar uma nova vaga
    st.subheader("Adicionar Nova Vaga")
    company = st.text_input("Empresa")
    position = st.text_input("Cargo")
    salary = st.number_input("Salário", min_value=0)

    if st.button("Submeter Vaga"):
        vac_id = generate_id()
        vacancies_db[vac_id] = {
            "company": company,
            "position": position,
            "salary": salary,
            "email": recruiter_email,
        }
        save_database(vacancies_db, VACANCIES_FILE)  # Salvar no CSV
        st.success("Vaga adicionada com sucesso!")

    if st.sidebar.button("Sair"):
        st.session_state["authenticated"] = False
        st.experimental_rerun()

# Página principal da aplicação
def main():
    # Carregar dados ao iniciar a aplicação
    load_data()

    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        page = st.sidebar.selectbox("Selecione a Página", ["Login", "Cadastro"])
        if page == "Login":
            authentication_page()
        elif page == "Cadastro":
            registration_page()
    else:
        user_type = st.session_state.get("user_type", "")

        if user_type == "Admin":
            admin_dashboard()
        elif user_type == "Candidato":
            candidate_dashboard()
        elif user_type == "Recrutador":
            recruiter_dashboard()

if __name__ == "__main__":
    main()

