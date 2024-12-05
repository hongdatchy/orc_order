import fitz  # PyMuPDF
from PIL import Image
from psd_tools import PSDImage
import io

def extract_thumbnail_from_ai(ai_file, ext):
#    open ai file as pdf
    doc = fitz.open(ai_file)
    
    # get page 1
    page = doc[0]
    
    # convert page to image
    pix = page.get_pixmap()
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    
    # check size and resize if necessary
    max_size = 3000
    if img.width > max_size or img.height > max_size:
        # Tính tỉ lệ để resize ảnh về 3000px theo chiều lớn nhất
        scale = max_size / max(img.width, img.height)
        new_width = int(img.width * scale)
        new_height = int(img.height * scale)
        img = img.resize((new_width, new_height))
    
    # save image to byte stream
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format=ext[1:].upper())
    img_byte_arr.seek(0)

    return img.size, img_byte_arr
    
# test function
# extract_thumbnail_from_ai("File cut gửi anh Tính.ai", "outputFolder/ai/File cut gửi anh Tính.PNG")



def extract_thumbnail_from_psd(psd_file, ext):
    # open psd file
    psd = PSDImage.open(psd_file)

    # get thumbnail
    thumbnail = psd.composite()

    # check size and resize if necessary
    max_size = 3000
    if thumbnail.width > max_size or thumbnail.height > max_size:
        scale = max_size / max(thumbnail.width, thumbnail.height)
        new_width = int(thumbnail.width * scale)
        new_height = int(thumbnail.height * scale)
        thumbnail = thumbnail.resize((new_width, new_height))

    # save thumbnail to byte stream
    img_byte_arr = io.BytesIO()
    thumbnail.save(img_byte_arr, format=ext[1:].upper())
    img_byte_arr.seek(0)  # Đặt lại con trỏ file về đầu

    return thumbnail.size, img_byte_arr

# test function
# extract_thumbnail("Gửi Đức 21-12 Dương.psd", "outputFolder/psd/Gửi Đức 21-12 Dương.PNG")

