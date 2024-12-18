
---
# **Scraping-API**

**Documentation:** [https://rafaeldbo.github.io/scraping-api/](https://rafaeldbo.github.io/scraping-api/)

**Source Code:** [https://github.com/rafaeldbo/scraping-api](https://github.com/rafaeldbo/scraping-api)

**Docker Image:** [https://hub.docker.com/r/rafaeldbo/scraping-api](https://hub.docker.com/r/rafaeldbo/scraping-api)

**API Access** [http://scraping-api.us-east-1.elb.amazonaws.com/docs](http://a5f54ce5261df479cb6d1104d0a981a8-1418404177.us-east-1.elb.amazonaws.com/docs)

---
Essa é uma API criada para o projeto da disciplina de `Computação em Nuvem` do 6º Semestre (2024.2) do curso de Engenharia da Computação do Insper. [[Enunciado do Projeto]](https://hsandmann.github.io/insper.cloud.projeto/)

---       
### **Recursos Implementados**

A API permite a autenticação de usuários por meio de login e validação de assinaturas JWT e a obtenção de informações de notícias presentes na [Home Page do G1](https://g1.globo.com/) por meio de um *Web Scraping* do site utilizando o `BeautifulSoup`.

[**Vídeo da API**](https://youtu.be/YDXsAyenDn0)

---
### **Tecnologias Usadas**

- Python 3.9+
    - FastAPI [ API FrameWork ]
    - BeautifulSoup [ Web Scraping ]
    - PyJWT [ Assinatura JWT ]
    - SQLmodel + Psycopg2 [ Integração com Banco de dados ]
- PostegreSQL [ Banco de Dados ]
- Docker [ Disponibilização ]
- Amazon EKS [ Deploy ]
- MKdocs Material [ Documentação ]

---
### **Créditos**

!!! info "Aluno/Desenvolvedor"

    Rafael Dourado Bastos de Oliveira [[Github]](https://github.com/rafaeldbo) [[Linkedin]](https://www.linkedin.com/in/rafael-dourado-rdbo/)

!!! info "Professor/Orientador"

    Humberto Rodrigo Sandmann