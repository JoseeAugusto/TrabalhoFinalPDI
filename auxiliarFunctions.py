import cv2
import numpy as np

def segmentImage(img):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lowerThreshold = np.array([90, 70, 90])
    upperThreshold = np.array([150, 255, 255])
    segmentedImage = cv2.inRange(imgHSV, lowerThreshold, upperThreshold)
    return segmentedImage


def handleImageFlaws(img):
    structuringElement = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    img = cv2.erode(img, structuringElement, iterations=1)
    img = cv2.dilate(img, structuringElement, iterations=1)
    return img


def enlargeSaber(img, iterations=10):
    structuringElement = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    img = cv2.dilate(img, structuringElement, iterations=iterations)
    img = cv2.erode(img, structuringElement, iterations=6)
    return img


def processLightSaber(img): 
  segmentedImage = segmentImage(img)

  withoutNoiseImage = handleImageFlaws(segmentedImage)

  enlargedImage = enlargeSaber(withoutNoiseImage, 10)

  firstChannel = img[:, :, 0]
  secondChannel = img[:, :, 1]
  thirdChannel = img[:, :, 2]

  finalImage = img
  finalImage[:, :, 0] = cv2.add(firstChannel, enlargedImage)
  finalImage[:, :, 1] = cv2.add(secondChannel, enlargedImage)
  finalImage[:, :, 2] = cv2.add(thirdChannel, enlargedImage)

  for i in range(3):
    blurredImage = cv2.GaussianBlur(enlargedImage, (37,  37), 0)
    enlargeBlurredImage = enlargeSaber(blurredImage, 8)
    finalImage[:, :, 0] = cv2.add(firstChannel, cv2.subtract(
        enlargeBlurredImage, 150))  # B = 255 - 40 = 215
    finalImage[:, :, 1] = cv2.add(secondChannel, cv2.subtract(
        enlargeBlurredImage, 150))  # G = 255 - 150 = 105
    finalImage[:, :, 2] = cv2.add(thirdChannel, cv2.subtract(
        enlargeBlurredImage, 40))  # R = 255 - 80 = 175
  return img


