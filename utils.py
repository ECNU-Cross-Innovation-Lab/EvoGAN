from FER.recognizer import Recognizer
from skimage import io

path = "results/000034_0/20_19.jpg"
img = io.imread(path)
recognizer = Recognizer()
res = recognizer.recognize(img)
recognizer.save_res_img("rec")