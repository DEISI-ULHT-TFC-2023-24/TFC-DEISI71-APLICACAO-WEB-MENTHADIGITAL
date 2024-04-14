# MentHA Digital

⚙️ Requisitios
======
1. Python 3.10 ou superior

🔧 Deployment
======
1. Abrir o cmd
2. fazer "git clone https://github.com/MentHA-ULHT/mentha_digital"
3. Fazer cd para o dir onde está o "requirements.txt"
4. Correr o comando "pip install -r requirements.txt"
5. Fazer cd para o dir onde está o manage.py
6. Correr o comando "py manage.py runserver"
7. Abrir http://127.0.0.1:8000/ no browser
8. Fazer login com as credenciais user:"superuser" pw:"super123"

🔌 Sockets
======
(Se o requirements.txt não estiver atualizado)
Se os sockets não estiverem instalados corretamente, quando um dinamizador muda o exercício partilhado, a aplicação não vai ser atualizada no ecrã dos participantes.
Para isso precisamos de uma versão específica do package 'channels'
```
pip install channels==3.0.5
```

## sincronizar servidor 

### com github

1. fazer `git push` para o master no gitHub
2. login no servidor (ver acesso anterior)
3. fazer `git pull`

### à la pate
* para cada pasta aplicação (diario e protocolo) copiar tudo excepto migrations


## re-lançar servidor

4. fazer cd env2, cd bin
5. ativar ambiente virtual: `source activate`
6. atualizar app:
    * `python manage collectstatic`
    * `python manage makemigrations`
    * `python manage migrate`
5. copiar conteudo da pasta "static" (dentro do projeto) para a pasta "static" (fora, junto às pastas do servidor)
6. desantivar ambiente virtual, para voltar ao linux: `deactivate`
7. lançar servidor gunicorn: `sudo systemctl restart gunicorn`
8. para ver possiveis erros:  `sudo systemctl status gunicorn`
9. login a psql com admin da máquina (leda)

## psql 

https://stackoverflow.com/questions/12720967/how-can-i-change-a-postgresql-user-password

manipular base de dados:
* sudo -u postgres psql
* postgres=# create database mydb;
* postgres=# create user myuser with encrypted password 'mypass';
* postgres=# grant all privileges on database mydb to myuser;


🔖 Logs

sudo systemctl status gunicorn



🔖 Passar DB para PSQL
======

1. Se quisermos importar dados da bd antiga em sqlite, temos de exportar a bd em UTF-8, senão vai dar erro de encoding,  para isso fazemos: 
```
python manage.py -Xutf8 dumpdata > <nome_ficheiro>.json
```
2. Instalar psycogpg2 (package adaptador de PostgreSQL para Django)
```
pip install psycopg2
```
3. Editar a variável DATABASES no settings.py para:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': ‘<nome_bd>’,
        'USER': '<username_bd>',
        'PASSWORD': '<password>',
        'HOST': '<ip_bd>',
        'PORT': '<port_bd>',
    }
}
```
4. Como demos expor da bd em UTF-8 vamos ter caracteres estranhos no lugar de de caracteres portuguêses.
5. Para corrigir todos os caracteres errados em todos os modelos da bd, fazemos um dicionario onde metemos como chave o char errado e como valor char correto
6. Para isto usamos tb smart_str() para dar para correr em linux senão vai dar erro de encoding
```
from django.utils.encoding import smart_str

char_map = {
    smart_str("<char_errado>", encoding='utf-8', strings_only=True, errors='strict'): smart_str("<char_correto>", encoding='utf-8', strings_only=True, errors='strict'),
}
```
7. Depois definimos uma função para substituir esses caracteres num texto recebido
```
def replace_chr(text):
    if text is not None:
        smart_txt = smart_str(text, encoding='utf-8', strings_only=True, errors='strict')
        for incorrect_char, correct_char in char_map.items():
            smart_txt = text.replace(incorrect_char, correct_char)
        return smart_txt
    return text 
```
8. Executar o environment e abrir a python shell
```
source bin/activate
python manage.py shell
```
9. Importar o que for necessário (onde está a funçao decode() e executá-la) p.ex, se a funçao estiver no views.py:
```
from mentha.views import * 
decode()
```
