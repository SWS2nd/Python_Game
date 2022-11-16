import random
from time import sleep

import pygame
from pygame.locals import *

WINDOW_WIDTH = 480
WINDOW_HEIGHT = 640

BLACK = (0, 0, 0)  # RGB (0, 0, 0) -> Black
WHITE = (255, 255, 255)  # RGB (255, 255, 255) -> White
YELLOW = (250, 250, 50)
RED = (250, 50, 50)

FPS = 60  # Frame Per Sec(초당 프레임)


# 전투기 클래스
class Fighter(pygame.sprite.Sprite):
    def __init__(self):
        # 상위 클래스의 __init__() 호출
        super(Fighter, self).__init__()
        # 전투기 이미지 가져오기
        self.image = pygame.image.load('fighter.png')
        # 이미지 크기(위치) 가져오기
        self.rect = self.image.get_rect()
        # 처음 전투기 이미지가 보여질 위치 지정하기
        # 전투기 가로 위치 지정
        self.rect.x = int(WINDOW_WIDTH / 2) # 화면 너비를 2로 나누면 == 중앙
        # 전투기 세로 위치 지정
        self.rect.y = WINDOW_HEIGHT - self.rect.height # 화면 높이 - 전투기 높이 -> 화면 아래쪽에 위치하도록
        # 방향 정의를 위한 direction 초기화
        self.dx = 0
        self.dy = 0

    # 전투기가 위치값을 업데이트 하기 위한 함수
    def update(self):
        self.rect.x += self.dx # 전투기 가로 위치 += 전투기 가로 방향 값
        self.rect.y += self.dy # 전투기 세로 위치 += 전투기 세로 방향 값

        # 전투기 위치가 화면에서 벗어나지 않도록 하기 위한 조건문
        # 전투기 가로 위치와 관련된 조건문
        # 전투기 위치가 0보다 작거나(화면 왼쪽) or 가로 위치값 + 전투기 가로 너비가 화면 너비보다 크다면(화면 오른쪽)
        if self.rect.x < 0 or self.rect.x + self.rect.width > WINDOW_WIDTH:
            self.rect.x -= self.dx # 더 이상 해당 방향으로 움직이지 못하도록 가로 방향 값을 뺌

        # 전투기 세로 위치와 관련된 조건문
        if self.rect.y < 0 or self.rect.y + self.rect.height > WINDOW_HEIGHT:
            self.rect.y -= self.dy

    # 화면에 이미지를 그려주는 함수
    def draw(self, screen):
        # screen.blit(screen에 표시할 객체, 표시할 위치)
        screen.blit(self.image, self.rect)

    # 전투기 충돌시 함수
    def collide(self, sprites):
        for sprite in sprites:
            # Sprite는 게임에서 나타내는 모든 캐릭터, 장애물등을 표현할 때 사용하는 Surface
            # 전투기가 게임에서 나타내는 캐릭터나 장애물들과 충돌이 발생한다면
            if pygame.sprite.collide_rect(self, sprite):
                # 전투기와 충돌이 발생한 장애물을 반환
                return sprite


# 전투기에서 발사하는 미사일 클래스
class Missile(pygame.sprite.Sprite):
    # 미사일은 x,y 위치를 받아오고 혹시 모르니 속도까지
    def __init__(self, xpos, ypos, speed):
        # 상위 클래스의 __init__() 호출
        super(Missile, self).__init__()
        # 미사일 이미지 가져오기
        self.image = pygame.image.load('missile.png')
        # 미사일 크기(위치) 가져오기
        self.rect = self.image.get_rect()
        # 미사일은 전투기에서 발사되야 하고 따라서, 전투기 위치 값을 넘겨주기 위함
        self.rect.x = xpos
        self.rect.y = ypos
        # 미사일 속도
        self.speed = speed
        # 미사일 사운드
        self.sound = pygame.mixer.Sound('missile.wav')

    # 미사일 발사와 관련된 함수
    def launch(self):
        # 미사일 발사시 미사일 사운드 재생
        self.sound.play()

    # 미사일 위치값 업데이트 함수
    def update(self):
        # 화면 위쪽으로 발사 = y축 위치값 - 미사일 속도
        self.rect.y -= self.speed
        # 미사일의 y축 위치값 + 미사일의 높이 < 0 면, 미사일이 화면 밖으로 나감
        if self.rect.y + self.rect.height < 0:
            # 미사일을 없애줌
            self.kill()

    # 미사일 충돌시 함수
    # def collide(미사일, 장애물들)
    def collide(self, sprites):
        # 장애물들 중에서
        for sprite in sprites:
            # 미사일과 장애물이 충돌한다면
            if pygame.sprite.collide_rect(self, sprite):
                # 장애물을 반환
                return sprite


# 우주에서 날아오는 운석 클래스
class Rock(pygame.sprite.Sprite):
    # 운석의 초기 위치를 위해(x,y 값), 속도를 위해 speed를 가져옴
    def __init__(self, xpos, ypos, speed):
        super(Rock, self).__init__()
        rock_images = ('rock01.png', 'rock02.png', 'rock03.png', 'rock04.png', 'rock05.png', \
                       'rock06.png', 'rock07.png', 'rock08.png', 'rock09.png', 'rock10.png', \
                       'rock11.png', 'rock12.png', 'rock13.png', 'rock14.png', 'rock15.png', \
                       'rock16.png', 'rock17.png', 'rock18.png', 'rock19.png', 'rock20.png', \
                       'rock21.png', 'rock22.png', 'rock23.png', 'rock24.png', 'rock25.png', \
                       'rock26.png', 'rock27.png', 'rock28.png', 'rock29.png', 'rock30.png')
        # 운석 이미지는 운석 인스턴스가 생성될 때마다 30개 중에서 랜덤으로 한개를 골라서 나타냄
        self.image = pygame.image.load(random.choice(rock_images))
        # 운석의 크기(위치)
        self.rect = self.image.get_rect()
        # 운석의 위치
        self.rect.x = xpos
        self.rect.y = ypos
        # 운석의 속도
        self.speed = speed

    # 운석의 위치값 업데이트 함수
    def update(self):
        # 운석의 y축 위치값 = y축 위치값 + 운석의 속도
        self.rect.y += self.speed

    # 운석도 화면 밖으로 나갈 수 있으므로 체크해주는 함수
    def out_of_screen(self):
        # 운석의 y축 위치값 > 화면 높이 이면(즉, 화면 아래쪽을 벗어나면)
        if self.rect.y > WINDOW_HEIGHT:
            # True 반환
            return True


# 점수 등을 출력하기 위한 함수
def draw_text(text, font, surface, x, y, main_color):
    # 텍스트 객체 정의
    text_obj = font.render(text, True, main_color)
    # 텍스트 위치값 정의
    text_rect = text_obj.get_rect()
    # 화면 중앙에 위치 시키기 위함
    text_rect.centerx = x
    text_rect.centery = y
    # 화면에 text_obj를 text_rect 위치에 뿌려줌
    surface.blit(text_obj, text_rect)


# 폭발과 관련된 함수
def occur_explosion(surface, x, y):
    # 폭발이 발생시 폭발이 발생한 위치에 폭발 이미지를 그려주고
    explosion_image = pygame.image.load('explosion.png')
    explosion_rect = explosion_image.get_rect()
    explosion_rect.x = x
    explosion_rect.y = y
    surface.blit(explosion_image, explosion_rect)

    # 3개의 폭발 사운드 중에 랜덤으로 1개를 골라서 사운드를 재생시킴
    explosion_sounds = ('explosion01.wav', 'explosion02.wav', 'explosion03.wav')
    explosion_sound = pygame.mixer.Sound(random.choice(explosion_sounds))
    explosion_sound.play()


# 반복되는 게임과 관련된 함수
def game_loop():
    default_font = pygame.font.Font('NanumGothic.ttf', 28)
    background_image = pygame.image.load('background.png')
    gameover_sound = pygame.mixer.Sound('gameover.wav')
    pygame.mixer.music.load('music.wav')
    # 음악 무한 반복 -> play(-1)
    pygame.mixer.music.play(-1)
    fps_clock = pygame.time.Clock()

    fighter = Fighter()
    # 전투기와는 달리 미사일은 여러개를 발사하여 여러개가 존재할 수 있기에
    # pygame.sprite.Gruop()으로 묶음
    missiles = pygame.sprite.Group()
    # 운석들도 미사일과 마찬가지로 그룹으로 묶음
    rocks = pygame.sprite.Group()

    # 운석 발생 확률
    occur_prob = 40
    # 맞힌 운석 갯수
    shot_count = 0
    # 놓친 운석 갯수
    count_missed = 0

    done = False
    while not done:
        # 이벤트를 받아오고
        for event in pygame.event.get():
            # 이벤트 타입이 키가 눌린 이벤트인 경우
            if event.type == pygame.KEYDOWN:
                # 왼쪽 방향키가 눌릴경우 x축 방향으로 5만큼 빼기
                if event.key == pygame.K_LEFT:
                    fighter.dx -= 5
                # 오른쪽 방향키가 눌릴경우 x축 방향으로 5만큼 더하기
                elif event.key == pygame.K_RIGHT:
                    fighter.dx += 5
                # 위쪽 방향키가 눌릴경우 y축 방향으로 5만큼 빼기
                # 화면 위쪽으로 가는 경우 y축 값이 줄어듬!
                elif event.key == pygame.K_UP:
                    fighter.dy -= 5
                # 아래쪽 방향키가 눌릴경우 y축 방향으로 5만큼 더하기
                elif event.key == pygame.K_DOWN:
                    fighter.dy += 5
                # 스페이스 키가 눌릴경우 미사일 발사와 관련된 이벤트 작성
                elif event.key == pygame.K_SPACE:
                    # 미사일 인스턴스 생성(전투기의 정중앙 위치, 전투기의 높이가 끝나는 지점, 속도는 10)
                    missile = Missile(fighter.rect.centerx, fighter.rect.y, 10)
                    # 미사일 발사 -> 미사일 사운드 재생
                    missile.launch()
                    # missiles = pygame.sprite.Group()
                    missiles.add(missile)

            # 이벤트 타입이 키에서 손을 뗀 이벤트인 경우
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    fighter.dx = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    fighter.dy = 0

        screen.blit(background_image, background_image.get_rect())

        # 운석 발생 빈도 = 맞힌 운석 갯수가 많을 수록 점점 더 운석을 많이 등장하게끔 함
        occur_of_rocks = 1 + int(shot_count / 300)
        # 운석의 최소, 최대 속도 = 맞힌 운석 갯수가 많을 수록 증가하도록
        min_rock_speed = 1 + int(shot_count / 200)
        max_rock_speed = 1 + int(shot_count / 100)

        # 운석 발생과 관련한 조건문
        # 1 ~ 위에서 정의한 운석 발생 확률 상수값 중에서 랜덤하게 뽑은 값이 1이 될 경우
        if random.randint(1, occur_prob) == 1:
            # 0~운석 발생 빈도-1 에서(즉, 운석 발생 갯수)
            for i in range(occur_of_rocks):
                # 운석 속도는 최소, 최대 속도 중에서 하나를 랜덤하게 고름
                speed = random.randint(min_rock_speed, max_rock_speed)
                # 운석 인스턴스 생성(운석의 x 위치는 0 ~ 화면 끝 - 30 중 랜덤하게, y 위치는 화면 맨위인 0, 그리고 운석 속도)
                rock = Rock(random.randint(0, WINDOW_WIDTH - 30), 0, speed)
                # rocks = pygame.sprite.Group()
                rocks.add(rock)

        # 위에서 정의한 화면에 점수 등을 출력하기 위한 draw_text(text, font, surface, x, y, main_color) 함수
        # 파괴한 운석
        # default_font = pygame.font.Font('NanumGothic.ttf', 28)
        # screen에 위치는 왼쪽 위(100, 20) 파괴한 운석 갯수를 노란색으로 출력
        draw_text('파괴한 운석: {}'.format(shot_count), default_font, screen, 100, 20, YELLOW)
        # 놓친 운석
        # 화면 오른쪽 위에 빨간색으로 출력
        draw_text('파괴한 운석: {}'.format(count_missed), default_font, screen, 400, 20, RED)

        # 미사일이 여러개가 발사됨
        # 따라서, 미사일 여러개가 충돌이 발생했는지를 체크
        for missile in missiles:
            rock = missile.collide(rocks)
            if rock:
                missile.kill()
                rock.kill()
                occur_explosion(screen, rock.rect.x, rock.rect.y)
                shot_count += 1

        # 여러개의 운석들이 존재함
        for rock in rocks:
            if rock.out_of_screen():
                rock.kill()
                count_missed += 1

        rocks.update()
        rocks.draw(screen)
        missiles.update()
        missiles.draw(screen)
        fighter.update()
        fighter.draw(screen)
        # 디스플레이에 flip()으로 전체 반영
        pygame.display.flip()

        if fighter.collide(rocks) or count_missed >= 3:
            pygame.mixer.music.stop()
            occur_explosion(screen, fighter.rect.x, fighter.rect.y)
            pygame.display.update()
            gameover_sound.play()
            sleep(1)
            done = True

        fps_clock.tick(FPS)

    return 'game_menu'


def game_menu():
    start_image = pygame.image.load('background.png')
    screen.blit(start_image, [0, 0])
    draw_x = int(WINDOW_WIDTH / 2)
    draw_y = int(WINDOW_HEIGHT / 4)
    font_70 = pygame.font.Font('NanumGothic.ttf', 70)
    font_40 = pygame.font.Font('NanumGothic.ttf', 40)

    draw_text('지구를 지켜라!', font_70, screen, draw_x, draw_y, YELLOW)
    draw_text('엔터 키를 누르면', font_40, screen, draw_x, draw_y + 200, WHITE)
    draw_text('게임이 시작됩니다.', font_40, screen, draw_x, draw_y + 250, WHITE)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            # 엔터 == K_RETURN
            if event.key == pygame.K_RETURN:
                return 'play'
        if event.type == QUIT:
            return 'quit'

    return 'game_menu'


def main():
    global screen

    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('PyShooting')

    action = 'game_menu'
    while action != 'quit':
        if action == 'game_menu':
            action = game_menu()
        elif action == 'play':
            action = game_loop()

    pygame.quit()


# 해당 스크립트에서 실행시 __main__: 이 부분이 먼저 실행됨
if __name__ == '__main__':
    main()


