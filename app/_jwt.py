from jwt import decode,encode
from flask import current_app


def generate_token(token_name,data):
    token = encode({token_name:data},key=current_app.config['JWT_KEY'],algorithm='HS256')
    return token

def decode_token(token):
    payload = decode(token,key=current_app.config['JWT_KEY'],algorithms=['HS256'])
    return payload