import pygame
import math
import random
import os
from rrt import rrt

# ------------ Setup ------------
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Autonomous Car Navigation with RRT Pathfinding")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
RED   = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW= (255, 255, 0)
GREY  = (128, 128, 128)

# ------------ Car image ------------
car_width, car_height = 30, 30
car_image = None
image_path = os.path.join(os.path.dirname(__file__), "..", "assets", "car.png")  
try:
    car_image = pygame.image.load(image_path)
    car_image = pygame.transform.scale(car_image, (car_width, car_height))
except Exception as e:
    # Fallback: a simple surface if image not found
    car_image = pygame.Surface((car_width, car_height), pygame.SRCALPHA)
    car_image.fill((30, 120, 200))

# ------------ Car state ------------
car_x, car_y = 15, HEIGHT // 2  # center coordinates
car_angle = 0.0
car_speed = 140.0  # pixels per second (use dt for smooth motion)

# ------------ Obstacles ------------
obstacle_size = 20
num_obstacles = 40
margin = 6  

# ------------ Target ------------
target_radius = 15
target_x = WIDTH - target_radius * 2 - 10
target_y = HEIGHT // 2

def generate_random_distributed_obstacles(num_obstacles, obstacle_size, width, height, car_rect, target_rect):
    obstacles = []
    attempts = 0
    max_attempts = num_obstacles * 50
    while len(obstacles) < num_obstacles and attempts < max_attempts:
        attempts += 1
        x = random.randint(0, width - obstacle_size)
        y = random.randint(0, height - obstacle_size)
        new_ob = pygame.Rect(x, y, obstacle_size, obstacle_size)
  
        new_ob_infl = new_ob.inflate(margin, margin)
        if any(new_ob_infl.colliderect(ex) for ex in obstacles):
            continue
        if new_ob_infl.colliderect(car_rect) or new_ob_infl.colliderect(target_rect):
            continue
        obstacles.append(new_ob)
    return obstacles

# Build centered rects for car & target (for obstacle placement only)
car_rect_place = pygame.Rect(car_x - car_width//2, car_y - car_height//2, car_width, car_height)
target_rect_place = pygame.Rect(target_x - target_radius, target_y - target_radius, target_radius*2, target_radius*2)

obstacle_list = generate_random_distributed_obstacles(
    num_obstacles, obstacle_size, WIDTH, HEIGHT, car_rect_place, target_rect_place
)


obstacle_list_for_rrt = obstacle_list

# ------------ Pathfinding state ------------
path_found = False
path = []
current_waypoint_index = 0

running = True
while running:
    dt = clock.tick(60) / 1000.0 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)

    # Draw obstacles
    for obstacle in obstacle_list:
        pygame.draw.rect(screen, GREY, obstacle)

    # Draw target (outlined circle)
    pygame.draw.circle(screen, GREEN, (target_x, target_y), target_radius, 5)

    # Compute RRT path once
    if not path_found:
        path = rrt(
            start=(int(car_x), int(car_y)),
            goal=(int(target_x), int(target_y)),
            obstacles=obstacle_list_for_rrt,
            map_dim=(WIDTH, HEIGHT),
            car_size=(car_width, car_height),
            step_size=20,
            max_iter=1000,
            screen=screen,    
            car_image=car_image  =
        )
        if path and len(path) > 0:
           
            path = [(int(px), int(py)) for (px, py) in path]
            path_found = True
            current_waypoint_index = 0
        else:
          
            print("No path found. Try reducing obstacles, increasing max_iter, or step_size.")
            running = False

    # Visualize waypoints 
    if path_found:
        for waypoint in path:
            pygame.draw.rect(screen, RED, (waypoint[0] - 2, waypoint[1] - 2, 4, 4))

    # Draw the car
    rotated_car = pygame.transform.rotate(car_image, -car_angle)
    car_draw_rect = rotated_car.get_rect(center=(car_x, car_y))
    screen.blit(rotated_car, car_draw_rect.topleft)

    # Follow the path
    if path_found and current_waypoint_index < len(path):
        waypoint_x, waypoint_y = path[current_waypoint_index]
        dx = waypoint_x - car_x
        dy = waypoint_y - car_y
        distance = math.hypot(dx, dy)

        # Update heading
        if distance > 1e-6:
            car_angle = math.degrees(math.atan2(dy, dx))

        # Move using dt
        step = car_speed * dt
        if distance > step:
            car_x += (dx / distance) * step
            car_y += (dy / distance) * step
        else:
            car_x, car_y = float(waypoint_x), float(waypoint_y)
            current_waypoint_index += 1

    # End condition (at/after last waypoint and within target)
    if path_found and current_waypoint_index >= len(path):
        if math.hypot(car_x - target_x, car_y - target_y) <= target_radius:
            print("Target Reached!")
            # Optional: running = False

    pygame.display.flip()

pygame.quit()


