# app/views.py

from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Image
from .serializers import ImageSerializer
from .imageprocessing import imageProcessing
from rest_framework.permissions import IsAuthenticated
from django.core.files.base import ContentFile
import io
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

class ImageProcessingView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    @extend_schema(
        request=ImageSerializer,
        responses={201: ImageSerializer},
        description="Upload an image to process",
    )
    def post(self, request, *args, **kwargs):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            image_instance = serializer.save()
            original_image = image_instance.image

            # Применение функции обработки изображения
            processed_image = imageProcessing(original_image)

            # Сохранение обработанного изображения
            buffer = io.BytesIO()
            processed_image.save(buffer, format='PNG')
            image_instance.processed_image.save(f"processed_{original_image.name}", ContentFile(buffer.getvalue()))
            image_instance.save()

            return Response(ImageSerializer(image_instance).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
