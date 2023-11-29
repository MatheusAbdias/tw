## Introdução ao Django Rest Framewokr

- O Django é um framework para desenvolvimento web, conhecido pelo termo: "All Batteries Included" e isso significa que inclui todos os recursos necessários para acelerar o pontapé inicial no desenvolvimento de um projeto, tais como: integração com banco de dados, validadores, etc.

## Como Iniciar um projeto Django

- Feramentas necessarias:
  - [ ] Python
  - [ ] [Poetry](https://python-poetry.org/docs/#installing-with-the-official-installer)
  - [ ] [Docker](https://docs.docker.com/get-docker/)
- O poetry e o docker são ferramentas opcionais porem elas vão vacilitar muito o processo de desenvolvimento do projeto e durante esse documento eu vou presumir que você utilizando essas duas ferramentas.
- Como python utiliza uma virtualenv para evitar que você tenha que baixar as dependências de seu projeto de forma global esse será nosso primeiro passo. Para que o poetry crie nossa virtalenv no diretorio do projeto, precisamos criar um aquivo de configuração com o nome poetry.toml:

```toml
[virtualenvs]
in-project = true
```

- Para inicializar o poetry:

```bash
poetry init
```

- Ao inicializar você verá que o poetry vai gerar um arquivo pyproject.toml similar a este:

```toml
[tool.poetry]
name = "tw"
version = "0.1.0"
description = ""
authors = ["Matheus Abdias <matheusabdias@b2bit.company>"]
readme = "README.md"

[tool.poetry.dependencies]
python = "^3.11"


[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

- Para executar venv basta rodar:

```bash
poetry shell
```

- Agora adicione as duas dependências iniciais do projeto:

```bash
poetry add django
poetry add djangorestframework
```

- Ao adicionar as dependências você poderá ver que foi gerado um arquivo poetry.lock e no nosso pyproject.toml terá as nossas duas novas dependências:

```toml
[tool.poetry]
name = "tw"
version = "0.1.0"
description = ""
authors = ["Matheus Abdias <matheusabdias@b2bit.company>"]
readme = "README.md"

[tool.poetry.dependencies]
python = "^3.11"
django = "^4.2.7"
djangorestframework = "^3.14.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

- Agora finalmente podemos criar nosso projeto:

```bash
django-admin startproject {PROJECT_NAME} .
```

- O django vai gerar para você uma estrutura de projeto idêntica a esta:

```
PROJECT_NAME/
  __init__.py
  asgi.py
  settings.py
  urls.py
  wsgi.py
manage.py
```

- Sobre os arquivos gerados pelo django:
  - asgi.py e wsgi.py: são utilizadas no deploy de seu projeto para tornar sua API acessível.
  - settings.py: neste arquivo será onde todo tipo de configuração relacionada ao seu projeto deve estar. Exemplos: configuração de banco de dados, autenticação,etc.
- Hora de ver o resultado! Para isso basta executar:

```bash
./manage.py runserver
```

- Ao executar este comando a aplicação será inicializada e você receberá um output similar a este:
  ![Console output](https://back-end-master-class-assets.s3.amazonaws.com/Pasted+image+20231108224448.png)
- Mal começamos e já temos um mensagem de erro, mas, por enquanto vamos ignorá-lo. Ao abrir o link no navegador você verá uma tela como esta:
  ![Django](https://back-end-master-class-assets.s3.amazonaws.com/Pasted+image+20231108224828.png)
- Hora de arrumar os erros. Primeiramente, é importante entender o que o erro está nos informando: foi dito que há 18 migrações não aplicadas e que devemos rodar o comando:
  ```bash
  ./manage.py migrate
  ```
- Ao rodar o comando e iniciar a aplicação novamente poderemos ver que os erros sumiram e que temos agora um arquivo em nosso diretório raiz com o nome db.sqlite3. Por padrão o django vem configurado para utilizar o banco de dados sqlite3 como podemos ver no arquivo settings.py:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

- As migrações são uma forma de versionamento do seu banco de dados para evitar inconsistência de dados ou para se caso uma mudaça precise ser revertida basta apenas reverter a migrate necessária. No django, as migrações são geradas utilizando o seguinte comando:

```bash
./manage.py makemigrations
```

- E são aplicadas utilizando este comando:

```bash
./manage.py migrate
```

## Execicios

- Integração com banco de dados postgres.
- Cadastro de usuário
  - Como um usuário, quero poder fazer meu cadastro para que eu possa ter acesso ao login.
- [Introdução ao Docker Compose](extra_docker.md)
- [Resolução](exercise.md)
