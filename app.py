from fastapi import HTTPException


@app.get("/dominio/{usuario_id}")
def obter_dominio_email(usuario_id: int) -> dict:
    df = carregar_usuarios()

    usuario = df[df["id"] == usuario_id]

    if usuario.empty:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    email = str(usuario.iloc[0]["email"]).strip()

    if "@" not in email:
        raise HTTPException(
            status_code=400,
            detail="E-mail inválido"
        )

    dominio = email.split("@", maxsplit=1)[1]

    return {
        "usuario_id": usuario_id,
        "dominio": dominio
    }