
# CRUD Flask (nomeId, nome, e-mail) com DB em memória e Docker

Este projeto implementa um CRUD simples em Flask com interface web (Bootstrap) para gerenciar pessoas com os campos **nomeId**, **nome** e **e-mail**. O banco de dados é **em memória** (SQLite `:memory:`), ou seja, os dados são armazenados somente durante a execução do processo/container.

## Como executar localmente

```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
# Acesse http://127.0.0.1:5000
```

## Como executar com Docker

```bash
# Build da imagem
docker build -t flask-crud:latest .

# Executar o container
docker run --rm -p 5000:5000 flask-crud:latest
# Acesse http://localhost:5000
```

> Observação: como o banco é em memória, todos os dados serão perdidos ao reiniciar a aplicação ou o container. Se desejar persistir, troque a string de conexão em `app.config['SQLALCHEMY_DATABASE_URI']` para um arquivo local (ex.: `sqlite:///data.db`) e remova a lógica de in-memory.
