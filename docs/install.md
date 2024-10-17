
---
## **Pré-Requisitos**

Para a instalação da aplicação é necessário apenas a intalação do [Docker](https://docs.docker.com/engine/install/). Mas, também é recomendado a instalação do [Git](https://git-scm.com/downloads) para facilitar o download dos arquivos necessários para a instalação.

Caso não queira instalar o `Git` você pode apenas criar um arquivo `compose.yaml` com as informações abaixo:
???- note "Arquivo Compose"
    ``` yaml title="compose.yaml"
        name: scraping-api

        services:

        web:
            image: rafaeldbo/scraping-api
            ports:
            - ${WEB_PORT:-8080}:8080
            depends_on:
            - db
            environment:
            DATABASE_URL: postgresql+psycopg2://${POSTGRES_USER:-cloud}:${POSTGRES_PASSWORD:-cloudpassword}@db:${DB_PORT:-5430}/${DB_NAME:-cloud}
            SECRET_KEY: cloudkey

        db:
            image: postgres
            ports:
            - ${DB_PORT:-5430}:${DB_PORT:-5430}
            expose:
            - ${DB_PORT:-5430}
            volumes:
            - postgres_data:/var/lib/postgresql/data/
            command: 
            -p ${DB_PORT:-5430}
            environment:
            POSTGRES_USER: cloud
            POSTGRES_PASSWORD: cloudpassword

        volumes:
            postgres_data:  
    ```

## **Instalação Rápida**

Com os pré-requisitos atendidos siga os passos abaixo:

!!! info "Intalação"
    No terminal, execute:

    === "Com Git"
        ``` bash
        git clone https://github.com/rafaeldbo/scraping-api
        cd ./scraping-api
        docker compose up -d
        ```

    === "Sem Git"
        No mesmo diretório em que o arquivo `compose.yaml` que você criou está presente. 
        ``` shell
        docker compose up -d
        ```

???+ info "Customizando"
    É possível customizar o banco de dados, as portas de acesso, assim como a assinatura dos token JWT, por meio da criação de um arquivo `.env` como o abaixo:
    ``` yaml title=".env"
    POSTGRES_USER = "cloud"               # Usuário do Banco de dados
    POSTGRES_PASSWORD = "cloudpassword"   # Senha do Banco de dados
    DB_PORT = 5432                        # Porta de conexão do Banco de dados
    DB_NAME = "cloud"                     # Nome do Banco de dados
    WEB_PORT = 8080                       # Porta de conexão da API
    SECRET_KEY = "cloudkey"               # Assinatura dos token JWT
    ```
    **OBS.:** no repositório do Github há um arquivo `.env.example` que também pode ser usado como inspiração para essa customização.
