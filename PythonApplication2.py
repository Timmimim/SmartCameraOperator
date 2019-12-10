
import argparse
import cv2
import numpy as np
import matplotlib.pyplot as plt
import math as ma


img = cv2.imread('cheetahs.jpg',0)
assert img is not None # check if the image was successfully loaded

print('shape:', img.shape)
print('dtype:', img.dtype)

gaussian = cv2.GaussianBlur(img, (11, 11), 0)
dx = cv2.Sobel(gaussian, cv2.CV_32F,1,0)
dy = cv2.Sobel(gaussian, cv2.CV_32F,0,1)
grad = cv2.sqrt(cv2.pow(dx, 2) + cv2.pow(dy, 2))
directions = np.arctan2(dy, dx)
edges = cv2.Canny(img, 150, 250, True)


plt.figure(figsize=(8,3))
plt.subplot(131)
plt.title('cheetahs')
plt.imshow(directions, cmap='gray')
plt.subplot(132)
plt.axis('off')
plt.imshow(grad, cmap='gray')
plt.title(r'$\frac{dI}{dx}$')
plt.subplot(133)
plt.axis('off')
plt.title(r'$\frac{dI}{d^y}$')
plt.imshow(edges, cmap='gray')
plt.tight_layout()
plt.show()






cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()


