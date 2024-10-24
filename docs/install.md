
---
## **Pré-Requisitos**

Para a instalação da aplicação é necessário a intalação do [Docker](https://docs.docker.com/engine/install/). Também é necessário possuir um arquivo `compose.yaml` com as informações abaixo. Caso queira, você pode baixa-lo por esse [link](https://alinsperedu-my.sharepoint.com/:u:/g/personal/rafaeldbo_al_insper_edu_br/EZfWwkgEXfFMkuFo3k7owHkB7EJIMdCWln_UM4_A1WthVQ?e=glbhfu):
???- note "Arquivo Compose"
    ``` yaml title="compose.yaml"
    name: scraping-api

    services:

    web:
        image: rafaeldbo/scraping-api:latest
        ports:
            - ${WEB_PORT:-8080}:8080
        depends_on:
            - db
        environment:
            DATABASE_URL: postgresql+psycopg2://${POSTGRES_USER:-cloud}:${POSTGRES_PASSWORD:-cloudpassword}@db:${DB_PORT:-5430}/${DB_NAME:-cloud}
            SECRET_KEY: ${SECRET_KEY:-cloudkey}

    db:
        image: postgres:latest
        volumes:
            - postgres_data:/var/lib/postgresql/data/
        command: 
            - -p ${DB_PORT:-5430}
        environment:
            POSTGRES_USER: ${POSTGRES_USER:-cloud}
            POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-cloudpassword}

    volumes:
        postgres_data: 
    ```

## **Instalação Rápida**

Com os pré-requisitos atendidos siga os passos abaixo:

!!! info "Intalação"
    No terminal, no mesmo diretório em que está o arquivo `compose.yaml`, execute:
    ``` shell title="compose"
    docker compose up -d
    ```

!!! info "Customizando"
    É possível customizar o banco de dados, as portas de acesso, assim como a assinatura dos token JWT, por meio da criação de um arquivo `.env` como o abaixo:
    ``` yaml title=".env"
    POSTGRES_USER = "cloud"               # Usuário do Banco de dados
    POSTGRES_PASSWORD = "cloudpassword"   # Senha do Banco de dados
    DB_PORT = 5432                        # Porta de conexão do Banco de dados
    DB_NAME = "cloud"                     # Nome do Banco de dados
    WEB_PORT = 8080                       # Porta de conexão da API
    SECRET_KEY = "cloudkey"               # Assinatura dos token JWT
    ```
    Também é possível alterar o funcionamento da API criando sua própria versão do codígo fonte. Para isso, será necessário possuir o [Git](https://git-scm.com/downloads) para acessar o repositório da API.
    Com o Git instalado, além do Docker é claro, execute:
    ``` shell title="Código Fonte"
    git clone https://github.com/rafaeldbo/scraping-api
    ```
    O repositório possui os seguintes arquivos.
    ``` tree title="Estutura do Repositório"
    app
        dockerfile @ arquivo de build da imagem da API
        main.py # arquivo principal da API
        requirements.txt 
        ...
    docs # arquivos da documentação em mkdocs
        ...
    compose.yaml # arquivo compose que utiliza a imagem padrão da API
    compose.build.yaml # arquivo compose para modificações da API
    .env.example # exemplo de .env para a API
    ...
    ```
    Após realizar as edições desejadas no código fonte da API. Para subir a aplicação, dentro da pasta do repositório, execute:
    ``` shell title="build & compose"
    docker compose -f compose.build.yaml up -d --build
    ```
