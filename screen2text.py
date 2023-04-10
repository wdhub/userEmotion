# screenshot the current screen and extract the text
# real time
# easyOCR is faster than keras,

# import easyocr
# import keras_ocr # too slow as well
import pytesseract
# import cv2

# test: read the text from one prepared image

# reader = easyocr.Reader(['en'])
# detector=keras_ocr.detection.Detector(
#     weights='clovaai_general', load_from_torch=False, optimizer='adam', backbone_name='vgg'
# )
# image = cv2.imread('t1.png', 1)
# result1=detector.detect(
#     image, detection_threshold=0.7, text_threshold=0.4, link_threshold=0.4, size_threshold=10,
# )
# half = cv2.resize(image, (0, 0), fx = 0.5, fy = 0.5)
# result = reader.readtext(image,detail=0,batch_size=2)# get rid of the meaningless numbers
#print(result)

result2=pytesseract.image_to_string('t1.png')