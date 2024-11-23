import pdf2image
import pytesseract
from concurrent.futures import ThreadPoolExecutor

crop_area_list = [
    {"titleArea": "address1", "crop_area_coordinator": (37, 313, 738, 393)},
    {"titleArea": "address2", "crop_area_coordinator": (142, 565, 735, 660)},
    {"titleArea": "trackingNumber", "crop_area_coordinator": (200, 965, 560, 995)},
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
    
    result_dict = pdf_to_text(pdf_file)
    
    # In kết quả, bạn có thể lấy kết quả từ dictionary
    # for key, value in result_dict.items():
    #     print(f"Title: {key}\nOCR Text: {value}\n")
    

# print_PDF('1234.pdf')
