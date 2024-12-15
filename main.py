import streamlit as st
import uuid

# Banco de dados simulado no session_state
def initialize_db():
    if 'vacancies_db' not in st.session_state:
        st.session_state.vacancies_db = {}
    if 'candidates_db' not in st.session_state:
        st.session_state.candidates_db = {}
    if 'recruiters_db' not in st.session_state:
        st.session_state.recruiters_db = {}

# Funções auxiliares
def generate_id():
    return str(uuid.uuid4())

# Função de registro
def registration_page():
    st.title("Cadastro")

    # Seleção de tipo de usuário (Candidato ou Recrutador)
    user_type = st.selectbox("Selecione o Tipo de Usuário", ["Candidato", "Recrutador"])
    name = st.text_input("Nome")
    email = st.text_input("Email")
    password = st.text_input("Senha", type="password")

    # Ao clicar em "Cadastrar", o sistema verifica qual tipo de usuário é e registra no banco de dados correto
    if st.button("Cadastrar"):
        if user_type == "Candidato":
            db = st.session_state.candidates_db
        else:
            db = st.session_state.recruiters_db

        # Verifica se o email já está cadastrado
        if email in db:
            st.error("Este email já está cadastrado!")
        else:
            db[email] = {
                "name": name,
                "password": password,
                "email": email,
            }
            st.success(f"{user_type} cadastrado com sucesso! Agora você pode fazer login.")

# Função de autenticação
def authenticate_user(user_type, email, password):
    if user_type == "Candidato":
        db = st.session_state.candidates_db
    elif user_type == "Recrutador":
        db = st.session_state.recruiters_db
    else:
        return None

    user = db.get(email)
    if user and user["password"] == password:
        return user
    return None

def authentication_page():
    st.title("Login")

    # Seleção de tipo de usuário
    user_type = st.selectbox("Selecione o Tipo de Usuário", ["Admin", "Candidato", "Recrutador"])
    email = st.text_input("Email")
    password = st.text_input("Senha", type="password")

    if st.button("Login"):
        if user_type == "Admin" and email == "admin@example.com" and password == "admin":
            st.session_state["authenticated"] = True
            st.session_state["user_type"] = "Admin"
            st.session_state["user_email"] = email
            st.success(f"Bem-vindo Admin!")
            st.experimental_rerun()  # Redireciona para o painel admin
        else:
            user = authenticate_user(user_type, email, password)
            if user:
                st.session_state["authenticated"] = True
                st.session_state["user_type"] = user_type
                st.session_state["user_email"] = email
                st.session_state["user_name"] = user["name"]
                st.success(f"Bem-vindo {user['name']}!")
                st.experimental_rerun()  # Redireciona para o painel de candidato ou recrutador
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
        for email, candidate in st.session_state.candidates_db.items():
            st.write(f"Nome: {candidate['name']}, Email: {candidate['email']}")
            if st.button(f"Excluir {candidate['email']}", key=f"delete_{email}"):
                del st.session_state.candidates_db[email]
                st.experimental_rerun()

        st.subheader("Adicionar Novo Candidato")
        name = st.text_input("Nome do Candidato")
        email = st.text_input("Email do Candidato")
        password = st.text_input("Senha do Candidato", type="password")
        if st.button("Adicionar Candidato"):
            if email in st.session_state.candidates_db:
                st.error("Este email já está cadastrado!")
            else:
                st.session_state.candidates_db[email] = {
                    "name": name,
                    "password": password,
                    "email": email,
                }
                st.success("Candidato adicionado com sucesso!")

    elif action == "Gerenciar Recrutadores":
        st.subheader("Gerenciamento de Recrutadores")
        for email, recruiter in st.session_state.recruiters_db.items():
            st.write(f"Nome: {recruiter['name']}, Email: {recruiter['email']}")
            if st.button(f"Excluir {recruiter['email']}", key=f"delete_{email}"):
                del st.session_state.recruiters_db[email]
                st.experimental_rerun()

        st.subheader("Adicionar Novo Recrutador")
        name = st.text_input("Nome do Recrutador")
        email = st.text_input("Email do Recrutador")
        password = st.text_input("Senha do Recrutador", type="password")
        if st.button("Adicionar Recrutador"):
            if email in st.session_state.recruiters_db:
                st.error("Este email já está cadastrado!")
            else:
                st.session_state.recruiters_db[email] = {
                    "name": name,
                    "password": password,
                    "email": email,
                }
                st.success("Recrutador adicionado com sucesso!")

    elif action == "Gerenciar Vagas":
        st.subheader("Gerenciamento de Vagas")

        # Exibindo as vagas existentes e permitindo a edição ou exclusão
        for vac_id, vacancy in st.session_state.vacancies_db.items():
            st.write(f"ID: {vac_id}")
            st.write(f"Empresa: {vacancy['company']}")
            st.write(f"Cargo: {vacancy['position']}")
            st.write(f"Salário: {vacancy['salary']}")
            if st.button(f"Editar {vacancy['position']}", key=f"edit_{vac_id}"):
                edit_vacancy(vac_id)  # Função para editar a vaga
            if st.button(f"Excluir {vacancy['position']}", key=f"delete_{vac_id}"):
                del st.session_state.vacancies_db[vac_id]
                st.success("Vaga excluída com sucesso!")
                st.experimental_rerun()

        # Seção para adicionar uma nova vaga
        st.subheader("Adicionar Nova Vaga")
        company = st.text_input("Empresa")
        position = st.text_input("Cargo")
        salary = st.number_input("Salário", min_value=0)

        if st.button("Submeter Vaga"):
            vac_id = generate_id()
            st.session_state.vacancies_db[vac_id] = {
                "company": company,
                "position": position,
                "salary": salary,
                "email": "admin@example.com",  # Defina o e-mail de quem está criando a vaga
            }
            st.success("Vaga adicionada com sucesso!")

    if st.sidebar.button("Sair"):
        st.session_state["authenticated"] = False
        st.experimental_rerun()

# Função de edição de vaga
def edit_vacancy(vac_id):
    st.subheader("Editar Vaga")

    vacancy = st.session_state.vacancies_db.get(vac_id)

    if vacancy:
        # Exibir campos para edição
        company = st.text_input("Empresa", value=vacancy["company"])
        position = st.text_input("Cargo", value=vacancy["position"])
        salary = st.number_input("Salário", min_value=0, value=vacancy["salary"])

        if st.button("Salvar alterações"):
            # Atualizar a vaga com os novos dados
            st.session_state.vacancies_db[vac_id] = {
                "company": company,
                "position": position,
                "salary": salary,
                "email": vacancy["email"],  # Não alterar o email do recrutador
            }
            st.success("Vaga editada com sucesso!")
            st.experimental_rerun()  # Redireciona para o painel admin após a edição


# Painel do Candidato
def candidate_dashboard():
    st.title("Painel do Candidato")
    st.subheader("Vagas Disponíveis")

    if not st.session_state.vacancies_db:
        st.write("Não há vagas disponíveis no momento.")
    else:
        for vac_id, vacancy in st.session_state.vacancies_db.items():
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

    my_vacancies = {k: v for k, v in st.session_state.vacancies_db.items() if v['email'] == recruiter_email}

    if not my_vacancies:
        st.write("Você ainda não cadastrou nenhuma vaga.")
    else:
        for vac_id, vacancy in my_vacancies.items():
            st.write(f"ID: {vac_id}")
            st.write(f"Empresa: {vacancy['company']}")
            st.write(f"Cargo: {vacancy['position']}")
            st.write(f"Salário: {vacancy['salary']}")
            st.write("---")

    st.subheader("Adicionar Nova Vaga")
    company = st.text_input("Empresa")
    position = st.text_input("Cargo")
    salary = st.number_input("Salário", min_value=0)

    if st.button("Submeter Vaga"):
        vac_id = generate_id()
        st.session_state.vacancies_db[vac_id] = {
            "company": company,
            "position": position,
            "salary": salary,
            "email": recruiter_email,
        }
        st.success("Vaga adicionada com sucesso!")

    if st.sidebar.button("Sair"):
        st.session_state["authenticated"] = False
        st.experimental_rerun()

# Página principal da aplicação
def main():
    initialize_db()

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

