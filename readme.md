# SCTeste

API em Python/Flask com exemplos de autentica��o JWT e organiza��o de acessos em Blueprints, atrav�s de uma simula��o de servi�o financeiro.

## Installation

### Pacotes
Crie uma ambiente virtual (venv) e instale todos os pacotes que est�o listados em **"requirements.txt"**

```bash
pip install -r requirements.txt
```

### Base de dados - Sqlite

#### Caso os arquivos de banco n�o estejam na pasta do projeto, siga os seguintes passos:

Execute os scripts **systemA.db.sql, systemB.db.sql, systemC.db.sql,** contidos na pasta **"testes"** em seu gerenciador de banco sqlite.

Salve os arquivos de banco na pasta de raiz da aplica��o.

Recomendo utilizar o [DB Broser fo SQLite](https://sqlitebrowser.org/dl/) 
##### Caso deseje alterar o banco de dados para rodar os testes � necess�rio adaptar o fonte para o novo tipo de conex�o.



## Aplica��o

### Primeira execu��o

Esse bloco de c�digo contido no **"main.py"** devera ser executado somente a primeira vez que a aplica��o rodar na maquina, ou quando o arquivo **"developer.db"** n�o existe na pasta raiz do projeto.

Esse bloco � respons�vel por criar as credenciais para teste da aplica��o.

```python
# *********************** Warning ******************
# Use only on the promised execution
# Creates test users
# **************************************************

from database import init_db, db_session
from models.auth.User import User
@app.before_first_request
def create_user():
    init_db()
    user1 = User(email='user1@user.com',
                 password= bcrypt.generate_password_hash('senha'),
                 name='Usuario 1',
                 username='user1')
    user2 = User(email='user2@user.com',
                 password= bcrypt.generate_password_hash('senha2'),
                 name='Usuario 2',
                 username='user2')
    db_session.add_all([user1, user2])

    db_session.commit()

```

Apos o a primeira execu��o o bloco de c�digo pode ser comentado.

### Testes

Para testar a aplica��o existe arquivos dentro da pasta "teste"

#### Arquivo - requests.txt

Esse arquivo possui o modelo e a url b�sica para cada requisi��o da aplica��o.

Substitua %____% pelas informa��es pertinentes.  
###### Login
http://%endere�o da API%/auth/login  
{"username":%usuario%,"password":%senha%}

###### SystemA
http://%endere�o da API%/systema/consultadividacpf  
{"cpf":%numero do CPF%}

###### SystemB
http://%endere�o da API%/systemb/scorecreditocpf  
{"cpf":%numero do CPF%}

###### SystemC
http://%endere�o da API%/systemc/eventoscpf  
{"cpf":%numero do CPF%}

#### Arquivo - SCTeste.postman_collection.json

Esse arquivo � o projeto de teste para ser utilizado no programa [Postman](https://www.getpostman.com/).