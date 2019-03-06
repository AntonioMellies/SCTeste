# SCTeste

API em Python/Flask com exemplos de autenticação JWT e organização de acessos em Blueprints, através de uma simulação de serviço financeiro.

## Installation

### Pacotes
Crie uma ambiente virtual (venv) e instale todos os pacotes que estão listados em **"requirements.txt"**

```bash
pip install -r requirements.txt
```

### Base de dados - Sqlite

#### Caso os arquivos de banco não estejam na pasta do projeto, siga os seguintes passos:

Execute os scripts **systemA.db.sql, systemB.db.sql, systemC.db.sql,** contidos na pasta **"testes"** em seu gerenciador de banco sqlite.

Salve os arquivos de banco na pasta de raiz da aplicação.

Recomendo utilizar o [DB Broser fo SQLite](https://sqlitebrowser.org/dl/) 
##### Caso deseje alterar o banco de dados para rodar os testes é necessário adaptar o fonte para o novo tipo de conexão.



## Aplicação

### Primeira execução

Esse bloco de código contido no **"main.py"** devera ser executado somente a primeira vez que a aplicação rodar na maquina, ou quando o arquivo **"developer.db"** não existe na pasta raiz do projeto.

Esse bloco é responsável por criar as credenciais para teste da aplicação.

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

Apos o a primeira execução o bloco de código pode ser comentado.

### Testes

Para testar a aplicação existe arquivos dentro da pasta "teste"

#### Arquivo - requests.txt

Esse arquivo possui o modelo e a url básica para cada requisição da aplicação.

Substitua %____% pelas informações pertinentes.  
###### Login
http://%endereço da API%/auth/login  
{"username":%usuario%,"password":%senha%}

###### SystemA
http://%endereço da API%/systema/consultadividacpf  
{"cpf":%numero do CPF%}

###### SystemB
http://%endereço da API%/systemb/scorecreditocpf  
{"cpf":%numero do CPF%}

###### SystemC
http://%endereço da API%/systemc/eventoscpf  
{"cpf":%numero do CPF%}

#### Arquivo - SCTeste.postman_collection.json

Esse arquivo é o projeto de teste para ser utilizado no programa [Postman](https://www.getpostman.com/).