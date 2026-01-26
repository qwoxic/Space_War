import arcade

class Player(arcade.SpriteCircle):
    def __init__(self, x, y):
        super().__init__(20, arcade.color.BLUE)
        self.center_x = x
        self.center_y = y
        self.health = 100
        self.max_health = 100
        self.change_x = 0
        self.change_y = 0

    def update(self, delta_time):
        self.center_x += self.change_x * delta_time
        self.center_y += self.change_y * delta_time
        
        self.center_x = max(20, min(1004, self.center_x))
        self.center_y = max(20, min(748, self.center_y))

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            return True
        return False
