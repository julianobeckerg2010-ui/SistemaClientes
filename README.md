# Gestão Fácil — Sistema Web de Cadastro de Clientes

Aplicação Flask com HTML, CSS, JavaScript e SQLite para cadastrar, consultar, buscar, editar e excluir clientes.

## Rodar no Windows (PowerShell)

```powershell
cd sistema-clientes
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Abra http://127.0.0.1:5000

Se o PowerShell bloquear a ativação, use diretamente ` .\.venv\Scripts\python.exe -m pip install -r requirements.txt ` e ` .\.venv\Scripts\python.exe app.py `.

## Testes

```powershell
python -m pytest -q
```

## Publicar no Render

1. Crie um repositório no GitHub e envie **os arquivos de dentro desta pasta**.
2. No Render, crie um **New > Web Service** e conecte o repositório.
3. Use ambiente Python, build command `pip install -r requirements.txt` e start command `gunicorn app:app`.
4. Crie a variável `SECRET_KEY` com um valor aleatório forte. O arquivo `render.yaml` também permite criar um Blueprint com essas configurações.
5. Aguarde o deploy e abra o endereço `.onrender.com` fornecido pelo Render.

**ATENÇÃO: Persistência de dados.** No plano gratuito do Render, o sistema de arquivos é efêmero. O banco SQLite local pode ser apagado em reinícios/redeploys. Para uso real com dados duráveis, use um disco persistente (plano compatível) com `DATABASE_PATH=/var/data/clientes.db`, ou migre para PostgreSQL. SQLite também não é ideal para várias instâncias simultâneas.

**Segurança:** aplicação didática, sem login de usuários. Não cadastre dados pessoais reais em uma instância pública sem adicionar autenticação, proteção CSRF, HTTPS e controles adequados.
