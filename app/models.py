from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str = Field(max_length=50)
    email: str = Field(unique=True)
    senha: str = Field(min_length=6)
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "nome": "Humberto Sandmann",
                    "email": "humbertors@insper.edu.br",
                    "senha": "R4u1_Ik3d4"
                }
            ]
        }
    }
    
class UserLogin(SQLModel):
    email: str = Field(unique=True)
    senha: str = Field(min_length=6)
     
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "humbertors@insper.edu.br",
                    "senha": "R4u1_Ik3d4"
                }
            ]
        }
    }
   
class News(SQLModel):
    titulo: str
    link: str
    tema: str
    tempo_publicacao: str
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "titulo": "Imprensa internacional fala em 'derrota' para Musk após X cumprir ordens e ser liberado; veja repercussão",
                    "link": "https://g1.globo.com/tecnologia/noticia/2024/10/09/imprensa-internacional-fala-em-derrota-para-musk-apos-x-cumprir-ordens-e-ser-liberado-veja-repercussao.ghtml",
                    "tema": "Tecnologia",
                    "tempo_publicacao": "Há X dias"
                }
            ]
        }
    }
    
class Token(SQLModel):
    jwt: str  
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "jwt": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Imh1bWJlcnRvcnNAaW5zcGVyLmVkdS5iciJ9.gV2UGe8UsU2fYQNldydzaCbXjWzEC6EDblbPwF2gC1o"
                }
            ]
        }
    }