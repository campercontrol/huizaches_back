from fastapi import APIRouter, Depends,Response, BackgroundTasks,UploadFile
import aiofiles
from PIL import Image

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