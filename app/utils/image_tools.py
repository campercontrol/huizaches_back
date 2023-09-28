from fastapi import APIRouter, Depends,Response, BackgroundTasks,UploadFile
import aiofiles
from PIL import Image
import base64


#Guarda una imagen de forma asyncrona
async def write_image(file_name: str, file: UploadFile):
    async with aiofiles.open(file_name, "wb") as buffer:
        data = await file.read()
        await buffer.write(data)
    #Redimencionar
    image = Image.open(file_name)
    image.thumbnail((800, 800))
    image.save(file_name)

    return file_name


#Guarda una imagen de forma asyncrona
async def open_image(file_name: str,tmp_file_name,w,h):
    #Redimencionar
    image = Image.open(file_name)

    image_resized = image.resize((w, h))
    image_resized.save(tmp_file_name)

    return tmp_file_name


#Obtiene la imagen del path temporal y la guarda en la carpeta de photos con un nombre real
async def rewrite_image(file_name: str, final_name: str):
    image = Image.open(file_name)
    image.save(final_name)

    return final_name

#Convertir una imagen en base 64 para adjuntar en pdf
def img_to_base_64(path):
    # Convert the image to base64 format
    with open(path, "rb") as f:
        encoded_image = base64.b64encode(f.read())
    
    return encoded_image
