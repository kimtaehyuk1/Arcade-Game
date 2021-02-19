import pygame

pygame.init() #초기화 (반드시 필요) ,저장하면 빨간줄 떠서 우리는  File->Preference->Setting->linting검색 파이썬링틴 체크 지워주기

#화면 크기 설정
screen_width = 480 #가로크기
screen_height = 640 #세로크기
screen = pygame.display.set_mode((screen_width, screen_height)) #화면 설정한것을 변수 screen으로 받기

#화면 타이틀 설정
pygame.display.set_caption("TaeHyuk Game") #게임이름

#프로그램 종료되지 않도록 어디서 대기->파이게임에선 이벤트 루프가 항상 실행되고 있어야 창이 꺼지지 않는다
#이벤트 루프
running = True # 이변수 역활은 게임이 진행중인가 확인
while running:
    for event in pygame.event.get():      #여기까지 코드해석: 게임이 진행되는 동안 어떤 이벤트가 발생하면 처리
        if event.type == pygame.QUIT:     #여러 이벤트 발생할수 있는데 그중에 QUIT(창닫을때 엑스 버튼) 누르면 저렇게 바뀜
            running = False                #게임이 진행중이 아님

#만약 running이 어디서 false가 되면 게임 나가지는거 리일
pygame.quit()