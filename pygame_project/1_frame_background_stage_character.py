
import os
#!!!!!!!!!!여긴 다음에 게임 계발할때도 여기서 frame 따 놓고!!!!!!!!!!!!!!!!!!!!!!!!!!

import pygame

########################################################################################################################
pygame.init() #초기화 (반드시 필요) ,저장하면 빨간줄 떠서 우리는  File->Preference->Setting->linting검색 파이썬링틴 체크 지워주기

#화면 크기 설정
screen_width = 640 #가로크기
screen_height = 480 #세로크기
screen = pygame.display.set_mode((screen_width, screen_height)) #화면 설정한것을 변수 screen으로 받기

#화면 타이틀 설정
pygame.display.set_caption("아케이드 게임") #게임이름

#FPS
clock = pygame.time.Clock()
#여기 까진 무조건 해줘야 되는거
#######################################################################################################################

# 1. 사용자 게임 초기화 (배경화면, 게임 이미지, 좌표, 속도, 폰트)

current_path = os.path.dirname(__file__) #이러면 지금 수행하려는 이 파일 위치를 반환
image_path = os.path.join(current_path, "images") #이렇게 하면 image폴더 위치 반환

#배경 만들기
background = pygame.image.load(os.path.join(image_path, "background.png")) # 절대경로 말고 이렇게 함

#stage 만들기
stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1] # 스테이지 높이 계산해서 캐릭터 이 위에 두려고




#캐릭터(스프라이트) 불러오기
character = pygame.image.load("C:/Users/98tae/OneDrive/바탕 화면/PythonWorkspace/Arcade-Game/pygame_basic/character.png")
character_size = character.get_rect().size #이렇게 적으면 캐릭터 가로 세로 가 얼만지 구해옴
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = screen_width / 2 - (character_width / 2)#화면 가로의 절반 크기에 해당하는 곳에 위치(가로)
character_y_pos = screen_height - character_height #화면 세로크기 가장 아래에(세로)
# 배경은 (0,0)으로 해서 오른쪽 밑으로 퍼지면서 그려졌다. 즉 캐릭터도 그 생길 위치를 계산해서 오른쪽 밑으로 퍼지면서 그려줘야된다.

#이동할 좌표
to_x = 0
to_y = 0

#이동속도
character_speed = 0.6

#적 enemy 캐릭터
enemy = pygame.image.load("C:/Users/98tae/OneDrive/바탕 화면/PythonWorkspace/Arcade-Game/pygame_basic/enemy.png")
enemy_size = enemy.get_rect().size #이렇게 적으면 캐릭터 가로 세로 가 얼만지 구해옴
enemy_width = enemy_size[0]
enemy_height = enemy_size[1]
enemy_x_pos = (screen_width / 2) - (enemy_width / 2)#화면 가로의 절반 크기에 해당하는 곳에 위치(가로)
enemy_y_pos = (screen_height / 2) - (enemy_height / 2) #화면 세로크기 가장 아래에(세로)


# 폰트 정의
game_font = pygame.font.Font(None, 40) #폰트 객체 생성 (폰트,크기)

#총 시간
total_time = 10

#시작 시간 정보
start_ticks = pygame.time.get_ticks() #시작 tick 을 받아옴



#프로그램 종료되지 않도록 어디서 대기->파이게임에선 이벤트 루프가 항상 실행되고 있어야 창이 꺼지지 않는다
#이벤트 루프
running = True # 이변수 역활은 게임이 진행중인가 확인
while running:
    dt = clock.tick(30) #게임화면의 초당 프레임 수를 설정

    # 2. 이벤트 처리( 키보드, 마우스 등)
    for event in pygame.event.get():      #여기까지 코드해석: 게임이 진행되는 동안 어떤 이벤트가 발생하면 처리
        if event.type == pygame.QUIT:     #여러 이벤트 발생할수 있는데 그중에 QUIT(창닫을때 엑스 버튼) 누르면 저렇게 바뀜
            running = False                #게임이 진행중이 아님

        if event.type == pygame.KEYDOWN:  #대문자 주의 이렇게 했을때는 즉 키보드 눌렀을때 밑에는 어떤 키보드 눌렸는지 확인하는거 집어넣기
            if event.key == pygame.K_LEFT: #캐릭터를 왼쪽으로
                to_x -= character_speed
            elif event.key == pygame.K_RIGHT: #캐릭터 오른쪽으로
                to_x += character_speed
            elif event.key == pygame.K_UP: #캐릭터 위
                to_y -= character_speed
            elif event.key == pygame.K_DOWN: #캐릭터 아래로
                to_y += character_speed 

        if event.type == pygame.KEYUP: #방향키를 떼면 멈춤
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                to_y = 0

    #3. 게임 캐릭터 위치 정의
    character_x_pos += to_x * dt
    character_y_pos += to_y * dt

    #가로 경계값 처리
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width: #오른쪽에 붙어있을땐  옆과 같이 해줘야 화면 안나감 (쫌 생각해보기)
        character_x_pos = screen_width - character_width
    #세로 경계값 처리
    if character_y_pos < 0:
        character_y_pos = 0
    elif character_y_pos > screen_height - character_height:
        character_y_pos = screen_height - character_height

    #4. 충돌 처리
    #충돌처리
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    enemy_rect = enemy.get_rect()
    enemy_rect.left = enemy_x_pos
    enemy_rect.top = enemy_y_pos

    #충돌 체크
    if character_rect.colliderect (enemy_rect): #캐릭터가 적이랑 충돌을 했느냐 확인
        print("충돌했어요")
        running = False

    #5. 화면에 그리기

    screen.blit(background, (0,0)) #백드라운드 이미지가 어디 좌표 0,0에서 부터 blit하면 배경 그려준다. 오른쪽 밑으로 퍼지면서 이미지 그려짐

    screen.blit(stage, (0,screen_height - stage_height))

    screen.blit(character, (character_x_pos, character_y_pos)) #캐릭터 그리기

    screen.blit(enemy, (enemy_x_pos, enemy_y_pos))  #적 그리기

    #타이머 집어 넣기
    #경과 시간 계산
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000 #나누는 이유는 이거는 밀리세컨드(ms)여서 우리는 초로 환산하기 위해
    
    timer = game_font.render(str(int(total_time - elapsed_time)), True, (255,255,255)) #랜더는 실제 글짜 그리는거 다시 정리하면 출력할글자,True,글자색상

    screen.blit(timer,(10,10))

    #만약 시간이 0 이하이면 게임 종료
    if total_time - elapsed_time <= 0:
        print("타임아웃")
        running = False


    pygame.display.update() #파이게임에서는 와일을 계속 돌면서 화면을 계속 그려주는거 


#잠시 대기
pygame.time.delay(2000) #2초 정도 대기

#만약 running이 어디서 false가 되면 게임 나가지는거 리일 
pygame.quit()
