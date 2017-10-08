import threading
import os
import socket
import basicOperations  # own python file



def handler(sock):
    """ this function will be running in a seperate thread and handle the communication to one client """
    # as the very first thing we have to send the client a string describing all the files in the sharedData folder
    # we can get 3 different messages from the client:
    #   1. quit
    #   2. download
    #   3. upload
    while True:
        filesOnTheServer = ', '.join(os.listdir('sharedData/'))
        sock.send(bytes(filesOnTheServer, 'utf-8'))

        message = str(sock.recv(32), 'utf-8')
        sock.send(bytes('ACK', 'utf-8'))
        print('also')

        if message == 'quit':
            sock.close()
            break
        
        elif message == 'download':
            # this means that the client wants a file from the sharedData folder and we need to
            #   1. get the name of the desired file
            #   2. send the file

            name = 'sharedData/' + str(sock.recv(32), 'utf-8')
            print('ja so')
            basicOperations.uploadFile(sock, name)
            sock.recv(32)
        
        elif message == 'upload':
            # this means that the client wants to send a file to the sharedData folder and we need to:
            #   1. get the name of the new file
            #   2. produce a name that won't have a name conflict in sharedData
            #   3. receive the actual file

            name = str(sock.recv(128), 'utf-8')

            sock.send(bytes('ACK', 'utf-8'))

            name = basicOperations.getDuplicateSafeName('sharedData/' + name)

            basicOperations.receiveFile(sock, name)
        



if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('192.168.0.0', 0000))    # TODO: add your machine's information here (ip, port)
    sock.listen(1)

    while True:
        c, a = sock.accept()
        cThread = threading.Thread(target = handler, args = (c,))
        cThread.start()
        print(a[0] + ' connected')
