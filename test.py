import pdf2image
import pytesseract
import time
import asyncio

crop_area_list = [
    {"titleArea": "address1", "crop_area_coordinator": (37, 313, 738, 393)},
    {"titleArea": "address2", "crop_area_coordinator": (142, 565, 735, 660)},
    {"titleArea": "trackingNumber", "crop_area_coordinator": (200, 965, 560, 995)},
]


async def ocr_core(image, titleArea):
    # Sử dụng pytesseract để nhận diện văn bản từ ảnh (bất đồng bộ)
    text = pytesseract.image_to_string(image)
    return {titleArea: text}

async def process_image(img, crop_area):
    # Cắt ảnh và thực hiện OCR bất đồng bộ
    crop_area_coordinator = crop_area['crop_area_coordinator']
    titleArea = crop_area['titleArea']
    cropped_img = img.crop(crop_area_coordinator)
    return await ocr_core(cropped_img, titleArea)

async def pdf_to_text(pdf_file):
    images = pdf2image.convert_from_path(pdf_file)
    result_dict = {}  # Dùng dictionary để lưu trữ kết quả
    
    tasks = []  # Danh sách các tasks bất đồng bộ

    for img in images:
        for crop_area in crop_area_list:
            # Đẩy các công việc vào danh sách tasks
            tasks.append(process_image(img, crop_area))
    
    # Chạy tất cả các task bất đồng bộ cùng lúc
    results = await asyncio.gather(*tasks)

    # Thu thập kết quả vào dict
    for result in results:
        result_dict.update(result)

    return result_dict  # Trả về dictionary thay vì string

def print_PDF(pdf_file):
    start_time = time.time()

    # Chạy bất đồng bộ bằng asyncio.run
    result_dict = asyncio.run(pdf_to_text(pdf_file))

    end_time = time.time()  # End time in seconds
    elapsed_time = (end_time - start_time) * 1000  # Convert to milliseconds
    
    # In kết quả, bạn có thể lấy kết quả từ dictionary
    for key, value in result_dict.items():
        print(f"Title: {key}\nOCR Text: {value}\n")
    
    print(f"Time taken: {elapsed_time:.2f} ms")

print_PDF('1234.pdf')
