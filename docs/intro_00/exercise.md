- O Django segue um padrão chamado **Model-View-Controller (MVC)**, mas na verdade, a implementação do Django é mais próxima do **Model-View-Template (MVT)**. No MVT, o controlador é substituído pelo "Template", que lida com a lógica de apresentação, enquanto o Django lida automaticamente com o controle por meio de suas views.
- **Model (Modelo):** Esta entidade é responsável por se comunicar com o banco de dados. Os modelos no Django representam as tabelas do banco de dados e são usados para interagir com os dados.
- **View (Visão):** A visão no Django representa a lógica de apresentação. As views são responsáveis por processar as requisições HTTP e retornar as respostas adequadas.
- **Template (Modelo de Apresentação):** Os templates no Django são responsáveis por gerar a apresentação final que será enviada ao usuário. Eles incluem marcação HTML com incorporação de tags e expressões Python para tornar a apresentação dinâmica.

### Definindo nosso modelo de usuário

```python
class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts.",
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
```

- Para evitar retrabalho, vamos herdar de `AbstractBaseUser` e `PermissionsMixin`. Essas duas classes nos auxiliarão na gestão da autenticação futura e nas permissões do Django admin.
- Ao realizar o login, utilizaremos o campo de email definido no modelo, que foi configurado como único.
- `is_staff` é um campo destinado ao Django admin; ele determina quais usuários podem efetuar login no Django admin.
- `is_active` é utilizado para desativar o usuário; quando este campo está definido como False, o usuário não conseguirá mais realizar login na aplicação.
- `date_joined` é um campo que armazena a data de registro do usuário. Por esse motivo, definimos um valor padrão como `timezone.now`.
- `USERNAME_FIELD` é uma variável que define qual dos campos será utilizado no login do usuário.
- `REQUIRED_FIELDS` determina quais campos precisam ser preenchidos, excluindo `USERNAME_FIELD` e a senha.
- Por fim, `objects` armazena o gerenciador (manager) desse modelo. A função real de um gerenciador ficará mais clara à medida que formos utilizando-o.

### Settings

- Para utilizar um modelo personalizado de usuário, é necessário definir a variável `AUTH_USER_MODEL` no arquivo de `settings.py`:

```python
AUTH_USER_MODEL = "{NOME_DO_APP}.{NOME_DO_MODELO}"
```

### Serializadores

- É onde definimos nossas regras de negócio para os campos:

```python
class SignupUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128, write_only=True)

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def validate_email(self, email: str):
        return User.validate_email(email)

    def validate_username(self, username: str):
        return User.validate_username(username)

```

- Neste serializer, definimos os campos `email`, `username` e `password`, que são os campos necessários para registrar um usuário em nossa aplicação
- O serializer segue o padrão de validar os dados chamando um metodo chamada `validate_{NOME_DO_CAMPO}`. Neste serializer, para exemplificar como funciona a validação de regras de negócio, adicionei duas validações, uma para o `email` e outra para o `username`.
- `validate_email`: Como definimos o campo de email como único no banco, é interessante validar no serializer se já existe algum usuário cadastrado com aquele email. Para isso, precisamos executar uma busca no banco em busca de outro usuário com aquele `email`.

```python
  class EmailAlreadyExistsError(ValidationError):
    default_detail = _("A user with that email already exists.")
    default_code = "email_already_exists"

@classmethod
    def validate_email(cls, email: str):
        email = cls.objects.normalize_email(email).lower()
        if cls.objects.filter(email=email).exists():
            raise cls.EmailAlreadyExistsError

        return email

```

- Na maioria das vezes, no Django, não é necessário escrever SQL, pois, como foi citado anteriormente, o framework foi pensado para facilitar nossa vida e acelerar o processo de desenvolvimento. Sendo assim, utilizamos o ORM do Django para realizar a query.
- Basicamente, formatamos o `email` para realizar a busca utilizando os dados como estão no banco.

```python
email = cls.objects.normalize_email(email).lower()
```

- E execultamos a query buscando por aquele campo:

```python
 cls.objects.filter(email=email).exists():
```

- Nesta query, estamos executando um filtro na tabela de usuários procurando se existe algum usuário com aquele `email`, e por fim, se caso existir, levantamos um erro avisando para o serializer que um usuário com aquele `email` já existe, fazendo assim o cliente receber um erro HTTP 400, com a mensagem de erro que foi definida."

### Views

```python
class SignupViewSet(CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = SignupUserSerializer
    permission_classes = [AllowAny]

```

- "Existem vários tipos de view no Django Rest. Para mais detalhes, consulte a [Documentação de Views](https://www.django-rest-framework.org/tutorial/quickstart/#views). Mas para esse cadastro, podemos utilizar o tipo mais básico dela, que seria `viewsets.GenericViewSet` com o mixin de criação.

```python
class SignupViewSet(CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = SignupUserSerializer
    permission_classes = [AllowAny]
```

- Basicamente, `viewsets.GenericViewSet` é o `viewset` mais simples do Django Rest e nela podemos adicionar métodos como `create`, `update`, `list`, `destroy`, `retrieve` e `partial_update`. Novamente, o Django, para facilitar nossa vida, tem um tipo de viewset com todos esses métodos já implementados chamado `ModelViewSet`. No entanto, para nosso caso, não é necessário, pois é apenas um cadastro. Então, para isso, vamos adicionar um dos mixins do `ModelViewSet` chamado `CreateModelMixin`.

```python
class CreateModelMixin:
    """
    Create a model instance.
    """
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}
```

- Como foi explicado anteriormente, o trabalho da view é direcionar os dados. Observando essa implementação, vemos que tudo que o mixin faz é passar os dados para o serializer que definimos na view, nesse nosso caso seria: `serializer_class = SignupUserSerializer`. Após passar os dados para o serializer, a view chama o método do serializer para validar os dados e por fim, realizar a criação da instância.

#### View Permission

- Na view, também é onde lidamos com as permissões do usuário. Definimos isso no campo `permission_classes`. Como nosso método é um cadastro (signup), não faz sentido ter algum tipo de limitação nesta view. Portanto, definimos nossos `permission_classes` como `AllowAny`.

#### Urls

- Por fim, para nossa view poder receber as requisições de nossos usuários, é necessário criar um roteamento para ela. Existem muitas formas de fazer isso, porém, como estamos utilizando um viewset, existe uma forma simples de fazer, que é criando um arquivo `urls.py`.

```python
app_name = "authentication"

router = routers.DefaultRouter()
router.register("signup", SignupViewSet, basename="signup")

urlpatterns = [path("", include(router.urls))]

```

- Neste arquivo, definimos qual é o app do Django ao qual pertence aquele roteamento e quais views aquele app tem. Nesse nosso caso, o app se chama `authentication` e temos apenas uma view de signup.
- Por fim, adicionamos esse arquivo de roteamento do app no arquivo de roteamento do projeto, que é o `urls.py` que fica no app Django que tem o nome do seu projeto.

```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("authentication.urls", namespace="authentication")),
]
```

## **Autenticação (Login)**

- O usuário deve ser autenticado no sistema através de um Token JWT. Como usuário, ele deve poder fazer login para ter acesso ao sistema. Este token deve ter uma data de expiração.

## **Fazer uma publicação**

- O usuário deve poder criar um post. Esta publicação é persistida no sistema. Como usuário, ele deve poder criar uma publicação para que possa ser vista por outros usuários do sistema.
