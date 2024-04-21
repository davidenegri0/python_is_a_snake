import pygame
import random

# VARIABLES
DEBUG = False
PLAYER_SIZE = 64
SNAKE_INIT = 3
speed = 500

# pygame setup
pygame.init()
pygame.display.set_caption("Python is a Snake")

screen = pygame.display.set_mode((832, 640))
# screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)
font = pygame.font.Font(pygame.font.get_default_font(), 36)
game_over_screen = font.render("Game Over", True, "black")

clock = pygame.time.Clock()
running = True

n_grid_y = screen.get_height() / PLAYER_SIZE
n_grid_x = screen.get_width() / PLAYER_SIZE

SCREEN_OVERSIZE_V = screen.get_height() % PLAYER_SIZE
SCREEN_OVERSIZE_O = screen.get_width() % PLAYER_SIZE

player_pos = pygame.Vector2(int(n_grid_x / 2) * PLAYER_SIZE , int(n_grid_y / 2) * PLAYER_SIZE)
pygame.time.set_timer(pygame.USEREVENT, speed)
direction = 'left'

print(f"Initial player pos -> X: {player_pos.x} | Y: {player_pos.y}")

grass = pygame.image.load("grass.jpg")

playerSnake = []
for i in range (0, SNAKE_INIT):
    Rect = pygame.Rect(PLAYER_SIZE,PLAYER_SIZE,PLAYER_SIZE,PLAYER_SIZE)
    Rect.x = player_pos.x + (i-1) * PLAYER_SIZE
    Rect.y = player_pos.y
    playerSnake.append(Rect)
    print(f"X: {playerSnake[i].x} | Y: {playerSnake[i].y}")

player_pos = pygame.Vector2(playerSnake[0].x, playerSnake[0].y)

# FUNCTIONS
def check_game_over(head, snake_body):
    if snake_body == []:
        return False
    elif head.x == snake_body[0].x and head.y == snake_body[0].y:
        return True
    else :
        return check_game_over(head, snake_body[1:])

def check_food_eaten(food, snake_head):
    if food.x == snake_head.x and food.y == snake_head.y:
        return True
    else:
        return False

def spawn_food(snake):
    food_x = random.randint(1, n_grid_x-1) * PLAYER_SIZE - PLAYER_SIZE / 2
    food_y = random.randint(1, n_grid_y-1) * PLAYER_SIZE - PLAYER_SIZE / 2
    foodPos = pygame.Rect(food_x - PLAYER_SIZE/2, food_y - PLAYER_SIZE/2, PLAYER_SIZE, PLAYER_SIZE)
    print(f"Food coord : {foodPos.x}, {foodPos.y}")
    if not check_game_over(foodPos, snake) :
        # food = pygame.draw.circle(screen, "red", (food_x, food_y), PLAYER_SIZE)       # QUA C'E' DA FIXARE
        if foodPos.x == 0 or foodPos.y == 0:
            return spawn_food(snake)
        else:
            return foodPos
    else:
        return spawn_food(snake)
    
foodPos = spawn_food(playerSnake)

print(f"Foods pos -> X: {foodPos.x} | Y: {foodPos.y}")

while running:
    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("lightyellow")
    
    # Grid checking
    if DEBUG:
        for i in range(0, int(n_grid_y)):
            pygame.draw.line(screen, "black", (0, i * PLAYER_SIZE), (screen.get_width(), i * PLAYER_SIZE))

        for i in range(0, int(n_grid_x)):
            pygame.draw.line(screen, "black", (i * PLAYER_SIZE, 0), (i * PLAYER_SIZE, screen.get_height()))
        
        pygame.draw.line(screen, "blue", (0, foodPos.y + PLAYER_SIZE/2), (screen.get_width(), foodPos.y + PLAYER_SIZE/2))
        pygame.draw.line(screen, "blue", (foodPos.x + PLAYER_SIZE/2, 0), (foodPos.x + PLAYER_SIZE/2, screen.get_height()))
        
        pygame.draw.line(screen, "blue", (0, player_pos.y + PLAYER_SIZE/2), (screen.get_width(), player_pos.y + PLAYER_SIZE/2))
        pygame.draw.line(screen, "blue", (player_pos.x + PLAYER_SIZE/2, 0), (player_pos.x + PLAYER_SIZE/2, screen.get_height()))
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and direction != 'down':
        direction = 'up'
    if keys[pygame.K_s] and direction != 'up':
        direction = 'down'
    if keys[pygame.K_a] and direction != 'right':
        direction = 'left'
    if keys[pygame.K_d] and direction != 'left':
        direction = 'right'
    
    # Cheching for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == pygame.USEREVENT:
            headRect = playerSnake[0].copy()
            if direction == 'up':
                if player_pos.y <= 0:
                    player_pos.y = screen.get_height() - SCREEN_OVERSIZE_V - PLAYER_SIZE
                else:
                    player_pos.y -= PLAYER_SIZE
            if direction == 'down':
                if player_pos.y >= screen.get_height() - SCREEN_OVERSIZE_V - PLAYER_SIZE:
                    player_pos.y = 0
                else:
                    player_pos.y += PLAYER_SIZE
            if direction == 'left':
                if player_pos.x <= 0:
                    player_pos.x = screen.get_width() - SCREEN_OVERSIZE_O - PLAYER_SIZE
                else:
                    player_pos.x -= PLAYER_SIZE
            if direction == 'right':
                if player_pos.x >= screen.get_width() - SCREEN_OVERSIZE_O - PLAYER_SIZE:
                    player_pos.x = 0
                else:
                    player_pos.x += PLAYER_SIZE
            headRect.x = player_pos.x
            headRect.y = player_pos.y
            
            if check_game_over(headRect, playerSnake):                
                direction = 'none'
                running = False
            
            playerSnake.insert(0, headRect)
            if check_food_eaten(foodPos, playerSnake[0]):
                print("Food eaten")
                foodPos = spawn_food(playerSnake)
                print(f"New foods pos -> X: {foodPos.x} | Y: {foodPos.y}")
            else:
                playerSnake.pop(-1)
            
            # print(f"Foods pos -> X: {food.x} | Y: {food.y}")
            # print(f"Head pos -> X: {playerSnake[0].x} | Y: {playerSnake[0].y}")
            # print(check_food_eaten(food, playerSnake[0]))

    # RENDER YOUR GAME HERE
    for y in range(0, screen.get_height(), grass.get_height()):
        for x in range(0, screen.get_width(), grass.get_width()):
            screen.blit(grass, (x,y))
    
    for i in range(0, len(playerSnake)):
        pygame.draw.rect(surface=screen, color="green", rect=playerSnake[i])
    
    pygame.draw.circle(screen, "red", (foodPos.x + PLAYER_SIZE/2, foodPos.y + PLAYER_SIZE/2), PLAYER_SIZE / 3)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

if direction=="none": 
    screen.blit(game_over_screen, (screen.get_width() / 2 - game_over_screen.get_width() / 2, 32))
    pygame.display.flip()
    pygame.time.wait(2000)
pygame.quit()