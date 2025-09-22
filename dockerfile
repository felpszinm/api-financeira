# Usa uma imagem Python leve como base.
# 'slim' significa que ela tem apenas o necessário, resultando em um tamanho menor.
FROM python:3.12.11-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia o arquivo de requisitos para o contêiner e instala as dependências.
# Fazer isso primeiro aproveita o cache do Docker.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do seu código para o contêiner.
# O ponto '.' significa 'todo o resto do projeto'.
COPY . .

# Expõe a porta que sua aplicação vai usar.
EXPOSE 8000

# Define o comando que será executado quando o contêiner iniciar.
# O '--host 0.0.0.0' garante que a API seja acessível de fora do contêiner.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]