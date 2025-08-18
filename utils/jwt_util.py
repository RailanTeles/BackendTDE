import os
import jwt
import dotenv
from datetime import datetime, timedelta, timezone

now = datetime.now(timezone.utc)


MINHA_CHAVE_SECRETA = os.getenv("MINHA_CHAVE_SECRETA")

if not MINHA_CHAVE_SECRETA:
    dotenv.load_dotenv()
    MINHA_CHAVE_SECRETA = os.getenv("MINHA_CHAVE_SECRETA")

def generate_token(id: int):
    """
    Gera um token JWT para o usuário com base no id
    """

    payload = {
        id: id,
        "iat": now,
        "exp": now + timedelta(hours=2)
    }

    token = jwt.encode(payload,MINHA_CHAVE_SECRETA, algorithm='HS256')
    return token

def decode_token(token: str):
    """
    Decodifica o token JWT e retorna o id do usuário.
    Aceita token com ou sem prefixo 'Bearer '.
    Se o token for inválido, retorna None.
    """

    if token and token.startswith('Bearer '):
        token = token.split(" ")[1]
    
    try:
        payload = jwt.decode(token, MINHA_CHAVE_SECRETA, algorithms=['HS256'])
        return payload[id]
    except:
        return None
    