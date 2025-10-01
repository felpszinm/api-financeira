### LEIA-ME ###

## Métodos já criados ##

*Users*
-> Coletar info. Usuario (GET)✅
-> Coletar info todos os users (GET)✅
-> Criação de Usuario (POST)✅
-> Atualizar Usuario (PATCH)✅
-> Deletar um usuário (DELETE)✅

*Transactions*
-> Coletar todas as transações (GET)✅
-> Coletar transações de um Usuario (GET)✅
-> Criação de Transação (POST)✅
-> Atualizar Transação de um usuário (PATCH)✅
-> Exclusão de uma transação de um Usuario (DELETE)✅

*Categories*
-> Coletar todas as categorias (GET)✅
-> Criação de uma categoria (POST)✅
-> Atualizar uma Categoria (PATCH)✅
-> Exclusão de uma categoria (DELETE)✅

*Métodos do Código*
-> *ON DELETE CASCADE* na definição da Foreign Key no SQLAlchemy para deletar as transações ligadas automaticamente ou bloquear a exclusão✅
-> Ajustar Status Codes (Tirar a função de raise_http_exception) ✅

---

## 🎯 Roteiro de Desenvolvimento e Prioridades

Este é o plano de ação para elevar a API ao nível profissional, categorizado por prioridade de implementação.

### 🥇 Prioridade Alta (Essencial para Produção e Estabilidade)

Foco em **Segurança, Testes e Arquitetura** base, garantindo que o sistema seja confiável e robusto.

1.  **Segurança da Autenticação:** Implementar **OAuth 2.0 / JWT Bearer Token** para proteger *todas* as rotas de dados sensíveis.
2.  **Arquitetura Profissional:** Finalizar a separação da lógica em camadas: **Serviços** (lógica de negócio) e **Repositórios** (acesso ao DB), usando a Injeção de Dependência do FastAPI.
3.  **Testes de Integração:** Implementar o `TestClient` do FastAPI para testar **100% das rotas** principais (CRUD de Usuário e Transação).
4.  **Tratamento de Erros:** Criar *handlers* globais para capturar e padronizar as respostas de erro HTTP (e.g., `404 Not Found`, `401 Unauthorized`).

### 🥈 Prioridade Média (Novas Funcionalidades e Regras de Negócio)

Foco em adicionar os recursos necessários para um aplicativo financeiro real.

1.  **[Novo] Classe e Tabela `Accounts`:** Criar o modelo e a estrutura de dados para **Contas Bancárias/Carteiras** (ex: Saldo Separado).
2.  **[Novo] Vínculo de Transações:** Modificar o modelo `Transaction` para vincular obrigatoriamente a uma **Conta** específica (Chave Estrangeira).
3.  **Regra de Saldo e Consistência:** Implementar a lógica de cálculo de **saldo atual** por conta e a validação para evitar transações de despesa (`EXPENSE`) que gerem saldo negativo (se for a regra de negócio).
4.  **Testes de Unidade:** Escrever testes Pytest para a **lógica de Serviço/Negócio** (cálculos financeiros, validação de saldo), utilizando *Mocks*.

### 🥉 Prioridade Baixa (Melhorias de UX/DX e Refinamento)

Foco em usabilidade da API (Developer Experience) e qualidade de código.

1.  **[Melhoria] Paginação:** Adicionar **Query Parameters** (`skip` e `limit`) às rotas de listagem de Transações.
2.  **[Melhoria] Filtragem Avançada:** Adicionar **Query Parameters** para filtrar `Transactions` por **intervalo de datas** e **valor**.
3.  **Qualidade de Código:** Configurar **Black** (formatação) e **Flake8/Pylint** (análise estática) para garantir a consistência e padrões de código.
4.  **Rate Limiting:** Implementar um mecanismo de limite de requisições por IP/Usuário para evitar *Brute Force* e *DDoS*.

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python
* **Framework:** FastAPI
* **Testes:** Pytest, unittest.mock
* **ORM:** SQLAlchemy
* **Banco de Dados:** PostgreSQL

## 🧪 Rodando os Testes

# Rodar todos os testes com relatório de cobertura
pytest --cov=./ --cov-report=html