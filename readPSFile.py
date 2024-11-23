import fitz  # PyMuPDF
from PIL import Image
from psd_tools import PSDImage

def extract_thumbnail_from_ai(ai_file, output_file):
    # Mở file AI như PDF
    doc = fitz.open(ai_file)
    
    # Lấy trang đầu tiên (thumbnail thường nằm ở trang này)
    page = doc[0]
    
    # Chuyển đổi trang thành ảnh
    pix = page.get_pixmap()
    
    # Lưu ảnh ra file
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    img.save(output_file, "png")

# Sử dụng hàm
# extract_thumbnail_from_ai("File cut gửi anh Tính.ai", "outputFolder/ai/File cut gửi anh Tính.PNG")



def extract_thumbnail_from_psd(psd_file, output_file):
    # Mở file PSD
    psd = PSDImage.open(psd_file)

    # Lấy composite image (thumbnail)
    thumbnail = psd.composite()
    
    # Lưu thumbnail ra file
    thumbnail.save(output_file, 'png')

# Sử dụng hàm
# extract_thumbnail("Gửi Đức 21-12 Dương.psd", "outputFolder/psd/Gửi Đức 21-12 Dương.PNG")
