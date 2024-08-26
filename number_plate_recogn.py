# Loading the required python modules
import pytesseract # this is tesseract module
import matplotlib.pyplot as plt
import cv2 # this is opencv module
import glob
import os
from datetime import datetime
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import csv
from gpiozero import Servo
import RPi.GPIO as GPIO 
from time import sleep

servo = Servo(25)
#Disable warnings (optional)
GPIO.setwarnings(False)
#Select GPIO mode
GPIO.setmode(GPIO.BCM)
#Set buzzer - pin 23 as output
buzzer=23
GPIO.setup(buzzer,GPIO.OUT) 


# specify path to the license plate images folder as shown below
#path needs to be changed

path_for_license_plates = "/home/coding/iot_project/plates2/**/*.jpg"
list_license_plates = []
predicted_license_plates = []
valid_licence_number = ['KA.19.S7982']



def gate_open_close():
    print("gate opened")
    servo.min()
    sleep(secs=10)
    servo.max()
    print("gate closed")

def buzz(seconds):
    GPIO.output(buzzer,GPIO.HIGH)
    print ("Beep")
    sleep(secs=seconds)  
    GPIO.output(buzzer,GPIO.LOW)

def find_valid(lnumber):
    found = 0
    if lnumber in valid_licence_number:
        found = 1
        return found
    max = 0
    for x in valid_licence_number:
        accuracy = fuzz.ratio(x,lnumber)
        if max < accuracy:
            max = accuracy
            nearest_value = x
    if accuracy > 70:
            found = 1
            return found

    





for path_to_license_plate in glob.glob(path_for_license_plates, recursive = True):
      
    license_plate_file = path_to_license_plate.split("/")[-1]
    license_plate, _ = os.path.splitext(license_plate_file)
    '''
    Here we append the actual license plate to a list
    '''
    list_license_plates.append(license_plate)
      
    '''
    Read each license plate image file using openCV
    '''
    img = cv2.imread(path_to_license_plate)
      
    '''
    We then pass each license plate image file
    to the Tesseract OCR engine using the Python library 
    wrapper for it. We get back predicted_result for 
    license plate. We append the predicted_result in a
    list and compare it with the original the license plate
    '''
    predicted_result = pytesseract.image_to_string(img, lang ='eng',
    config ='--oem 3 --psm 6 ')
    # pytesseract config option  -c tessedit_char_whitelist = ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789
    # Comparing predicted result to actual result.
    if fuzz.ratio(predicted_result,license_plate) > 65:
        print("Valid number")
        #prints the time car has appeared before the gate
        now = datetime.now()
        current_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        print("Current Time =", current_time)
        #updating the information of the traffic that has entered.
        #specify path correctly
        with open('valid.csv', 'a',newline= '') as file:
            # Use file to refer to the file object
            csv_file = csv.writer(file)
            csv_file.writerow([license_plate,current_time])
        #open gate and close gate
        gate_open_close()
        #buzzer code
        buzz(1)        
    elif find_valid(predicted_result):
        print("Valid number")
        #prints the time car has appeared before the gate
        now = datetime.now()
        current_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        print("Current Time =", current_time)
        #nearest match of predicted string and valid string
        for x in valid_licence_number:
            accuracy = fuzz.ratio(x,predicted_result)
            if max < accuracy:
                max = accuracy
                nearest_value = x
        #updating the information of the traffic that has entered.
        #specify path correctly
        with open('valid.csv', 'a',newline= '') as file:
            # Use file to refer to the file object
            csv_file = csv.writer(file)
            csv_file.writerow([nearest_value,current_time])
        #open gate and close gate
        gate_open_close()
        #buzzer code
        buzz(1) 
    else :
        print("Not a valid number")
        #prints the time car has appeared before the gate
        now = datetime.now()
        current_time = now.strftime("%m/%d/%Y, %H:%M:%SS")
        print("Current Time =", current_time)
        #specify path correctly
        with open('invalid.csv', 'a') as file:
            csv_file = csv.writer(file)
            csv_file.writerow([predicted_result,current_time]) 
        #gate is closed
        #buzzer code to indicate the car is not allowed
        buzz(5)

      
    filter_predicted_result = "".join(predicted_result.split()).replace(":", "").replace("-", "")
    predicted_license_plates.append(filter_predicted_result)

#print(list_license_plates,predicted_license_plates) 


print("Actual License Plate", "\t", "Predicted License Plate", "\t", "Accuracy")
print("--------------------", "\t", "-----------------------", "\t", "--------")
  
def calculate_predicted_accuracy(actual_list, predicted_list):
    for actual_plate, predict_plate in zip(actual_list, predicted_list):
        accuracy = "0 %"
        num_matches = 0
        if actual_plate == predict_plate:
            accuracy = "100 %"
        else:
            if len(actual_plate) == len(predict_plate):
                for a, p in zip(actual_plate, predict_plate):
                    if a == p:
                        num_matches += 1
                accuracy = str(round((num_matches / len(actual_plate)), 2) * 100)
                accuracy += "%"
            accuracy = str(fuzz.ratio(actual_plate,predict_plate))
            accuracy += "%"
        print("     ", actual_plate, "\t\t\t", predict_plate, "\t\t  ", accuracy)
  

#prints how accurately it identified the images
calculate_predicted_accuracy(list_license_plates, predicted_license_plates)
