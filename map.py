import pygame

class TileKind:
    def __init__(self, name, image, is_solid):
        self.name = name
        self.image = pygame.image.load(image)
        self.is_solid = is_solid

class Map:
    def __init__(self, map_file, tile_kinds, tile_size):
        self.tile_kinds = tile_kinds

        file = open(map_file, "r")
        data = file.read()
        file.close()

        self.tiles = []
        for line in data.split('\n'):
            if not line.strip(): continue # Skip empty lines
            row = []
            for tile_number in line:
                row.append(int(tile_number))
            self.tiles.append(row)

        self.tile_size = tile_size
        
        # Calculate Map Dimensions in Pixels
        self.pixel_width = len(self.tiles[0]) * tile_size
        self.pixel_height = len(self.tiles) * tile_size

    def draw(self, screen, camera):
        # Go row by row
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                # Calculate world position
                world_x = x * self.tile_size
                world_y = y * self.tile_size
                
                # Calculate screen position
                screen_x = world_x - camera.x
                screen_y = world_y - camera.y
                
                # Optimization: Only draw if visible on screen
                if -self.tile_size < screen_x < screen.get_width() and -self.tile_size < screen_y < screen.get_height():
                    image = self.tile_kinds[tile].image
                    screen.blit(image, (screen_x, screen_y))

    def is_blocked(self, x, y, width, height):
        corners = [
            (x, y),
            (x + width - 1, y),
            (x, y + height - 1),
            (x + width - 1, y + height - 1)
        ]
        
        for cx, cy in corners:
            grid_x = int(cx // self.tile_size)
            grid_y = int(cy // self.tile_size)
            
            if 0 <= grid_y < len(self.tiles) and 0 <= grid_x < len(self.tiles[0]):
                tile_index = self.tiles[grid_y][grid_x]
                if self.tile_kinds[tile_index].is_solid:
                    return True
        return False