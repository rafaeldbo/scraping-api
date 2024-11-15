
---
## **Introdução**

Nesse guia serão mostrados os passos necessários para realizar o deploy da API em um cluster kubernets utilizando o **AWS EKS** (Amazon Elastic Kubernetes Service).

É possível acessar a API por meio do desse [link](http://a5f54ce5261df479cb6d1104d0a981a8-1418404177.us-east-1.elb.amazonaws.com/docs).

[**Vídeo Explicativo**]()

## **Pré-Requisitos**

Será necessesário acesso a uma conta AWS com permissão sufieciente para criar um cluster EKS (preferencialmente permissões de adminstrador). Além disso, será útil possui o **[AWS CLI](https://aws.amazon.com/pt/cli/)** e o **[EKSCTL](https://eksctl.io/installation/)** para ser possuível utilizar os comandos mostrados nesse guia direto no console de seu computador. Caso não queira instala-los, é possível executar os comando no **AWS Cloud Shell**, porém podem haver algumas diferenças não apontadas nesse guia.

## **Construção do Cluster**

Ulizando o **EKSCTL** é possível criar o cluster EKS de maneira fácil, dando a responsabilidade de criar os recursos necessários para o EKSCTL:

``` shell
eksctl create cluster --name scraping-api --region us-east-1 --nodes 2 --node-type t3.small
```

!!! info "Entendendo o Comando"

    `--name`: nome do cluster e dos recursos necessários para sua criação

    `--region`: região da AWS em que o cluster será hospedado

    `--nodes`: quantidade de nós que o cluster possuirá

    `--node-type`: tipo padrão para as instâncias criadas no _node group_ do cluster


**OBS¹.:** Foi escolhida a instância do tipo `t3.small` pois ela supre as necessidades de recursos da API e possui baixo preço de utilização.

**OBS².:** Esse comando pode demorar alguns minutos para terminar.

!!! info "Recursos Criados"
    Para a criação do cluster EKS são necessários alguns recursos que o **EKSCTL** criou automaticamente, são eles:
    
    - Uma `Role` do **IAM** para atribuir as permissões necessárias para o funcionamento do cluster;
    
    - Outra `Role` do **IAM** para atribuir as permissões necessárias para o funcionamento do _node group_ do cluster;
    
    - Uma `Stack` do **Cloud Formation** onde foi construida toda a infraestrutura de rede (roteadores, subredes, etc) necessária para criar o cluster;

    - O `Cluster` do **EKS** em si, que será responsável por orquestrar os conteiners das aplicações;

    - O `Node Group` do **EC2** em que as instâncias utilizadas pelo cluster serão alocadas;


## Deploy dos Containers

Com o cluster criado, é necessário fazer o deploy dos containers de cada parte da nossa aplicação (o banco de dados e a API), mas antes disso, precisamos mudar o contexto do **kubectl** para que ele acesse o cluster recém criado:

!!! note "Mudando o Contexto"

    ``` shell title="Comando"
    aws eks update-kubeconfig --name scraping-api --region us-east-1
    ```
    ``` title="Resultado Esperado"
    Updated context arn:aws:eks:us-east-1:<Account ID>:cluster/scraping-api in C:\Users\Rafael\.kube\config
    ```

Além da mudança de contexto, é necessário criar os arquivos com as configurações dos containers que serão criados. Será necessário um arquivo `db-deploy.yaml` para o container do banco de dados e um arquivo `web-deploy.yaml` para o container da API. As informações a serem escritas nos arquivos estão nas sessões abaixo: 

???- note "db-deploy.yaml" 
    Caso queira, você pode baixar o arquivo por meio desse link: [db-deploy.yaml](https://alinsperedu-my.sharepoint.com/:u:/g/personal/rafaeldbo_al_insper_edu_br/EcuiuN40sJlCjC7uqzNbO3QBmWGFYwrh4FPAjo9xCT4tTw?e=G9af6a) 

    ``` yaml title="db-deploy.yaml"
    apiVersion: apps/v1
    kind: Deployment
    metadata:
    name: db
    labels:
        app: scraping-api
        tier: database
    spec:
    replicas: 1
    selector:
        matchLabels:
        app: scraping-api
        tier: database
    template:
        metadata:
        labels:
            app: scraping-api
            tier: database
        spec:
        containers:
            - name: db
            image: postgres:latest
            env:
                - name: POSTGRES_USER
                value: "cloud"
                - name: POSTGRES_PASSWORD
                value: "cloudpassword"
                - name: POSTGRES_DB
                value: 'cloud'
    ---
    apiVersion: v1
    kind: Service
    metadata:
    name: db
    labels:
        app: scraping-api
    spec:
    ports:
        - port: 5432
        targetPort: 5432
    selector:
        app: scraping-api
        tier: database
    ```



???- note "web-deploy.yaml" 
    Caso queira, você pode baixar o arquivo por meio desse link: [web-deploy.yaml](https://alinsperedu-my.sharepoint.com/:u:/g/personal/rafaeldbo_al_insper_edu_br/EZbU33XDvsFBn4-OqIuyNKIBLbQOa6-_1_k4uHzYUNF6BQ?e=C6JUoV) 

    ``` yaml title="web-deploy.yaml"
    apiVersion: apps/v1
    kind: Deployment
    metadata:
    name: web
    labels:
        app: scraping-api
    spec:
    replicas: 1
    selector:
        matchLabels:
        app: scraping-api
        tier: backend
    template:
        metadata:
        labels:
            app: scraping-api
            tier: backend
        spec:
        containers:
            - name: web
            image: rafaeldbo/scraping-api:latest
            ports:
                - containerPort: 8080
            env:
                - name: DATABASE_URL
                value: "postgresql+psycopg2://cloud:cloudpassword@db:5432/cloud"
                - name: SECRET_KEY
                value: "cloudkey"
    ---
    apiVersion: v1
    kind: Service
    metadata:
    name: web
    labels:
        app: scraping-api
    spec:
    type: LoadBalancer
    ports:
        - port: 80
        targetPort: 8080
    selector:
        app: scraping-api
        tier: backend
    ```
    **OBS.:** O container da API é do tipo `LoadBalancer`, para permitir que o container seja acessado por fora. Além disso, também permite que, quando houver mais de uma réplica desse container, o acesso a API seja distribuido equilibradamente entre cada uma das réplicas, evitando sobrecarga.

!!! note "Realizando o Deploy"
    No mesmo diretório dos arquivos de deploy acima execute os comandos para configurar os containers:
    ``` shell title="Banco de Dados"
    kubectl apply -f ./db-deploy.yaml
    ```
    ``` shell title="API"
    kubectl apply -f ./web-deploy.yaml
    ```

!!! info "Resultado"
    O comando abaixo permite visualizar os serviços criados e ter acesso ao Ip atribuido a API:

    ``` shell title="Comando"
    kubectl get services
    ```
    ``` title="Resultado Esperado"
    NAME         TYPE           CLUSTER-IP       EXTERNAL-IP                                                               PORT(S)        AGE
    db           ClusterIP      10.100.174.148   <none>                                                                    5432/TCP       29m
    kubernetes   ClusterIP      10.100.0.1       <none>                                                                    443/TCP        42m
    web          LoadBalancer   10.100.15.240    a5f54ce5261df479cb6d1104d0a981a8-1418404177.us-east-1.elb.amazonaws.com   80:32200/TCP   27m
    ```