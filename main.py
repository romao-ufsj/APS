import streamlit as st
import pandas as pd

class Usuario:
    def __init__(self, username, email, senha):
        self.username = username
        self.email = email
        self.senha = senha

    def autenticar(self, username, senha):
        # Verifica se as credenciais de login são válidas
        return self.username == username and self.senha == senha

class Candidato:
    def __init__(self, nome, idade, cargo, experiencia, habilidades):
        self.nome = nome
        self.idade = idade
        self.cargo = cargo
        self.experiencia = experiencia
        self.habilidades = habilidades

    def adicionar(self):
        # Adiciona um novo candidato ao banco de dados
        df = BancoDeDados.carregar_dados()
        df = df.append(self.to_dict(), ignore_index=True)
        BancoDeDados.salvar_dados(df)

    def editar(self, nome_filtro):
        # Edita as informações de um candidato existente
        df = BancoDeDados.carregar_dados()
        if nome_filtro in df["Nome"].values:
            df.loc[df["Nome"] == nome_filtro, "Nome"] = self.nome
            df.loc[df["Nome"] == nome_filtro, "Idade"] = self.idade
            df.loc[df["Nome"] == nome_filtro, "Cargo"] = self.cargo
            df.loc[df["Nome"] == nome_filtro, "Experiência"] = self.experiencia
            df.loc[df["Nome"] == nome_filtro, "Habilidades"] = self.habilidades
            BancoDeDados.salvar_dados(df)
            return True
        return False

    def excluir(self, nome_filtro):
        # Exclui um candidato do banco de dados
        df = BancoDeDados.carregar_dados()
        df = df[df["Nome"] != nome_filtro]
        BancoDeDados.salvar_dados(df)

    def to_dict(self):
        # Converte o candidato para um dicionário
        return {
            "Nome": self.nome,
            "Idade": self.idade,
            "Cargo": self.cargo,
            "Experiência": self.experiencia,
            "Habilidades": self.habilidades
        }

class BancoDeDados:
    @staticmethod
    def carregar_dados():
        try:
            # Tenta ler o arquivo CSV e retornar um DataFrame
            return pd.read_csv('candidatos.csv')
        except FileNotFoundError:
            # Se o arquivo não existir, retorna um DataFrame vazio com as colunas necessárias
            return pd.DataFrame(columns=["Nome", "Idade", "Cargo", "Experiência", "Habilidades"])

    @staticmethod
    def salvar_dados(df):
        # Salva o DataFrame no arquivo CSV
        df.to_csv('candidatos.csv', index=False)

class GestorCandidatos:
    def __init__(self, usuario):
        self.usuario = usuario

    def cadastrar_candidato(self, nome, idade, cargo, experiencia, habilidades):
        # Cria um novo candidato e salva no banco de dados
        candidato = Candidato(nome, idade, cargo, experiencia, habilidades)
        candidato.adicionar()

    def editar_candidato(self, nome_filtro, novo_nome, nova_idade, novo_cargo, nova_experiencia, novas_habilidades):
        # Cria o objeto Candidato com os novos dados
        candidato = Candidato(novo_nome, nova_idade, novo_cargo, nova_experiencia, novas_habilidades)
        return candidato.editar(nome_filtro)

    def excluir_candidato(self, nome_filtro):
        # Exclui o candidato do banco de dados
        candidato = Candidato(nome_filtro, None, None, None, None)
        candidato.excluir(nome_filtro)

    def visualizar_candidatos(self):
        # Carrega e retorna os dados dos candidatos
        return BancoDeDados.carregar_dados()

def login():
    st.title("Login - Gestor de Candidatos RH")
    username = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        usuario = Usuario(username="admin", email="admin@example.com", senha="admin123")  # Usuário fixo
        if usuario.autenticar(username, senha):
            # Inicializando o atributo 'usuario' no session_state
            st.session_state.logged_in = True
            st.session_state.usuario = usuario
            st.success("Login bem-sucedido!")
            st.experimental_rerun()  # Recarregar a página
        else:
            st.error("Usuário ou senha inválidos!")

def pagina_inicial():
    st.title("Bem-vindo ao Gestor de Candidatos RH!")
    st.markdown("""
    **Gestor de Candidatos** é um aplicativo simples desenvolvido para **gestores de RH**.
    Ele permite que você cadastre, edite, exclua e visualize informações sobre os candidatos em sua base de dados.
    """)

def app():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        login()
    else:
        # Verifica se o usuário está logado antes de acessar o atributo 'usuario'
        if 'usuario' not in st.session_state:
            st.session_state.usuario = Usuario(username="admin", email="admin@example.com", senha="admin123")

        usuario = st.session_state.usuario
        gestor = GestorCandidatos(usuario)

        st.sidebar.title(f"Bem-vindo, {usuario.username}!")
        option = st.sidebar.selectbox("Escolha uma opção", [
            "Página Inicial", "Cadastrar Candidato", "Editar Candidato", "Excluir Candidato", 
            "Visualizar Candidatos"
        ])

        if option == "Página Inicial":
            pagina_inicial()
        elif option == "Cadastrar Candidato":
            nome = st.text_input("Nome")
            idade = st.number_input("Idade", min_value=18, max_value=100)
            cargo = st.text_input("Cargo Desejado")
            experiencia = st.text_area("Experiência Profissional")
            habilidades = st.text_area("Habilidades")

            if st.button("Cadastrar"):
                gestor.cadastrar_candidato(nome, idade, cargo, experiencia, habilidades)
                st.success(f"Candidato {nome} cadastrado com sucesso!")

        elif option == "Editar Candidato":
            nome_filtro = st.text_input("Digite o nome do candidato para filtrar", "")
            if nome_filtro:
                df = gestor.visualizar_candidatos()
                candidatos_filtrados = df[df["Nome"].str.contains(nome_filtro, case=False, na=False)]
                if not candidatos_filtrados.empty:
                    st.write(candidatos_filtrados)
                    nome_selecionado = st.selectbox("Selecione o candidato para editar", candidatos_filtrados["Nome"])
                    candidato_selecionado = df[df["Nome"] == nome_selecionado].iloc[0]

                    novo_nome = st.text_input("Nome", value=candidato_selecionado["Nome"])
                    nova_idade = st.number_input("Idade", value=candidato_selecionado["Idade"])
                    novo_cargo = st.text_input("Cargo Desejado", value=candidato_selecionado["Cargo"])
                    nova_experiencia = st.text_area("Experiência Profissional", value=candidato_selecionado["Experiência"])
                    novas_habilidades = st.text_area("Habilidades", value=candidato_selecionado["Habilidades"])

                    if st.button("Salvar Alterações"):
                        if gestor.editar_candidato(nome_selecionado, novo_nome, nova_idade, novo_cargo, nova_experiencia, novas_habilidades):
                            st.success(f"Candidato {novo_nome} atualizado com sucesso!")
                        else:
                            st.error("Erro ao atualizar o candidato.")
                else:
                    st.warning("Nenhum candidato encontrado com esse nome.")
        
        elif option == "Excluir Candidato":
            nome_filtro = st.text_input("Digite o nome do candidato para filtrar", "")
            if nome_filtro:
                df = gestor.visualizar_candidatos()
                candidatos_filtrados = df[df["Nome"].str.contains(nome_filtro, case=False, na=False)]
                if not candidatos_filtrados.empty:
                    st.write(candidatos_filtrados)
                    nome_selecionado = st.selectbox("Selecione o candidato para excluir", candidatos_filtrados["Nome"])

                    if st.button("Excluir"):
                        gestor.excluir_candidato(nome_selecionado)
                        st.success(f"Candidato {nome_selecionado} excluído com sucesso!")
                else:
                    st.warning("Nenhum candidato encontrado com esse nome.")

        elif option == "Visualizar Candidatos":
            df = gestor.visualizar_candidatos()
            st.write(df)

if __name__ == "__main__":
    app()
