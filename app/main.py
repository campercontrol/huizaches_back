from fastapi import FastAPI
from service.prueba_service import prueba_routes
from service.catalogs.currencies_service import currencies_routes
app = FastAPI()

app.include_router(prueba_routes)  # Login
app.include_router(currencies_routes)

@app.post("/", )
def root_test():
    return "Cadena de prueba"