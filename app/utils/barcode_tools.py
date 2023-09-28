import barcode
from barcode.writer import ImageWriter
import code128


def generate_code128(codigo):
    ruta_codigo = f"media/tmp/barcode_{codigo}.png"
    code128.image("codigo").save(ruta_codigo)  
    
    return ruta_codigo


def generate_code128_no_fotter(codigo):
    ruta_codigo = f"media/tmp/barcode_{codigo}.png"
    code128.image("codigo").save(ruta_codigo)  

    return ruta_codigo