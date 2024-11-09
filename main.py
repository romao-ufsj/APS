import streamlit as st
import pandas as pd

# Função para carregar o banco de dados CSV
def carregar_dados():
    try:
        # Tenta ler o arquivo CSV e retornar um DataFrame
        df = pd.read_csv('candidatos.csv')
        return df
    except FileNotFoundError:
        # Se o arquivo não existir, retorna um DataFrame vazio com as colunas necessárias
        return pd.DataFrame(columns=["Nome", "Idade", "Cargo", "Experiência", "Habilidades"])

# Função para salvar dados no CSV
def salvar_dados(df):
    # Salva o DataFrame no arquivo CSV
    df.to_csv('candidatos.csv', index=False)

# Função de login
def login():
    st.title("Login - Gestor de Candidatos RH")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if username == "admin" and password == "admin123":
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Login bem-sucedido!")
            st.experimental_rerun()  # Recarregar a página
        else:
            st.error("Usuário ou senha inválidos!")

# Função para filtrar candidatos por nome
def filtrar_por_nome(df, nome_filtro):
    return df[df["Nome"].str.contains(nome_filtro, case=False, na=False)]

# Página de Cadastro de Candidatos
def cadastrar_candidato():
    st.title("Cadastro de Candidatos")
    nome = st.text_input("Nome")
    idade = st.number_input("Idade", min_value=18, max_value=100)
    cargo = st.text_input("Cargo Desejado")
    experiencia = st.text_area("Experiência Profissional")
    habilidades = st.text_area("Habilidades")

    if st.button("Cadastrar"):
        # Carregar dados existentes
        df = carregar_dados()

        # Adicionar novo candidato
        novo_candidato = {
            "Nome": nome,
            "Idade": idade,
            "Cargo": cargo,
            "Experiência": experiencia,
            "Habilidades": habilidades,
        }
        df = df.append(novo_candidato, ignore_index=True)

        # Salvar de volta no CSV
        salvar_dados(df)
        st.success(f"Candidato {nome} cadastrado com sucesso!")

# Página de Edição de Candidatos
def editar_candidato():
    st.title("Editar Candidato")
    # Carregar dados existentes
    df = carregar_dados()

    # Permitir filtragem por nome
    nome_filtro = st.text_input("Digite o nome do candidato para filtrar", "")
    
    if nome_filtro:
        # Filtra os candidatos que contêm o texto inserido (ignorando maiúsculas/minúsculas)
        candidatos_filtrados = filtrar_por_nome(df, nome_filtro)

        if not candidatos_filtrados.empty:
            # Exibe os candidatos filtrados
            st.write(candidatos_filtrados)

            # Seleciona o candidato para editar
            nome_selecionado = st.selectbox("Selecione o candidato para editar", candidatos_filtrados["Nome"])

            candidato_selecionado = df[df["Nome"] == nome_selecionado].iloc[0]

            # Formulário para editar os dados
            novo_nome = st.text_input("Nome", value=candidato_selecionado["Nome"])
            nova_idade = st.number_input("Idade", value=candidato_selecionado["Idade"])
            novo_cargo = st.text_input("Cargo Desejado", value=candidato_selecionado["Cargo"])
            nova_experiencia = st.text_area("Experiência Profissional", value=candidato_selecionado["Experiência"])
            novas_habilidades = st.text_area("Habilidades", value=candidato_selecionado["Habilidades"])

            if st.button("Salvar Alterações"):
                # Atualizar o DataFrame com as novas informações
                df.loc[df["Nome"] == nome_selecionado, "Nome"] = novo_nome
                df.loc[df["Nome"] == nome_selecionado, "Idade"] = nova_idade
                df.loc[df["Nome"] == nome_selecionado, "Cargo"] = novo_cargo
                df.loc[df["Nome"] == nome_selecionado, "Experiência"] = nova_experiencia
                df.loc[df["Nome"] == nome_selecionado, "Habilidades"] = novas_habilidades

                # Salvar as mudanças no CSV
                salvar_dados(df)
                st.success(f"Candidato {novo_nome} atualizado com sucesso!")
        else:
            st.warning("Nenhum candidato encontrado com esse nome.")
    else:
        st.warning("Digite um nome para filtrar.")

# Página de Exclusão de Candidatos
def excluir_candidato():
    st.title("Excluir Candidato")
    # Carregar dados existentes
    df = carregar_dados()

    # Permitir filtragem por nome
    nome_filtro = st.text_input("Digite o nome do candidato para filtrar", "")
    
    if nome_filtro:
        # Filtra os candidatos que contêm o texto inserido (ignorando maiúsculas/minúsculas)
        candidatos_filtrados = filtrar_por_nome(df, nome_filtro)

        if not candidatos_filtrados.empty:
            # Exibe os candidatos filtrados
            st.write(candidatos_filtrados)

            # Seleciona o candidato para excluir
            nome_selecionado = st.selectbox("Selecione o candidato para excluir", candidatos_filtrados["Nome"])

            if st.button("Excluir"):
                df = df[df["Nome"] != nome_selecionado]
                # Salvar o DataFrame atualizado no CSV
                salvar_dados(df)
                st.success(f"Candidato {nome_selecionado} excluído com sucesso!")
        else:
            st.warning("Nenhum candidato encontrado com esse nome.")
    else:
        st.warning("Digite um nome para filtrar.")

# Página de Visualização de Candidatos
def visualizar_candidatos():
    st.title("Visualização de Candidatos")
    # Carregar dados do CSV
    df = carregar_dados()
    
    # Exibir a tabela com todos os candidatos
    st.write(df)

# Página inicial com informações sobre o aplicativo
def pagina_inicial():
    st.title("Bem-vindo ao Gestor de Candidatos RH!")
    st.markdown("""
    **Gestor de Candidatos** é um aplicativo simples desenvolvido para **gestores de RH**.
    Ele permite que você cadastre, edite, exclua e visualize informações sobre os candidatos em sua base de dados.

    O aplicativo tem as seguintes funcionalidades:
    - **Cadastro de Candidatos**: Adicione novos candidatos com informações como nome, idade, cargo desejado, experiência e habilidades.
    - **Edição de Candidatos**: Modifique as informações de um candidato existente filtrando pelo nome.
    - **Exclusão de Candidatos**: Exclua candidatos da sua base de dados.
    - **Visualização de Candidatos**: Veja a lista completa de todos os candidatos cadastrados.

    Para começar, faça o login e escolha a funcionalidade desejada no menu lateral.

    ### Instruções
    1. Entre com o usuário e senha para acessar o sistema.
    2. Use o menu lateral para navegar entre as funcionalidades.
    3. A qualquer momento, você pode visualizar, editar ou excluir candidatos.

    **Login:**
    - Usuário: `admin`
    - Senha: `admin123`

    Boa sorte no gerenciamento dos candidatos!
    """)

# Função principal
def app():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        login()
    else:
        st.sidebar.title(f"Bem-vindo, {st.session_state.username}!")
        option = st.sidebar.selectbox("Escolha uma opção", [
            "Página Inicial", "Cadastrar Candidato", "Editar Candidato", "Excluir Candidato", 
            "Visualizar Candidatos"
        ])

        if option == "Página Inicial":
            pagina_inicial()
        elif option == "Cadastrar Candidato":
            cadastrar_candidato()
        elif option == "Editar Candidato":
            editar_candidato()
        elif option == "Excluir Candidato":
            excluir_candidato()
        elif option == "Visualizar Candidatos":
            visualizar_candidatos()

if __name__ == "__main__":
    app()

