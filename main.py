import streamlit as st
import pandas as pd
import uuid
import os

# Caminho dos arquivos CSV
VACANCIES_FILE = "vagas.csv"
CANDIDATES_FILE = "candidatos.csv"
RECRUITERS_FILE = "agentes_rh.csv"

# Banco de dados simulado
users_db = {
    "admins": {
        "admin@example.com": {
            "name": "Admin User",
            "password": "admin123",
            "username": "admin"
        }
    },
    "candidates": {},  # Inicializando como um dicionário vazio
    "recruiters": {},  # Inicializando como um dicionário vazio
}

vacancies_db = {}

# Funções auxiliares
def generate_id():
    return str(uuid.uuid4())

# Carregar candidatos do CSV
def load_candidates():
    if os.path.exists(CANDIDATES_FILE):
        df = pd.read_csv(CANDIDATES_FILE)
        users_db['candidates'] = {row['email']: row.to_dict() for _, row in df.iterrows()}
    else:
        users_db['candidates'] = {}

# Carregar recrutadores do CSV
def load_recruiters():
    if os.path.exists(RECRUITERS_FILE):
        df = pd.read_csv(RECRUITERS_FILE)
        users_db['recruiters'] = {row['email']: row.to_dict() for _, row in df.iterrows()}
    else:
        users_db['recruiters'] = {}

# Carregar vagas do arquivo CSV
def load_vacancies():
    global vacancies_db
    if os.path.exists(VACANCIES_FILE):
        vacancies_df = pd.read_csv(VACANCIES_FILE)
        vacancies_db = vacancies_df.to_dict(orient='index')
    else:
        vacancies_db = {}

# Salvar vagas no arquivo CSV
def save_vacancies():
    vacancies_df = pd.DataFrame.from_dict(vacancies_db, orient='index')
    vacancies_df.to_csv(VACANCIES_FILE, index=False)

# Função de autenticação
def authenticate_user(user_type, email, password):
    if email in users_db[user_type] and users_db[user_type][email]['password'] == password:
        return users_db[user_type][email]
    return None

# Função para editar a vaga
def edit_vacancy(vacancy_id):
    vacancy = vacancies_db.get(vacancy_id)
    if vacancy:
        st.subheader("Editar Vaga")
        company = st.text_input("Empresa", value=vacancy["company"])
        position = st.text_input("Cargo", value=vacancy["position"])
        salary = st.number_input("Salário", min_value=0, value=vacancy["salary"])
        email = st.text_input("Email para Contato", value=vacancy["email"])

        if st.button("Salvar alterações"):
            vacancies_db[vacancy_id] = {
                "company": company,
                "position": position,
                "salary": salary,
                "email": email,
            }
            save_vacancies()
            st.success("Vaga atualizada com sucesso!")
    else:
        st.error("Vaga não encontrada!")

# Função para criar um novo candidato
def create_candidate():
    st.subheader("Criar Novo Candidato")
    name = st.text_input("Nome do Candidato")
    email = st.text_input("Email")
    password = st.text_input("Senha", type="password")

    if st.button("Criar Candidato"):
        if email in users_db["candidates"]:
            st.error("Este email já está cadastrado!")
        else:
            users_db["candidates"][email] = {
                "name": name,
                "password": password,
                "email": email,
            }
            save_candidates()
            st.success("Candidato criado com sucesso!")

# Função para criar um novo recrutador
def create_recruiter():
    st.subheader("Criar Novo Recrutador")
    name = st.text_input("Nome do Recrutador")
    email = st.text_input("Email")
    password = st.text_input("Senha", type="password")

    if st.button("Criar Recrutador"):
        if email in users_db["recruiters"]:
            st.error("Este email já está cadastrado!")
        else:
            users_db["recruiters"][email] = {
                "name": name,
                "password": password,
                "email": email,
            }
            save_recruiters()
            st.success("Recrutador criado com sucesso!")

# Função de painel do Admin
def admin_dashboard():
    st.title("Painel do Admin")
    st.sidebar.subheader("Ações do Admin")

    action = st.sidebar.selectbox("Escolha uma ação", [
        "Gerenciar Vagas", 
        "Gerenciar Candidatos", 
        "Gerenciar Recrutadores", 
        "Criar Novo Candidato",
        "Criar Novo Recrutador",
        "Sair"
    ])

    if action == "Gerenciar Vagas":
        st.subheader("Gerenciamento de Vagas")
        for vac_id, vacancy in vacancies_db.items():
            st.write(f"ID: {vac_id}")
            st.write(f"Empresa: {vacancy['company']}")
            st.write(f"Cargo: {vacancy['position']}")
            st.write(f"Salário: {vacancy['salary']}")
            st.write(f"Email: {vacancy['email']}")
            if st.button(f"Editar Vaga {vac_id}"):
                edit_vacancy(vac_id)

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
            save_vacancies()  # Salvar no CSV
            st.success("Vaga adicionada com sucesso!")

    elif action == "Gerenciar Candidatos":
        st.subheader("Gerenciamento de Candidatos")
        for email, candidate in users_db["candidates"].items():
            st.write(candidate)
            if st.button(f"Editar {email}"):
                edit_candidate(email)

    elif action == "Gerenciar Recrutadores":
        st.subheader("Gerenciamento de Recrutadores")
        for email, recruiter in users_db["recruiters"].items():
            st.write(recruiter)
            if st.button(f"Editar {email}"):
                edit_recruiter(email)

    elif action == "Criar Novo Candidato":
        create_candidate()

    elif action == "Criar Novo Recrutador":
        create_recruiter()

    elif action == "Sair":
        st.session_state["authenticated"] = False
        st.experimental_rerun()

# Função para editar o candidato
def edit_candidate(email):
    candidate = users_db['candidates'].get(email)
    if candidate:
        st.subheader("Editar Candidato")
        name = st.text_input("Nome", value=candidate["name"])
        password = st.text_input("Senha", type="password", value=candidate["password"])
        if st.button("Salvar alterações"):
            users_db['candidates'][email] = {
                "name": name,
                "password": password,
                "email": email,
            }
            save_candidates()
            st.success("Candidato atualizado com sucesso!")
    else:
        st.error("Candidato não encontrado!")

# Função para editar o recrutador
def edit_recruiter(email):
    recruiter = users_db['recruiters'].get(email)
    if recruiter:
        st.subheader("Editar Recrutador")
        name = st.text_input("Nome", value=recruiter["name"])
        password = st.text_input("Senha", type="password", value=recruiter["password"])
        if st.button("Salvar alterações"):
            users_db['recruiters'][email] = {
                "name": name,
                "password": password,
                "email": email,
            }
            save_recruiters()
            st.success("Recrutador atualizado com sucesso!")
    else:
        st.error("Recrutador não encontrado!")

# Função para salvar candidatos no arquivo CSV
def save_candidates():
    df = pd.DataFrame.from_dict(users_db['candidates'], orient='index')
    df.to_csv(CANDIDATES_FILE, index=False)

# Função para salvar recrutadores no arquivo CSV
def save_recruiters():
    df = pd.DataFrame.from_dict(users_db['recruiters'], orient='index')
    df.to_csv(RECRUITERS_FILE, index=False)

# Função de painel do Candidato
def candidate_dashboard():
    st.title("Painel do Candidato")
    st.subheader("Vagas Disponíveis")

    # Exibir vagas disponíveis
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

    # Opção de sair
    if st.button("Sair"):
        st.session_state["authenticated"] = False
        st.experimental_rerun()

# Função de painel do Recrutador
def recruiter_dashboard():
    st.title("Painel do Recrutador")
    st.subheader("Postar uma Vaga")

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
        save_vacancies()  # Salvar no CSV
        st.success("Vaga postada com sucesso!")

    # Opção de sair
    if st.button("Sair"):
        st.session_state["authenticated"] = False
        st.experimental_rerun()

# Página de autenticação
def authentication_page():
    st.title("Login")

    user_type = st.selectbox("Selecione o Tipo de Usuário", ["Admin", "Candidato", "Recrutador"])
    email = st.text_input("Email")
    password = st.text_input("Senha", type="password")

    if st.button("Login"):
        user = authenticate_user(user_type.lower() + 's', email, password)
        if user:
            st.session_state["authenticated"] = True
            st.session_state["user_type"] = user_type
            st.session_state["user_email"] = email
            st.success(f"Bem-vindo {user['name']}!")
            st.experimental_rerun()  # Forçar o rerun para ir ao painel correto
        else:
            st.error("Email ou senha inválidos")

# Aplicação principal
if __name__ == "__main__":
    # Carregar as vagas e usuários do CSV quando o app iniciar
    load_vacancies()
    load_candidates()
    load_recruiters()

    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        authentication_page()
    else:
        user_type = st.session_state.get("user_type", "")

        if user_type == "Admin":
            admin_dashboard()
        elif user_type == "Candidato":
            candidate_dashboard()
        elif user_type == "Recrutador":
            recruiter_dashboard()
if __name__ == "__main__":
    app()
