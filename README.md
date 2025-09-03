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
