import fitz  # PyMuPDF
from PIL import Image
from psd_tools import PSDImage
import io

def extract_thumbnail_from_ai(ai_file):
    # Mở file AI dưới dạng PDF
    doc = fitz.open(ai_file)
    
    # Lấy trang đầu tiên (thumbnail thường nằm ở trang này)
    page = doc[0]
    
    # Chuyển đổi trang thành ảnh
    pix = page.get_pixmap()
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    
    # Kiểm tra kích thước và resize nếu cần
    max_size = 3000
    if img.width > max_size or img.height > max_size:
        # Tính tỉ lệ để resize ảnh về 3000px theo chiều lớn nhất
        scale = max_size / max(img.width, img.height)
        new_width = int(img.width * scale)
        new_height = int(img.height * scale)
        img = img.resize((new_width, new_height))
    
    # Lưu ảnh vào bộ nhớ dưới dạng byte stream (WEBP format)
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='WEBP')
    img_byte_arr.seek(0)  # Đặt lại con trỏ file về đầu

    # Trả về kích thước của ảnh đã resize và byte stream
    return img.size, img_byte_arr

# Sử dụng hàm
# extract_thumbnail_from_ai("File cut gửi anh Tính.ai", "outputFolder/ai/File cut gửi anh Tính.PNG")



def extract_thumbnail_from_psd(psd_file):
    # Mở file PSD
    psd = PSDImage.open(psd_file)

    # Lấy composite image (thumbnail)
    thumbnail = psd.composite()

    # Kiểm tra kích thước và resize nếu cần
    max_size = 3000
    if thumbnail.width > max_size or thumbnail.height > max_size:
        # Tính tỉ lệ để resize ảnh về 3000px theo chiều lớn nhất
        scale = max_size / max(thumbnail.width, thumbnail.height)
        new_width = int(thumbnail.width * scale)
        new_height = int(thumbnail.height * scale)
        thumbnail = thumbnail.resize((new_width, new_height))

    # Lưu thumbnail vào bộ nhớ (byte stream) dưới dạng WEBP
    img_byte_arr = io.BytesIO()
    thumbnail.save(img_byte_arr, format='WEBP')
    img_byte_arr.seek(0)  # Đặt lại con trỏ file về đầu

    # Trả về kích thước của ảnh đã resize và byte stream
    return thumbnail.size, img_byte_arr

# Sử dụng hàm
# extract_thumbnail("Gửi Đức 21-12 Dương.psd", "outputFolder/psd/Gửi Đức 21-12 Dương.PNG")

