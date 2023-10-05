from enum import Enum

# Command Pattern: Create command classes for 'M', 'L', 'R'
class Command(Enum):
    MOVE = 'M'
    TURN_LEFT = 'L'
    TURN_RIGHT = 'R'

# Component Pattern: Define a Grid class to represent the grid
class Grid:
    def _init_(self, width, height):
        self.width = width
        self.height = height
        self.obstacles = set()

    def add_obstacle(self, x, y):
        self.obstacles.add((x, y))

# Command Pattern: Create command classes with execute method
class MoveCommand:
    def execute(self, rover):
        rover.move()

class TurnLeftCommand:
    def execute(self, rover):
        rover.turn_left()

class TurnRightCommand:
    def execute(self, rover):
        rover.turn_right()

# Receiver Pattern: Create a Rover class to receive and execute commands
class Rover:
    def _init_(self, x, y, direction, grid):
        self.x = x
        self.y = y
        self.direction = direction
        self.grid = grid

    def move(self):
        new_x, new_y = self.calculate_new_position()
        if self.is_valid_move(new_x, new_y):
            self.x = new_x
            self.y = new_y

    def turn_left(self):
        directions = ['N', 'E', 'S', 'W']
        current_index = directions.index(self.direction)
        new_index = (current_index - 1) % len(directions)
        self.direction = directions[new_index]

    def turn_right(self):
        directions = ['N', 'E', 'S', 'W']
        current_index = directions.index(self.direction)
        new_index = (current_index + 1) % len(directions)
        self.direction = directions[new_index]

    def calculate_new_position(self):
        x, y = self.x, self.y
        if self.direction == 'N':
            y += 1
        elif self.direction == 'S':
            y -= 1
        elif self.direction == 'E':
            x += 1
        elif self.direction == 'W':
            x -= 1
        return x, y

    def is_valid_move(self, new_x, new_y):
        return (
            0 <= new_x < self.grid.width and
            0 <= new_y < self.grid.height and
            (new_x, new_y) not in self.grid.obstacles
        )

    def send_status_report(self):
        return f"Rover is at ({self.x}, {self.y}) facing {self.direction}. No Obstacles detected."

# Get user input for grid size
grid_width = int(input("Enter grid width: "))
grid_height = int(input("Enter grid height: "))

# Create a grid
grid = Grid(grid_width, grid_height)

# Get user input for obstacle positions
while True:
    obstacle_x = int(input("Enter obstacle x-coordinate (or -1 to finish): "))
    if obstacle_x == -1:
        break
    obstacle_y = int(input("Enter obstacle y-coordinate: "))
    grid.add_obstacle(obstacle_x, obstacle_y)

# Get user input for rover initial position and direction
rover_x = int(input("Enter rover x-coordinate: "))
rover_y = int(input("Enter rover y-coordinate: "))
rover_direction = input("Enter rover initial direction (N, E, S, W): ")

# Initialize the rover
rover = Rover(rover_x, rover_y, rover_direction, grid)

# Get user input for rover commands
commands_input = input("Enter rover commands (e.g., 'MMRLM'): ")
commands = []
for char in commands_input:
    if char == 'M':
        commands.append(MoveCommand())
    elif char == 'L':
        commands.append(TurnLeftCommand())
    elif char == 'R':
        commands.append(TurnRightCommand())

# Execute the rover commands
for command in commands:
    command.execute(rover)

# Print the final position and status report
final_position = (rover.x, rover.y, rover.direction)
status_report = rover.send_status_report()

print(f"Final Position: {final_position}")
print(status_report)
