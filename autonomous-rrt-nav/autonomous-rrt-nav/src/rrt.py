import random
import math
import pygame

class Node:
    def __init__(self, x, y, parent=None):
        self.x = x
        self.y = y
        self.parent = parent

def distance(node1, node2):
    """Calculate the Euclidean distance between two nodes."""
    return math.sqrt((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2)

def is_collision_free(node1, node2, obstacles, car_size):
    """
    Check if the path between two nodes is collision-free.
    Args:
        node1, node2: Start and end nodes.
        obstacles: List of pygame.Rect representing obstacles.
        car_size: Tuple (width, height) of the car in pixels.
    Returns:
        bool: True if the path is collision-free, False otherwise.
    """
    steps = int(distance(node1, node2)) + 1
    car_rect = pygame.Rect(0, 0, car_size[0], car_size[1])

    for i in range(steps):
        t = i / steps
        x = node1.x + t * (node2.x - node1.x)
        y = node1.y + t * (node2.y - node1.y)
        car_rect.topleft = (x - car_size[0] // 2, y - car_size[1] // 2)

        
        for obstacle in obstacles:
            if car_rect.colliderect(obstacle):
                return False
    return True

def waypoints2path(waypoints, steps=5):
    """
    Smooth the path by adding intermediate points between waypoints.
    Args:
        waypoints: List of tuples representing waypoints [(x1, y1), (x2, y2), ...].
        steps: Number of interpolation steps between each pair of waypoints.
    Returns:
        List of tuples representing the smoothed path.
    """
    smoothed_path = []
    for i in range(len(waypoints) - 1):
        x1, y1 = waypoints[i]
        x2, y2 = waypoints[i + 1]
        
        # Add intermediate points
        for j in range(steps + 1):
            u = j / steps  # Interpolation factor (0 to 1)
            x = int(x2 * u + x1 * (1 - u))
            y = int(y2 * u + y1 * (1 - u))
            smoothed_path.append((x, y))

    return smoothed_path

def rrt(start, goal, obstacles, map_dim, car_size, step_size=20, max_iter=1000, screen=None,car_image=None):
    """
    RRT pathfinding algorithm with visualization of progress.
    Args:
        start: Tuple (x, y) start position in pixels.
        goal: Tuple (x, y) goal position in pixels.
        obstacles: List of pygame.Rect representing obstacles.
        map_dim: Tuple (width, height) of the map in pixels.
        car_size: Tuple (width, height) of the car in pixels.
        step_size: Maximum step size for each extension in pixels.
        max_iter: Maximum number of iterations for the RRT algorithm.
        screen: Pygame screen object for visualization (optional).
    Returns:
        List of tuples representing the path from start to goal, or an empty list if no path is found.
    """
    start_node = Node(start[0], start[1])
    goal_node = Node(goal[0], goal[1])
    tree = [start_node]

    for _ in range(max_iter):
        # Sample a random point
        rand_x = random.randint(0, map_dim[0])
        rand_y = random.randint(0, map_dim[1])
        random_node = Node(rand_x, rand_y)

        # Find the nearest node in the tree
        nearest_node = min(tree, key=lambda node: distance(node, random_node))

        # Extend towards the random node
        theta = math.atan2(random_node.y - nearest_node.y, random_node.x - nearest_node.x)
        new_x = nearest_node.x + step_size * math.cos(theta)
        new_y = nearest_node.y + step_size * math.sin(theta)
        new_node = Node(new_x, new_y, nearest_node)

        # Check for collision
        if is_collision_free(nearest_node, new_node, obstacles, car_size):
            tree.append(new_node)

            # Visualize the new node
            if screen:
                

                # Draw the car
                rotated_car = pygame.transform.rotate(car_image, 0)  # Assuming the car is not rotating here
                car_rect = rotated_car.get_rect(center=(start[0], start[1]))
                screen.blit(rotated_car, car_rect.topleft)
# Draw the tree (branches)
                for node in tree:
                    if node.parent:  # Draw a line from the node to its parent
                        pygame.draw.line(screen, (0, 0, 255), (node.x, node.y), (node.parent.x, node.parent.y), 2)
                pygame.display.flip()
                pygame.time.delay(25)  


            # Check if the goal is reached
            if distance(new_node, goal_node) < step_size:
                goal_node.parent = new_node
                return reconstruct_path(goal_node)

    return []  # No path found


def reconstruct_path(node, steps=2):
    """
    Reconstruct the path from the goal to the start and smooth it.
    Args:
        node: The goal node.
        steps: Number of interpolation steps between waypoints.
    Returns:
        List of tuples representing the smoothed path.
    """
    path = []
    while node:
        path.append((node.x, node.y))
        node = node.parent
    path.reverse()

    # Smooth the path using waypoints2path
    return waypoints2path(path, steps=steps)

