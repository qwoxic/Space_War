import arcade
from database import save_score

class MenuView(arcade.View):
    def on_draw(self):
        self.clear()
        arcade.set_background_color((20, 20, 30))
        arcade.draw_text("DANGER MONSTERS", 512, 600, 
                         arcade.color.WHITE, 48, anchor_x="center")
        arcade.draw_text("ЛКМ или ENTER - начать", 512, 450, 
                         arcade.color.LIGHT_GRAY, 24, anchor_x="center")
        arcade.draw_text("WASD - движение", 512, 400, 
                         arcade.color.LIGHT_GRAY, 20, anchor_x="center")
        arcade.draw_text("ЛКМ/ПРОБЕЛ - стрельба", 512, 370, 
                         arcade.color.LIGHT_GRAY, 20, anchor_x="center")
        arcade.draw_text("ESC - выйти в меню", 512, 340, 
                         arcade.color.LIGHT_GRAY, 20, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            from game import GameView
            self.window.show_view(GameView())

    def on_mouse_press(self, x, y, button, modifiers):
        from game import GameView
        self.window.show_view(GameView())

class GameOverView(arcade.View):
    def __init__(self, score, won):
        super().__init__()
        self.score = score
        self.won = won
        save_score("Игрок", score)
    
    def on_draw(self):
        self.clear()
        arcade.set_background_color((20, 20, 30))
        
        if self.won:
            title = "ПОБЕДА!"
            color = arcade.color.GREEN
            message = "Вы победили Колдуна!"
        else:
            title = "ПОРАЖЕНИЕ"
            color = arcade.color.RED
            message = "Вы погибли"
        
        arcade.draw_text(title, 512, 500, color, 48, anchor_x="center")
        arcade.draw_text(message, 512, 430, arcade.color.WHITE, 32, anchor_x="center")
        arcade.draw_text(f"Очки: {self.score}", 512, 350, 
                         arcade.color.YELLOW, 36, anchor_x="center")
        arcade.draw_text("Нажмите ENTER для возврата в меню", 512, 250, 
                         arcade.color.LIGHT_GRAY, 24, anchor_x="center")
        arcade.draw_text("Нажмите ESC для выхода", 512, 200, 
                         arcade.color.LIGHT_GRAY, 20, anchor_x="center")
    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            self.window.show_view(MenuView())
        elif key == arcade.key.ESCAPE:
            self.window.close()
