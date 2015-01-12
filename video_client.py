import socket
import cv2
import numpy

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf
# http://stupidpythonideas.blogspot.it/2013/05/sockets-are-byte-streams-not-message.html


TCP_IP = "192.168.1.107"
TCP_PORT = 5002

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
while (True):
    
    
    length = recvall(s,16)
    stringData = recvall(s, int(length))
    data = numpy.fromstring(stringData, dtype='uint8')
    
    
    decimg=cv2.imdecode(data,1)
    cv2.imshow('SERVER',decimg)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
s.close()
cv2.destroyAllWindows() 
# http://stackoverflow.com/questions/20820602/image-send-via-tcp
