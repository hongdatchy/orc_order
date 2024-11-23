import pdf2image
import pytesseract
import time
from concurrent.futures import ThreadPoolExecutor
import queue

max_workers = 5
crop_area_list = [
    {"titleArea": "address1", "crop_area_coordinator": (37, 313, 738, 393)},
    {"titleArea": "address2", "crop_area_coordinator": (142, 565, 735, 660)},
    {"titleArea": "trackingNumber", "crop_area_coordinator": (200, 965, 560, 995)},
]

def pdf_to_text(pdf_file):
    images = pdf2image.convert_from_path(pdf_file, dpi=200)
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
    
    return results


def ocr_core(image, titleArea, result_queue):
    text = f"{titleArea}\n{pytesseract.image_to_string(image)}\n"
    result_queue.put(text)


def print_PDF(pdf_file):
    start_time = time.time()
    rs = pdf_to_text(pdf_file)
    end_time = time.time()  # End time in seconds
    
    elapsed_time = (end_time - start_time) * 1000  # Convert to milliseconds
    
    print(rs)
    print(f"Time taken: {elapsed_time:.2f} ms")

print_PDF('1234.pdf')
