import jwt
import datetime
import os
from flask import Flask, request
from flask_mysqldb import MySQL

INVALID_CREDENTIALS = "Invalid credentials"
MISSING_CREDENTIALS = "Missing credentials"
NOT_AUTHORIZED = "Not authorized"
#TODO: Please delete this comment, this is just testing
# Server para pegarle a la BD

server = Flask(__name__)
mysql = MySQL(server)

# config
server.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST')
server.config['MYSQL_USER'] = os.environ.get('MYSQL_USER')
server.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
server.config['MYSQL_DB'] = os.environ.get('MYSQL_DB')
server.config['MYSQL_PORT'] = os.environ.get('MYSQL_PORT')


def createJWT(username, secret, auth):
    """
    Las credenciales son validas, se debe otorgar token de acceso para que el usuario pueda hacerle request a la API.
    auth: nos dice si el usuario es administrador o no.
    """

    return jwt.encode({"username": username,
                        "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=1),
                        "iat": datetime.datetime.utcnow(),
                        "admin": auth},
                        secret,
                        algorithm="HS256")



@server.route('/login', methods=['POST'])
def login():
    auth = request.authorization
    if not auth:
        return MISSING_CREDENTIALS,401
    
    # Chequeo de credenciales de usuario (tiene que estar en la DB MySql)
    cur = mysql.connection.cursor()
    query = "SELECT email, password FROM user WHERE email=%s"
    res = cur.execute(query, (auth.username)) # email = username

    # Se valida que el usuario exista
    if res > 0:
        user_row = cur.fetchone()
        email = user_row[0]
        password = user_row[1]

        if auth.username != email or auth.password != password:
            return INVALID_CREDENTIALS, 401
        else:
            return createJWT(auth.username, os.environ.get("JWT_SECRET"), True)
    else:
        return INVALID_CREDENTIALS, 401




@server.route("validate/", method=["POST"])
def validate():
    """
    Utilizado por el API gateway para validar los request del cliente.
    """
    encoded_jwt = request.headers["Authorization"]
    if not encoded_jwt: 
        return MISSING_CREDENTIALS, 401
    
    # Authorizatoin: Bearer <token>
    encoded_jwt = encoded_jwt.split(" ")[1] # token
    try:
        decoded = jwt.decode(
            encoded_jwt,
            os.environ.get("JWT_SECRET"),
            algorithm=["HS256"]
        )
    except:
        return NOT_AUTHORIZED, 403
    
    return decoded, 200




if __name__ == "__main__":
    server.run(port=5000, host="0.0.0.0")
