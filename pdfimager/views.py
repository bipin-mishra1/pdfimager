import os
import string
import zipfile
import tempfile
import random
from uuid import uuid4

from django.http import FileResponse
from rest_framework import viewsets
from rest_framework.response import Response

from .serializer import PDFFileSerializer
from .utils import extract_images_from_pdf
from rest_framework import status
from .models import ImageZipFile


def generate_unique_filename():
    random_filename = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    return f'{random_filename}.zip'


class ExtractImagesViewSet(viewsets.ViewSet):

    def create(self, request):
        serializer = PDFFileSerializer(data=request.data)
        if serializer.is_valid():
            pdf_file = request.FILES['pdf_file']
            temp_dir = tempfile.TemporaryDirectory()

            try:
                temp_pdf_file_path = os.path.join(temp_dir.name, pdf_file.name)
                with open(temp_pdf_file_path, 'wb') as temp_pdf_file:
                    for chunk in pdf_file.chunks():
                        temp_pdf_file.write(chunk)

                images = extract_images_from_pdf(temp_pdf_file_path)
                temp_files = []
                for i, image in enumerate(images):
                    if image.mode == 'RGBA':
                        image = image.convert('RGB')
                    temp_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
                    image.save(temp_file, format='JPEG')
                    temp_files.append(temp_file.name)

                with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as zip_file:
                    with zipfile.ZipFile(zip_file, 'w') as zipf:
                        for temp_file in temp_files:
                            zipf.write(temp_file, os.path.basename(temp_file))

                target_directory = './pdfimager/../temp'
                zip_file_name = generate_unique_filename()
                file_uuid = str(uuid4())
                ImageZipFile(filename=zip_file_name,
                             path=f"{target_directory}/{zip_file_name}",
                             size=pdf_file.size,
                             uuid=file_uuid).save()
                target_file_path = os.path.join(target_directory, zip_file_name)
                os.rename(zip_file.name, target_file_path)

                return Response(
                    {'download_path': f"http://127.0.0.1:8000/api/download/{file_uuid}"})
            finally:
                temp_dir.cleanup()

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FileDownloadViewSet(viewsets.ViewSet):
    lookup_field = 'uuid'

    def retrieve(self, request, uuid=None):
        try:
            file = ImageZipFile.objects.get(uuid=uuid)
            file_path = file.path
            return FileResponse(open(file_path, 'rb'), content_type='application/zip')
        except ImageZipFile.DoesNotExist:
            return Response(status=404)

