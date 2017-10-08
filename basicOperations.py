import socket
import os

def getDuplicateSafeName(name):
    """ this function appends ' to the name until it describes a name in the filesystem that isn't already taken """
    while os.path.isfile(name):
        tmp = name.rpartition('.')
        name = tmp[0] + "'." + tmp[2]
    return name



def uploadFile(sock, fileName):
    """this function takes a socket and a fileName. The function sends the file over the socket
       It is the callee's responsibility to make sure that fileName is valid"""

    fileSize = os.path.getsize(fileName)
    sock.send(bytes(str(fileSize), 'utf-8'))

    with open(fileName, 'rb') as file:
        bytesToSend = file.read(2048)
        sock.send(bytesToSend)
        while bytesToSend != bytes('', 'utf-8'):
            bytesToSend = file.read(2048)
            sock.send(bytesToSend)
        
        # print for debugging
        print('The uploadFile function terminates')



def receiveFile(sock, fileName):
    """This function takes a socket and a filename. The function receives the file and stores it to the location given by fileName.
       It is the callee's responsibility to make sure that the fileName doesn't produce name conflicts"""
    
    fileSize = int(str(sock.recv(128), 'utf-8'))
    transferedSize = 0
    percentTransfered = 0
    print('hoffemers mal')

    with open(fileName, 'wb') as file:
        while transferedSize < fileSize:
            data = sock.recv(2048)
            file.write(data)
            transferedSize += len(data)
            
            # gives the client a hint of how much has been transfered. To avoid too many prints we only print when the 
            # the percent transfered number actually gets larger
            newPercentTransfered = int(transferedSize/float(fileSize)*100)
            if  newPercentTransfered > percentTransfered:
                percentTransfered =  newPercentTransfered
                print(str(percentTransfered) + '% downloaded')
        
        print('The receiveFile function terminates')
    