### LEIA-ME ###

## Métodos já criados ##

*Users*
-> Coletar info. Usuario (GET)
-> Coletar info todos os users (GET)
-> Criação de Usuario (POST)
-> Deletar um usuário (DELETE)

*Transactions*
-> Coletar todas as transações (GET)
-> Coletar transações de um Usuario (GET)
-> Criação de Transação (POST)
-> Exclusão de uma transação de um Usuario (DELETE)

*Categories*
-> Coletar todas as categorias (GET)
-> Criação de uma categoria (POST)
-> Exclusão de uma categoria (DELETE)


## Métodos para se criar ##

*Users*
-> Atualizar as informações de um usuário (PUT)

*Transactions*
-> Atualizar uma transação de um usuário (PUT)

*Categories*
-> Atualizar uma categoria (PUT)

## Novas classes a se adicionar ##

*Categories*
-> Criar uma tabela no banco para que cada transação possa ser classificada
Exemplos: Alimentação, Transporte, Moradia, Lazer, Salário
-> Faça CRUD nela

*Accounts*
-> Criar uma tabela de contas bancárias / carteiras.
-> Onde cada nova transação sera vinculada a essa conta.
-> Usuario também pode ter saldos separados.

## Oportunidades de Melhoria ##

>> Implementar a função PUT/PATCH (Update):
-> adicionar os endpoints PUT (substituição completa) ou PATCH (atualização parcial) para 'User', 'Transaction' e 'Category'.

>> Melhorar a função delete_category:
-> usar o *ON DELETE CASCADE* na definição da Foreign Key no SQLAlchemy para deletar as transações ligadas automaticamente ou bloquear a exclusão
se houver transações vinculadas.

>> Ajustar Status Codes (Tirar a função de raise_http_exception):
-> Usar os IFS diretamente nos raise HTTPException.
-> Métodos POST devem retornar = status.HTTP_201_CREATED
-> Métodos DELETE devem retornar = status.HTTP_204_NO_CONTENT

>> Filtragem e Paginação nas TRANSACTIONS:
-> Adicionar parâmetros de consulta (*query parameters*) para *skip, limit* (para paginação) e filtragem para data ou valor.
