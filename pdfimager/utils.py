import fitz
from PIL import Image
import io


def extract_images_from_pdf(pdf_path):
    images = []
    pdf_file = fitz.open(pdf_path)
    for page_num in range(len(pdf_file)):
        page_content = pdf_file[page_num]
        image_list = page_content.get_images(full=True)
        for image_index, img in enumerate(image_list):
            xref = img[0]
            base_image = pdf_file.extract_image(xref)
            image_bytes = base_image["image"]
            image = Image.open(io.BytesIO(image_bytes))
            images.append(image)
    return images
