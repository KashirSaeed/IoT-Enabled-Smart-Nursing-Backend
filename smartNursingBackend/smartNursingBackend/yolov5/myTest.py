# from DetectObject import DetectObject

import cv2

# # Load an image using cv2.imread()
# img = cv2.imread("data/images/bus.jpg")

# # cv2.imshow("Image", img)
# # cv2.waitKey(0)
# # cv2.destroyAllWindows()


# obj = DetectObject()

# obj.run(img)



from detect import detect


obj=detect()

for i in range(10):
    img = cv2.imread("data/images/bus.jpg")

    obj.run(im0=img)