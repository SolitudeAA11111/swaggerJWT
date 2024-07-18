# app/imageprocessing.py

from PIL import Image as PilImage
from io import BytesIO

def imageProcessing(image_field):
    # Загрузка изображения из ImageField
    image = PilImage.open(image_field)

    # Конвертируем изображение в оттенки серого
    grayscale_image = image.convert('L')
    
    # Применяем бинарную (черно-белую) пороговую обработку
    threshold = 128
    binary_image = grayscale_image.point(lambda p: p > threshold and 255)
    
    return binary_image
