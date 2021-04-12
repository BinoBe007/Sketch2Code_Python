import cv2
img = cv2.imread('test.png')

width = int(1345)
height = int(602)
dimension = (width,height)

resized=cv2.resize(img,dimension, interpolation=cv2.INTER_AREA)
print(resized.shape)

cv2.imshow('Resized Pic', resized)
cv2.imwrite('test.png',resized)

cv2.waitKey(0)
cv2.destroyAllWindows()