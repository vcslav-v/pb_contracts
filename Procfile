release: alembic upgrade head
web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker contract_manager.main:app