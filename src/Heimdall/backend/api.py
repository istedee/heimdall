"""API routes for Vue frontend"""

from flask import Blueprint
from flask_restful import Api
from .flask_resources.ping import GetPing
from .flask_resources.elastic import GetConfig
from .flask_resources.config import ScannerConfig
from .flask_resources.scan_history import ScannerHistory
from .flask_resources.command import GetCommand

API_BP = Blueprint("api", __name__, url_prefix="/api")
API = Api(API_BP)

API.add_resource(GetPing, "/ping/")
API.add_resource(GetConfig, "/elastic/")
API.add_resource(ScannerConfig, "/scanner-config/")
API.add_resource(ScannerHistory, "/scanner-history/")
API.add_resource(GetCommand, "/command/check-scanner/")
