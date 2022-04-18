import pygame
import random

# Initialize pygame
pygame.init()

# Get display info
pygame_info = pygame.display.Info()

# Create a display surface and display its caption
WINDOW_WIDTH = pygame_info.current_w
WINDOW_HEIGHT = pygame_info.current_h
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Beer catcher!")

# Set game values
BUFFER_DISTANCE = 100

# Set FPS and clock
FPS = 60
clock = pygame.time.Clock()


class Game:
    """A class to manage and run the game"""

    def __init__(self, beer_bottle_group):
        self.beer_bottle_group = beer_bottle_group
        # self.beer_bottle = beer_bottle
        self.beer_box = beer_box

        # Set game values
        self.STARTING_SCORE = 0
        self.score = self.STARTING_SCORE

        # Set font
        self.font = pygame.font.Font("Assets/Fonts/Franxurter.ttf", 32)

        # Create the beer bottles
        for i in range((WINDOW_WIDTH // 6) // 64, (WINDOW_WIDTH - WINDOW_WIDTH // 6) // 64):
            self.beer_bottle = BeerBottle(i * 64, 10, self.beer_bottle_group)
            self.beer_bottle_group.add(self.beer_bottle)

    def update(self):
        self.side_images()
        self.check_collision_beer_box()
        self.check_missed_bottle()
        self.check_game_over()

    def check_collision_beer_box(self):
        if pygame.sprite.spritecollide(self.beer_box, self.beer_bottle_group, True):
            self.score += 1
            self.beer_bottle = BeerBottle(
                random.randrange((WINDOW_WIDTH // 6) // 64, (WINDOW_WIDTH - WINDOW_WIDTH // 6) // 64) * 64, 10,
                beer_bottle_group)
            beer_bottle_group.add(self.beer_bottle)

    def check_missed_bottle(self):
        for beer in (self.beer_bottle_group.sprites()):
            if beer.rect.top >= WINDOW_HEIGHT:
                self.beer_box.lives -= 1

                beer.kill()
                self.beer_bottle = BeerBottle(
                    random.randrange((WINDOW_WIDTH // 6) // 64, (WINDOW_WIDTH - WINDOW_WIDTH // 6) // 64) * 64, 10,
                    self.beer_bottle_group)
                self.beer_bottle_group.add(self.beer_bottle)

    def side_images(self):
        """Load and change side images"""
        # list of images
        self.images_list = []

        self.images_list.append(pygame.image.load("Assets/Images/sides/1.png"))
        self.images_list.append(pygame.image.load("Assets/Images/sides/2.png"))
        self.images_list.append(pygame.image.load("Assets/Images/sides/3.png"))
        self.images_list.append(pygame.image.load("Assets/Images/sides/4.png"))
        self.images_list.append(pygame.image.load("Assets/Images/sides/5.png"))

        if self.score >= 200:
            self.image = self.images_list[4]

            self.beer_bottle.beer_bottle_velocity_max_range += 1

        elif self.score == 150:
            self.image = self.images_list[3]

            self.beer_bottle.beer_bottle_velocity_max_range += 1

        elif self.score == 100:
            self.image = self.images_list[2]

            self.beer_bottle.beer_bottle_velocity_max_range += 1

        elif self.score == 50:
            self.image = self.images_list[1]

            self.beer_bottle.beer_bottle_velocity_max_range += 1

        elif self.score == 0:
            self.image = self.images_list[0]

        # initial image size
        initial_width = self.image.get_width()
        initial_height = self.image.get_height()

        # desired image scale
        self.image_width = WINDOW_WIDTH // 6 - 32
        self.image = pygame.transform.scale((self.image), (self.image_width, int(initial_width / self.image_width *
                                                                                 initial_height)))

        # draw images
        self.rect_right = self.image.get_rect()
        self.rect_right.midleft = (((WINDOW_WIDTH // 6) * 5 + 32), WINDOW_HEIGHT // 2)
        display_surface.blit(self.image, self.rect_right)

        self.rect_left = self.image.get_rect()
        self.rect_left.midleft = (0, WINDOW_HEIGHT // 2)
        display_surface.blit(self.image, self.rect_left)

    def draw(self):

        # Set colors
        BLUE = (1, 175, 209)
        YELLOW = (248, 231, 28)

        # Set text
        score_text = self.font.render("Score: " + str(self.score), True, YELLOW)
        score_rect = score_text.get_rect()
        score_rect.topleft = (50, 10)

        lives_text = self.font.render("Lives: " + str(self.beer_box.lives), True, BLUE)
        lives_rect = lives_text.get_rect()
        lives_rect.topleft = (50, 50)

        # Blit text
        display_surface.blit(score_text, score_rect)
        display_surface.blit(lives_text, lives_rect)

        # Draw ground
        pygame.draw.line(display_surface, (255, 255, 255), (0, WINDOW_HEIGHT - 3), (WINDOW_WIDTH, WINDOW_HEIGHT - 3), 1)

    def check_game_over(self):
        """Check to see if the player lost the game"""
        if self.beer_box.lives <= 0:
            self.pause_game("Game over! Final Score: " + str(self.score), "Press 'Enter' to play again...")
            self.reset_game()

    def pause_game(self, main_text, sub_text):
        """Pause the game"""
        global running

        # Set colors
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        GREEN = (25, 200, 25)

        # Create main pause text
        main_text = self.font.render(main_text, True, GREEN)
        main_rect = main_text.get_rect()
        main_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

        # Create sub pause text
        sub_text = self.font.render(sub_text, True, WHITE)
        sub_rect = sub_text.get_rect()
        sub_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 64)

        # Display the pause text
        display_surface.fill(BLACK)
        display_surface.blit(main_text, main_rect)
        display_surface.blit(sub_text, sub_rect)
        pygame.display.update()

        # Pause the game until user hits enter or quits
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    # User wants to continue
                    if event.key == pygame.K_RETURN:
                        is_paused = False

                # User wants to quit
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False
                # Quit game when pressing Q
                if pygame.key.get_pressed()[pygame.K_q]:
                    is_paused = False
                    running = False

    def reset_game(self):
        """Reset the game"""
        self.score = self.STARTING_SCORE
        self.beer_box.lives = self.beer_box.STARTING_LIVES
        self.beer_bottle_group.empty()
        self.beer_bottle.beer_bottle_velocity_max_range = 5
        # Create the beer bottles
        for i in range((WINDOW_WIDTH // 6) // 64, (WINDOW_WIDTH - WINDOW_WIDTH // 6) // 64):
            self.beer_bottle = BeerBottle(i * 64, 10, self.beer_bottle_group)
            self.beer_bottle_group.add(self.beer_bottle)


class BeerBox(pygame.sprite.Sprite):
    """A class to represent a beer box"""

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Assets/Images/beer_box.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = WINDOW_WIDTH // 2
        self.rect.bottom = WINDOW_HEIGHT

        self.STARTING_LIVES = 5
        self.lives = self.STARTING_LIVES

        self.velocity = 10

    def update(self):
        """Update the player"""
        self.move()

    def draw(self):
        display_surface.blit(self.image, self.rect)

    def move(self):
        """Move the player continuously"""

        # Move with left and right arrows
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            if self.rect.centerx > 0:
                self.rect.centerx -= self.velocity
        if keys[pygame.K_RIGHT]:
            if self.rect.centerx < WINDOW_WIDTH:
                self.rect.centerx += self.velocity

        # Move with mouse on x axis
        if event.type == pygame.MOUSEMOTION and 0 < event.pos[0] < WINDOW_WIDTH:
            pygame.mouse.set_visible(False)
            mouse_x = event.pos[0]
            self.rect.centerx = mouse_x


class BeerBottle(pygame.sprite.Sprite):
    """A class to represent a beer bottle"""

    def __init__(self, x, y, beer_bottle_group):
        super().__init__()
        self.image = pygame.image.load("Assets/Images/beer_bottle.png")
        self.rect = self.image.get_rect()
        self.rect.midtop = (x, y - BUFFER_DISTANCE)
        self.beer_botle_group = beer_bottle_group

        self.beer_bottle_velocity_max_range = 5
        self.velocity = random.randint(1, self.beer_bottle_velocity_max_range)

    def update(self):
        """Update and move the bottle"""
        self.rect.y += self.velocity


# Create a beer bottle group
beer_bottle_group = pygame.sprite.Group()

# # Create a beerBox object
beer_box = BeerBox()

# Create a game object
my_game = Game(beer_bottle_group)

# The main game loop
running = True
while running:
    # Loop through a list of Event objects that have occurred
    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            running = False

    # Quit game when pressing Q
    if pygame.key.get_pressed()[pygame.K_q]:
        running = False

    # Fill the display
    display_surface.fill((0, 0, 0))

    # # Update and Draw assets
    beer_box.update()
    beer_box.draw()

    beer_bottle_group.update()
    beer_bottle_group.draw(display_surface)

    # Update the game
    my_game.update()
    my_game.draw()

    # Update the display and tick the clock
    pygame.display.update()
    clock.tick(FPS)

# End the game
pygame.quit()
