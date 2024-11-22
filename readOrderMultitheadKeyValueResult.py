import pdf2image
import pytesseract
import time
from concurrent.futures import ThreadPoolExecutor
import queue
from collections import OrderedDict

crop_area_list = [
    {"titleArea": "address1", "crop_area_coordinator": (37, 313, 738, 393)},
    {"titleArea": "address2", "crop_area_coordinator": (142, 565, 735, 660)},
    {"titleArea": "trackingNumber", "crop_area_coordinator": (200, 965, 560, 995)},
    # ... Add more areas here ...
]

def pdf_to_text(pdf_file):
    images = pdf2image.convert_from_path(pdf_file)
    result_dict = {}  # Dùng dictionary để lưu trữ kết quả
    
    # Use ThreadPoolExecutor to limit the number of concurrent threads
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_crop_area = {}
        for i, img in enumerate(images):
            for j, crop_area in enumerate(crop_area_list):
                crop_area_coordinator = crop_area['crop_area_coordinator']
                titleArea = crop_area['titleArea']
                cropped_img = img.crop(crop_area_coordinator)
                future = executor.submit(ocr_core, cropped_img, titleArea)
                future_to_crop_area[future] = titleArea

        # Collect results in order and store them in the dictionary with key as titleArea
        for future in future_to_crop_area:
            titleArea = future_to_crop_area[future]
            result_dict[titleArea] = future.result()
    
    return result_dict  # Trả về dictionary thay vì string


def ocr_core(image, titleArea):
    text = pytesseract.image_to_string(image)
    return {titleArea: text}  # Trả về một dictionary với titleArea là key và text là value


def print_PDF(pdf_file):
    start_time = time.time()
    result_dict = pdf_to_text(pdf_file)
    end_time = time.time()  # End time in seconds
    
    elapsed_time = (end_time - start_time) * 1000  # Convert to milliseconds
    
    # In kết quả, bạn có thể lấy kết quả từ dictionary
    for key, value in result_dict.items():
        print(f"Title: {key}\nOCR Text: {value}\n")
    
    print(f"Time taken: {elapsed_time:.2f} ms")

print_PDF('1234.pdf')
