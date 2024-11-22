import time
from PIL import Image
from io import BytesIO
import pytesseract
import pdf2image
import queue
from concurrent.futures import ThreadPoolExecutor

max_workers = 5
crop_area_list = [
    {"titleArea": "address1", "crop_area_coordinator": (37, 313, 738, 393), "config": ""},
    {"titleArea": "address2", "crop_area_coordinator": (142, 565, 735, 660), "config": ""},
    {"titleArea": "trackingNumber", "crop_area_coordinator": (200, 965, 560, 995), "config": ""},
    # Thêm các crop area khác nếu cần
]

def compress_image_in_memory(img, quality=100):
    # Nén ảnh và trả về ảnh nén ở dạng bytes
    if img.mode == 'RGBA':
        img = img.convert('RGB')
    
    img_byte_array = BytesIO()
    img.save(img_byte_array, 'JPEG', quality=quality)
    img_byte_array.seek(0)
    return img_byte_array

def ocr_core(image, titleArea, config, result_queue):
    text = f"{titleArea}\n{pytesseract.image_to_string(image, config=config)}\n"
    result_queue.put(text)

def pdf_to_text(pdf_file):
    # Chuyển đổi PDF thành ảnh
    images = pdf2image.convert_from_path(pdf_file)
    result_queue = queue.Queue()
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for i, img in enumerate(images):
            for j, crop_area in enumerate(crop_area_list):
                crop_area_coordinator = crop_area['crop_area_coordinator']
                titleArea = crop_area['titleArea']
                config = crop_area['config']
                cropped_img = img.crop(crop_area_coordinator)
                
                # Nén ảnh sau khi crop
                compressed_img = compress_image_in_memory(cropped_img)
                
                # Thực hiện OCR trên ảnh nén
                executor.submit(ocr_core, compressed_img, titleArea, config, result_queue)
    
    # Collect results from the queue
    results = ""
    while not result_queue.empty():
        results += result_queue.get()

    return results

def print_PDF(pdf_file):
    start_time = time.time()  # Thời gian bắt đầu toàn bộ quá trình
    results = pdf_to_text(pdf_file)
    end_time = time.time()  # Thời gian kết thúc toàn bộ quá trình
    total_time = (end_time - start_time) * 1000  # Thời gian tính bằng millisecond
    print(results)
    print(f"Total time: {total_time:.2f} ms")  # In thời gian tổng thể của quá trình

# Gọi hàm print_PDF với tên file PDF của bạn
print_PDF('1234.pdf')


from PIL import Image

def downscale_resolution(image_path, output_path, dpi=150):
    # Mở ảnh
    img = Image.open(image_path)
    
    # Lưu ảnh với độ phân giải thấp hơn
    img.save(output_path, dpi=(dpi, dpi))

downscale_resolution('a.png', '2.jpg', 150)


def compress_image(image_path, output_path, quality=1):
    # Mở ảnh
    img = Image.open(image_path)
    
    # Lưu ảnh với chất lượng nén thấp hơn
    img.save(output_path, 'JPEG', quality=quality)

compress_image('a.png', '3.jpg', 1)