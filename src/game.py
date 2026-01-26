import arcade
import random
import math
from levels import LevelManager
from player import Player
from enemy import Enemy
from boss import Boss

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        
        self.level_manager = LevelManager()
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)
        
        self.enemy_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.boss_bullet_list = arcade.SpriteList()
        self.boss_list = arcade.SpriteList()  # Добавляем список для босса
        
        self.score = 0
        self.is_boss_level = False
        self.boss = None
        
        self.level_type = self.level_manager.start_next_level()
        if self.level_type == "boss":
            self.start_boss_level()

    def on_draw(self):
        self.clear()
        arcade.set_background_color((30, 30, 40))
        
        self.player_list.draw()
        self.enemy_list.draw()
        self.bullet_list.draw()
        self.boss_bullet_list.draw()
        self.boss_list.draw()  # Отрисовываем босса через список
        
        arcade.draw_text(f"Уровень: {self.level_manager.current_level}", 20, SCREEN_HEIGHT - 40, 
                         arcade.color.WHITE, 24)
        arcade.draw_text(f"Очки: {self.score}", 20, SCREEN_HEIGHT - 80, 
                         arcade.color.WHITE, 24)
        arcade.draw_text(f"HP: {self.player.health}", 
                         20, SCREEN_HEIGHT - 120, arcade.color.WHITE, 24)
        
        if self.is_boss_level and self.boss:
            arcade.draw_text(f"Босс HP: {self.boss.health}", 
                             SCREEN_WIDTH - 200, SCREEN_HEIGHT - 40, 
                             arcade.color.RED, 24)

    def on_update(self, delta_time):
        self.level_manager.update(delta_time)
        
        if self.is_boss_level:
            if not self.boss or self.boss.health <= 0:
                self.score += 1000
                self.level_type = self.level_manager.start_next_level()
                if self.level_type == "complete":
                    self.win_game()
                    return
                elif self.level_type == "boss":
                    self.start_boss_level()
                else:
                    self.is_boss_level = False
                    self.boss = None
                    self.boss_list.clear()
                return
            self.boss.update(delta_time, self.player, self.boss_bullet_list)
        else:
            self.spawn_enemies()
        
        self.player.update(delta_time)
        
        for enemy in self.enemy_list:
            enemy.update(delta_time)
            enemy.move_towards(self.player.center_x, self.player.center_y, delta_time)
        
        for bullet in self.bullet_list:
            bullet.center_x += bullet.change_x * delta_time
            bullet.center_y += bullet.change_y * delta_time
            if (bullet.center_x < -100 or bullet.center_x > SCREEN_WIDTH + 100 or 
                bullet.center_y < -100 or bullet.center_y > SCREEN_HEIGHT + 100):
                bullet.remove_from_sprite_lists()
        
        for bullet in self.boss_bullet_list:
            bullet.center_x += bullet.change_x * delta_time
            bullet.center_y += bullet.change_y * delta_time
            if (bullet.center_x < -100 or bullet.center_x > SCREEN_WIDTH + 100 or 
                bullet.center_y < -100 or bullet.center_y > SCREEN_HEIGHT + 100):
                bullet.remove_from_sprite_lists()
        
        hits = arcade.check_for_collision_with_list(self.player, self.enemy_list)
        for enemy in hits:
            if self.player.take_damage(20):
                self.game_over()
            enemy.remove_from_sprite_lists()
        
        boss_bullet_hits = arcade.check_for_collision_with_list(self.player, self.boss_bullet_list)
        for bullet in boss_bullet_hits:
            if self.player.take_damage(15):
                self.game_over()
            bullet.remove_from_sprite_lists()
        
        for bullet in self.bullet_list[:]:
            hit_enemies = arcade.check_for_collision_with_list(bullet, self.enemy_list)
            if hit_enemies:
                for enemy in hit_enemies:
                    enemy.take_damage(25)
                    if enemy.health <= 0:
                        enemy.remove_from_sprite_lists()
                        self.score += 50
                        self.level_manager.enemy_killed()
                bullet.remove_from_sprite_lists()
            
            if self.boss and arcade.check_for_collision(bullet, self.boss):
                self.boss.take_damage(25)
                bullet.remove_from_sprite_lists()
        
        if not self.is_boss_level and self.level_manager.is_level_complete():
            self.level_type = self.level_manager.start_next_level()
            if self.level_type == "boss":
                self.start_boss_level()
            else:
                self.enemy_list.clear()
                self.bullet_list.clear()

    def spawn_enemies(self):
        if self.level_manager.should_spawn_enemy():
            for _ in range(self.level_manager.get_spawn_count()):
                self.spawn_enemy()

    def spawn_enemy(self):
        side = random.choice(['top', 'bottom', 'left', 'right'])
        
        if side == 'top':
            x = random.randint(0, SCREEN_WIDTH)
            y = SCREEN_HEIGHT + 20
        elif side == 'bottom':
            x = random.randint(0, SCREEN_WIDTH)
            y = -20
        elif side == 'left':
            x = -20
            y = random.randint(0, SCREEN_HEIGHT)
        else:
            x = SCREEN_WIDTH + 20
            y = random.randint(0, SCREEN_HEIGHT)
        
        enemy = Enemy(x, y)
        enemy.speed = self.level_manager.get_enemy_speed()
        enemy.health = self.level_manager.get_enemy_health()
        self.enemy_list.append(enemy)

    def game_over(self):
        from menu import GameOverView
        self.window.show_view(GameOverView(self.score, False))

    def win_game(self):
        from menu import GameOverView
        self.window.show_view(GameOverView(self.score, True))

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.player.change_y = 300
        elif key == arcade.key.S:
            self.player.change_y = -300
        elif key == arcade.key.A:
            self.player.change_x = -300
        elif key == arcade.key.D:
            self.player.change_x = 300
        elif key == arcade.key.SPACE:
            self.shoot_at_mouse()
        elif key == arcade.key.ESCAPE:
            from menu import MenuView
            self.window.show_view(MenuView())

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.W, arcade.key.S):
            self.player.change_y = 0
        if key in (arcade.key.A, arcade.key.D):
            self.player.change_x = 0

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.shoot_at_position(x, y)

    def shoot_at_position(self, x, y):
        dx = x - self.player.center_x
        dy = y - self.player.center_y
        dist = max(math.sqrt(dx*dx + dy*dy), 1)
        
        bullet = arcade.SpriteCircle(5, arcade.color.YELLOW)
        bullet.center_x = self.player.center_x
        bullet.center_y = self.player.center_y
        bullet.change_x = dx / dist * 500
        bullet.change_y = dy / dist * 500
        
        self.bullet_list.append(bullet)

    def shoot_at_mouse(self):
        mouse_x = arcade.get_mouse_x()
        mouse_y = arcade.get_mouse_y()
        self.shoot_at_position(mouse_x, mouse_y)

    def start_boss_level(self):
        self.is_boss_level = True
        self.enemy_list.clear()
        self.bullet_list.clear()
        self.boss = Boss(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        self.boss_list.clear()
        self.boss_list.append(self.boss)
