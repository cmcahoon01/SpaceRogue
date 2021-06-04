import pygame
from ships import gunner, medic

button_size = 100
padding_size = 6
font = None
text_color = (110, 187, 235)


class UI:
    def __init__(self, control):
        self.space_control = control
        self.width = control.settings.dimensions[0]
        self.height = control.settings.dimensions[1]
        global font
        font = pygame.font.SysFont(None, 24)

        self.buttons = []
        b1 = "Gunner", 150, pygame.Rect(self.width - button_size - padding_size,
                                        self.height - button_size - padding_size,
                                        button_size, button_size)
        b2 = "Medic", 225, pygame.Rect(self.width - button_size - padding_size,
                                       self.height - button_size * 2 - padding_size * 2,
                                       button_size, button_size)
        self.buttons.append(b1)
        self.buttons.append(b2)

    def click(self, x, y):
        for button in self.buttons:
            if button[2].collidepoint((x, y)):
                if button[1] <= self.space_control.money:
                    self.space_control.money -= button[1]
                    if button[0] == 'Gunner':
                        self.space_control.purchased(gunner.Gunner)
                    elif button[0] == 'Medic':
                        self.space_control.purchased(medic.Medic)

    def draw(self, window):
        for button in self.buttons:
            self.buy_unit(window, button)
        self.show_creds(window)

    def buy_unit(self, window, button_info):
        rect = button_info[2]
        x, y = rect.x, rect.y
        pygame.draw.rect(window, (255, 0, 0), rect, 1)
        image = pygame.image.load('assets/' + button_info[0] + '.png')
        image = pygame.transform.scale(image, (button_size, button_size))
        rect = image.get_rect(center=image.get_rect(center=(x + button_size / 2, y + button_size / 2)).center)
        window.blit(image, rect)

        text = font.render(button_info[0], True, text_color)
        window.blit(text, (x + 20, y + padding_size))
        text = font.render(str(button_info[1]), True, text_color)
        window.blit(text, (x + 35, y + button_size - padding_size * 4))

    def show_creds(self, window):
        text = font.render("$" + str(self.space_control.money), True, text_color)
        window.blit(text, (self.width - padding_size * 15, padding_size * 2))
