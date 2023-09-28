import glob

import cv2

#img = cv2.imread("galaxy.jpg", 0)
#img = cv2.imread("rsc0.jpg", 1)
#print(img)
#print(img.shape)
#print(img.ndim)
#help(cv2.imread)

images = glob.glob("images/*.jpg")
for image in images:
    print(image[7:])
    img = cv2.imread(image)
    #resized_image = cv2.resize(img, (int(img.shape[1]/4), int(img.shape[0]/4)))
    resized_image = cv2.resize(img, (100, 100))
    cv2.imshow("Hello", resized_image)
    cv2.waitKey(1000)
    cv2.destroyAllWindows()
    cv2.imwrite("images/resized_"+image[7:], resized_image)
