from xmlrpc.client import boolean

from fastapi import APIRouter, Depends,Response, BackgroundTasks,UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session


from model.user import User
# from utils.check_role import chek_permission
from utils.db import SessionLocal
from utils.image_tools import write_image,open_image

image_routes = APIRouter()

# Dependency


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()



@image_routes.post("/photo/upload_image", tags=["Photo"])
async def upload_image_async(
    file: UploadFile,
    response: Response,
    db: Session = Depends(get_db)
):
    arr_image_mime_type = ["image/jpeg","image/ief"]
    file_name = f"media/tmp/{file.filename}"
    print(file_name)
    if file.content_type in arr_image_mime_type: 
        file_name_result = await write_image(file_name,file)
        response.status_code = 200
        return {"path": file_name_result}
    else:
        response.status_code = 401
        return {"mensaje": "El archivo que se inteno subir no cumple con el formato de imagen", "data": ""}


#/camper/photo/[id] - Trae la foto original 
@image_routes.get("/camper/photo/{id_camping}", tags=["Photo"])
async def return_image(
    id_camping: str,
    path:str,
    response: Response,
    db: Session = Depends(get_db)
):
    #Añadir logica parabuscar en camping
    return FileResponse(path)


#/camper/photo/thumb/[id] - Trae la foto de 10X10
@image_routes.get("/camper/photo/thumb/{id_camping}", tags=["Photo"])
async def return_thumb_image(
    id_camping: str,
    path:str,
    response: Response,
    db: Session = Depends(get_db)
):  
    temporal_path_name = str(path.split("/")[-1]).split(".")[0]
    temporal_path_name = f"media/tmp/{temporal_path_name}_10.jpg"

    print(temporal_path_name)
    path_image_file = await open_image(path,temporal_path_name,100,100)

    return FileResponse(path_image_file)
