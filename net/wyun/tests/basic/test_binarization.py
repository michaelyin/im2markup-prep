import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from scipy import misc

img = cv.imread('data/ocr-gray.jpg',cv.IMREAD_GRAYSCALE)
img = cv.medianBlur(img,7)
ret,th1 = cv.threshold(img,127,255,cv.THRESH_BINARY)
th2 = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_MEAN_C,\
            cv.THRESH_BINARY,15,8)
th3 = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv.THRESH_BINARY,11,4)
titles = ['Original Image', 'Global Thresholding (v = 127)',
            'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']
images = [img, th1, th2, th3]


print type(th2)


#th2 = array(th2).convert('L')
#th2 = 1 * (th2 > 128)
#th2 = 0 * (th2 < 128)
th2 = th2.astype(np.uint8)
print th2.shape, th2.dtype

cv.imwrite('data/ocr-bin.jpg', th2, [int(cv.IMWRITE_JPEG_QUALITY), 20])
misc.imsave('data/misc-bin.jpg', th2)
print th2.shape, th2.dtype

for i in xrange(4):
    plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])
plt.show()