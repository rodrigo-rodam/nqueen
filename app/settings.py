import logging

DEBUG_MODE = True
IP_FILTER = "0.0.0.0"
HOST_PORT = 8080

# FLASK SETTINGS
FLASK_DEBUG = True
SWAGGER_UI_DOC_EXPANSION = "list"
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False

DB_DRIVER = True
# DB SETTINGS
DB_PATH = "data/nqueen.db"
SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"

DB_HOST = "db"
DB_USER = "elizabeth"
DB_PASS = "victoria"
DB_NAME = "nqueen"
POSTGRESS_SQLALCHEMY_DATABASE_URI = (
    f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
)

#  API SEC SETTINGS
SEC_USER = "queen"
SEC_AP = "motherofdragons"

# LOG SETTINGS
LOG_LEVEL = logging.DEBUG
LOG_FILEPATH = "logs/nqueen.log"
LOG_FORMAT = "%(asctime)s-%(levelname)s-%(name)s-:%(message)s"
LOG_MAX_SIZE = 500000
LOG_HISTORY = 20

API_CONF = {
    "username": "queen",
    "password": "motherofdragons",
    "headers": {"Accept": "application/json"},
    "host": "localhost",
    "port": "8080",
}
