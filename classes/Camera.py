if __name__ == 'classes.Camera':

    from settings import SIZE, F_SIZE


    class Camera:
        def __init__(self):
            self.x = self.y = 0
            self.width, self.height = 320, 250

        def render(self, target_x, target_y):
            if self.x + self.width > target_x:
                self.x = target_x - self.width
            if self.x + SIZE[0] - self.width < target_x:
                self.x = target_x - SIZE[0] + self.width

            if self.y + self.height > target_y:
                self.y = target_y - self.height
            if self.y + SIZE[1] - self.height < target_y:
                self.y = target_y - SIZE[1] + self.height

            if self.x < 0:
                self.x = 0
            elif self.x + SIZE[0] > F_SIZE[0]:
                self.x = F_SIZE[0] - SIZE[0]

            if self.y + SIZE[1] > F_SIZE[1]:
                self.y = F_SIZE[1] - SIZE[1]

        def get_pos(self, x, y, rounded=False):
            if rounded:
                return round(x - self.x), round(y - self.y)
            else:
                return x - self.x, y - self.y
