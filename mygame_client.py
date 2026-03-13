import sys
import zmq
import pygame

from Action import Action
from Game_State import Game_State

def main(name, port, host):
    # connect to server
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(f"tcp://{host}:{port}")
    print(f"Connecting to port '{port}' of host '{host}'.")

    # start pygame
    pygame.init()
    display = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
    pygame.display.set_caption('mygame')
    surface = pygame.display.get_surface()
    clock = pygame.time.Clock()
    background_color = (0,0,0)
    name_textures = Name_Textures()
    game_state = None
    started = False
    font = pygame.font.SysFont('Comic Sans MS', 48)
    small_font = pygame.font.SysFont('Comic Sans MS', 24)
    
    running = True
    while running:
        display.fill(background_color)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if not started and event.type == pygame.KEYDOWN:
                started = True

        if not started:
            # Draw start screen
            title = font.render('MyGame', False, (255, 255, 255))
            prompt = small_font.render('Press Enter to start', False, (255, 255, 255))

            title_rect = title.get_rect(center=(display.get_width() // 2, display.get_height() // 2 - 40))
            prompt_rect = prompt.get_rect(center=(display.get_width() // 2, display.get_height() // 2 + 30))

            surface.blit(title, title_rect)
            surface.blit(prompt, prompt_rect)
        else:
            socket.send_pyobj(get_action(name, pygame.key.get_pressed())) # send action
            if game_state:
                game_state.draw(name,surface,name_textures) # draw while waiting for answer
            game_state = socket.recv_pyobj() # receive game_state
            #print("game_state:",game_state)        

        pygame.display.flip()
        clock.tick(60) # run at 60 frames per second

def get_action(name,keys):
    left = keys[pygame.K_LEFT] or keys[pygame.K_a]
    right = keys[pygame.K_RIGHT] or keys[pygame.K_d]
    jump = keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_SPACE]
    return Action(name, left, right, jump)

class Name_Textures: # class to generate and store textures of user names

    def __init__(self):
        self.name_textures={}

    def get_texture(self, name):
        if not name in self.name_textures:
            font = pygame.font.SysFont('Comic Sans MS', 20)
            name_texture = font.render(name, False, (255,255,255))
            self.name_textures[name] = name_texture
        return self.name_textures[name]
        
if __name__ == "__main__":
    name = "_"
    port = 2345
    host = "127.0.0.1"
    if len(sys.argv)>1:
        name = sys.argv[1]
    if len(sys.argv)>2:
        port = int(sys.argv[2])
    if len(sys.argv)>3:
        host = sys.argv[3]
    main(name, port, host)
