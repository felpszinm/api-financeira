
FROM python:3.12.11-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /usr/src/app

# Vaviáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copia o arquivo de requisitos para o contêiner e instala as dependências.
# Fazer isso primeiro aproveita o cache do Docker.
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do seu código para o contêiner.
# O ponto '.' significa 'todo o resto do projeto'.
COPY . /usr/src/app

# Expõe a porta que sua aplicação vai usar.
EXPOSE 8000