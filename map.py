import pygame

class TileKind:
    def __init__(self, name, image, is_solid):
        self.name = name
        self.image = pygame.image.load(image)
        self.is_solid = is_solid

class Map:
    def __init__(self, map_file, tile_kinds, tile_size):
        # Keep a list of different kinds of files (grass, sand, water, etc.)
        self.tile_kinds = tile_kinds

        # Load the data from the file
        file = open(map_file, "r")
        data = file.read()
        file.close()

        # Set up the tiles from loaded data
        self.tiles = []
        for line in data.split('\n'):
            row = []
            for tile_number in line:
                row.append(int(tile_number))
            self.tiles.append(row)

        # How big in pixels are the tiles?
        self.tile_size = tile_size

    def draw(self, screen):
        # Go row by row
        for y, row in enumerate(self.tiles):
            # Within the current row, go through each tile
            for x, tile in enumerate(row):
                location = (x * self.tile_size, y * self.tile_size)
                image = self.tile_kinds[tile].image
                screen.blit(image, location)

    # --- NEW METHOD ---
    def is_blocked(self, x, y, width, height):
        # Check the four corners of the player's rectangle
        corners = [
            (x, y),
            (x + width - 1, y),
            (x, y + height - 1),
            (x + width - 1, y + height - 1)
        ]
        
        for cx, cy in corners:
            # Convert pixel coordinates to grid coordinates
            grid_x = int(cx // self.tile_size)
            grid_y = int(cy // self.tile_size)
            
            # Check if within map bounds
            if 0 <= grid_y < len(self.tiles) and 0 <= grid_x < len(self.tiles[0]):
                tile_index = self.tiles[grid_y][grid_x]
                if self.tile_kinds[tile_index].is_solid:
                    return True
        return False