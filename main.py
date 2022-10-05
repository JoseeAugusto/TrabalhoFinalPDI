import cv2
from auxiliarFunctions import processLightSaber

def processVideo(capture):
  ret, frame = capture.read()

  frame_width = int(capture.get(3))
  frame_height = int(capture.get(4))

  out = cv2.VideoWriter('videoSaida4.avi', cv2.VideoWriter_fourcc(
      *'DIVX'), 30, (frame_width, frame_height))

  while True:
    ret, frame = capture.read()

    if not ret:
      print("Can't receive frame (stream end?). Exiting ...")
      break
    frame = processLightSaber(frame)
    frame = cv2.flip(frame, -1)

    out.write(frame)

    cv2.imshow('frame', frame)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
      break

  capture.release()
  out.release()


if __name__ == "__main__":
  capture = cv2.VideoCapture('videoOriginal.mp4')
  processVideo(capture)

  cv2.destroyAllWindows()
  cv2.waitKey(0)

