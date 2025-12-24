import arcade

class MenuView(arcade.View):
    def on_draw(self):
        self.clear()
        arcade.draw_text("DANGER MONSTERS", 512, 600, 
                         arcade.color.WHITE, 48, anchor_x="center")
        arcade.draw_text("ЛКМ или ENTER - начать", 512, 450, 
                         arcade.color.LIGHT_GRAY, 24, anchor_x="center")
        arcade.draw_text("WASD - движение", 512, 400, 
                         arcade.color.LIGHT_GRAY, 20, anchor_x="center")
        arcade.draw_text("ЛКМ - стрельба", 512, 370, 
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
