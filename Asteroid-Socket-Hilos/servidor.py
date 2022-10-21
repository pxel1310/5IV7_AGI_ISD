import socket
import threading

connections = []
total_connections = 0

class Client(threading.Thread):
    def __init__(self, socket, address, id, name, signal):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self.id = id
        self.name = name
        self.signal = signal
    
    def __str__(self):
        return str(self.id) + " " + str(self.address)
    
    def run(self, dataArr = []):

        
        while self.signal:
            try:
                data = self.socket.recv(32)
            except:
                print("CLiente " + str(self.address) + " se ha desconectado")
                self.signal = False
                connections.remove(self)
                break
            
            if data != "":
                bat = data.decode("utf-8")
                arbat = bat.split(",")

                dataArr.insert(0, arbat[0])
                
                print(f"{arbat[1]} obtuvo: {arbat[0]} puntos")
                maxVa = max(dataArr)
     
                print(f'El usuario {arbat[1]} su mayor puntuacion es de {maxVa} puntos')
                
                print("-----------------")
                for client in connections:
                    if client != self:
                        client.socket.send(data)

                for client in connections:
                    if client.id != self.id:
                        client.socket.sendall(data)


def newConnections(socket):
    while True:
        sock, address = socket.accept()
        global total_connections
        connections.append(Client(sock, address, total_connections, "Name", True))
        connections[len(connections) - 1].start()
        print("Nuevo CLiente at ID " + str(connections[len(connections) - 1]))
        total_connections += 1

def main():
    #Get host and port
    host = socket.gethostbyname(socket.gethostname())
    port = 6969

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(5)

    print(f"Servidor iniciado en {host}:{port}")
    print("Esperando conexiones...")

    newConnectionsThread = threading.Thread(target = newConnections, args = (sock,))
    newConnectionsThread.start()
    
main()