import pygame
import random
import os
from time import sleep

image_resource_path = './PyRacingCar_Resource/image/'
game_intro_image_resource_path = image_resource_path + 'Game_Intro_image/'
racing_car_image_resource_path = image_resource_path + 'RacingCar_image/'
sound_resource_path = './PyRacingCar_Resource/sound/'

WINDOW_WIDTH = 480
WINDOW_HEIGHT = 800

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
RED = (255, 0, 0)


# car 클래스
class Car:
    image_car = os.listdir(racing_car_image_resource_path)

    def __init__(self, x=0, y=0, dx=0, dy=0):
        self.image = ''
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    def load_image(self):
        self.image = pygame.image.load(racing_car_image_resource_path + random.choice(self.image_car))
        self.width = self.image.get_rect().size[0]  # size[0] : 0 인덱스가 width
        self.height = self.image.get_rect().size[1]  # size[1] : 1 인덱스가 height

    def draw_image(self):
        # 스크린의 x,y 좌표에 image를 뿌려라
        screen.blit(self.image, [self.x, self.y])

    def move_x(self):
        # x축으로 플레이어가 방향하는 만큼 더해줌(해당 방향으로 방향키를 누르는 만큼)
        self.x += self.dx

    def move_y(self):
        self.y += self.dy

    # 자동차가 화면 밖으로 나가지 않도록 해주는 함수
    def check_out_of_screen(self):
        # 자동차의 x축에서의 위치와 자동차의 너비를 더한 값이 화면 너비보다 커지거나(오른쪽 끝)
        # 자동차의 x축에서의 위치가 0보다 작아지면(왼쪽 끝)
        if self.x + self.width > WINDOW_WIDTH or self.x < 0:
            # 자동차의 x축 좌표에서 해당 방향으로 이동하는 만큼을 빼줌
            # 그러면 아무리 해도 화면 밖으로 나가지지 않겠지
            self.x -= self.dx

    # 자동차의 충돌을 체크하는 함수
    def check_crash(self, computer_car):
        # 자동차와 자동차 간의 겹치는 부분을 체크하는 조건문 모두 True가 나오면 충돌 발생
        if (self.x + self.width > computer_car.x) and (self.x < computer_car.x + computer_car.width) and \
                (self.y < computer_car.y + computer_car.height) and (self.y + self.height > computer_car.y):
            return True
        else:
            return False


# 메인 메뉴를 그려주는 함수
def draw_main_menu():
    draw_x = (WINDOW_WIDTH / 2) - 200
    draw_y = WINDOW_HEIGHT / 2
    image_intro = pygame.image.load(game_intro_image_resource_path + 'PyCar.png')
    # y축은 뺄수록 화면 위쪽으로 상승, x축은 뺄수록 화면 왼쪽으로 감
    screen.blit(image_intro, [draw_x, draw_y - 280])
    font_40 = pygame.font.SysFont('FixedSys', 40, True, False)
    font_30 = pygame.font.SysFont('FixedSys', 30, True, False)
    text_title = font_40.render('PyCar: Racing Car Game', True, BLACK)
    screen.blit(text_title, [draw_x, draw_y])
    text_score = font_40.render('Score: ' + str(score), True, WHITE)
    screen.blit(text_score, [draw_x, draw_y + 70])
    text_start = font_30.render('Press Space Key to Start!', True, RED)
    screen.blit(text_start, [draw_x, draw_y + 140])
    pygame.display.flip()


# 게임 중 보여지는 점수(score)를 그려주는 함수
def draw_score():
    font_30 = pygame.font.SysFont('FixedSys', 30, True, False)
    text_score = font_30.render('Score: ' + str(score), True, BLACK)
    screen.blit(text_score, [15, 15])


if __name__ == '__main__':

    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('PyCar: Racing Car Game')
    clock = pygame.time.Clock()

    pygame.mixer.music.load(sound_resource_path + 'race.wav')
    sound_crash = pygame.mixer.Sound(sound_resource_path + 'crash.wav')
    sound_engine = pygame.mixer.Sound(sound_resource_path + 'engine.wav')

    # Car(x좌표 위치는 화면 중앙, y좌표 위치는 밑에서 150정도 뺀 밑에서 살짝 위쪽, dx = 0, dy = 0)
    player = Car(int(WINDOW_WIDTH / 2), (WINDOW_HEIGHT - 150), 0, 0)
    player.load_image()

    cars = []
    car_count = 3
    for i in range(car_count):
        # 컴퓨터 레이싱 카의 x축 위치는 (0~WINDOW_WIDTH-55) 중 랜덤한 곳에서
        x = random.randrange(0, WINDOW_WIDTH-55)
        # y축 위치는 약간 위쪽에서 나타나도록
        y = random.randrange(-150, -50)
        # Car(자동차의 x,y축 위치, dx=0, dy=random.randint(5, 10))
        car = Car(x, y, 0, random.randint(5, 10))
        car.load_image()
        # 실제 car 인스턴스를 cars 리스트에 append
        cars.append(car)

    # 도로에 회색만 있다면 박진감이 없음
    # 주변의 움직임이 자동차가 움직이고 있다는 것을 좀 더 느끼게 해줌
    # 따라서 도로 가운데 차선을 넣어서 차선을 움직이게 하여 박진감을 느끼도록 함
    lanes = []
    lane_width = 10  # 차선의 가로 길이
    lane_height = 80  # 차선의 세로 길이
    lane_margin = 20  # 차선 간의 폭
    lane_count = 20  # 화면 내에서 20개의 차선을 보여주게끔
    # 차선의 x 축 위치는 화면의 중앙에 위치 시켜야 하므로
    # (화면 너비 - 차선 가로 너비) / 2 == 화면의 정중앙에 차선이 보여지게 됨
    lane_x = (WINDOW_WIDTH - lane_width) / 2
    lane_y = -10
    for i in range(lane_count):
        lanes.append([lane_x, lane_y])
        lane_y += lane_height + lane_margin

    # 점수를 보여주게할 score 변수 초기화
    score = 0
    # 자동차가 충돌 되었을 때를 확인할 crash 변수 초기화
    crash = True
    game_on = True
    # 게임이 진행중인 동안 반복문
    while game_on:
        # 게임 진행중 모든 이벤트 관련 반복문
        for event in pygame.event.get():
            #  게임 종료 버튼(창 닫기 버튼) 클릭 시 발생하거나 커맨드창에서 Ctrl + C를 입력하면 발생함
            if event.type == pygame.QUIT:
                game_on = False

            # 충돌이 발생하면
            if crash:
                # 스페이스바를 누르면 게임이 다시 시작되도록
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    # 게임이 새로 시작 되었으므로 crash 변수는 False로 다시 바꿔주고
                    crash = False
                    # 새로운 컴퓨터 자동차들이 나타나도록 car_count에서 반복문을 돌림
                    for i in range(car_count):
                        # 자동차의 x축 위치는 (0 ~ 화면너비 - 자동차의 가로 길이) 중에서 랜덤으로
                        cars[i].x = random.randrange(0, WINDOW_WIDTH - cars[i].width)
                        # 자동차의 y축 위치는 (-150 ~ -50) 중 랜덤으로
                        cars[i].y = random.randrange(-150, -50)
                        # 자동차의 위치를 선정했으면, 자동차의 이미지를 load 해줌
                        cars[i].load_image()

                    # 플레이어 자동차도 초기화
                    player.load_image()
                    player.x = WINDOW_WIDTH / 2
                    player.dx = 0

                    # 점수 초기화
                    score = 0
                    # 마우스도 화면에서 보이지 않도록 해줌
                    pygame.mouse.set_visible(False)
                    # 게임이 시작될 때 엔진음이 울리고 게임이 시작됨
                    sound_engine.play()
                    sleep(5) # 엔진 소리 좀 듣고 있도록 5초 정도 쉬고
                    pygame.mixer.music.play(-1) # race.wav가 반복 재생되도록 -1 파라미터를 줌

            # crash가 나지 않았을 경우 -> 현재 게임중
            if not crash:
                # 해당 방향키가 눌렸을 경우엔 해당 방향으로 플레이어가 움직이도록하고
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        player.dx = 4
                    elif event.key == pygame.K_LEFT:
                        player.dx = -4
                # 해당 방향키가 떼졌을 경우엔 해당 방향에서 가만히 있도록 함
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        player.dx = 0
                    elif event.key == pygame.K_LEFT:
                        player.dx = 0

        # 게임 진행중 이벤트 제외 외적인 부분
        # 화면을 회색 바탕으로 채우고
        screen.fill(GRAY)

        # 충돌이 발생하지 않을 경우 -> 게임 진행중
        if not crash:
            # 차선과 관련된 반복문
            for i in range(lane_count):
                # pygame.draw.rect(Surface, color, Rect, Width = default 0)
                # Rect 부분은 사각형의 [x축, y축, 가로, 세로]의 형태로 삽입함
                # Width는 사각형의 선 크기를 말하며, 생략 가능(default = 0)
                # lanes = [[lane_x1, lane_y1], [lane_x2, lane_y2], [lane_x3, lane_y3] ... ]
                # 따라서, lanes[i][0] == lane_x 시리즈, lanes[i][1] == lane_y 시리즈
                pygame.draw.rect(screen, WHITE, [lanes[i][0], lanes[i][1], lane_width, lane_height])
                # 중요!
                # lanes가 계속 밑으로 내려오도록(움직이는 것처럼 보이도록) 함
                lanes[i][1] += 10
                # 너무 내려가서 화면 세로 길이보다 커질 경우
                if lanes[i][1] > WINDOW_HEIGHT:
                    # 화면 위쪽에서 내려오는 것처럼 보이도록 다시 위로 올림
                    lanes[i][1] = -40 - lane_height

            # 플레이어 자동차를 그려줌
            player.draw_image()
            # 플레이어 자동차가 y좌표로는 움직이지 않으므로 move_x()만
            player.move_x()
            # 플레이어 자동차가 화면 밖으로 나갔는지를 체크해주는 함수를 실행 시킴
            player.check_out_of_screen()

            # 컴퓨터 자동차 관련 반복문(여러개의 자동차가 배열에 있기 때문에 반복문으로 접근)
            for i in range(car_count):
                cars[i].draw_image() # 자동차를 그려주고
                cars[i].y += cars[i].dy # 컴퓨터 자동차는 y축 방향으로만 움직임
                # 만약 컴퓨터 자동차의 y축 위치가 화면 세로 길이를 벗어난다면
                # 그러면, 플레이어가 컴퓨터 자동차를 피한 것이되므로
                if cars[i].y > WINDOW_HEIGHT:
                    # 점수 += 10
                    score += 10
                    # 새로운 컴퓨터 자동차를 등장시킴
                    # 자동차의 x축 위치는 (0 ~ 화면너비 - 자동차의 가로 길이) 중에서 랜덤으로
                    cars[i].x = random.randrange(0, WINDOW_WIDTH - cars[i].width)
                    # 자동차의 y축 위치는 (-150 ~ -50) 중 랜덤으로
                    cars[i].y = random.randrange(-150, -50)
                    # 새로 나타나는 컴퓨터 자동차의 속도 역시 5 ~ 10 중에서 랜덤한 값으로 설정
                    cars[i].dy = random.randint(5, 10)
                    # 자동차의 위치, 속도를 설정했으면, 자동차의 이미지를 load 해줌
                    cars[i].load_image()

            # 플레이어 자동차가 컴퓨터 자동차와 충돌이 발생했는지를 체크
            for i in range(car_count):
                # 만약 충돌이 발생했다면
                if player.check_crash(cars[i]):
                    crash = True  # crash 변수를 True로 변경해주고
                    pygame.mixer.music.stop()  # pygame.mixer.music 즉, 배경음악을 멈추고
                    sound_crash.play()  # 충돌 음악을 약 2초간 플레이 해주고
                    sleep(2)
                    pygame.mouse.set_visible(True)  # 마우스를 다시 보여줘서 게임이 끝났다는 것을 알리고
                    break  # 반복문 종료

            # 점수를 화면에 띄우고 새로운 화면으로 flip()
            draw_score()
            pygame.display.flip()

        # 충돌이 발생했을 경우 혹은 처음 시작시
        else:
            draw_main_menu()

        clock.tick(60)

    # while game_on = False로 게임이 진행중이란 반복문이 종료된 경우
    pygame.quit()












