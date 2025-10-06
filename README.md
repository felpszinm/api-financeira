# API de Controle Financeiro

Esta é uma API RESTful robusta para gerenciamento financeiro, construída com Python, FastAPI e SQLAlchemy. A API permite o controle de usuários, transações e categorias, fornecendo uma base sólida para o desenvolvimento de aplicações financeiras completas.

## Funcionalidades

- **Gerenciamento de Usuários:**
  - Criar, ler, atualizar e deletar usuários.
  - Buscar usuários por ID ou e-mail.
- **Gerenciamento de Transações:**
  - Registrar novas transações (receitas e despesas).
  - Listar todas as transações de um usuário específico.
  - Obter detalhes de uma transação específica.
  - Atualizar e deletar transações.
- **Gerenciamento de Categorias:**
  - Criar, ler, atualizar e deletar categorias para organizar as transações.

## Tecnologias Utilizadas

- **Python 3.12**
- **FastAPI:** Framework web de alta performance para construção de APIs.
- **SQLAlchemy:** ORM para interação com o banco de dados.
- **Pydantic:** Para validação de dados e schemas.
- **PostgreSQL:** Banco de dados relacional.
- **Docker & Docker Compose:** Para containerização e orquestração da aplicação e do banco de dados.
- **Uvicorn:** Servidor ASGI para rodar a aplicação FastAPI.

## Arquitetura do Projeto

A API segue uma arquitetura limpa e modular, separando as responsabilidades em diferentes componentes:

- `main.py`: Ponto de entrada da aplicação, onde os endpoints da API são definidos.
- `crud.py`: Contém as funções que realizam as operações de Create, Read, Update e Delete no banco de dados.
- `models.py`: Define os modelos de dados do SQLAlchemy, que representam as tabelas do banco de dados.
- `schemas.py`: Define os schemas do Pydantic, que são usados para validação de dados de entrada e saída da API.
- `database.py`: Gerencia a conexão com o banco de dados e as sessões.

## Como Começar

Siga os passos abaixo para configurar e rodar a aplicação em seu ambiente local.

### Pré-requisitos

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Instalação e Execução

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/api-gerenciamento-financeiro.git
   cd api-gerenciamento-financeiro
   ```

2. **Configure as variáveis de ambiente:**
   Crie um arquivo `.env` na raiz do projeto, baseado no `docker-compose.yml`. Este arquivo não está presente no repositório por questões de segurança.

   ```
   DATABASE_URL=postgresql://postgres:apikey123@db:5432/api_financeira
   ```

3. **Inicie a aplicação com Docker Compose:**
   ```bash
   docker-compose up --build
   ```

   A API estará disponível em `http://localhost:8002`.

4. **Acesse a documentação interativa:**
   A documentação da API, gerada automaticamente pelo FastAPI, pode ser acessada em:
   - **Swagger UI:** `http://localhost:8002/docs`
   - **ReDoc:** `http://localhost:8002/redoc`

## Endpoints da API

A seguir, uma descrição detalhada dos endpoints disponíveis.

### Usuários

| Método | Endpoint                  | Descrição                               |
|--------|---------------------------|-----------------------------------------|
| GET    | `/api/users/`             | Lista todos os usuários.                |
| GET    | `/api/users/{user_id}/`   | Obtém um usuário específico por ID.     |
| GET    | `/api/users/by_email/`    | Obtém um usuário específico por e-mail. |
| POST   | `/api/users/`             | Cria um novo usuário.                   |
| PATCH  | `/api/users/{user_id}/`   | Atualiza um usuário existente.          |
| DELETE | `/api/users/{user_id}/`   | Deleta um usuário.                      |

**Exemplo de corpo para POST:**
```json
{
  "name": "Felipe Santos",
  "email": "felipe.santos@example.com"
}
```

### Transações

| Método | Endpoint                                              | Descrição                                     |
|--------|-------------------------------------------------------|-----------------------------------------------|
| GET    | `/api/users/{user_id}/transactions/`                  | Lista todas as transações de um usuário.      |
| GET    | `/api/users/{user_id}/transactions/{transaction_id}/` | Obtém uma transação específica de um usuário. |
| POST   | `/api/users/{user_id}/transactions/`                  | Cria uma nova transação para um usuário.      |
| PATCH  | `/api/users/{user_id}/transactions/{transaction_id}/` | Atualiza uma transação de um usuário.         |
| DELETE | `/api/users/{user_id}/transactions/{transaction_id}/` | Deleta uma transação de um usuário.           |

**Exemplo de corpo para POST:**
```json
{
  "description": "Salário",
  "amount": 5000.00,
  "category_id": 1
}
```

### Categorias

| Método | Endpoint                  | Descrição                               |
|--------|---------------------------|-----------------------------------------|
| GET    | `/api/categories/`        | Lista todas as categorias.              |
| GET    | `/api/categories/{category_id}/` | Obtém uma categoria específica por ID.  |
| POST   | `/api/categories/`        | Cria uma nova categoria.                |
| PATCH  | `/api/categories/{category_id}/` | Atualiza uma categoria existente.       |
| DELETE | `/api/categories/{category_id}/` | Deleta uma categoria.                   |

**Exemplo de corpo para POST:**
```json
{
  "name": "Salário"
}
```

## Ambiente de Desenvolvimento

Este projeto inclui uma configuração de [Dev Container](https://code.visualstudio.com/docs/remote/containers), que permite um ambiente de desenvolvimento consistente e isolado. Para utilizá-lo, abra o projeto no VS Code com a extensão [Remote - Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) instalada e execute o comando `Reopen in Container`.

## Testes

Os testes para esta API ainda não foram implementados. No entanto, a estrutura para os testes está pronta e pode ser encontrada no diretório `src/tests/`. Para executar os testes (quando implementados), utilize o Pytest:

```bash
pytest
```

---
## Próximos Passos e Melhorias

- **Segurança:** Implementar autenticação e autorização com OAuth2 e JWT.
- **Contas:** Adicionar a funcionalidade de contas bancárias/carteiras.
- **Testes:** Implementar testes de unidade e integração para garantir a qualidade e a estabilidade da API.
- **Paginação e Filtros:** Adicionar paginação e filtros avançados para as listagens de transações.
- **Qualidade de Código:** Configurar ferramentas de linting e formatação como Black e Flake8.

