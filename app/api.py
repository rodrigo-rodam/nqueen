# coding=utf-8
import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask import Blueprint
from app import settings
from app import app
from app.restplus import api
from app.model import db
from app.endpoints.nqueen import ns as nqueen
from app.web.views import web

log = logging.getLogger(__name__)

application = app


def setup_log():
    log.setLevel(settings.LOG_LEVEL)
    handler = RotatingFileHandler(
        settings.LOG_FILEPATH,
        maxBytes=settings.LOG_MAX_SIZE,
        backupCount=settings.LOG_HISTORY,
    )
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(settings.LOG_FORMAT)
    handler.setFormatter(formatter)
    log.addHandler(handler)


def configure_app(flask_app):
    flask_app.config["RESTPLUS_VALIDATE"] = settings.RESTPLUS_VALIDATE
    if settings.DB_DRIVER:
        flask_app.config[
            "SQLALCHEMY_DATABASE_URI"
        ] = settings.POSTGRESS_SQLALCHEMY_DATABASE_URI
    else:
        flask_app.config["SQLALCHEMY_DATABASE_URI"] = settings.SQLALCHEMY_DATABASE_URI

    flask_app.config["SWAGGER_UI_DOC_EXPANSION"] = settings.SWAGGER_UI_DOC_EXPANSION
    flask_app.config["RESTPLUS_MASK_SWAGGER"] = settings.RESTPLUS_MASK_SWAGGER


def initialize_app(flask_app):
    setup_log()
    configure_app(flask_app)
    blueprint = Blueprint("api", __name__, url_prefix="/api")
    api.init_app(blueprint)
    api.namespaces = []
    api.add_namespace(nqueen)
    flask_app.register_blueprint(web)
    flask_app.register_blueprint(blueprint)
    db.init_app(flask_app)
    with flask_app.app_context():
        log.debug(f"Creating database: {settings.SQLALCHEMY_DATABASE_URI}")
        db.create_all(app=flask_app)


def get_wsgi_application(wsgi=False):
    initialize_app(application)
    port = settings.HOST_PORT
    debugMode = settings.DEBUG_MODE
    ip_filter = settings.IP_FILTER
    start_msg = f"Starting Service at {ip_filter}:{port}/api/ in debugMode:{debugMode}"
    print(start_msg)
    log.info(start_msg)
    if wsgi:
        application.run(port=port, debug=debugMode, host=ip_filter)
    return application


if __name__ == "__main__":
    get_wsgi_application(True)

