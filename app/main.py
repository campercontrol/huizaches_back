from fastapi import FastAPI
from service.prueba_service import prueba_routes
app = FastAPI()

app.include_router(prueba_routes)  # Login

@app.post("/", )
def root_test():
    return "Cadena de prueba"