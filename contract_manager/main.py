from fastapi import FastAPI
from contract_manager.api.routes import routes

app = FastAPI(debug=True)

app.include_router(routes)
