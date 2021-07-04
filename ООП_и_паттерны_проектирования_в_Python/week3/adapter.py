class MappingAdapter:
    def __init__(self, adaptee):
        self.adaptee = adaptee
    
    @staticmethod
    def get_lights_coords(grid):
        coords = []
        for i, line in enumerate(grid):
            for j, element in enumerate(line):
                if element == 1:
                    coords.append((j, i))
        return coords

    @staticmethod
    def get_obstacles_coords(grid):
        coords = []
        for i, line in enumerate(grid):
            for j, element in enumerate(line):
                if element == -1:
                    coords.append((j, i))
        return coords


    def lighten(self, grid):
        self.adaptee.set_dim([len(grid[0]), len(grid)])
        lights = self.get_lights_coords(grid)
        self.adaptee.set_lights(lights)

        obstacles = self.get_obstacles_coords(grid)
        self.adaptee.set_obstacles(obstacles)

        return self.adaptee.generate_lights()
