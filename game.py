import sys;
from pygame.locals import *
import pygame
import time
from random import randint

screen_width = 1080
screen_height = 720

win_size = screen_width,screen_height
ground =  screen_height - 150
max_jump_height = ground - 180
start_score = 1000
movement_speed = 15
bullet_speed = 100
jumpStrength = 15
gravity = 10
dayLength = 10
TopSunX = screen_width/2 - 200
TopSunY = 0
startMenuDayLength = 1
screen = pygame.display.set_mode(win_size);
#kidEffect = pygame.mixer.Sound('kidLaughing.wav')
#bossEffect = pygame.mixer.Sound('MaleGrunt.mp3')
#cellEffect = pygame.mixer.Sound('pheoneRinging.mp3')
start_time = time.time()

sound_library = {}
def play_sound(path):
  global _sound_library
  sound = _sound_library.get(path)
  if sound == None:
    canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
    sound = pygame.mixer.Sound(canonicalized_path)
    _sound_library[path] = sound
  sound.play()

def loadImage(name):
    image = pygame.image.load("assets/"+name).convert_alpha()
    return image

def collision(x1, y1, x2, y2,cSize):
    if(x1 >= x2 -cSize and (x1 <= x2+cSize)):
        if(y1 >= y2 -cSize and (y1-cSize<= y2+cSize)):
            return True
    return False

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = [loadImage("8bitBeach{}.png".format(i + 1)) for i in range(12)]
        self.frame = 0
        self.timeFrame = dayLength
        self.setTime = time.time()
        self.rect = self.image[self.frame].get_rect()
        self.rect.left, self.rect.top = location

    def reset(self):
        self.frame = 0
        self.timeFrame = dayLength
        self.setTime = time.time()

    def update(self):
        if time.time() >= self.setTime + self.timeFrame:
            if self.frame >= 11:
                self.reset()
            else:
                self.frame += 1
                self.setTime = time.time()

    def draw(self):
        screen.blit(self.image[self.frame], self.rect);

class FireBall():
    def __init__(self):
        self.speed = gravity * 1.3
        self.hori = 0
        self.image = pygame.image.load("assets/fireball.png").convert_alpha();
        self.rect = self.image.get_rect()
        self.rect.x = TopSunX
        self.rect.y = -400
        self.rect.width = 230
        self.rect.height = -180
        self.falling = False

    def update(self):
        if(self.falling):
            self.rect.y += self.speed
        self.stop()

    def fall(self):
        self.falling = True

    def stop(self):
        if(self.falling):
            if(self.rect.y > screen_height):
                self.rect.y = -400
                self.falling = False


    def reset(self):
        self.Falling = False
        self.rect.x = TopSunX
        self.rect.y = -400

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, False, True), self.rect)


class healthPack():
    def __init__(self):
        self.poopSpeed = gravity * 1.5
        self.hori = 0
        self.image = pygame.image.load("assets/hearts.png").convert_alpha();
        self.rect = self.image.get_rect()
        self.rect.x = -100
        self.rect.y = -100
        self.rect.width = 10
        self.rect.height = 10
        self.pooping = False

    def update(self):
        if(self.pooping):
            self.rect.y += self.poopSpeed
            self.stop()

    def poop(self, x, y):
        self.rect.x = x
        self.rect.y = y
        self.pooping = True

    def stop(self):
        if(self.pooping):
            if(self.rect.y >= screen_height - 30 or self.rect.y <= -30 ):
                self.pooping = False

    def reset(self):
        self.pooping = False
        self.rect.x = -30
        self.rect.y = -30

    def draw(self):
        screen.blit(self.image,self.rect);

class Projectile():
    def __init__(self):
        self.speed = bullet_speed;
        self.poopSpeed = gravity * 1.5
        self.hori = 0
        self.dir = 1
        self.image = pygame.image.load("assets/fire.png").convert_alpha();
        self.poopImg = pygame.image.load("assets/poop.png").convert_alpha();
        self.rect = self.image.get_rect()
        self.rect.x = -100
        self.rect.y = -100
        self.rect.width = 10
        self.rect.height = 10
        self.firing = False
        self.pooping = False

    def update(self):
        if(self.firing):
            self.rect.x += self.speed * self.dir
            self.removeBullet()
        if(self.pooping):
            self.rect.y += self.poopSpeed * self.dir
            self.removeBullet()

    def shoot(self, x, y,dir):
        self.rect.x = x
        self.dir = dir
        self.rect.y = y
        self.firing = True

    def fireSize(self):
        self.rect.width = 40
        self.rect.height = 40

    def poop(self, x, y,dir):
        self.rect.x = x
        self.dir = dir
        self.rect.y = y
        self.pooping = True

    def removeBullet(self):
        if(self.firing):
            if(self.rect.x >= screen_width + 100 or self.rect.x <= -30 ):
                self.firing = False
                self.rect.x = -30
        if(self.pooping):
            if(self.rect.y >= screen_height + 100 or self.rect.y <= -30 ):
                self.pooping = False
                self.rect.y = -30

    def reset(self):
        self.pooping = False
        self.firing = False
        self.rect.x = -30
        self.rect.y = -30

    def draw(self):
        screen.blit(self.image,self.rect);
    def drawPoop(self):
        screen.blit(self.poopImg,self.rect);

class Player():

    def __init__(self):
        self.step = movement_speed;
        self.jumpSpeed = jumpStrength
        self.veri = 0
        self.hori = 0
        self.maxHealth = 5
        #self.image = pygame.image.load("spriteGirl.gif").convert_alpha();
        self.image = [loadImage("LaurenWalkRight_{}.png".format(i)) for i in range(16)]
        self.shoot = [loadImage("LaurenShootright_{}.png".format(i)) for i in range(8)]
        self.hearts = [loadImage("hearts.png") for i in range(self.maxHealth)]
        self.heartsRect = self.hearts[0].get_rect()
        self.heartsRect.x = 10
        self.heartsRect.y = 10
        self.imgFrame = 0
        self.shootFrame = 0
        self.rect = self.image[self.imgFrame].get_rect()
        self.rect.x = screen_width / 2
        self.rect.y = ground
        self.rect.width = 52
        self.jumping = False
        self.facing = "Right"
        self.dead = False
        self.dmg = 0
        self.health = 5
        self.firing = False

    def update(self):
        if(not(self.dead)):
            self.rect.x += self.hori
            if(self.jumping):
                self.rect.y -= self.veri
            if(self.imgFrame > 14):
                self.imgFrame = 0
            if(self.shootFrame > 6):
                self.firing = False
                self.shootFrame = 0
            else:
                self.shootFrame += 1
            self.hori = 0
            self.gravity()
            self.loseHealth()


    def loseHealth(self):
        if(self.dmg >= 12):
            self.health -= 1
            self.dmg = 0
        if(self.health <= 0):
            self.dead = True

    def reset(self):
        self.health = 5
        self.dmg = 0
        self.imgFrame = 0
        self.shootFrame = 0
        self.hori = 0
        self.veri = 0
        self.dead = False
        self.rect.x = screen_width / 2
        self.rect.y = ground

    def move_Right(self):
        if(not(self.dead)):
            if(self.rect.x <= screen_width -40):
                self.hori += self.step;
            if(self.imgFrame > 14):
                self.imgFrame = 0
            self.imgFrame +=1

    def move_Left(self):
        if(not(self.dead)):
            if(self.rect.x >= 0):
                self.hori -= self.step;
            if(self.imgFrame > 14):
                self.imgFrame = 0
            self.imgFrame +=1

    def jump(self):
        if(not(self.dead)):
            if(not(self.jumping)):
                self.veri += self.jumpSpeed
                self.jumping = True

    def gravity(self):
        if(self.jumping and self.rect.y <= max_jump_height):
            self.veri = -gravity
        if(self.jumping and self.rect.y == ground):
            self.veri = 0
            self.jumping = False

    def draw(self):
        if(self.firing):
            if(self.facing == "Right"):
                screen.blit(self.shoot[self.shootFrame], self.rect)
            elif(self.facing == "Left"):
                screen.blit(pygame.transform.flip(self.shoot[self.shootFrame], True, False), self.rect)
        else:
            if(self.facing == "Right"):
                screen.blit(self.image[self.imgFrame], self.rect)
            elif(self.facing == "Left"):
                screen.blit(pygame.transform.flip(self.image[self.imgFrame], True, False), self.rect)
        for i in range((self.health)):
            screen.blit(self.hearts[i],(self.heartsRect.x * (i *2),self.heartsRect.y))


class Raymond:
    def __init__(self):
        self.step = movement_speed -6
        self.image = [loadImage("Blackwolfrun{}.png".format(i+1)) for i in range(6)]
        self.imgFrame = 0
        self.rect = self.image[self.imgFrame].get_rect()
        self.rect.x = -300
        self.rect.y = ground + 85
        self.rect.width = 25
        self.rect.height = 40
        self.facing = "Left"

    def update(self):
        self.flipChance = randint(-1,2)
        if(self.facing == "Left"):
            self.rect.x -= self.step
        elif(self.facing == "Right"):
            self.rect.x += self.step
        if(self.imgFrame > 4):
            self.imgFrame = 0
        self.imgFrame += 1
        self.resetPos()

    def reset(self):
        self.imgFrame = 0
        self.rect.x = -300

    def resetPos(self):
        if(self.facing == "Left"):
            if(self.rect.x < -200):
                self.rect.x = screen_width + 1000
        elif(self.facing == "Right"):
            if(self.rect.x > screen_width + 200):
                self.rect.x = -1010

    def draw(self):
        if(self.facing == "Left"):
            screen.blit(self.image[self.imgFrame], self.rect)
        elif(self.facing == "Right"):
            screen.blit(pygame.transform.flip(self.image[self.imgFrame], True, False), self.rect)



class Bird:
    def __init__(self):
        self.step = movement_speed - 11;
        self.image = [loadImage("seagull{}.png".format(i)) for i in range(16)]
        self.imgFrame = 0
        self.rect = self.image[self.imgFrame].get_rect()
        self.rect.x = randint(1,1000) * -1
        self.flipChance = 0
        self.rect.y =  max_jump_height + 40
        self.rect.width = 9
        self.rect.height = 10
        self.facing = "Left"
        self.poopRNG = randint(1,2000)
        self.poopTime = False


    def update(self):
        self.flipChance = randint(-1,2)
        if(self.facing == "Left"):
            self.rect.x -= self.step
        elif(self.facing == "Right"):
            self.rect.x += self.step
        if(self.imgFrame > 14):
            self.imgFrame = 0
        self.imgFrame += 1
        self.poopSetup()
        self.resetPos()

    def poopSetup(self):
        self.poopRNG = randint(1,2000)
        if(self.poopRNG >= 1995):
            self.poopTime = True

    def reset(self):
        self.imgFrame = 0
        self.rect.x = randint(1,1000) * -1

    def resetPos(self):
        if(self.facing == "Left"):
            if(self.rect.x < -200):
                if(self.flipChance):
                    self.facing = "Right"
                else:
                    self.rect.x = screen_width + 1000
        elif(self.facing == "Right"):
            if(self.rect.x > screen_width + 200):
                if(self.flipChance):
                    self.facing = "Left"
                else:
                    self.rect.x = screen_width + 1000
    def draw(self):
        if(self.facing == "Right"):
            screen.blit(self.image[self.imgFrame], self.rect)
        elif(self.facing == "Left"):
            screen.blit(pygame.transform.flip(self.image[self.imgFrame], True, False), self.rect)

class Child:
    def __init__(self):
        self.step = movement_speed-5;
        self.image = [loadImage("KidRunRight_{}.png".format(i)) for i in range(8)]
        self.imgFrame = 0
        self.rect = self.image[self.imgFrame].get_rect()
        self.rect.x = randint(1000,3000) * -1
        self.flipChance = 0
        self.rect.y =  ground
        self.rect.width = 50
        self.rect.height = 200
        self.facing = "Right"
        self.awake = True


    def update(self):
        self.flipChance = randint(-1,2)
        if(self.awake):
            if(self.facing == "Left"):
                self.rect.x -= self.step
            elif(self.facing == "Right"):
                self.rect.x += self.step
            if(self.imgFrame > 6):
                self.imgFrame = 0
            self.imgFrame += 1
        else:
            self.reset()
        #if(self.inBounds()):
            #kidEffect.play()
        self.resetPos()

    def reset(self):
        self.imgFrame = 0
        if(self.facing == "Left"):
            if(self.flipChance):
                self.facing = "Right"
                self.rect.x = -2910
            else:
                self.rect.x = screen_width + 2999
        elif(self.facing == "Right"):
            if(self.flipChance):
                self.facing = "Left"
                self.rect.x = screen_width + 2999
            else:
                self.rect.x = -2910

    def resetPos(self):
        if(self.facing == "Left"):
            if(self.rect.x < -3000):
                if(self.flipChance):
                    self.facing = "Right"
                else:
                    self.rect.x = screen_width + 2999
        elif(self.facing == "Right"):
            if(self.rect.x > screen_width + 3000):
                if(self.flipChance):
                    self.facing = "Left"
                else:
                    self.rect.x =  -2999

    def inBounds(self):
        if(self.rect.x < screen_width and self.rect.x > 10):
            return True

    def draw(self):
        if(self.facing == "Right"):
            screen.blit(self.image[self.imgFrame], self.rect)
        elif(self.facing == "Left"):
            screen.blit(pygame.transform.flip(self.image[self.imgFrame], True, False), self.rect)

class CellPhone:
    def __init__(self):
        self.multi = 1
        self.step = (movement_speed - 12) * self.multi
        self.image = loadImage("cellPhone.png")
        self.rect = self.image.get_rect()
        self.rect.width = 30
        self.rect.height = 70
        self.rect.x = -300
        self.rect.y = ground + 60
        self.flipChance = randint(-1,2)
        self.facing = "Left"
        self.calling = True

    def update(self):
        if(self.calling):
            self.flipChance = randint(-1,2)
            if(self.facing == "Left"):
                self.rect.x -= self.step
            elif(self.facing == "Right"):
                self.rect.x += self.step
        else:
            self.reset()
        #if(self.inBounds()):
            #cellEffect.play()
        self.resetPos()

    def reset(self):
        if(self.facing == "Left"):
            if(self.flipChance):
                self.facing = "Right"
                self.rect.x = -1010
            else:
                self.rect.x = screen_width + 1000
        elif(self.facing == "Right"):
            if(self.flipChance):
                self.facing = "Left"
                self.rect.x = screen_width + 1000
            else:
                self.rect.x = -1010

    def resetPos(self):
        if(self.facing == "Left"):
            if(self.rect.x < -200):
                if(self.flipChance):
                    self.facing = "Right"
                else:
                    self.rect.x = screen_width + 1000
        elif(self.facing == "Right"):
            if(self.rect.x > screen_width + 200):
                if(self.flipChance):
                    self.facing = "Left"
                else:
                    self.rect.x = -1010
    def inBounds(self):
        if(self.rect.x < screen_width and self.rect.x > 10):
            return True
    def draw(self):
        if(self.facing == "Left"):
            screen.blit(pygame.transform.flip(self.image, False, False), self.rect)
        elif(self.facing == "Right"):
            screen.blit(pygame.transform.flip(self.image, True, False), self.rect)

class Boss:
    def __init__(self):
        self.step = movement_speed-13;
        self.image = [loadImage("DadWalkRight{}.png".format(i)) for i in range(16)]
        self.imgFrame = 0
        self.rect = self.image[self.imgFrame].get_rect()
        self.rect.x = -300
        self.flipChance = 0
        self.rect.y = ground - 300
        self.health = 70
        #self.rect.width = 50
        #self.rect.height = 200
        self.facing = "Right"
        self.awake = False


    def update(self):
        self.flipChance = randint(-1,2)
        if(self.awake):
            if(self.facing == "Left"):
                self.rect.x -= self.step
            elif(self.facing == "Right"):
                self.rect.x += self.step
            if(self.imgFrame > 6):
                self.imgFrame = 0
            self.imgFrame += 1
        else:
            self.reset()
        if(self.health <= 0):
            self.reset()
        self.resetPos()

    def reset(self):
        self.imgFrame = 0
        self.awake = False
        self.health = 70
        if(self.facing == "Left"):
            if(self.flipChance):
                self.facing = "Right"
                self.rect.x = screen_width + 400
            else:
                self.rect.x = -400
        elif(self.facing == "Right"):
            if(self.flipChance):
                self.facing = "Left"
                self.rect.x = -400
            else:
                self.rect.x = screen_width + 400

    def resetPos(self):
        if(self.facing == "Left"):
            if(self.rect.x < -300):
                if(self.flipChance):
                    self.facing = "Right"
                else:
                    self.rect.x = screen_width +300
        elif(self.facing == "Right"):
            if(self.rect.x > screen_width):
                if(self.flipChance):
                    self.facing = "Left"
                else:
                    self.rect.x =  -300

    def inBounds(self):
        if(self.rect.x < screen_width and self.rect.x > 10):
            return True

    def draw(self):
        if(self.facing == "Right"):
            screen.blit(self.image[self.imgFrame], self.rect)
        elif(self.facing == "Left"):
            screen.blit(pygame.transform.flip(self.image[self.imgFrame], True, False), self.rect)


class Score:
    myfont = None;
    text = None;
    def __init__(self,):
        pygame.font.init();
        self.num = start_score
        self.day = 0
        self.myfont = pygame.font.SysFont('Comic Sans MS', 30);
        self.text = self.myfont.render("Score: ", False,(0,0,0));
        self.text2 = self.myfont.render("Day: ", False,(0,0,0));

    def update(self):
        self.text = self.myfont.render("Score: {}".format(self.num), False,(0,0,0));
        self.text2 = self.myfont.render("Day: {}".format(self.day+1), False,(0,0,0));

    def draw(self):
        screen.blit(self.text,(screen_width - 200,10));
        screen.blit(self.text2,(screen_width/2.5,10));

class Death:
    myfont = None;
    text = None;
    def __init__(self,):
        pygame.font.init();
        self.num = 1000
        self.myfont = pygame.font.SysFont('Comic Sans MS', 50)
        self.lessonfont = pygame.font.SysFont('Comic Sans MS', 25)
        self.text2 = self.myfont.render("YOU DIED!", False,(0,0,0))
        self.lessonLearned = 0
        self.lesson = ["" for i in range(7)]
        self.overlay_bg = pygame.Surface(win_size)
        self.overlay_bg.fill(0)
        self.overlay_bg.set_alpha(130)

    def lessons(self):
        self.lesson[0] = "Lesson 1: Ray does not care if you hit him with projeciles. He will just keep coming at you."
        self.lesson[1] = "Lesson 2: Birds poop here constantly, but when life gets too crappy, we clean it up. Doing so may rejuvenate you"
        self.lesson[2] = "Lesson 3: Children can't be avoided. You have to beat them"
        self.lesson[3] = "Lesson 4: Nothing's gonna hit you harder than life."
        self.lesson[4] = "Lesson 5: I don't even know what that was, lets just not talk about it."
        self.lesson[5] = "Lesson 6: Find a way to stay out of the heat"
        self.lesson[6] = "Lesson 7: Honestly, just runaway from your problems"

    def setLesson(self):
        self.lessons()
        self.text = self.lessonfont.render(self.lesson[self.lessonLearned], False,(255,255,255))


    def draw(self):
        self.setLesson()
        screen.blit(self.overlay_bg,(0,0))
        screen.blit(self.text2,((screen_width /2) - 130,screen_height/2))
        screen.blit(self.text,((screen_width /2) - 400,screen_height - 300))


class Paused:
    myfont = None;
    text = None;
    def __init__(self,):
        pygame.font.init();
        self.num = 1000
        self.myfont = pygame.font.SysFont('Comic Sans MS', 50)
        self.text2 = self.myfont.render("PAUSED", False,(0,0,0))
        self.overlay_bg = pygame.Surface(win_size)
        self.overlay_bg.fill(0)
        self.overlay_bg.set_alpha(130)

    def draw(self):
        screen.blit(self.overlay_bg,(0,0))
        screen.blit(self.text2,((screen_width /2) - 130,screen_height/2))

class Start:
    myfont = None;
    text = None;
    def __init__(self,):
        pygame.font.init();
        self.num = 1000
        self.myfont = pygame.font.SysFont('Comic Sans MS', 50)
        self.timer = time.time()
        self.text2 = self.myfont.render("TUGLAND HERO", False,(0,0,0))
        self.myfont = pygame.font.SysFont('Comic Sans MS', 20)
        self.text = self.myfont.render("press 'SPACE' to start", False,(255,255,255))

    def draw(self):
        screen.blit(self.text2,((screen_width /2) - 130,screen_height/2))
        screen.blit(self.text,((screen_width /2) - 70,screen_height/2 + 150))


class Game:
    player = 0;
    ammo = 5
    maxFlock = 10
    def __init__(self):
        self.state = 0
        self.flock = 1
        self.birdIncTime = 10
        self.start_time = time.time()
        self.last_time = time.time()
        self.startOfDay = time.time()
        self.dayLength = 120
        self.BackGround = Background('beach.gif', [0,0])
        self.fireball = FireBall()
        self.start = Start()
        self.player = Player()
        self.child = Child()
        self.boss = Boss()
        self.projectiles = [Projectile() for i in range(self.ammo)]
        self.poop =  [Projectile() for i in range(self.maxFlock)]
        self.packs =  [healthPack() for i in range(self.maxFlock)]
        self.poopLoc = [100 for i in range(self.maxFlock)]
        self.ray = Raymond()
        self.ray2 = Raymond()
        self.cellP = CellPhone()
        self.death = Death()
        self.paused = Paused()
        self.seagull =  [Bird() for i in range(self.maxFlock)]
        self.score = Score()
        self.bullet = 0
        self.playerDir = 1
        self.multiplierGiven = False
        self.day = 0
        #self.logic = GameLogic();
        self.running = True;
        self.waiting = False;
        for i in range(self.ammo):
            self.projectiles[i].fireSize()

    def on_init(self):
        pygame.init();
        self.running = True;

    def quitEvent(self, event):
        if(event.type == QUIT):
            self.running = False;


    def render(self):
        screen.fill((255,255,255));
        self.BackGround.draw()
        if(self.state == 0):
            self.BackGround.timeFrame = 1
            self.start.draw()
            for i  in range(self.maxFlock):
                self.seagull[i].draw()
        if(self.state == 1):
            self.score.draw()
            self.player.draw();
            self.fireball.draw()
            self.child.draw()
            self.boss.draw()
            for i  in range(self.ammo):
                self.projectiles[i].draw()
            for i  in range(self.maxFlock):
                self.poop[i].drawPoop()
            for i  in range(self.maxFlock):
                self.packs[i].draw()
            self.ray.draw()
            self.ray2.draw()
            self.ray2.facing = "Right"
            for i  in range(self.flock):
                self.seagull[i].draw()
            self.cellP.draw()
        if(self.state == 2):
            self.death.draw()
        if(self.state == 3):
            self.paused.draw()
        pygame.display.flip()

    def loop(self):
        if(self.state ==0 ):
            self.BackGround.update()
            for i  in range(self.maxFlock):
                self.seagull[i].update()
        if(self.state ==1):
            self.BackGround.update()
            self.player.update();
            self.projectiles[self.bullet].update();
            for i  in range(self.maxFlock):
                self.poop[i].update()
            for i  in range(self.maxFlock):
                self.packs[i].update()
            self.ray.update()
            self.ray2.update()
            for i  in range(self.flock):
                self.seagull[i].update()
            self.cellP.update()
            self.score.update()
            self.score.day = self.day
            self.fireball.update()
            self.child.update()
            self.boss.update()

            if(time.time() >= self.startOfDay + self.dayLength) and self.BackGround.frame == 0:
                self.day += 1
                self.dayChanges()
                self.startOfDay = time.time()
            #update day
            if(self.BackGround.frame == 0):
                self.multiplierGiven = False

            #drop the fireball at peak sun height
            if(self.BackGround.frame == 4):
                self.fireball.fall()

            #work stops calling at night
            if(self.BackGround.frame >= 9):
                self.cellP.calling = False
                if(self.flock == self.maxFlock):
                    self.flock = 3
            else:
                self.cellP.calling = True

            if( self.BackGround.frame >= 9 or self.BackGround.frame < 2 ):
                self.child.awake = False
            else:
                self.child.awake = True

            #ray 1 collision
            if(self.ray.rect.colliderect(self.player.rect)):
                self.score.num -= 2
                self.player.dmg += 4
                self.death.lessonLearned = 0

            #ray 2 collision
            if(self.ray2.rect.colliderect(self.player.rect)):
                self.score.num -= 2
                self.player.dmg += 4
                self.death.lessonLearned = 0

            #bird collision
            for i  in range(self.flock):
                if(self.seagull[i].rect.colliderect(self.player.rect)):
                    self.score.num -= 5
                    self.player.dmg += 4
                    self.death.lessonLearned = 1

            #Fireball collision
            if(self.fireball.rect.colliderect(self.player.rect)):
                self.score.num -= 1000
                self.player.health -=3
                self.fireball.reset()
                self.death.lessonLearned = 5

            #projectile hits cellphone
            for i  in range(self.ammo):
                if(self.projectiles[i].rect.colliderect(self.cellP.rect) and self.cellP.inBounds()):
                    self.cellP.reset()
                    self.score.num += 250

            #projectile hits cellphone
            for i  in range(self.ammo):
                if(self.projectiles[i].rect.colliderect(self.child.rect) and self.child.inBounds()):
                    self.child.reset()
                    self.score.num += 200

            #projectile hits boss
            for i  in range(self.ammo):
                if(self.projectiles[i].rect.colliderect(self.boss.rect) and self.boss.inBounds()):
                    self.boss.health -= 1
                    self.score.num += 100

            #CellPhone collision
            if(self.cellP.rect.colliderect(self.player.rect)):
                self.score.num -= 1000
                self.player.health -=4
                self.cellP.reset()
                self.death.lessonLearned = 3

            #Child collision
            if(self.child.rect.colliderect(self.player.rect)):
                self.score.num -= 1000
                self.player.health -=3
                self.child.reset()
                self.death.lessonLearned = 2

            #boss collision
            if(self.boss.rect.colliderect(self.player.rect)):
                self.score.num -= 10000
                self.player.health -=5
                self.boss.reset()
                self.death.lessonLearned = 6


            if(self.score.num < 0):
                self.score.num = 0
            if(self.player.dead):
                self.state = 2

            for i  in range(self.maxFlock):
                if(self.poop[i].rect.colliderect(self.player.rect)):
                    self.score.num -= 1
                    self.player.dmg += 10
                    self.poop[i].reset()
                    self.death.lessonLearned = 1

            for i  in range(self.maxFlock):
                if(self.packs[i].rect.colliderect(self.player.rect)):
                    self.score.num += 1
                    if(self.player.health < self.player.maxHealth):
                        self.player.health += 1
                    self.packs[i].reset()

            self.poops()
            self.dogScoreAdd()
            self.incFLock()

            if((self.day + 1) % 2 == 0) and self.BackGround.frame < 4:
                self.flock = 3
                self.cellP.calling = False
                self.child.awake = False
                self.boss.awake = True
            else:
                self.boss.awake = False
            pass

    def dayChanges(self):
        if not(self.multiplierGiven):
            self.score.num = self.score.num * (self.day +1)
            self.cellP.multi *= self.day
            self.multiplierGiven = True
            if(self.flock == self.maxFlock):
                self.flock = 5

    def shoot(self):
        #print(self.waiting)
        if(self.bullet == self.ammo):
            self.bullet = 0

        if(not(self.waiting)):
            self.projectiles[self.bullet].shoot(self.player.rect.x + (50 * self.playerDir), self.player.rect.y + 60,self.playerDir)
            self.waiting = True
            self.player.firing = True
        if(self.waiting):
            if(not(self.projectiles[self.bullet].firing)):
                self.waiting = False

    def poops(self):
        self.poopLoc = [randint(100,(screen_width - 200)) for i in range(self.flock)]
        for i in range(self.flock):
            if(self.seagull[i].poopTime):
                if(self.seagull[i].rect.x > (self.poopLoc[i]-50) and self.seagull[i].rect.x < (self.poopLoc[i]+50)):
                    poop = randint(-1,2)
                    if(not(poop) and self.player.health < 5):
                        self.packs[i].poop(self.seagull[i].rect.x, self.seagull[i].rect.y+20)
                    else:
                        self.poop[i].poop(self.seagull[i].rect.x, self.seagull[i].rect.y+20,1)
                    self.seagull[i].poopTime = False;

    def dogScoreAdd(self):
        if(self.ray2.rect.x <= screen_width +10 and self.ray2.rect.x >= screen_width -10):
            self.score.num += 100
        if(self.ray.rect.x <=  10 and self.ray.rect.x >= 0):
            self.score.num += 100

    def incFLock(self):
        if(time.time() >= self.last_time + self.birdIncTime) and (self.flock < self.maxFlock):
            self.flock += 1
            self.last_time = time.time()

    def restart(self):
        self.player.reset()
        self.ray.reset()
        self.ray2.reset()
        self.child.reset()
        self.fireball.reset()
        self.BackGround.reset()
        self.cellP.reset()
        self.boss.reset()
        for i  in range(self.maxFlock):
            self.seagull[i].reset()
        for i  in range(self.maxFlock):
            self.poop[i].reset()
        for i  in range(self.maxFlock):
            self.packs[i].reset()
        self.flock = 1
        self.score.num = start_score
        self.last_time = time.time()
        self.state = 1

    def endGame(self):
        self.running = False
        pygame.quit();
        sys.exit(0)

    def playGame(self):
        if self.on_init() == False:
            self._running = False;
        while(self.running):
            while(self.state == 0):
                pygame.event.pump()
                keys = pygame.key.get_pressed()
                if(keys[K_ESCAPE]):
                    self.endGame()
                if(keys[K_r] or keys[K_SPACE]):
                    self.restart()
                self.render()
                self.loop()

            while(self.state == 1):
                pygame.event.pump()
                keys = pygame.key.get_pressed()
                if(keys[K_RIGHT] or keys[K_d]):
                    self.player.move_Right();
                    self.playerDir = 1
                    self.player.facing = "Right"
                if(keys[K_LEFT] or keys[K_a]):
                    self.player.move_Left();
                    self.playerDir = -1
                    self.player.facing = "Left"
                if(keys[K_w] or keys[K_UP]):
                    self.player.jump();
                if(keys[K_SPACE]):
                    self.shoot();
                if(keys[K_p]):
                    self.state = 3
                    time.sleep (1.0 / 10.0)
                if(keys[K_ESCAPE]):
                    self.endGame()
                self.render()
                self.loop()
                time.sleep (1.0 / 10000000000000.0)
            while(self.state == 2):
                pygame.event.pump()
                keys = pygame.key.get_pressed()
                if(keys[K_ESCAPE]):
                    self.endGame()
                if(keys[K_r]):
                    self.restart()
                self.render()
            while(self.state == 3):
                pygame.event.pump()
                keys = pygame.key.get_pressed()
                if(keys[K_SPACE]):
                    self.BackGround.setTime = time.time()
                    self.last_time = time.time()
                    self.state = 1
                if(keys[K_r]):
                    self.last_time = time.time()
                    self.restart()
                if(keys[K_ESCAPE]):
                    self.endGame()
                self.render()

        self.endGame();

if __name__ == "__main__" :
    theGame = Game();
    theGame.playGame();
# snake
