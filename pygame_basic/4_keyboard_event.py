import pygame

pygame.init() #초기화 (반드시 필요) ,저장하면 빨간줄 떠서 우리는  File->Preference->Setting->linting검색 파이썬링틴 체크 지워주기

#화면 크기 설정
screen_width = 480 #가로크기
screen_height = 640 #세로크기
screen = pygame.display.set_mode((screen_width, screen_height)) #화면 설정한것을 변수 screen으로 받기

#화면 타이틀 설정
pygame.display.set_caption("TaeHyuk Game") #게임이름


#우선 배경에 이미지 넣기 위해서 윈도우+R키누르고 msprint 누르면 그림판 실행됨 크기조정에서 우리가 만든 가로 세로로 조정
#대충 연습이니까 색깔만 칠하고 저장 폴더를 왼쪽과 같이 한다.
background = pygame.image.load("C:/Users/98tae/OneDrive/바탕 화면/PythonWorkspace/Arcade-Game/pygame_basic/background.png") #load(여기다 경로 주면 이 경로 파일 불러옴)
#탈출문자 어쩌구 로인해 \를 / 로 바꾸기(경로는 파일 만들어진거 copy path로 가져옴)


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


#프로그램 종료되지 않도록 어디서 대기->파이게임에선 이벤트 루프가 항상 실행되고 있어야 창이 꺼지지 않는다
#이벤트 루프
running = True # 이변수 역활은 게임이 진행중인가 확인
while running:
    for event in pygame.event.get():      #여기까지 코드해석: 게임이 진행되는 동안 어떤 이벤트가 발생하면 처리
        if event.type == pygame.QUIT:     #여러 이벤트 발생할수 있는데 그중에 QUIT(창닫을때 엑스 버튼) 누르면 저렇게 바뀜
            running = False                #게임이 진행중이 아님

        if event.type == pygame.KEYDOWN:  #대문자 주의 이렇게 했을때는 즉 키보드 눌렀을때 밑에는 어떤 키보드 눌렸는지 확인하는거 집어넣기
            if event.key == pygame.K_LEFT: #캐릭터를 왼쪽으로
                to_x -= 1
            elif event.key == pygame.K_RIGHT: #캐릭터 오른쪽으로
                to_x += 1
            elif event.key == pygame.K_UP: #캐릭터 위
                to_y -= 1
            elif event.key == pygame.K_DOWN: #캐릭터 아래로
                to_y += 1 

        if event.type == pygame.KEYUP: #방향키를 떼면 멈춤
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                to_y = 0

    character_x_pos += to_x
    character_y_pos += to_y

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

    screen.blit(background, (0,0)) #백드라운드 이미지가 어디 좌표 0,0에서 부터 blit하면 배경 그려준다. 오른쪽 밑으로 퍼지면서 이미지 그려짐

    screen.blit(character, (character_x_pos, character_y_pos)) #캐릭터 그리기


    pygame.display.update() #파이게임에서는 와일을 계속 돌면서 화면을 계속 그려주는거 


#만약 running이 어디서 false가 되면 게임 나가지는거 리일 
pygame.quit()
