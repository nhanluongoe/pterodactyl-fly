import pygame
import os
import time
import random
import math

WIDTH, HEIGHT = 1000, 500
SIZE = WIDTH, HEIGHT

# Load images
player_img_1 = pygame.transform.scale(pygame.image.load(
    os.path.join("images", "fly-1.png")), (70, 70))
player_img_2 = pygame.transform.scale(pygame.image.load(
    os.path.join("images", "fly-2.png")), (70, 70))

t_rex_img_1 = pygame.transform.scale(pygame.image.load(
    os.path.join("images", "t-rex-1.png")), (100, 100))
t_rex_img_2 = pygame.transform.scale(pygame.image.load(
    os.path.join("images", "t-rex-2.png")), (100, 100))

cloud_img_1 = pygame.transform.scale(pygame.image.load(
    os.path.join("images", "cloud-1.png")), (50, 50))
cloud_img_2 = pygame.transform.scale(pygame.image.load(
    os.path.join("images", "cloud-2.png")), (50, 50))
cloud_img_3 = pygame.transform.scale(pygame.image.load(
    os.path.join("images", "cloud-3.png")), (50, 50))

rocket_img = pygame.transform.scale(pygame.image.load(
    os.path.join("images", "rocket.png")), (100, 52))

tree_img_1 = pygame.transform.scale(pygame.image.load(
    os.path.join("images", "tree-1.png")), (100, 100))
tree_img_2 = pygame.transform.scale(pygame.image.load(
    os.path.join("images", "tree-2.png")), (100, 100))
tree_img_3 = pygame.transform.scale(pygame.image.load(
    os.path.join("images", "tree-3.png")), (100, 100))

road_img = pygame.transform.scale(pygame.image.load(
    os.path.join("images", "road.png")), (2*WIDTH, int(HEIGHT/2)))


class Object:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = []
        self.animation = True  # flag for swap image to create animation effect
        self.velocity = 5

    def render(self, screen):
        if self.animation:
            screen.blit(self.img[0], (self.x, self.y))
            self.animation = not self.animation
        else:
            screen.blit(self.img[1], (self.x, self.y))
            self.animation = not self.animation

    def move(self):
        self.x -= self.velocity


class Player(Object):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.img = [player_img_1, player_img_2]
        self.mask = pygame.mask.from_surface(player_img_1)

    def jump(self):
        self.y -= 10

    def drown(self):
        self.y += 3


class Trex(Object):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.img = [t_rex_img_1, t_rex_img_2]
        self.mask = pygame.mask.from_surface(t_rex_img_1)
        self.velocity = 7


class Cloud(Object):
    def __init__(self, x, y, img):
        super().__init__(x, y)
        self.img = img

    def render(self, screen):
        screen.blit(self.img, (self.x, self.y))


class Tree(Object):
    def __init__(self, x, y, img):
        super().__init__(x, y)
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def render(self, screen):
        screen.blit(self.img, (self.x, self.y))


class Rocket(Object):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.img = rocket_img
        self.mask = pygame.mask.from_surface(self.img)
        self.velocity = 10

    def render(self, screen):
        screen.blit(self.img, (self.x, self.y))


class Road:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = road_img
        self.velocity = 5

    def render(self, screen):
        screen.blit(self.img, (self.x, self.y))

    def move(self):
        self.x -= self.velocity


def collide(obj1, obj2):
    offset_x = int(obj2.x - obj1.x)
    offset_y = int(obj2.y - obj1.y)
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


def main():
    run = True
    lost = False
    end_game = False
    lost_time = 0  # time interval between when player died to return to homepage
    fps = 120
    score = 0
    clock = pygame.time.Clock()

    player = Player(50, 360)
    t_rexs = [Trex(WIDTH - t_rex_img_1.get_width() - 20, 340)]
    clouds = [
        Cloud(WIDTH - cloud_img_1.get_width() - 600, 20, cloud_img_1),
        Cloud(WIDTH - cloud_img_1.get_width() - 20, 40, cloud_img_2),
        Cloud(WIDTH - cloud_img_1.get_width() - 250, 80, cloud_img_3),
        Cloud(WIDTH - cloud_img_1.get_width() - 400, 120, cloud_img_1)
    ]
    roads = [Road(0, 240)]
    rockets = [
        Rocket(2*WIDTH, 40)
    ]
    trees = [
        Tree(WIDTH, 330, tree_img_1),
        Tree(WIDTH * 1.2, 330, tree_img_2),
        Tree(WIDTH * 2.3, 330, tree_img_3)
    ]

    # Initialize screen
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Jumping T-Rex")

    # Initialize font
    pygame.font.init()
    score_font = pygame.font.Font(os.path.join("fonts", "pixel.ttf"), 30)
    lost_font = pygame.font.Font(os.path.join("fonts", "pixel.ttf"), 60)

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    def on_render():
        # render background
        screen.blit(background, (0, 0))

        # render text label
        score_label = score_font.render(
            "Score: {}".format(math.floor(score)), 1, (0, 0, 0))
        screen.blit(score_label, (WIDTH - score_label.get_width() - 10, 10))

        # render infinity road
        for road in roads:
            road.render(screen)

        # render trees
        for tree in trees:
            tree.render(screen)

        # render clouds
        for cloud in clouds:
            cloud.render(screen)

        # render t-rex
        for t_rex in t_rexs:
            t_rex.render(screen)

        # render rocket
        for rocket in rockets:
            rocket.render(screen)

        # render player
        player.render(screen)

        if lost:
            lost_label = lost_font.render("Game Over!", 1, (0, 0, 0))
            screen.blit(
                lost_label, (WIDTH/2 - lost_label.get_width()/2, HEIGHT/2))

        pygame.display.update()

    # Event loop
    while run:
        clock.tick(fps)
        on_render()

        score += 0.2

        if end_game:
            lost = True
            lost_time += 1

        if lost:
            if lost_time > fps:
                run = False
            else:
                continue

        for t_rex in t_rexs:
            t_rex.move()
            if t_rex.x < -10:
                t_rex.x = WIDTH*random.randrange(1, 3)
                t_rex.velocity = random.randrange(7, 10)
            if collide(player, t_rex):
                end_game = True

        for cloud in clouds:
            cloud.move()
            if cloud.x < - 10:
                cloud.x = WIDTH*random.randrange(1, 5)

        for rocket in rockets:
            rocket.move()
            if rocket.x < - 10:
                rocket.x = WIDTH*random.randrange(1, 5)
                rocket.y = random.randrange(20, 360)
                rocket.velocity = random.randrange(6, 20)
            if collide(player, rocket):
                end_game = True

        for tree in trees:
            tree.move()
            if tree.x < -10:
                tree.x = WIDTH * random.randrange(1, 3)
            if collide(player, tree):
                end_game = True

        for road in roads:
            road.move()
            if road.x == -WIDTH:
                roads.append(Road(WIDTH, 240))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN] and player.y < 360:
            player.y += 8
        if keys[pygame.K_SPACE] and player.y > 0:
            player.jump()
        if (not keys[pygame.K_SPACE]) and (not keys[pygame.K_DOWN]) and player.y < 360:
            player.drown()


def home():
    # Initialize font
    pygame.font.init()
    title_font = pygame.font.Font(os.path.join("fonts", "pixel.ttf"), 70)

    # Initialize screen
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Jumping T-Rex")

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    # Event loop
    run = True
    while run:
        screen.blit(background, (0, 0))
        title_label = title_font.render(
            "Press the space to begin...", 1, (0, 0, 0))
        screen.blit(title_label, (WIDTH/2 - title_label.get_width() /
                                  2, HEIGHT/2 - title_label.get_height()/2))

        pygame.display.update()
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if keys[pygame.K_SPACE]:
                main()


if __name__ == '__main__':
    home()
