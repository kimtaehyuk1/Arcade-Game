# 목표
# 1. 모든 공을 없애면 게임 종료 (성공)
# 2. 캐릭터는 공에 닿으면 게임 종료 (실패)
# 3. 시간 제한 99초 초과 시 게임 종료 (실패)

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


#캐릭터 만들기
character = pygame.image.load(os.path.join(image_path, "character.png"))
character_size = character.get_rect().size #이렇게 적으면 캐릭터 가로 세로 가 얼만지 구해옴
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2) - (character_width / 2)#화면 가로의 절반 크기에 해당하는 곳에 위치(가로)
character_y_pos = screen_height - character_height - stage_height  #스테이지 위에 놓이도록
# 배경은 (0,0)으로 해서 오른쪽 밑으로 퍼지면서 그려졌다. 즉 캐릭터도 그 생길 위치를 계산해서 오른쪽 밑으로 퍼지면서 그려줘야된다.

# 캐릭터가 이동할 좌표
character_to_x = 0


#이동속도
character_speed = 5

#무기 만들기
weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0] 
 
# 무기는 한 번에 여러 발 발사 가능
weapons = []

#무기 이동 속도
weapon_speed = 10

#공 만들기 (4개 크기에 대해 따로 처리)
ball_images = [ 
    pygame.image.load(os.path.join(image_path, "balloon1.png")),
    pygame.image.load(os.path.join(image_path, "balloon2.png")),
    pygame.image.load(os.path.join(image_path, "balloon3.png")),
    pygame.image.load(os.path.join(image_path, "balloon4.png"))]

# 공 크기에 따른 최초 스피드
ball_speed_y = [-18, -15, -12, -9] #인덱스 0,1,2,3 에 해당하는 값 -붙은 이유는 올라갈땐 -로 빠져야 되니까

#공들
balls = []

#최초로 발생하는 큰 공 추가 !!!!!딕셔너리로 저장한거임 그냥 갖다 이름만 쓰면 되는거
balls.append({
    "pos_x" : 50, #공의 x좌표
    "pos_y" : 50, #공의 y좌표
    "img_idx" :  0, #공크기에 따라 쓰는 공 다르니까 
    "to_x" : 3, #공의 x축 이동방향 -는 왼쪽 +면 오른쪽으로 간다.
    "to_y" : -6, #y축 이동방향,
    "init_spd_y" : ball_speed_y[0]}) #y로 최초 속도 즉 공마다 위로 올라가는 속도 다르다


#사라질 무기와 공 정보 저장 변수
weapon_to_remove = -1
ball_to_remove = -1


# 폰트 정의
game_font = pygame.font.Font(None, 40) #폰트 객체 생성 (폰트,크기)

#게임 종료 메시지 / 상태에 따라 TimeOut, Mission Complete, Game Over
game_result = "Game Over"

#총 시간
total_time = 100

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
                character_to_x -= character_speed
            elif event.key == pygame.K_RIGHT: #캐릭터 오른쪽으로
                character_to_x += character_speed
            elif event.key == pygame.K_SPACE: #무기 발사
                weapon_x_pos = character_x_pos + (character_width / 2) - (weapon_width / 2) #캐릭터의 위치가 계속 바뀌니까 무기 위치 계속 바뀜
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos]) #weapons에는 x,y값이 묶여져가지고 들어가있다.

        
        if event.type == pygame.KEYUP: #방향키를 떼면 멈춤
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0
            

    #3. 게임 캐릭터 위치 정의
    character_x_pos += character_to_x
    

    #가로 경계값 처리
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width: #오른쪽에 붙어있을땐  옆과 같이 해줘야 화면 안나감 (쫌 생각해보기)
        character_x_pos = screen_width - character_width

    # 무기 위치 조정
    weapons = [ [w[0], w[1] - weapon_speed] for w in weapons] # 무기 위치를 위로 !! 우선 한줄 for가 쓰였다.
    #설명: weapons에 있는 List에 있는 값들을 불러와서 w라고 하고, 그 w에 있는 값을 통해서 for 왼쪽의 처리를 한다, 
    # 뭘 처리하냐? w는 무기의 x,y좌표를 갖는 또다른 리스트인데, 리스트에서 0번째 인덱스의 값(즉 무기의 x는 변함없다.), 
    # 1번째 인덱스에 있는 값(y값은 스피드에 따라서 사라 져야 되니까) 에서 스피드를 뺸 값 이 두개를
    #엮어서 또다른 하나의 리스트로 감싼다.
    # 처리 한것들을 다시 weapons에 집어 넣는다.
    
    #천장에 닿은 무기 없애기
    weapons = [ [w[0], w[1] ] for w in weapons if w[1] > 0 ] #즉 y좌표가 스크린 안에 있을때만이라는 조건 달고 weapons의 x,y포지션만 뿌린다라는 뜻으로 받아드리자!

    ##여기져기 weapons썼다고 언제 누가 실행되냐 이런 문제가 아니라 걍 weapons에 대한 조건을 계속 달아준다고 생각하기

    #공 위치 정의
    for ball_idx, ball_val in enumerate(balls): #이것은 볼 리스트있는거 가져와서 현재 볼리스트에 있는 몇번쨰 인덱스인지 또 값을 출력
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        #가로벽에 닿았을떄 공 이동 위치 변경
        if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width:
            ball_val["to_x"] = ball_val["to_x"] * -1

        #세로 위치
        #스테이지에 튕겨서 올라가는 처리
        if ball_pos_y >= screen_height - stage_height - ball_height:  #이게 스테이지 닿았을때임
            ball_val["to_y"] = ball_val["init_spd_y"]

        else: #그 외의 모든 경우에는 속도를 증가
            ball_val["to_y"] += 0.5 #시작을 - 했기 땜에


        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]


    #4. 충돌 처리
    #충돌처리
    #캐릭터 rect 정보 업데이트
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    for ball_idx, ball_val in enumerate(balls): #이것은 볼 리스트있는거 가져와서 현재 볼리스트에 있는 몇번쨰 인덱스인지 또 값을 출력
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        #공 rect 정보 업데이트
        ball_rect = ball_images[ball_img_idx].get_rect()
        ball_rect.left = ball_pos_x
        ball_rect.top = ball_pos_y

        #공과 캐릭터 충돌 체크
        if character_rect.colliderect(ball_rect):
            running = False
            break

        #공과 무기들 충돌 처리 이것도 무기들이 많을수 있으니까 for으로
        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_pos_x =  weapon_val[0]
            weapon_pos_y =  weapon_val[1]

            #무기 rect 정보 업데이트
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x
            weapon_rect.top = weapon_pos_y

            #충돌 체크
            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove = weapon_idx #현재 무기 인덱스 값 넣줌 ; 해당무기 없애기 위한 값 설정
                ball_to_remove = ball_idx #해당 공 없애기 위한 값 설정

                if ball_img_idx < 3:  #가장 작은공이 아니라면 다음 단계의 공으로 나눠주는 역활

                    #현재 공 크기 정보를 가지고 옴
                    ball_width = ball_rect.size[0]
                    ball_height = ball_rect.size[1]

                    #나눠진 공 정보
                    small_ball_rect = ball_images[ball_img_idx + 1].get_rect() #나눠진 공이니까 ball_img_idx에서 +1하면 더 작은공 가져와짐
                    small_ball_width = small_ball_rect.size[0]
                    small_ball_height = small_ball_rect.size[1] 

                    #왼쪽으로 튕겨나가는 작은 공
                    balls.append({
                        "pos_x" : ball_pos_x + (ball_width / 2) - (small_ball_width / 2 ), #이렇게 해야 가운데서 쪼개지는데 더하여 왼쪽으로 가는거 처럼!
                        "pos_y" : ball_pos_y + (ball_height / 2) - (small_ball_height / 2),
                        "img_idx" : ball_img_idx + 1, # 작은거 나와야 되니까
                        "to_x" : -3, #공의 x축 이동방향 -는 왼쪽 +면 오른쪽으로 간다.
                        "to_y" : -6, #y축 이동방향 살짝 올라갔다 내려오는 그 속도
                        "init_spd_y" : ball_speed_y[ball_img_idx + 1]}) #y로 최초 속도 즉 공마다 위로 올라가는 속도 다르다

                    #오른쪽으로 튕겨나가는 작은 공
                    balls.append({
                        "pos_x" : ball_pos_x + (ball_width / 2) - (small_ball_width / 2 ), #이렇게 해야 가운데서 쪼개지는데 더하여 왼쪽으로 가는거 처럼!
                        "pos_y" : ball_pos_y + (ball_height / 2) - (small_ball_height / 2),
                        "img_idx" : ball_img_idx + 1, # 작은거 나와야 되니까
                        "to_x" : +3, #공의 x축 이동방향 -는 왼쪽 +면 오른쪽으로 간다.
                        "to_y" : -6, #y축 이동방향 살짝 올라갔다 내려오는 그 속도
                        "init_spd_y" : ball_speed_y[ball_img_idx + 1]}) #y로 최초 속도 즉 공마다 위로 올라가는 속도 다르다   


                break

    #충돌된 공 혹은 무기 없애기
    if ball_to_remove > -1: #위의 ball인덱스는 0 1 2 3 이렇게 될거기 때문에 즉 충돌하면 위의 충돌체크 메소드의 값이 들어가버리니까 -1 에서 0보다 숫자가 큰 것으로 바뀔것이다.
        del balls[ball_to_remove]
        ball_to_remove = -1 #이렇게 해야 다시 돌기 때문에

    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1
    
    #모든 공을 없앤 경우 게임 종료 (성공)
    if len(balls) == 0:
        game_result = "Mission Complete"
        running = False


    #5. 화면에 그리기

    screen.blit(background, (0,0)) #백드라운드 이미지가 어디 좌표 0,0에서 부터 blit하면 배경 그려준다. 오른쪽 밑으로 퍼지면서 이미지 그려짐

    for weapon_x_pos, weapon_y_pos in weapons: #무기 쏘아지는게 계속 바뀌니까 for로 screen 그려주기
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

    for idx, val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_idx = val["img_idx"]
        screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y))

    screen.blit(stage, (0,screen_height - stage_height))

    screen.blit(character, (character_x_pos, character_y_pos)) #캐릭터 그리기

    

    #타이머 집어 넣기
    #경과 시간 계산
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000 #나누는 이유는 이거는 밀리세컨드(ms)여서 우리는 초로 환산하기 위해
    
    timer = game_font.render("Time : {}".format(int(total_time - elapsed_time)), True, (255,255,255)) #랜더는 실제 글짜 그리는거 다시 정리하면 출력할글자,True,글자색상

    screen.blit(timer,(10,10))

    #만약 시간이 0 이하이면 게임 종료
    if total_time - elapsed_time <= 0:
        game_result = "Time Over"
        running = False


    pygame.display.update() #파이게임에서는 와일을 계속 돌면서 화면을 계속 그려주는거 


# 게임 오버 메시지
msg = game_font.render(game_result, True, (255,255,0)) #노란색
msg_rect = msg.get_rect(center=(int(screen_width / 2), int(screen_height / 2)))
screen.blit(msg, msg_rect)
pygame.display.update()

#잠시 대기
pygame.time.delay(2000) #2초 정도 대기

#만약 running이 어디서 false가 되면 게임 나가지는거 리일 
pygame.quit()
