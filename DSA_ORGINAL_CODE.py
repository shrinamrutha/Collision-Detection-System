import pygame
import math
pygame.init()
WIDTH, HEIGHT = 1100, 600
FPS = 60
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GREY = (150, 150, 150)
class QuadTree:
    def __init__(self, boundary, capacity):
        self.boundary = boundary
        self.capacity = capacity
        self.objects = []
        self.divided = False
    def subdivide(self):
        x, y, w, h = self.boundary
        nw = (x, y, w / 2, h / 2)
        ne = (x + w / 2, y, w / 2, h / 2)
        sw = (x, y + h / 2, w / 2, h / 2)
        se = (x + w / 2, y + h / 2, w / 2, h / 2)
        self.northwest = QuadTree(nw, self.capacity)
        self.northeast = QuadTree(ne, self.capacity)
        self.southwest = QuadTree(sw, self.capacity)
        self.southeast = QuadTree(se, self.capacity)
        self.divided = True
    def insert(self, obj):
        if not self.in_boundary(obj.rect):
            return False
        if len(self.objects) < self.capacity:
            self.objects.append(obj)
            return True
        else:
            if not self.divided:
                self.subdivide()
            if self.northwest.insert(obj):
                return True
            elif self.northeast.insert(obj):
                return True
            elif self.southwest.insert(obj):
                return True
            elif self.southeast.insert(obj):
                return True
    def in_boundary(self, rect):
        x, y, _, _ = self.boundary
        return x < rect.x + rect.width and x + self.boundary[2] > rect.x and y < rect.y + rect.height and y + self.boundary[3] > rect.y
    def query(self, rect):
        found = []
        if not self.boundary_intersect(rect):
            return found
        for obj in self.objects:
            if isinstance(obj, pygame.sprite.Sprite) and rect.colliderect(obj.rect):
                found.append(obj)
        if self.divided:
            found.extend(self.northwest.query(rect))
            found.extend(self.northeast.query(rect))
            found.extend(self.southwest.query(rect))
            found.extend(self.southeast.query(rect))
        return found
    def boundary_intersect(self, rect):
        x, y, w, h = self.boundary
        return not (x > rect.x + rect.width or x + w < rect.x or y > rect.y + rect.height or y + h < rect.y)
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, automated_paths):
        super().__init__()
        self.image = pygame.image.load(r"C:\Users\Shri Namrutha\Pictures\dsa\stickman20x29.png").convert_alpha()  # Replace with the path to your human image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5
        self.automated_paths = automated_paths
        self.current_path_index = 0
        self.current_point_index = 0
        self.current_path = self.automated_paths[self.current_path_index]

    def update(self):
        keys = pygame.key.get_pressed()

        if any(keys):  # Check if any arrow keys are pressed
            # Move in the automated path
            target_x, target_y = self.current_path[self.current_point_index]
            dx = target_x - self.rect.x
            dy = target_y - self.rect.y
            distance = math.sqrt(dx ** 2 + dy ** 2)

            if distance > self.speed:
                angle = math.atan2(dy, dx)
                self.rect.x += int(self.speed * math.cos(angle))
                self.rect.y += int(self.speed * math.sin(angle))
            else:
                self.current_point_index = (self.current_point_index + 1) % len(self.current_path)
                if self.current_point_index == 0:
                    self.current_path_index = (self.current_path_index + 1) % len(self.automated_paths)
                    self.current_path = self.automated_paths[self.current_path_index]


class AutomatedObject(pygame.sprite.Sprite):
    def __init__(self, x, y, z, path):
        super().__init__()
        self.image = pygame.Surface((15, 15))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.z = z
        self.speed = 3
        self.path = path
        self.current_point_index = 0
        self.collision_occurred = False
    def update(self):
        target_x, target_y = self.path[self.current_point_index]
        dx = target_x - self.rect.x
        dy = target_y - self.rect.y
        distance = math.sqrt(dx**2 + dy**2)
        if distance > self.speed:
            angle = math.atan2(dy, dx)
            self.rect.x += int(self.speed * math.cos(angle))
            self.rect.y += int(self.speed * math.sin(angle))
        else:
            self.current_point_index = (self.current_point_index + 1) % len(self.path)
        if self.collision_occurred and not self.rect.colliderect(player.rect):
            self.collision_occurred = False
            self.image.fill(RED)
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super().__init__()
        self.original_image = pygame.image.load(image_path).convert_alpha()
        # Resize the image to 30x30
        self.original_image = pygame.transform.scale(self.original_image, (60, 60))
        self.image = self.original_image.copy()  # Store the original image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.collision_occurred = False

    def update(self):
        if self.collision_occurred and not self.rect.colliderect(player.rect):
            self.collision_occurred = False
            # Restore the original image after collision
            self.image = self.original_image.copy()

class House(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
# Usage:
tree_image_path = r"C:\Users\Shri Namrutha\Pictures\dsa\tree30x30.png"
car_image_path = r"C:\Users\Shri Namrutha\Pictures\dsa\car30x30.png" 
house_image_path = r"C:\Users\Shri Namrutha\Pictures\dsa\house60x60.png"


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Collision Detection")
clock = pygame.time.Clock()
# Create house instances
house1 = House(50, 50, house_image_path)
house2 = House(750, 50, house_image_path)
# Add house instances to the sprite group
houses = pygame.sprite.Group()
houses.add(house1, house2)

path_automated_object1 = [(200, 100), (200, 500), (600, 500), (600, 100), (200, 100)]
path_automated_object2 = [(400, 200), (400, 400), (600, 400), (600, 200), (400, 200)]
path_automated_object3 = [(300, 300), (500, 300), (500, 500), (300, 500), (300, 300)]
path_automated_object4 = [(100, 400), (300, 400), (300, 600), (100, 600), (100, 400)]
path_automated_object5 = [(500, 100), (700, 100), (700, 300), (500, 300), (500, 100)]
path_automated_object6 = [(200, 500), (400, 500), (400, 700), (200, 700), (200, 500)]
path_automated_object7 = [(600, 200), (800, 200), (800, 400), (600, 400), (600, 200)]
path_automated_object8 = [(100, 100), (300, 100), (300, 300), (100, 300), (100, 100)]
path_automated_object9 = [(700, 400), (900, 400), (900, 600), (700, 600), (700, 400)]
path_automated_object10 = [(400, 700), (600, 700), (600, 900), (400, 900), (400, 700)]
# Create a list of paths for automated objects
paths_automated_objects = [
    path_automated_object1,
    path_automated_object2,
    path_automated_object3,
    path_automated_object4,
    path_automated_object5,
    path_automated_object6,
    path_automated_object7,
    path_automated_object8,
    path_automated_object9,
    path_automated_object10,
]
orange_obstacle1 = Obstacle(300, 100,car_image_path)
orange_obstacle2 = Obstacle(500, 200,car_image_path)
orange_obstacle3 = Obstacle(400, 300,car_image_path)
orange_obstacle4 = Obstacle(600, 500,car_image_path)


green_obstacle1 = Obstacle(200, 300,tree_image_path )  # Green color
green_obstacle2 = Obstacle(500, 400, tree_image_path)  # Green color
green_obstacle3 = Obstacle(700, 500, tree_image_path)  # Green color
green_obstacle4 = Obstacle(900, 400, tree_image_path)  # Green color
green_obstacle5 = Obstacle(400, 200, tree_image_path)  # Green color


# Create player with automated paths
player = Player(WIDTH // 4, HEIGHT // 2, paths_automated_objects)
automated_object1 = AutomatedObject(WIDTH // 1.5, HEIGHT // 2, 0, path_automated_object1)
automated_object2 = AutomatedObject(WIDTH // 1.5, HEIGHT // 2, 0, path_automated_object2)
automated_object3 = AutomatedObject(WIDTH // 1.5, HEIGHT // 2, 0, path_automated_object3)
automated_object4 = AutomatedObject(WIDTH // 1.5, HEIGHT // 2, 0, path_automated_object4)
automated_object5 = AutomatedObject(WIDTH // 1.5, HEIGHT // 2, 0, path_automated_object5)
automated_object6 = AutomatedObject(WIDTH // 1.5, HEIGHT // 2, 0, path_automated_object6)
automated_object7 = AutomatedObject(WIDTH // 1.5, HEIGHT // 2, 0, path_automated_object7)
automated_object8 = AutomatedObject(WIDTH // 1.5, HEIGHT // 2, 0, path_automated_object8)
automated_object9 = AutomatedObject(WIDTH // 1.5, HEIGHT // 2, 0, path_automated_object9)
automated_object10 = AutomatedObject(WIDTH // 1.5, HEIGHT // 2, 0, path_automated_object10)

# Add obstacles to all_sprites group

all_sprites = pygame.sprite.Group()
all_sprites.add(player, green_obstacle1, green_obstacle2,green_obstacle3,green_obstacle4,green_obstacle5,orange_obstacle1,orange_obstacle2,orange_obstacle3,orange_obstacle4)
all_sprites.add(player, automated_object1, automated_object2,
                automated_object3, automated_object4, automated_object5,
                automated_object6, automated_object7, automated_object8,
                automated_object9, automated_object10)
quadtree_boundary = (0, 0, WIDTH, HEIGHT)
quadtree = QuadTree(quadtree_boundary, 4)
collision_counter=0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    all_sprites.update()
    houses.update() 
    for obstacle in [green_obstacle1, green_obstacle2,green_obstacle3, green_obstacle4,green_obstacle5, orange_obstacle1, orange_obstacle2, orange_obstacle3, orange_obstacle4]:  # Add more obstacles as needed
        quadtree.insert(obstacle)

    quadtree.objects.clear()
    quadtree.divided = False
    # Insert all objects into the QuadTree for collision detection
    
    
    
    for sprite in all_sprites:
        quadtree.insert(sprite)
    potential_collisions = quadtree.query(player.rect)
    for sprite in potential_collisions:
        if (
            sprite != player
            and player.rect.colliderect(sprite.rect)
            and (isinstance(sprite, AutomatedObject) or isinstance(sprite, Obstacle))
            and not sprite.collision_occurred
        ):
            print("Collision Detected!")
            collision_counter += 1

            if isinstance(sprite, AutomatedObject):
                sprite.collision_occurred = True
                sprite.image.fill(BLUE)  # Change color to blue on collision
            elif isinstance(sprite, Obstacle):
                sprite.collision_occurred = True
                sprite.image.fill(BLUE)
                
    screen.fill((0, 0, 0))
    
    pygame.draw.lines(screen, GREY, False, path_automated_object1, 50)
    pygame.draw.lines(screen, GREY, False, path_automated_object2, 50)
    pygame.draw.lines(screen, GREY, False, path_automated_object3, 50)
    pygame.draw.lines(screen, GREY, False, path_automated_object4, 50)
    pygame.draw.lines(screen, GREY, False, path_automated_object5, 50)
    pygame.draw.lines(screen, GREY, False, path_automated_object6, 50)
    pygame.draw.lines(screen, GREY, False, path_automated_object7, 50)
    pygame.draw.lines(screen, GREY, False, path_automated_object8, 50)
    pygame.draw.lines(screen, GREY, False, path_automated_object9, 50)
    pygame.draw.lines(screen, GREY, False, path_automated_object10, 50)
    all_sprites.draw(screen)
    houses.draw(screen)
    font = pygame.font.Font(None, 36)
    text = font.render(f"Collisions: {collision_counter}", True, WHITE)
    screen.blit(text, (10, 10))
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()



