import pygame
import os
import sys
import random

pygame.init()

size = width, height = 1000, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Взлом сейфа")

all_sprites = pygame.sprite.Group()
sprite = pygame.sprite.Sprite()

# Загрузка изображения
def load_image(name, colorkey=None):
    fullname = os.path.join("image", name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
            colorkey = image.get_at((2, 2))
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()
    return image

def won(screen):
    font = pygame.font.Font(None, 50)
    text = font.render("Победа!", True, (100, 255, 100))
    text_x = 650
    text_y = 10
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
                                           text_w + 20, text_h + 20), 1)

# Класс "Ручка от сейфа"
class Handle(pygame.sprite.Sprite):

    def __init__(self, x, y, rotate):
        super().__init__(all_sprites)
        if rotate == 0:
            self.image = load_image("handle.png")
        else:
            self.image = load_image("handle_rot.png")
        self.image = pygame.transform.scale(self.image, (120, 120))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw_handle(self, x, y, rotate):
        if rotate == 0:
            image = load_image("handle.png")
        else:
            image = load_image("handle_rot.png")
        self.image = pygame.transform.scale(image, (120, 120))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        screen.blit(self.image, (x, y))


class Safe(pygame.sprite.Sprite):
    image = load_image("safe.png")
    image = pygame.transform.scale(image, (600, 600))

    def __init__(self, width, height):
        super().__init__(all_sprites)
        self.image = Safe.image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.sq = []
        self.width = width
        self.height = height
        self.left = 55
        self.top = 50
        self.cell_size = 120
        self.lst_handle = []

        self.render()


    def render(self):
        # Запоняем список значениями 0, 1. Где 0 - ручка по горизонтали, 1 - ручка по вертикали
        for y in range(self.height):
            lst = []
            for x in range(self.width):
                lst.append(random.randint(0, 1))
            self.sq.append(lst)

        # Рисуем ручки на сейфе
        for y in range(self.height):
            # временный список для срок картинок ручек сейфа
            lst = []
            for x in range(self.width):
                rotate = self.sq[y][x]
                # создаём объект класса "Ручка от сейфа"
                self.handle = Handle(x * self.cell_size + self.left, y * self.cell_size + self.top, rotate)
                # Добавляем рисунок ручки во временный список
                lst.append(self.handle)
            # Добавляем строку в общий список всех картинок с ручками
            self.lst_handle.append(lst)

    def update(self):
        for y in range(self.height):
            for x in range(self.width):
                self.lst_handle[y][x].draw_handle(x * self.cell_size + self.left, y * self.cell_size + self.top, self.sq[y][x])

    def check_click(self, pos):
        self.x, self.y = pos
        # Проверка, что клик попал в таблицу с ручками сейфа
        if self.x <= self.width * self.cell_size + self.left and self.y <= self.height * self.cell_size + self.top:
            x_pos = (self.x - self.left) // self.cell_size
            y_pos = (self.y - self.top) // self.cell_size

            # Меняем признак поворота текущей ручки
            if self.sq[y_pos][x_pos] == 0:
                self.sq[y_pos][x_pos] = 1
            else:
                self.sq[y_pos][x_pos] = 0

            # Меняем признак поворота у всех ручек по горизонтали
            for x in range(self.width):
                rotate = self.sq[y_pos][x]
                if rotate == 1:
                    self.sq[y_pos][x] = 0
                else:
                    self.sq[y_pos][x] = 1

            # Меняем признак поворота у всех ручек по вертикали
            for y in range(self.height):
                rotate = self.sq[y][x_pos]
                if rotate == 1:
                    self.sq[y][x_pos] = 0
                else:
                    self.sq[y][x_pos] = 1

    def check_win(self):
        return not all(self.sq)


safe = Safe(4, 4)

running = True
game_over = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            safe.check_click(event.pos)
    screen.fill((0, 0, 0))
    # обновление рисунка сейфа.
    all_sprites.draw(screen)
    all_sprites.update()
    if safe.check_win():
        won(screen)
        game_over = True
    pygame.display.flip()
pygame.display.quit()