import arcade

class Player(arcade.SpriteCircle):
    def __init__(self, x, y):
        super().__init__(20, arcade.color.BLUE)
        self.center_x = x
        self.center_y = y
        self.health = 100
        self.change_x = 0
        self.change_y = 0

    def update(self, delta_time):
        self.center_x += self.change_x * delta_time
        self.center_y += self.change_y * delta_time

    def take_damage(self, amount):
        self.health -= amount
        return self.health <= 0
