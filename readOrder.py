import pdf2image
import pytesseract
import os 
import time

saveImage = True
crop_area_list = [
    {
    "titlePage" : "address1",
    "crop_area" : (37, 313, 738, 393)
    },
    {
    "titlePage" : "address2",
    "crop_area" : (142, 565, 735, 660)
    },
    {
    "titlePage" : "trackingNumber",
    "crop_area" : (200, 965, 560, 995)
    },
]

def pdf_to_img(pdf_file):
    images = pdf2image.convert_from_path(pdf_file)
    list_cropped_img = []
    for i, img in enumerate(images) :
        for j, crop_area in enumerate(crop_area_list):
            crop_area_coordinator = crop_area['crop_area']
            cropped_img = img.crop(crop_area_coordinator)
            if(saveImage):
                image_path = os.path.join("outputFolder/ocr", f"page_{str(i + 1) + "_" + str(j)}.png")  # Đặt tên file ảnh
                cropped_img.save(image_path, 'PNG')
            list_cropped_img.append(
                {
                    "titlePage": crop_area['titlePage'], 
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
        rs += f"{img["titlePage"]}\n{ocr_core(img["cropped_img"])}\n"
    
    end_time = time.time()  # Lấy thời gian kết thúc tính bằng giây
    
    elapsed_time = (end_time - start_time) * 1000  # Chuyển đổi từ giây sang millisecond
    
    print(f"Time taken: {elapsed_time:.2f} ms")
    print(rs)

print_PDF('1234.pdf')

