from fastapi import APIRouter
from contract_manager.api.local_routes import api

routes = APIRouter()

routes.include_router(api.router, prefix='/api')
