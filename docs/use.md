

???+ tip "Início Rápido"
    A API possui uma documentação gerada automaticamente usando o modelo [OpenAPI](https://www.openapis.org/), nele é possível vizualiar de forma estruturada os `endpoints`, ver exemplos de `response`, e testa-los com exemplos pré-definidos.

    [http://localhost:8080/docs](http://localhost:8080/docs)

    O link acima só ira funcionar caso você tenha utilizado a porta padrão da API (`8080`).

---
## **Registar**

Utilize esse endpoint para registrar um novo usuário do serviço.

!!! note "Registro de Usuário"
    
    ``` http title="Endpoint"
    POST /registrar
    ```

    Request
    ``` json title="JSON body"
    {
        "nome": "Aluno Insper",
        "email": "aluno@al.insper.edu.br",
        "senha": "senha_super_segura"
    }
    ```

    Response
    ``` json title="JSON body"
    {
        "jwt": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFsdW5vQGFsLmluc3Blci5lZHUuYnIifQ.YE4QiMzDt8JFPTRPJAmSYD2OG37RrKkoHgH-dcf8nYo"
    }
    ```


???+ info "Campos"

    - **nome**: Seu nome de usuário;
    - **email**: Um e-mail válido que ainda não esteja associado a um usuário do serviço;
    - **senha** Uma senha de pelo menos 6 caracteres;

Além de criar o usuário, será retornado um **token JWT** que deverá ser usado para autenticar suas consultas ao serviço.

???- example "Resultado"
    === "Postman"
        ![Testando Endpoit "/registrar"](./img/registrar.png)

---
## **Login**

Utilize esse endpoint se autenticar como usuário do serviço e receber de volta seu **token JWT**.

!!! note "Autenticação de Usuário"
    
    ``` http title="Endpoint"
    POST /login
    ```

    Request
    ``` json title="JSON body"
    {
        "email": "aluno@al.insper.edu.br",
        "senha": "senha_super_segura"
    }
    ```

    Response
    ``` json title="JSON body"
    {
        "jwt": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFsdW5vQGFsLmluc3Blci5lZHUuYnIifQ.YE4QiMzDt8JFPTRPJAmSYD2OG37RrKkoHgH-dcf8nYo"
    }
    ```

!!! info "Campos"

    - **email**: Um e-mail válido de um usuário já registrado no serviço;
    - **senha** A senha de pelo menos 6 caracteres correspondente ao e-mail;

???- example "Resultado"
    === "Postman"
        ![Testando Endpoit "/login"](./img/login.png)

---
## **Consultar**

A cunsulta ao serviço retorna de 4 a 10 notícias presentes na capa do **G1**. De cada notícia, há as informações: título, link para a notícia, tema e a quanto tempo a publicação ocorreu.

!!! note "Consulta ao Serviço"
    
    ``` http title="Endpoint"
    GET /consultar
    
    HEADER 
    Authorization: Bearer <token JWT>
    ```

    Response
    ``` json title="JSON body"
    [
        {
            "titulo": "Com 760 mil imóveis em SP sem energia 2 dias após temporal, Aneel convoca reunião com Enel e mais 8 empresas",
            "link": "https://g1.globo.com/sp/sao-paulo/noticia/2024/10/13/aneel-convoca-reuniao-com-representantes-da-enel-e-empresas-que-atendem-sp-apos-apagao.ghtml",
            "tema": "São Paulo",
            "tempo_publicacao": "Há 3 horas"
        },
        {
            "titulo": "Mãe e filho mortos atingidos por muro passavam todo dia por rua do acidente",
            "link": "https://g1.globo.com/sp/bauru-marilia/noticia/2024/10/13/rua-onde-mae-e-filho-morreram-atingidos-por-muro-durante-temporal-era-caminho-da-escola-do-garoto-conhecia-bem-esse-trajeto.ghtml",
            "tema": "Bauru e Marília",
            "tempo_publicacao": "Há 18 horas"
        },
        {
            "titulo": "Cão morre após tocar em fio de média tensão que se rompeu com chuva",
            "link": "https://g1.globo.com/sp/sao-paulo/noticia/2024/10/13/cao-morre-apos-tocar-em-fio-de-alta-tensao-e-corpo-segue-mais-de-24-horas-na-rua-com-cabo-energizado-so-queremos-nos-despedir-dizem-tutores.ghtml",
            "tema": "São Paulo",
            "tempo_publicacao": "Há 7 horas"
        },
        {
            "titulo": "g1 promove debates com candidatos a prefeito de 5 cidades da Grande SP",
            "link": "https://g1.globo.com/sp/sao-paulo/eleicoes/2024/noticia/2024/10/11/g1-promove-debates-com-candidatos-a-prefeito-no-2o-turno-das-eleicoes-de-cinco-cidades-da-grande-sp.ghtml",
            "tema": "Eleições 2024 em São Paulo",
            "tempo_publicacao": "Há 7 horas"
        }
    ]
    ```
    ???- example "Resultado"
        === "Postman"
            ![Testando Endpoit "/consultar"](./img/consultar.png)