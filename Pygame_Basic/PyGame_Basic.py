import pygame
import sys
import time
import random

from pygame.locals import *


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
# 바둑판 처럼 화면을 나누기 위한 GRID 관련 내용
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH / GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT / GRID_SIZE

WHITE = (255, 255, 255)
GREEN = (0, 50, 0)
ORANGE = (250, 150, 0)
GRAY = (100, 100, 100)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

FPS = 10


# 뱀(Python) 클래스
class Python(object):
    def __init__(self):
        self.create()
        self.color = GREEN

    def create(self):
        # 초기 뱀의 길이
        self.length = 2
        # 길이가 2이상인 뱀이므로 길이 1당 위치들을 설정
        # 화면 정중앙으로 설정
        self.positions = [((WINDOW_WIDTH / 2), (WINDOW_HEIGHT / 2))]
        # 처음 뱀이 생성되고 화면 중앙에서 1씩만 랜덤하게 위아왼오 중에 한 방향으로 움직임
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def control(self, xy):
        # 뱀이 위로 갈때 아래로 가면 안되고 왼쪽으로 갈때 오른쪽으로 가면 안됨
        # 즉, 방향 조작시 반대 방향으로는 이동할 수 없게 해야 함
        # 만약 x, y축으로 조작과 달리 반대 방향으로 움직일 경우 아무것도 안하게끔
        if (xy[0] * -1, xy[1] * -1) == self.direction:
            return
        # 제대로 조작된 방향으로 움직일 경우 그대로 해당 방향으로 가도록 함
        else:
            self.direction = xy

    def move(self):
        cur = self.positions[0] # positions[0] 이므로 뱀의 머리 위치
        x, y = self.direction # 방향 조작을 x, y 좌표로
        # 이 부분을 잘 모르겠음
        # x축, y축으로 뱀이 이동하다가 화면을 한쪽 방향으로 벗어나면 화면의 반대 방향에서 뱀이 나오도록 설정
        new = (((cur[0] + (x * GRID_SIZE)) % WINDOW_WIDTH), ((cur[1] + (y * GRID_SIZE)) % WINDOW_HEIGHT))
        # 만약 뱀의 머리를 제외한 부분이 머리의 이동 방향에 놓여 겹치게 되면
        if new in self.positions[2:]:
            # 해당 뱀은 죽고 새로운 뱀을 생성
            self.create()
        # 그게 아닐경우
        else:
            # 뱀의 머리 위치 부분에 새로운 것을 추가
            self.positions.insert(0, new)
            # 그런데 새로운 것을 추가 하면 먹이를 먹지도 않았는데
            # 기존의 뱀 길이보다 포지션들의 총 합이 늘어남
            if len(self.positions) > self.length:
                # 그러면, 뱀의 포지션들 중 맨 뒤의 포지션을 끄집어냄
                # 이 말은 곧, 그 방향으로 1 포지션 만큼 움직인 셈.
                self.positions.pop()

    def eat(self):
        self.length += 1

    def draw(self, surface):
        for p in self.positions:
            draw_object(surface, self.color, p)


# 먹이 클래스
class Feed(object):
    def __init__(self):
        self.position = (0, 0)
        self.color = ORANGE
        self.create()

    def create(self):
        self.position = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE, random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self, surface):
        draw_object(surface, self.color, self.position)


# 뱀, 먹이를 화면에 그리기 위해 draw_object() 함수를 만듦
def draw_object(surface, color, pos):
    # pygame.Rect() 클래스의 인스턴스를 생성(초기 위치는 그리드 상 0,1)
    r = pygame.Rect((pos[0], pos[1]), (GRID_SIZE, GRID_SIZE))
    # 해당 인스턴스를 pygame.draw.rect() 함수의 매개변수로 넘겨줘서 surface에 그림
    pygame.draw.rect(surface, color, r)


# 뱀이 먹이를 먹었다는 것을 체크하기 위한 함수
def check_eat(python, feed):
    # 뱀의 머리가 먹이 위치와 일치하게 되면
    if python.positions[0] == feed.position:
        # 뱀이 먹이를 먹음
        python.eat()
        # 새로운 먹이 생성
        feed.create()


# 정보를 텍스트로 보여주기 위한 함수
def show_info(length, speed, surface):
    font = pygame.font.Font(None, 34)
    text = font.render('length: ' + str(length) + "    Speed: " + str(round(speed, 2)), 1, GRAY)
    pos = text.get_rect()
    pos.centerx = 150
    surface.blit(text, pos)


if __name__ == '__main__':
    python = Python()
    feed = Feed()

    pygame.init()
    # pygame.display.set_mode() : 화면 정의 메소드
    # pygame.display.set_mode(size=(0, 0), flags=0, depth=0, display=0, vsync=0) -> Surface
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
    # set_caption()을 통해 윈도우 창 위쪽에 이름을 붙임
    pygame.display.set_caption('Python Game')
    # pygmae.Surface() : 이미지를 나타내는 pygame 객체
    # Surface((width, height), flags=0, depth=0, masks=None) -> Surface
    # Surface((width, height), flags=0, Surface) -> Surface
    surface = pygame.Surface(window.get_size())
    # pygame.Surface.convert() : 이미지의 픽셀 형식 변경
    surface = surface.convert()
    # pygame.Surface.fill() : 단색으로 표면(Surface) 채우기
    surface.fill(WHITE)
    # pygame.time.Clock() : 시간을 추적하는데 도움이 되는 객체
    clock = pygame.time.Clock()
    # pygame.key.set_repeat() : 유지된 키가 반복되는 방식 제어
    # set_repeat(delay, interval) -> None
    pygame.key.set_repeat(1, 40)
    # pygame.Surface.blit() : 한 이미지를 다른 이미지 위에 그리기
    # blit(source, dest, area=None, special_flags=0) -> Rect
    window.blit(surface, (0, 0)) # window에 surface 표면을 그림

    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    python.control(UP)
                elif event.key == K_DOWN:
                    python.control(DOWN)
                elif event.key == K_LEFT:
                    python.control(LEFT)
                elif event.key == K_RIGHT:
                    python.control(RIGHT)

        surface.fill(WHITE)
        python.move()
        check_eat(python, feed)
        # 뱀이 먹이를 먹으면 속도가 점점 빨라지도록 speed 정의
        speed = (FPS + python.length) / 2
        show_info(python.length, speed, surface)
        python.draw(surface)
        feed.draw(surface)
        window.blit(surface, (0, 0))
        pygame.display.flip()
        pygame.display.update()
        clock.tick(speed)
