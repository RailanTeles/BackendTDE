# 🏥 Sistema Backend para Gestão de Clínicas

## Descrição do Projeto
Este projeto consiste no desenvolvimento de uma **API backend** para gestão de clínicas, utilizando **Python**, com **banco de dados relacional** para persistência das informações.  
O sistema foi construído seguindo os princípios da **programação orientada a objetos** e o padrão **MVC (Model-View-Controller)**, focando nas camadas de **model, controller e serviços**.  

Todos os dados trafegados no sistema utilizam o formato **JSON**, incluindo a autenticação via **token JWT**.  

## Objetivos
- Permitir ao aluno explorar aspectos da **programação orientada a serviços (backend)**.  
- Implementar endpoints seguros, garantindo que **todos os endpoints, exceto login, exijam autenticação**.  
- Desenvolver funcionalidades com **paginação em disco** para todos os endpoints que retornam listas de objetos.  
- Parametrizar o acesso ao banco de dados por **variáveis de ambiente**, sem utilizar informações hardcoded (URL, usuário, senha, nome do banco).  

## Tecnologias Utilizadas
- Linguagens: **Python**  
- Banco de dados: **SQLite** 
- Autenticação: **JWT**  
- Formato de dados: **JSON**  

## Cenário do Sistema
O sistema backend é responsável por gerenciar dados de clínicas, incluindo usuários, pacientes, atendimentos e procedimentos.  
A API disponibiliza **endpoints seguros e paginados**, permitindo que apenas usuários autenticados acessem os recursos, garantindo escalabilidade e segurança da aplicação.


# 📌 API Usuários

description: >
  API para gerenciamento de usuários com autenticação via token JWT.
  Todos os endpoints estão sob o prefixo /api/v1/usuarios.

authentication: >
  Todos os endpoints (exceto login) exigem envio de token JWT no header:
  Authorization: Bearer <token>

endpoints:
  - method: POST
    route: /login
    description: Login com email e senha, retorna token JWT
    access: Público
    request_example: |
      {
        "email": "example@gmail.com",
        "senha": "senha123"
      }
  
  - method: GET
    route: /<email>
    description: Retorna dados de um usuário específico
    access: Próprio usuário ou Admin
    request_example: |
      GET /api/v1/usuarios/example@gmail.com
      Authorization: Bearer <token>

  - method: GET
    route: /
    description: Lista usuários de forma paginada (query params: pagina, itensPorPagina)
    access: Admin
    request_example: |
      GET /api/v1/usuarios?pagina=1&itensPorPagina=5
      Authorization: Bearer <token>

  - method: POST
    route: /adicionar
    description: Adiciona um novo usuário (email, nome, tipo)
    access: Admin
    request_example: |
      {
        "email": "example@gmail.com",
        "nome": "example123",
        "tipo": "admin"
      }

  - method: PUT
    route: /editar
    description: Edita os próprios dados (email, nome)
    access: Usuário
    request_example: |
      {
        "email": "novoExample@gmail.com",
        "nome": "example1234"
      }

  - method: PUT
    route: /alterarSenha
    description: Usuário altera a própria senha (senha, novaSenha)
    access: Usuário
    request_example: |
      {
        "senha": "example123",
        "novaSenha": "example12345"
      }

  - method: PUT
    route: /resetarSenha
    description: Admin reseta senha de outro usuário pelo email
    access: Admin
    request_example: |
      {
        "email": "novoExample@gmail.com"
      }

  - method: DELETE
    route: /deletar
    description: Remove usuário (se não possuir atendimentos vinculados)
    access: Admin
    request_example: |
      {
        "email": "novoExample@gmail.com"
      }

notes: >
  - Apenas admins podem:
    - Obter dados de qualquer usuário pelo email
    - Adicionar, resetar senha ou deletar usuários
  - Caso não sejam informados, os valores padrão para paginação são:
    - pagina = 1
    - itensPorPagina = 2
