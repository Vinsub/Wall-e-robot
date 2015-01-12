import threading
import time		
import cv2
import timeit
import socket
import serial
import numpy
# this is all the libraries
global command
global face_positionx
global face_positiony
# this is the global variables, i think this is the worse and bad metod, but i'm learning python #queue
face_positionx = 0
face_positiony = 0
command = ""


class tasks(threading.Thread):
    def __init__(self, threadID, name, counter, functions):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.functions = functions
    def run(self):
        print "Starting " + self.name
        self.functions()
        print "Exiting " + self.name
# this is a class that performs the server that receives the command, i don't know why, but #without this class the thread doesn't works

def server():
    global command
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("localhost",5001))
    server_socket.listen(5)
    client_socket, address = server_socket.accept()
    while 1:        
        client_command = client_socket.recv(1024)
        client_socket.send("From " + repr(address) + " Recived " + repr(client_command))
                command = client_command
        if client_command == "q":
            time.sleep(5)
            client_socket.close()
            server_socket.close()
            break
    print "Uscito server"      
# this is a server that receives the command for the Wall-e, you can change the "localhost" #with a ip number and it works out of the same machine, if you want to send the command #out of the home network you must to redirect the port in the settings of your router
def cattura_immagine():
    time.sleep(1)
    global command
    global stringData 
    face_positionx = 0
    face_positiony = 0
    command_arduino = 0
    TCP_IP = "192.168.1.107"
    TCP_PORT = 5002
    print "before socket.socket"
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print "after socket.socket"
    sock.bind((TCP_IP, TCP_PORT))
    sock.listen(5)
    client_socket_video, address = sock.accept()
    # this part of code start the variables and the server that send video, you can change the ip
    # number as the server for commands
    
    print "ARDU"
    try:
        arduino = serial.Serial('/dev/ttyUSB0',115200)
        arduinoconnesso = 1
        print "ARDUINO CONNESSO"
    
    except:
        arduinoconnesso = 0
        print "ARDUINO NON CONNESSO"
    # this piece try to connect the Odroid U3 t the arduino, you can change the port name and
    # the speed 
        
    SCALA = 2
    TRAINSET = "/home/linaro/opencv-2.4.6.1/data/lbpcascades/lbpcascade_frontalface.xml"
    classifier = cv2.CascadeClassifier(TRAINSET)
    # this set the cascade for the search of faces, lbp is faster, but you can change

    webcam = cv2.VideoCapture(0)
    time.sleep(3)
    if webcam.isOpened():
        print "Video aperto"
        ret, frame = webcam.read()
        if ret:
            print "ret True"
            contatore = 0
            # this start the webcam capture, you can change the number of the webcam port\	
            
            while(1):
                contatore = contatore + 1
                ret, frame = webcam.read()
                t = timeit.default_timer()
                height = frame.shape[0]
                width = frame.shape[1]
                cv2.putText(frame, "Larghezza " + repr(width) +
                           "Altezza " + repr(height), (50,10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255))
                minisize = (frame.shape[1]/SCALA,frame.shape[0]/SCALA)
                miniframe = cv2.resize(frame, minisize)
                gray = cv2.cvtColor(miniframe, cv2.COLOR_BGR2GRAY)
                gray = cv2.equalizeHist(gray)
                # all this part of code starts to read frame to frame for ever, gets the time for FPS, 
                # shrinks the frame, turns the frame first to grey scala, then makes Histogram 
                # Equalization, to improves the contrast in the image, all to make faster the process 
                # of face detection
                    
                if command == "4":
                    command_arduino = "4"
                    
                if command == "5":
                    command_arduino = "3"
                    
                if command == "r":
                    command_arduino = "2"
                    
                if command == "t":
                    command_arduino = "1"
                if command_arduino != 0:
                    if arduinoconnesso == 1:
                        arduino.write (repr(command_arduino))
                    command_arduino = 0
                    command = ""
	    # this is for the manual command of pan and tilt of Wall-e head 

                if command == "f":
                    faces = classifier.detectMultiScale(gray)
                    for f in faces:
                        x, y, w, h = [ v*SCALA for v in f ]
                        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255))
                        cv2.rectangle(frame, (x+w/2-1,y+h/2-1), (x+w/2+1,y+h/2+1), (0,0,255))
                        cv2.putText(frame, "X = "+repr(x+w/2)+" Y = " + repr(y+h/2), (5, 25),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255))
                        face_positionx = repr(x+w/2)
                        face_positiony = repr(y+h/2)
                        cv2.putText(frame, "Volti n. " + repr(len(faces)), (x-50,y-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255))
		# this performs the real face detection, 
                        # (http://bytefish.de/blog/opencv/object_detection/)

                    if face_positionx != 0 or face_positiony != 0:
                        if int(face_positionx) < 220:
                            command_arduino = "4"
                        if int(face_positionx) > 390:
                            command_arduino = "3"
                        if command_arduino != 0:
                            if arduinoconnesso == 1:
                                arduino.write (repr(command_arduino))
                            command_arduino = 0
            
                        if int(face_positiony) < 160:
                            command_arduino = "1"
                        if int(face_positiony) > 320:
                            command_arduino = "2"
                        if command_arduino != 0:
                            if arduinoconnesso == 1:
                                arduino.write (repr(command_arduino))
                            command_arduino = 0
                    face_positionx = 0
                    face_positiony = 0
                dt = timeit.default_timer() - t
                cv2.putText(frame, "FPS =  " + repr(1/dt), (5, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255))
	    # this part sends the command to Wall-e head to track the faces
                
                encode_param = [int(cv2.IMWRITE_JPEG_QUALITY),90]
                result, imgencode = cv2.imencode('.jpg', gray, encode_param)
                data = numpy.array(imgencode)
                stringData = data.tostring()
                if contatore == 3:
                    client_socket_video.send(str(len(stringData)).ljust(16));
                    client_socket_video.send(stringData);
                    contatore = 0
	    # this send the stream video to the client video, it send strings of text!!

                cv2.imshow('frame',frame)
                
                if command == "q":
                    webcam.release()
                    cv2.destroyAllWindows()
                    break
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    command = "q"
                    break
            
            sock.close()
            time.sleep(2)
            if arduinoconnesso == 1:
                arduino.close()
            webcam.release()
            time.sleep(2)
            cv2.destroyAllWindows()
            print "Uscito Opencv"
            
            time.sleep(2)
               # this closes all when you push "q"

print "Comincio"
thread2 = tasks(2, "server", 2, server)
thread2.start()
cattura_immagine()
# this starts all!!
