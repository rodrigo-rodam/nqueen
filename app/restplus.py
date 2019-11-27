import logging
import traceback
from app import settings
from flask_restplus import Api
from flask_jwt import JWTError
from flask_httpauth import HTTPBasicAuth
from sqlalchemy.orm.exc import NoResultFound

log = logging.getLogger(__name__)

api = Api(version="1.0", title="Chess API", description="API for N Queen")

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    if username == settings.SEC_USER and password == settings.SEC_AP:
        return True
    else:
        return False


@api.errorhandler
def default_error_handler(e):
    message = str(e)
    log.exception(message)
    return {"message": message}, 500


@api.errorhandler(JWTError)
def authentication_error(e):
    log.warning(traceback.format_exc())
    return {"message": traceback.error_message}, 401


@api.errorhandler(NoResultFound)
def database_not_found_error_handler(e):
    log.warning(traceback.format_exc())
    return {"message": "A database result was required but none was found."}, 404
