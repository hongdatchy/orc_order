import pdf2image
import pytesseract
import os
from concurrent.futures import ThreadPoolExecutor
import queue

max_workers = 5
crop_area_list = [
    {"titleArea": "address1", "crop_area_coordinator": (37, 313, 738, 393)},
    {"titleArea": "address2", "crop_area_coordinator": (142, 565, 735, 660)},
    {"titleArea": "trackingNumber", "crop_area_coordinator": (200, 965, 560, 995)},
]

def pdf_to_text(pdf_file):
    images = pdf2image.convert_from_path(pdf_file)
    # images = images
    result_queue = queue.Queue()
    
    # Use ThreadPoolExecutor to limit the number of concurrent threads
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for i, img in enumerate(images):
            for j, crop_area in enumerate(crop_area_list):
                crop_area_coordinator = crop_area['crop_area_coordinator']
                titleArea = crop_area['titleArea']
                cropped_img = img.crop(crop_area_coordinator)
                executor.submit(ocr_core, cropped_img, titleArea, result_queue)
    
    # Collect results from the queue
    results = ""
    while not result_queue.empty():
        results += result_queue.get()
    
    return results, os.path.getsize(pdf_file)


def ocr_core(image, titleArea, result_queue):
    text = f"{titleArea}\n{pytesseract.image_to_string(image)}\n"
    result_queue.put(text)


def print_PDF(pdf_file):
    return pdf_to_text(pdf_file)

# print_PDF('1234.pdf')
