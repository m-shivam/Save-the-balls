from time import sleep
import shelve
import pygame as pg
from random import randint,randrange


#SOME STANDARD DECLARATION
pg.init()
gameIcon = pg.image.load('icon.jpg')
pg.display.set_icon(gameIcon)
window=pg.display.set_mode((800,600),0,32)
pg.display.set_caption("Save the balls")
c=pg.time.Clock()
bar=pg.image.load('redbar.png')
basket=pg.image.load('vball.png')
soccer=pg.image.load('cball.png')
sicon=pg.image.load('start.png')
qicon=pg.image.load('cross.png')
ricon=pg.image.load('repeat.png')
ts=pg.mixer.Sound('Tick.ogg')
gbs=pg.mixer.Sound('glass_break.wav')
my_font = pg.font.SysFont("comicsansms", 25,1)
overfont = pg.font.SysFont("comicsansms", 56)
startfont=pg.font.SysFont("comicsansms",85,1)
byfont=pg.font.SysFont("comicsansms",15,1)
hsfont=pg.font.SysFont("comicsansms",30,1)



d = shelve.open('score.txt') # here you will save the score variable
score=d['score']

#magic=pg.image.load('magic.png')

#FUNCTION DEFINITIONS
def button_action(p1,q1,p2,q2,do=None):
    drag=pg.mouse.get_pos()
    click=pg.mouse.get_pressed()
    if p1<drag[0]<p2 and q1<drag[1]<q2 and click[0]==1:
        if do=="play" or do=="reload":
            gameplay()
        #elif do=="home":
         #   goHome()
        elif do=="quit":
            pg.QUIT
            raise SystemExit


def startgame(scr):
    while True:
        window.fill([255, 240, 230])
        window.blit(sicon,(200,306))
        window.blit(qicon,(472,306))
        button_action(199, 305, 328, 434,"play")
        button_action(471, 305, 600, 434,"quit")

        start_text=startfont.render('Save the balls',True,[0,10,250])
        window.blit(start_text,(window.get_width() / 2 - start_text.get_rect().width / 2, 140))
        byme=byfont.render('By: Shivam Maurya',True,[0,0,0])
        window.blit(byme,(630,560))
        hscore = hsfont.render('Highest Score: '+str(scr), True, [0, 0, 0])
        hstext=hscore.get_rect()
        text_hs=window.get_width() / 2 - hstext.width / 2
        window.blit(hscore, (text_hs, 500))

        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.QUIT
                raise SystemExit
        pg.display.update()


def moveball(x,y,xp,yp,bx,scr,gover):
    xc, yc = xp,yp
    if x>=779:
        xc=randrange(-4,-3,1)
    elif y>=560:
        if bx-20>x or bx+220<x:
            gbs.set_volume(.2)
            gbs.play()
            sleep(1.5)
            gover=True
        else:
            ts.play()
            scr+=5
            yc = randrange(-6, -4, 1)
            if xc==0:
                if bx+110<x:
                    xc=randint(1,3)
                elif bx-112>x:
                    xc=randrange(-2,-1,1)

    elif x<=5:
        xc=randint(3,4)
    elif y<=5:
        yc=randint(4,6)
    return gover,scr,xc,yc

#def goHome():
#    startgame()

def gameover(scr):
    global score
    window.fill([250, 240, 230])
    text = overfont.render('Game Over', True, [250, 0, 0])
    yscr = overfont.render('You scored: ' + str(scr), True, [0, 50, 250])
    text_rect = text.get_rect()
    text_x = window.get_width() / 2 - text_rect.width / 2
    window.blit(text, (text_x,150 ))
    window.blit(yscr, (window.get_width()/2 - yscr.get_rect().width/2, 236 ))
    window.blit(ricon,(200,322))
    window.blit(qicon, (472, 322))
    button_action(200,332,328,460,"reload")
    button_action(470,332,598,460,"quit")
    if score<scr:
        d['score'] = scr

    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            pg.QUIT
            raise SystemExit
    pg.display.update()

def gameplay():
    scr = 0
    gover = False
    x1, y1 = randint(210, 450), 10
    x2, y2 = randint(351, 540), 310
    xb, yb = 390, 580
    xc1 = randint(-1, 1)
    yc1 = randint(3,5)
    xc2 = randint(1, 2)
    yc2 = randint(3,4)
    #to enable third ball uncomment the below lines containing '3'
    # x3,y3=randint(510,790),410
    # xc3=randint(-1,1)
    # yc3=randint(1,2)
    while True:
        if gover:
            gameover(scr)
        else:
            window.fill([255, 240, 230])
            window.blit(bar, (xb, yb))
            window.blit(basket, (x1, y1))
            window.blit(soccer, (x2, y2))
            #  window.blit(magic, (x3, y3))


            x1 += xc1
            y1 += yc1
            x2 += xc2
            y2 += yc2
            #  x3+=xc3
            #  y3+=yc3

            gover, scr, xc1, yc1 = moveball(x1, y1, xc1, yc1, xb, scr, gover)
            gover, scr, xc2, yc2 = moveball(x2, y2, xc2, yc2, xb, scr, gover)
            #  gover,scr,xc3,yc3=moveball(x3,y3,xc3,yc3,xb,scr,gover)
            scoresurf = my_font.render('score:' + str(scr), True, (0, 0, 0))
            window.blit(scoresurf, (10, 10))

            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    pg.QUIT
                    raise SystemExit
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_LEFT and xb > 5:
                        xb = xb - 5
                    if event.key == pg.K_RIGHT and xb < 805:
                        xb = xb + 5

            keys_pressed = pg.key.get_pressed()
            if keys_pressed[pg.K_RIGHT]:
                if xb > 595:
                    xb += 0
                else:
                    xb += 10
            elif keys_pressed[pg.K_LEFT]:
                if xb < 1:
                    xb += 0
                else:
                    xb -= 10

            pg.display.update()
            c.tick(callfps(scr))


def callfps(scr):
    fps=60
    if scr<=30:
        fps=30
    elif scr>30 and scr<=90:
        fps=45
    elif scr>90 and scr<=150:
        fps=60
    elif scr>150 and scr<=240:
        fps=75
    elif scr>240 and scr<=480:
        fps =90
    elif scr>480 and scr<=960:
        fps=120
    elif scr>960:
        fps=150
    return fps


startgame(score)
           # thats all, now it is saved on disk.
d.close()
raise SystemExit