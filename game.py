import random

# Constants for game elements
RABBIT = 'r'
RABBIT_WITH_CARROT = 'R'
CARROT = 'c'
RABBIT_HOLE = 'O'
PATHWAY_STONE = '-'

# Initialize game parameters
map_size = int(input("Enter the size of the map (minimum 100): "))
num_carrots = int(input("Enter the number of carrots: "))
num_rabbit_holes = int(input("Enter the number of rabbit holes: "))

while map_size < 3:
    map_size = int(input("Please enter grid size greater than 2: "))

while num_carrots <= 1:
    num_carrots = int(
        input("Please enter number of carrots greater than 1: "))

while num_rabbit_holes <= 1:
    num_rabbit_holes = int(
        input("Please enter number of holes greater than 1: "))

# Create a 2D map


def create_map(map_size, num_carrots, num_rabbit_holes):
    game_map = [[PATHWAY_STONE for _ in range(
        map_size)] for _ in range(map_size)]

    # Place rabbit
    rabbit_x, rabbit_y = random.randint(
        0, map_size - 1), random.randint(0, map_size - 1)
    game_map[rabbit_x][rabbit_y] = RABBIT

    # Place carrots
    for _ in range(num_carrots):
        carrot_x, carrot_y = random.randint(
            0, map_size - 1), random.randint(0, map_size - 1)
        while game_map[carrot_x][carrot_y] != PATHWAY_STONE:
            carrot_x, carrot_y = random.randint(
                0, map_size - 1), random.randint(0, map_size - 1)
        game_map[carrot_x][carrot_y] = CARROT

    # Place rabbit holes
    for _ in range(num_rabbit_holes):
        hole_x, hole_y = random.randint(
            0, map_size - 1), random.randint(0, map_size - 1)
        while game_map[hole_x][hole_y] != PATHWAY_STONE:
            hole_x, hole_y = random.randint(
                0, map_size - 1), random.randint(0, map_size - 1)
        game_map[hole_x][hole_y] = RABBIT_HOLE

    return game_map

# Find the position of the rabbit on the map


def find_rabbit_position(game_map):
    for i in range(map_size):
        for j in range(map_size):
            if game_map[i][j] == RABBIT or game_map[i][j] == RABBIT_WITH_CARROT:
                return i, j

# Display the game map


def display_map(game_map):
    for row in game_map:
        print(' '.join(row))

# Check if the move is within the boundaries of the map


def is_valid_move(game_map, x, y):
    if 0 <= x < map_size and 0 <= y < map_size and game_map[x][y] != CARROT and game_map[x][y] != RABBIT_HOLE:
        return True

    return False

# Pick up a carrot if available at the current position


def pick_carrot(game_map, x, y):
    if game_map[x][y+1] == CARROT:
        game_map[x][y+1] = PATHWAY_STONE
    elif game_map[x][y-1] == CARROT:
        game_map[x][y-1] = PATHWAY_STONE
    elif game_map[x+1][y] == CARROT:
        game_map[x+1][y] = PATHWAY_STONE
    elif game_map[x-1][y] == CARROT:
        game_map[x-1][y] = PATHWAY_STONE
    game_map[x][y] = RABBIT_WITH_CARROT if RABBIT else RABBIT

# Jump over a rabbit hole if adjacent


def jump_rabbit_hole(game_map, x, y):
    if game_map[x][y+1] == RABBIT_HOLE and y+2 < map_size:
        game_map[x][y] = PATHWAY_STONE
        game_map[x][y+2] = RABBIT if RABBIT else RABBIT_WITH_CARROT
    elif game_map[x][y-1] == RABBIT_HOLE and y-2>=0:
        game_map[x][y] = PATHWAY_STONE
        game_map[x][y-2] = RABBIT if RABBIT else RABBIT_WITH_CARROT
    elif game_map[x+1][y] == RABBIT_HOLE and x+2< map_size:
        game_map[x][y] = PATHWAY_STONE
        game_map[x+2][y] = RABBIT if RABBIT else RABBIT_WITH_CARROT
    elif game_map[x-1][y] == RABBIT_HOLE and x-2>=0:
        game_map[x][y] = PATHWAY_STONE
        game_map[x-2][y] = RABBIT if RABBIT else RABBIT_WITH_CARROT


# Check if the player has won by placing a carrot in any rabbit hole
def check_win(game_map):
    co = 0
    for i in range(map_size):
        for j in range(map_size):
            if game_map[i][j] == CARROT:
                co += 1
    c = num_carrots-co
    return c == RABBIT_HOLE

# Main game loop


def main():
    game_map = create_map(map_size, num_carrots, num_rabbit_holes)

    while True:
        display_map(game_map)
        rabbit_x, rabbit_y = find_rabbit_position(game_map)
        move = input("Enter your move (a/d/w/s/p/j/q): ").lower()

        if move == 'q':
            print("Exiting the game.")
            break

        elif move == 'p' or move == 'j':
            if move == 'p':
                pick_carrot(game_map, rabbit_x, rabbit_y)
            elif move == 'j':
                jump_rabbit_hole(game_map, rabbit_x, rabbit_y)

        else:
            new_x, new_y = rabbit_x, rabbit_y
            m = {'a', 'd', 'w', 's', 'wd', 'dw',
                 'wa', 'aw', 'as', 'sa', 'sd', 'ds'}
            if move in m:
                if move == 'a':
                    new_y -= 1
                elif move == 'd':
                    new_y += 1
                elif move == 'w':
                    new_x -= 1
                elif move == 's':
                    new_x += 1
                elif move == 'wd' or move == 'dw':
                    new_x -= 1
                    new_y += 1
                elif move == 'wa' or move == 'aw':
                    new_x -= 1
                    new_y -= 1
                elif move == 'as' or move == 'sa':
                    new_x += 1
                    new_y -= 1
                elif move == 'sd' or move == 'ds':
                    new_x += 1
                    new_y += 1

                if is_valid_move(game_map, new_x, new_y):
                    game_map[rabbit_x][rabbit_y] = PATHWAY_STONE
                    rabbit_x, rabbit_y = new_x, new_y
                    game_map[rabbit_x][rabbit_y] = RABBIT

                    if check_win(game_map):
                        display_map(game_map)
                        print("Congratulations! You won!")
                        break
            else:
                print("Invalid move. Try again.")


if __name__ == "__main__":
    main()
