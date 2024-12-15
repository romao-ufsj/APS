##Plataforma de Recrutamento com Streamlit
Este é um sistema de recrutamento desenvolvido com o Streamlit, permitindo a interação entre Administradores, Candidatos e Recrutadores. O sistema permite que Administradores gerenciem usuários e vagas, enquanto Recrutadores podem postar vagas e visualizar candidatos, e Candidatos podem se cadastrar e visualizar vagas disponíveis.

Funcionalidades
Administrador
Login: Acessa a plataforma com um email e senha de administrador.
Gerenciar Candidatos: Adiciona, edita ou exclui candidatos.
Gerenciar Recrutadores: Adiciona, edita ou exclui recrutadores.
Gerenciar Vagas: Adiciona, edita ou exclui vagas de emprego.
Criar Novo Candidato: Registra novos candidatos no sistema.
Criar Novo Recrutador: Registra novos recrutadores no sistema.
Recrutador
Login: Acessa a plataforma com um email e senha de recrutador.
Postar Vaga: Adiciona novas vagas de emprego.
Visualizar Candidatos: Visualiza os candidatos cadastrados no sistema.
Candidato
Login: Acessa a plataforma com um email e senha de candidato.
Visualizar Vagas: Visualiza as vagas de emprego disponíveis.
Requisitos
Python 3.7 ou superior.
Bibliotecas Python:
streamlit
pandas
uuid
os
Para instalar as dependências, execute o seguinte comando:

bash
Copy code
pip install streamlit pandas
Como Usar
Clone este repositório ou faça o download dos arquivos.

Execute o seguinte comando para iniciar a aplicação:

bash
Copy code
streamlit run app.py
Na página de login, selecione o tipo de usuário (Admin, Candidato ou Recrutador).

Para Administradores:

Gerencie as vagas, candidatos e recrutadores na plataforma.
Para Recrutadores:

Publique vagas e visualize candidatos.
Para Candidatos:

Visualize as vagas disponíveis e se cadastre para se candidatar.
Estrutura de Arquivos
app.py: Arquivo principal da aplicação Streamlit.
vagas.csv: Banco de dados de vagas de emprego (CSV).
candidatos.csv: Banco de dados de candidatos (CSV).
agentes_rh.csv: Banco de dados de recrutadores (CSV).
Banco de Dados Simulado
A plataforma utiliza arquivos CSV para armazenar dados de candidatos, recrutadores e vagas:

vagas.csv: Contém informações sobre as vagas de emprego.
candidatos.csv: Contém dados dos candidatos cadastrados.
agentes_rh.csv: Contém dados dos recrutadores cadastrados.
Funcionalidades Específicas
Carregar Dados
Quando a aplicação é iniciada, ela carrega os dados de vagas, candidatos e recrutadores a partir dos arquivos CSV.
Caso os arquivos não existam, o sistema começa com um banco de dados vazio.
Autenticação
O sistema possui um processo de autenticação simples. Os Administradores, Recrutadores e Candidatos precisam fornecer um email e uma senha para acessar suas respectivas áreas.
A senha e o email do Administrador estão previamente definidos no código.
Salvamento de Dados
Qualquer modificação nas informações de vagas, candidatos ou recrutadores é salva automaticamente nos arquivos CSV após cada ação (como criar, editar ou excluir).
