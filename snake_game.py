import pygame
import random
from settings import PLAYER_SIZE, SNAKE_INIT_SIZE, DEBUG
from settings import GRASS_SPRITE, SNAKE_HEAD_SPRITE, SNAKE_BODY_SPRITE, SNAKE_TAIL_SPRITE, MUSIC
from sprites_classes import Egg, Snake_part

# VARIABLES
score = 0
speed = 500

# pygame setup
pygame.init()
pygame.display.set_caption("Python is a Snake")

# Screen size setup
screen = pygame.display.set_mode((832, 640))

# Text overlays setup
font = pygame.font.Font(pygame.font.get_default_font(), 36)
score_screen = font.render(f"Score: {score}", True, "black")    
game_over_screen = font.render("Game Over", True, "black")

# Background load and setup
grass = pygame.image.load(GRASS_SPRITE)

# Music setup
pygame.mixer.music.load(MUSIC)
pygame.mixer.music.play(-1)

# Game loop basic configuration
clock = pygame.time.Clock()
running = True

# Grid setup
n_grid_y = screen.get_height() / PLAYER_SIZE
n_grid_x = screen.get_width() / PLAYER_SIZE
SCREEN_OVERSIZE_V = screen.get_height() % PLAYER_SIZE
SCREEN_OVERSIZE_O = screen.get_width() % PLAYER_SIZE

# Player movement setup
player_pos = pygame.Vector2(int(n_grid_x / 2) * PLAYER_SIZE , int(n_grid_y / 2) * PLAYER_SIZE)
pygame.time.set_timer(pygame.USEREVENT, speed)
direction = 'left'

snake = pygame.sprite.Group()

# PLAYER INITIALIZATION (SNAKE)
print(f"Initial player pos -> X: {player_pos.x} | Y: {player_pos.y}")
playerSnake = []
for i in range (0, SNAKE_INIT_SIZE):
    if i == 0:
        snk_p = Snake_part(SNAKE_HEAD_SPRITE)
    elif i == SNAKE_INIT_SIZE - 1:
        snk_p = Snake_part(SNAKE_TAIL_SPRITE)
    else:
        snk_p = Snake_part(SNAKE_BODY_SPRITE)
    snk_p.rect.x = player_pos.x + i * PLAYER_SIZE
    snk_p.rect.y = player_pos.y
    snake.add(snk_p)

player_pos = pygame.Vector2(snake.sprites()[0].rect.x, snake.sprites()[0].rect.y)

# FUNCTIONS
def check_game_over(head, snake_body):
    if snake_body == []:
        return False
    elif head.x == snake_body[0].rect.x and head.y == snake_body[0].rect.y:
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
    if DEBUG:
        print(f"Food coord : {foodPos.x}, {foodPos.y}")
    if not check_game_over(foodPos, snake) :
        # food = pygame.draw.circle(screen, "red", (food_x, food_y), PLAYER_SIZE)       # QUA C'E' DA FIXARE
        if foodPos.x == 0 or foodPos.y == 0:
            return spawn_food(snake)
        else:
            return foodPos
    else:
        return spawn_food(snake)

# FOOD INITIALIZATION
foodPos = spawn_food(playerSnake)
egg = Egg(foodPos)
if DEBUG:
    print(f"Foods pos -> X: {foodPos.x} | Y: {foodPos.y}")

# Main game loop
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
    
    # Keyboard input control
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and direction != 'down':
        direction = 'up'
    if keys[pygame.K_s] and direction != 'up':
        direction = 'down'
    if keys[pygame.K_a] and direction != 'right':
        direction = 'left'
    if keys[pygame.K_d] and direction != 'left':
        direction = 'right'
    
    # Cheching for events (close window, movement)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == pygame.USEREVENT:
            snake_sprites = snake.sprites()
            headRect = snake_sprites[0].rect.copy()
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
            
            if DEBUG:
                print(f"Head pos -> X: {headRect.x} | Y: {headRect.y}")

            snake_sprites.insert(0, Snake_part(SNAKE_HEAD_SPRITE, headRect, direction))
            snake_sprites[1] = Snake_part(SNAKE_BODY_SPRITE, snake_sprites[1].rect, snake_sprites[1].rotation)

            if DEBUG:
                for sprite in snake_sprites:
                    print(f"Sprite pos -> X: {sprite.rect.x} | Y: {sprite.rect.y}")

            if check_food_eaten(foodPos, snake_sprites[0].rect):
                print("Food eaten")
                score = score + 1
                score_screen = font.render(f"Score: {score}", True, "black") 
                foodPos = spawn_food(snake_sprites)
                print(f"New foods pos -> X: {foodPos.x} | Y: {foodPos.y}")
            else:
                snake_sprites.pop(-1)
                snake_sprites[-1] = Snake_part(SNAKE_TAIL_SPRITE, snake_sprites[-1].rect, snake_sprites[-2].rotation)

            if check_game_over(snake_sprites[0].rect, snake_sprites[1:]):                
                direction = 'none'
                running = False

            snake.empty()
            snake.add(snake_sprites)

    # RENDER YOUR GAME HERE
    for y in range(0, screen.get_height(), grass.get_height()):
        for x in range(0, screen.get_width(), grass.get_width()):
            screen.blit(grass, (x,y))
    
    screen.blit(egg.image, (foodPos.x, foodPos.y))
    snake.draw(screen)

    if direction=="none":
        screen.blit(game_over_screen, (screen.get_width() / 2 - game_over_screen.get_width() / 2, 32))
        final_score_screen = font.render(f"Final score: {score}", True, "black")
        screen.blit(final_score_screen, (screen.get_width() / 2 - final_score_screen.get_width() / 2, 64))
    else:
        screen.blit(score_screen, (screen.get_width() / 2 - game_over_screen.get_width() / 2, 32))
    
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

if direction=="none": 
    pygame.display.flip()
    pygame.mixer.music.fadeout(2000)
    pygame.time.wait(2000)
pygame.quit()