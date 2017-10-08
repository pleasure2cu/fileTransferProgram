import socket
import os
import basicOperations  # own python file


def getName(path):
    """ this function extracts the name of the file out of the path to it """
    # for linux users
    name = path.split('/')[-1]
    # for windows users
    name = name.split('\\')[-1]
    return name


# here the user input is processed
if __name__ == '__main__':
    sock = socket.create_connection(('192.168.0.0', 0000)) # TODO insert your server's information (ip, port)
    
    # the change flag is used to see, when we will receive an updated list of the files on the server
    # we won't get a new list if we find a problem locally
    changeFlag = True
    filesOnTheServer = ''
    while True:
        if changeFlag:
            filesOnTheServer = str(sock.recv(1024), 'utf-8')
            print('These file are on the server: ' + filesOnTheServer)
            filesOnTheServer = filesOnTheServer.split(', ')
        else:
            changeFlag = True

        print('wtf')

        # the user has now 3 options:
        #   1. download name
        #   2. upload path
        #   3. quit
        # where name is the full name of one of the files on the server and path is the path to a file the user wants to upload

        clientInput = input('>>> ')

        if clientInput.strip().lower() == 'quit':
            sock.send(bytes('quit', 'utf-8'))
            sock.close()
            break


        command = clientInput.split(' ', 1)[0].strip().lower()

        if not command in ['download', 'upload']:
            print('could not interpret the command\n')
            changeFlag = False
        
        if command == 'download':
            # we have to make sure that 
            #   1. the name is valid
            #   2. the file will get a name that won't cause duplicates
            #   3. tell the server what our intention is
            #   4. actually download the file
            
            # the user could have forgotten to provide a name
            if len(clientInput.split()) < 2:
                print('no name given')
                changeFlag = False
            else:
                name = clientInput.split(' ', 1)[1].strip()
                if not name in filesOnTheServer:
                    print(filesOnTheServer)
                    print('The given file does not exist on the server')
                    changeFlag = False
                else:            
                    nameSafe = basicOperations.getDuplicateSafeName(name)
                    sock.send(bytes('download', 'utf-8'))
                    # get an ACK
                    sock.recv(32)
                    sock.send(bytes(name, 'utf-8'))
                    basicOperations.receiveFile(sock, nameSafe)
                    sock.send(bytes('ACK', 'utf-8'))


        elif command == 'upload':
            # we have to
            #   1. make sure the entered path is valid
            #   2. tell the server what we want
            #   3. communicate the name of the file to the server
            #   4. send the file
            
            # the user could have forgotten to give a path
            if len(clientInput.split()) > 1:
                path = clientInput.split(' ', 1)[1].strip() 

                if not os.path.isfile(path):
                    print('the given path is not valid\n')
                    changeFlag = False
                else:
                    sock.send(bytes('upload', 'utf-8'))
                    # get an ACK
                    sock.recv(32)
                    sock.send(bytes(getName(path), 'utf-8'))
                    # get an ACK
                    sock.recv(32)
                    
                    basicOperations.uploadFile(sock, path)

            else:
                print ('no path given')
                changeFlag = False

        

