from random import choice, randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 15

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Определение родительского игрового класса"""

    def __init__(self, color=BOARD_BACKGROUND_COLOR) -> None:
        self.position = (SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)
        self.body_color = color

    def draw(self):
        """Абстрактный метод для отрисовка объекта на игровом поле"""
        raise NotImplementedError

    def draw_cell(self, position):
        """Отрисовка одной ячейки"""
        return pg.Rect(position, (GRID_SIZE, GRID_SIZE))


class Apple(GameObject):
    """Определение дочернего класса Яблоко"""

    def __init__(self, busy_positions=[]):
        super().__init__(APPLE_COLOR)
        self.randomize_position(busy_positions)

    def draw(self):
        """'Отрисовка яблока на игровом поле"""
        rect = self.draw_cell(self.position)
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self, positions):
        """Установка рандомной позиции яблока на поле"""
        while True:
            new_position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                            randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if new_position not in positions:
                self.position = new_position
                break


class Snake(GameObject):
    """Определение дочернего класса Змейка"""

    def __init__(self):
        super().__init__(SNAKE_COLOR)
        self.reset()
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Обновление движения змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Перемещение змейки по игровому полю"""
        position_head_of_snake = self.get_head_position()
        if self.direction == RIGHT or self.direction == LEFT:
            new_coordinate_x = (position_head_of_snake[0] + self.direction[0]
                                * GRID_SIZE) % SCREEN_WIDTH
            self.positions.insert(0,
                                  (new_coordinate_x, position_head_of_snake[1])
                                  )
        elif self.direction == UP or self.direction == DOWN:
            new_coordinate_y = (position_head_of_snake[1] + self.direction[1]
                                * GRID_SIZE) % SCREEN_HEIGHT
            self.positions.insert(0,
                                  (position_head_of_snake[0], new_coordinate_y)
                                  )

        if self.length < len(self.positions):
            self.last = self.positions.pop()

    def draw(self):
        """Отрисовка змейки на игровом поле"""
        for position in self.positions[:-1]:
            rect = self.draw_cell(position)
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = self.draw_cell(self.get_head_position())
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = self.draw_cell(self.last)
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает координаты головы змейки"""
        return self.positions[0]

    def reset(self):
        """
        Возвращает змейку в исходное положение и задает случайное
        направление движения
        """
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = choice((UP, DOWN, LEFT, RIGHT))


def handle_keys(game_object):
    """Обработка пользовательского ввода"""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """
    Основная функция, определяющая логику игры:
    инициализация игровых объектов,
    запуск основного игрового цикла,
    обработка событий нажатия клавиш,
    обновление состояния игры,
    проверка условия окончания игры,
    управление движением змеики и её увеличение
    """
    pg.init()
    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        clock.tick(SPEED)
        apple.draw()
        pg.display.update()
        handle_keys(snake)
        snake.draw()
        snake.update_direction()
        snake_head = snake.get_head_position()

        if snake_head in snake.positions[1::]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()

        if snake_head == apple.position:
            snake.length += 1
            snake.move()
            apple.randomize_position(snake.positions)
        else:
            snake.move()


if __name__ == '__main__':
    main()
