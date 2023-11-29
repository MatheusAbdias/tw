## Autenticação em APIs Restful

- As APIs Restful são stateless, o que significa que cada requisição é independente e não mantém conhecimento do estado anterior ou do próximo passo a ser executado. Essa característica é fundamental para a escalabilidade de aplicações, especialmente quando se lida com milhares de usuários.

- Isso no traz vantagens e desvantagens, muitas requisiões vão precisar de informação do usuário como permissões, controle de acesso entre outros. Sendo assim se faz necessario um metodo de autenticação que identifica exclusivamente cada usuário. Vamos utilizar a estrategia de tokens de acesso chama JWT (JSON Web Tokens) que é comumente difundida atualmente.

## Django Rest Framework simplejwt

- Não vamos implementar JWT do absoluto pois isso foge do objetivo desta aula, então vamos utilizar a lib [Django-Rest-Framework-simplejwt](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/).

- Primeiramente precisamos addincionar a lib utilizando o poetry:

```bash
poetry add djangorestframework-simplejwt
```

- Para utilizar o pacote vamos precisar adicionar o pacote na variavel `INSTALLED_APPS` que fica no settings.py:

```python
INSTALLED_APPS = [
    'rest_framework_simplejwt',
]
```

- Alem disso no objeto REST_FRAMEWOK é necessario adicionar um DEFAULT_AUTHENTICATION_CLASSES

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}
```

- Basicamente é tudo que precisamos fazer para configurar para utilizar o pacote, porem muitos tipos de configurações podem ser feitas, como alterar o algoritimo de hash life time do token entre outros, porem vou manter a configuração padrão, para manter o mais simples possivel.

### [Doumentação](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html#requirements)
