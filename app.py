# app.py

from fastapi import FastAPI
import pandas as pd
import requests

app = FastAPI()

CSV_FILE = "usuarios.csv"


def carregar_usuarios():
    return pd.read_csv(CSV_FILE)


def salvar_usuarios(df):
    df.to_csv(CSV_FILE, index=False)


@app.get("/usuarios")
def listar_usuarios():
    df = carregar_usuarios()

    return {
        "total": len(df),
        "usuarios": df.to_dict(orient="records")
    }


@app.get("/usuario/{usuario_id}")
def buscar_usuario(usuario_id: int):
    df = carregar_usuarios()

    usuario = df[df["id"] == usuario_id]

    if len(usuario) == 0:
        return {"erro": "Usuário não encontrado"}

    return usuario.to_dict(orient="records")[0]


@app.post("/sincronizar")
def sincronizar_usuarios():
    resposta = requests.get(
        "https://jsonplaceholder.typicode.com/users"
    )

    usuarios = resposta.json()

    dados = []

    for usuario in usuarios:
        dados.append({
            "id": usuario["id"],
            "nome": usuario["name"],
            "email": usuario["email"]
        })

    df = pd.DataFrame(dados)

    salvar_usuarios(df)

    return {
        "mensagem": "Usuários sincronizados",
        "quantidade": len(df)
    }


@app.get("/usuarios/busca/{nome}")
def buscar_por_nome(nome: str):
    df = carregar_usuarios()

    resultado = df[
        df["nome"].str.contains(nome, case=False)
    ]

    return {
        "quantidade": len(resultado),
        "usuarios": resultado.to_dict(orient="records")
    }