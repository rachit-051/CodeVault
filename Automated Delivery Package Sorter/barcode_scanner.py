import cv2
from pyzbar import pyzbar
import numpy as np

import serial
import time


cap = cv2.VideoCapture(0)                  

# cap.set(cv2.CAP_PROP_AUTOFOCUS, 0) # turn off autofocus

# strategy
# 1) use multiple angle views
# 2) use adaptive contrast to make image easier to see
# 3) greyscalling the image, make it easier for the software to detect barcodes

package_selected_station = {
  "A-0010-Z": "L_4",
  "A-0020-Z": "R_5",
  "A-0030-Z": "R_2",
  "A-0040-Z": "R_1",
  "A-0050-Z": "R_9",
  "A-0060-Z": "L_3",
  "A-0070-Z": "R_7",
  "A-0080-Z": "L_6",
  "A-0090-Z": "L_1",
}


def loop():
    lastbarcode =0
    while True:
    
        # setup display specs 
        ret, frame = cap.read() # read image from video captured
        # ret, frame = cv2.threshold(frame, 127, 255, cv2.ADAPTIVE_THRESH_MEAN_C)

        # ret, frame = cv2.threshold(frame, 127, 255, cv2.THRESH_BINARY)
        # ret, frame = cv2.threshold(frame, 127, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C)
        # frame = cv2.resize(frame, (0,0),fx = 1,fy=1) # resize the frame to display later on

        h, w = frame.shape[:2]

        # show instruction to close
        # cv2.putText(frame,"Press q to exit",(30,30),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),1)


        # display current camera view
        # cv2.imshow("Barcode Scanner",frame)
        
        center = (w // 2, h // 2)

        for i in range(6):
            rotate_angle = i*15  #(0 45 90 135)
            
            matrix = cv2.getRotationMatrix2D(center, rotate_angle, 1.0) 
            rotated_frame = cv2.warpAffine(frame, matrix, (w, h))
            # cv2.imshow(str(rotate_angle),rotated_frame)

            barcodeData = search_barcode(frame)
            if(barcodeData!= None):
                
                # barcode filter
                isEqualLastBarcode = lastbarcode != barcodeData
                if (isEqualLastBarcode):
                    # print(barcodeData)
                    lastbarcode = barcodeData

                    if barcodeData in package_selected_station:
                        station_location = package_selected_station[barcodeData]
                        print(station_location + " barcode: " + barcodeData)
                        ser.write(station_location.encode('Ascii'))
                    else:
                        print("error")
                cv2.putText(frame,text,(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),1)

        # rotate 45 degree
        matrix = cv2.getRotationMatrix2D(center, 45, 1.0) 
        frame_45 = cv2.warpAffine(frame, matrix, (w, h))
        cv2.imshow("45",frame_45)

        # rotate 90 degree
        matrix = cv2.getRotationMatrix2D(center, 90, 1.0) 
        frame_90 = cv2.warpAffine(frame, matrix, (w, h))
        cv2.imshow("90",frame_90)
        
        # rotate 135 degree
        matrix = cv2.getRotationMatrix2D(center, 135, 1.0) 
        frame_135 = cv2.warpAffine(frame, matrix, (w, h))
        cv2.imshow("135",frame_135)

        # search image for barcode
        barcodeData = search_barcode(frame)
        print(barcodeData)

        barcodeData = search_barcode(frame_45)
        print(barcodeData)

        barcodeData = search_barcode(frame_90)
        print(barcodeData)

        barcodeData = search_barcode(frame_135)
        print(barcodeData)

        if(barcodeData!= None):
            
            # barcode filter
            isEqualLastBarcode = lastbarcode != barcodeData
            if (isEqualLastBarcode):
                print(barcodeData)
                lastbarcode = barcodeData
            cv2.putText(frame,text,(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),1)
        

        # show image
        
        # exit when q is pressed
        # cv2.waitKey(1)
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows

# take in video image and output barcode values obtained, return None when no barcode is found
def search_barcode(frame):  

    # barcode processing
    barcodes = pyzbar.decode(frame)
    
    for barcode in barcodes:
        # (x,y,w,h) = barcode.rect
        # cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),1)
        barcodeData = barcode.data.decode('utf=8')
        # barcodeType = barcode.type

        return(barcodeData)



if __name__ == '__main__':
    # ser = serial.Serial('/dev/ttyUSB0',115200,timeout=0.1)
    ser = serial.Serial('COM5',115200,timeout=1)
    ser.reset_input_buffer()
loop()