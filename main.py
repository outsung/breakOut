import pygame
import random
import math

# 1300 x 800
screenX = 1300
screenY = 800
screenColor = (255,212,142)

# 900 x 700
GscreenX = screenX - 400
GscreenY = screenY - 100
GscreenColor = (20,20,20)
GscreenMargin = 50

pygame.init()

# sprite 로 만들어줌
class Block(pygame.sprite.Sprite):
    def __init__(self,img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = img.get_rect()


# 폰트
font = pygame.font.SysFont("notosanscjkkr",30)
Mfont = pygame.font.SysFont("notosanscjkkr",80)
Efont = pygame.font.SysFont("notosanscjkkr",180)

# 효과음
Sound = pygame.mixer.Sound("./sound/dding.wav")

# 게임 화면
screen = pygame.display.set_mode((screenX,screenY))

# 이미지 불러오기 (공, 벽돌)
ballSize = 20

ballimage = pygame.image.load('./img/ball.png').convert_alpha()
ballimage = pygame.transform.scale(ballimage, (ballSize, ballSize))
ball = Block(ballimage)

brickSizeX = 120
brickSizeY = 20

brickimage = pygame.image.load('./img/brick.png').convert_alpha()
brick = Block(brickimage)
#brickimage = pygame.transform.scale(brickimage,(120,20))

#블럭
block = []

blockX = 88
blockY = 25

blockMargin = 3

blockimage_red = pygame.image.load('./img/block_red.png').convert_alpha()
blockimage_red = pygame.transform.scale(blockimage_red, (blockX, blockY))

block_red = Block(blockimage_red)
block_red.rect.center = (1040,210)

block.append(blockimage_red)


blockimage_blue = pygame.image.load('./img/block_blue.png').convert_alpha()
blockimage_blue = pygame.transform.scale(blockimage_blue, (blockX, blockY))

block_blue = Block(blockimage_blue)
block_blue.rect.center = (1040,260)

block.append(blockimage_blue)


blockimage_yellow = pygame.image.load('./img/block_yellow.png').convert_alpha()
blockimage_yellow = pygame.transform.scale(blockimage_yellow, (blockX, blockY))

block_yellow = Block(blockimage_yellow)
block_yellow.rect.center = (1040,310)

block.append(blockimage_yellow)


blockimage_green = pygame.image.load('./img/block_green.png').convert_alpha()
blockimage_green = pygame.transform.scale(blockimage_green, (blockX, blockY))

block_green = Block(blockimage_green)
block_green.rect.center = (1040,360)

block.append(blockimage_green)



# Game 초기화
blockCountX = 3
blockCountY = 1

ballSpeed = 1

level = 1

# 뿌신것 red, green, yellow, blue
color = [0,0,0,0]


End = True

Game = True
while Game:

    score = 0

    #맵
    map = pygame.sprite.Group()

    # 3 ~ 9
    #blockCountX = 3
    blockCountX = min(blockCountX, 9)
    # 1 ~ 9
    #blockCountY = 1
    blockCountY = min(blockCountY, 9)

    mapMarginX = ( GscreenX - ( (blockCountX+1) * blockX) ) // 2
    mapMarginY = GscreenMargin + 30

    for j in range(1, blockCountY + 1):
        for i in range(1, blockCountX + 1):
            randomColor = random.randrange(4)
            setBlock = Block(block[randomColor])
            setBlock.rect.x = mapMarginX + i * (blockX + blockMargin)
            setBlock.rect.y = mapMarginY + j * (blockY + blockMargin)
            setBlock.mask = pygame.mask.from_surface(setBlock.image)
            setBlock.color = randomColor
            map.add(setBlock)



    # 공  초기화
    ballx = 475.0
    bally = 600.0

    ball.rect.center = (ballx, bally)
    ball.mask = pygame.mask.from_surface(ball.image)
    #ball.radius = ballSize


    #ballSpeed = 1

    # 0 ~ 90
    ballAngle = 70

    ballMoveXdir = 1
    ballMoveYdir = -1

    ballMoveX = math.cos(math.radians(ballAngle)) * ballSpeed * ballMoveXdir
    ballMoveY = math.sin(math.radians(ballAngle)) * ballSpeed * ballMoveYdir

    # 벽돌 초기화
    brick.mask = pygame.mask.from_surface(brick.image)

    brickY = 650

    brick.center = (pygame.mouse.get_pos()[0], brickY)
    if brick.rect.center[0] - (brickSizeX // 2) < GscreenMargin:
        brick.rect.center = ((brickSizeX // 2) + GscreenMargin, brickY)
    if brick.rect.center[0] + (brickSizeX // 2) > GscreenMargin + GscreenX :
        brick.rect.center = (GscreenMargin + GscreenX - (brickSizeX // 2), brickY)


    # 맵 루프
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                Game = False
                End = False

        # 맵 클리어
        if score == blockCountX * blockCountY:
            blockCountX += 1
            blockCountY += 1
            level += 1
            ballSpeed += 1
            done = True

        # 벽돌 이동
        pos = pygame.mouse.get_pos()
        brick.rect.center = (pos[0], brickY)
        if brick.rect.center[0] - (brickSizeX // 2) < GscreenMargin:
            brick.rect.center = ((brickSizeX // 2) + GscreenMargin, brickY)
        if brick.rect.center[0] + (brickSizeX // 2) > GscreenMargin + GscreenX :
            brick.rect.center = (GscreenMargin + GscreenX - (brickSizeX // 2), brickY)


        # block x ball 충돌
        hit_list = pygame.sprite.spritecollide(ball,map,True,pygame.sprite.collide_mask)
        for h in hit_list:
            Sound.play()

            color[h.color] += 1

            collide = pygame.sprite.collide_mask(h,ball)

            left = collide[0]
            right = blockX - left
            top = collide[1]
            bottom = blockY - top

            # 모서리
            if (left == top) or (left == bottom) or (right == top) or (right == bottom):
                ballMoveYdir *= -1
                ballMoveXdir *= -1
            else:
                if(min(left, right) < min(top, bottom)):
                    ballMoveXdir *= -1
                else:
                    ballMoveYdir *= -1

            score += 1
            #print("score : " + str(score))

        # brick x ball 충돌
        #hit_list = pygame.sprite.spritecollide(ball,brick,False,pygame.sprite.collide_mask)
        if pygame.sprite.collide_mask(ball,brick):
            ballMoveYdir = -1

        #ballx += ballMoveX
        #bally += ballMoveY

        # 출력
        screen.fill(screenColor)
        pygame.draw.rect(screen, GscreenColor,(GscreenMargin,GscreenMargin,GscreenX,GscreenY))

        map.draw(screen)
        #ball.draw(screen)
        screen.blit(ballimage, ball)
        screen.blit(brickimage, brick)


        scoreStr = font.render("score : " + str(score),True,(28,0,0))
        screen.blit(scoreStr,(870,20))

        mapStr = Mfont.render("level : " + str(level),True,(28,0,0))
        screen.blit(mapStr,(970,70))

        # 뿌신 거
        screen.blit(blockimage_red, block_red)
        redStr = font.render("X " + str(color[0]),True,(28,0,0))
        screen.blit(redStr,(1100,200))

        screen.blit(blockimage_green, block_green)
        greenStr = font.render("X " + str(color[1]),True,(28,0,0))
        screen.blit(greenStr,(1100,250))

        screen.blit(blockimage_yellow, block_yellow)
        yellowStr = font.render("X " + str(color[2]),True,(28,0,0))
        screen.blit(yellowStr,(1100,300))

        screen.blit(blockimage_blue, block_blue)
        blueStr = font.render("X " + str(color[3]),True,(28,0,0))
        screen.blit(blueStr,(1100,350))


        pygame.display.flip()

        # 위치 update

        ballMoveX = math.cos(math.radians(ballAngle)) * ballSpeed * ballMoveXdir
        ballMoveY = math.sin(math.radians(ballAngle)) * ballSpeed * ballMoveYdir

        ballx += ballMoveX
        bally += ballMoveY
        ball.rect.center = (ballx, bally)

        if ball.rect.center[0] + (ballSize // 2) > (GscreenMargin + GscreenX): #오른쪽
           ballMoveXdir = -1
        if ball.rect.center[0] - (ballSize // 2) < GscreenMargin: #왼쪽
           ballMoveXdir = 1
        if ball.rect.center[1] - (ballSize // 2) < GscreenMargin: #위
           ballMoveYdir = 1
        if ball.rect.center[1] + (ballSize // 2) > (GscreenMargin + GscreenY): #아래
           done = True
           Game = False


screen.fill((30,30,30))

mapStr = Efont.render("Top level : " + str(level),True,(200,200,200))
screen.blit(mapStr,(350,300))

pygame.display.flip()

while End:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            End = False

pygame.quit()
