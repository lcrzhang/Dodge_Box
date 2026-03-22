import zmq
import threading
import time

class NetworkClient:
    """Manages the network connection to the game server using a background thread and ZeroMQ."""
    
    def __init__(self, host: str, port: str):
        """Initializes the ZeroMQ context and starts the network thread."""
        self.host = host
        self.port = port
        self.context = zmq.Context()
        
        self.latest_game_state = None
        self.action_to_send = None
        self.lock = threading.Lock()
        self.running = True
        
        self.thread = threading.Thread(target=self._network_loop, daemon=True)
        self.thread.start()
        print(f"NetworkClient thread started for 'tcp://{host}:{port}'.")

    def _network_loop(self):
        socket = self.context.socket(zmq.REQ)
        socket.connect(f"tcp://{self.host}:{self.port}")
        
        # Use a poller to safely wait for replies without blocking forever
        poller = zmq.Poller()
        poller.register(socket, zmq.POLLIN)
        
        while self.running:
            with self.lock:
                act = self.action_to_send
                
            if act is not None:
                try:
                    # Send action
                    socket.send_pyobj(act)
                    
                    # Wait for response, checking running status every 100ms
                    while self.running:
                        events = dict(poller.poll(100))
                        if socket in events:
                            new_state = socket.recv_pyobj()
                            with self.lock:
                                self.latest_game_state = new_state
                            break
                except Exception:
                    pass
            else:
                time.sleep(0.01) # idle sleep

        socket.setsockopt(zmq.LINGER, 0)
        socket.close()

    def send_action(self, action):
        """Queues an Action object to be sent to the server in the background."""
        with self.lock:
            self.action_to_send = action

    def receive_game_state(self):
        """Returns the latest Game_State received from the server. Non-blocking."""
        with self.lock:
            return self.latest_game_state
            
    def send_disconnect_action(self, action):
        """Sends a disconnect action and terminates the network thread."""
        self.running = False
        self.thread.join(timeout=1.0)
        try:
            # We use a completely new socket inline so the thread shutdown is clean
            sock = self.context.socket(zmq.REQ)
            sock.setsockopt(zmq.LINGER, 0)
            sock.connect(f"tcp://{self.host}:{self.port}")
            sock.send_pyobj(action)
            
            poller = zmq.Poller()
            poller.register(sock, zmq.POLLIN)
            if dict(poller.poll(500)):  # 500ms timeout for graceful disconnect
                sock.recv_pyobj()
            sock.close()
        except Exception:
            pass
        self.context.term()
