import pdf2image
import pytesseract
import time

crop_area_list = [
    {"titleArea": "address1", "crop_area_coordinator": (37, 313, 738, 393)},
    {"titleArea": "address2", "crop_area_coordinator": (142, 565, 735, 660)},
    {"titleArea": "trackingNumber", "crop_area_coordinator": (200, 965, 560, 995)},
    # {"titleArea": "trackingNumber", "crop_area_coordinator": (200, 965, 560, 995)},
    # {"titleArea": "trackingNumber", "crop_area_coordinator": (200, 965, 560, 995)},
    # {"titleArea": "trackingNumber", "crop_area_coordinator": (200, 965, 560, 995)},
    # {"titleArea": "trackingNumber", "crop_area_coordinator": (200, 965, 560, 995)},
    # {"titleArea": "trackingNumber", "crop_area_coordinator": (200, 965, 560, 995)},
    # {"titleArea": "trackingNumber", "crop_area_coordinator": (200, 965, 560, 995)},
    # {"titleArea": "trackingNumber", "crop_area_coordinator": (200, 965, 560, 995)},
    # {"titleArea": "trackingNumber", "crop_area_coordinator": (200, 965, 560, 995)},
    # {"titleArea": "trackingNumber", "crop_area_coordinator": (200, 965, 560, 995)},
    # {"titleArea": "trackingNumber", "crop_area_coordinator": (200, 965, 560, 995)},
    # {"titleArea": "trackingNumber", "crop_area_coordinator": (200, 965, 560, 995)},
    # {"titleArea": "trackingNumber", "crop_area_coordinator": (200, 965, 560, 995)},
    # {"titleArea": "trackingNumber", "crop_area_coordinator": (200, 965, 560, 995)},
    # {"titleArea": "trackingNumber", "crop_area_coordinator": (200, 965, 560, 995)},
    # {"titleArea": "trackingNumber", "crop_area_coordinator": (200, 965, 560, 995)},
    # {"titleArea": "trackingNumber", "crop_area_coordinator": (200, 965, 560, 995)},
]

def pdf_to_img(pdf_file):
    images = pdf2image.convert_from_path(pdf_file)
    list_cropped_img = []
    for i, img in enumerate(images) :
        for j, crop_area in enumerate(crop_area_list):
            crop_area_coordinator = crop_area['crop_area_coordinator']
            cropped_img = img.crop(crop_area_coordinator)
            list_cropped_img.append(
                {
                    "titleArea": crop_area['titleArea'], 
                    "cropped_img": cropped_img
                }
            )
    return list_cropped_img


def ocr_core(image):
    return pytesseract.image_to_string(image)


def print_PDF(pdf_file):
    start_time = time.time()
    rs = ""
    images = pdf_to_img(pdf_file)
    for img in images:
        rs += f"{img["titleArea"]}\n{ocr_core(img["cropped_img"])}\n"
    
    end_time = time.time()  # Lấy thời gian kết thúc tính bằng giây
    
    elapsed_time = (end_time - start_time) * 1000  # Chuyển đổi từ giây sang millisecond
    
    print(rs)
    print(f"Time taken: {elapsed_time:.2f} ms")

print_PDF('1234.pdf')

