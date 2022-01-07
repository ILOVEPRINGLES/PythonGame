import pygame
import random
import os

# build the frame and display setting
pygame.init()
pygame.mixer.init()
WIDTH = 700
HEIGHT = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Billy the Cringe Killer')
clock = pygame.time.Clock()
game_on = True
init_display = True
FPS = 100
BLOOD = (102, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255,255,255)
GREY = (96,96,96)
font_name = pygame.font.match_font('Felix Titling')

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_itself = font.render(text, True, WHITE) # text appearance, such as content, font, size, color
    text_rect = text_itself.get_rect()  # text location
    text_rect.x = x
    text_rect.y = y
    surf.blit(text_itself, text_rect)

def draw_health(surf, cons, x, y):    #cons stands for conscience
    bar_length = 200
    bar_height = 20
    blood = (cons/100)*bar_length
    outline_frame = pygame.Rect(x,y,bar_length,bar_height)
    fill_rect = pygame.Rect(x,y,blood,bar_height)
    pygame.draw.rect(surf, WHITE, outline_frame,2)
    pygame.draw.rect(surf,WHITE, fill_rect)

def draw_lives(surf, count, img, x, y):
    for i in range(count):
        img_rect = img.get_rect()  # 这个意思是把图的框架先框出来 但还不知道他的location
        img_rect.x = x + 30*i
        img_rect.y = y
        surf.blit(img, img_rect)

def draw_init():
     screen.fill(BLOOD)
     draw_text(screen,'Cringe Killer', 26, WIDTH/3,HEIGHT/4)
     draw_text(screen, "We don't like cringes, ban those corny ass pieces and collect what's valuable.", 14, WIDTH/8 - 40, HEIGHT/3)
     draw_text(screen, 'Use arrow keys or "WSAD" to control the player, press SPACE to shoot', 14, WIDTH / 7, HEIGHT / 3 + 50)
     draw_text(screen, 'Press anywhere to start', 20, WIDTH / 3, 3*HEIGHT / 4)
     pygame.display.update()
     waiting = True   #waiting的作用是等user input来按任意键开始 与main中的init-display无关 init_display在完成draw这个指令后自动变false 不需要别的介入
     while waiting:
       clock.tick(FPS)
       for event in pygame.event.get():
          if event.type == pygame.QUIT:
            pygame.quit()
            return True    # True and False refer to "close"
          elif event.type == pygame.KEYUP:
            waiting = False #waiting变false 则不需要等user input draw_init也走完 回到main'中 init_display也变false 然后接着往下走
            return False

# pics
player_img = pygame.image.load(os.path.join("photos","player.png")).convert()
# to get multiple cringe pieces, use an array to list all of them, then use random function to randomly select the incoming one
cringe_imgs = []
cringe_imgs.append(pygame.image.load(os.path.join("photos","stussy.jpg")).convert())
cringe_imgs.append(pygame.image.load(os.path.join("photos", "tie.png")).convert())
cringe_imgs.append(pygame.image.load(os.path.join("photos", "dior.png")).convert())
cringe_imgs.append(pygame.image.load(os.path.join("photos", "2.png")).convert())
cringe_imgs.append(pygame.image.load(os.path.join("photos", "prada.png")).convert())
cringe_imgs.append(pygame.image.load(os.path.join("photos", "ring.png")).convert())
cringe_imgs.append(pygame.image.load(os.path.join("photos", "cos.png")).convert())
cringe_imgs.append(pygame.image.load(os.path.join("photos", "tabi.png")).convert())
cringe_imgs.append(pygame.image.load(os.path.join("photos", "vete.png")).convert())
ban_img = pygame.image.load(os.path.join("photos","ban.png")).convert()

#icon img
icon_img = pygame.image.load(os.path.join("photos", "icon.png")).convert()
pygame.display.set_icon(icon_img)

#grails img
grail_imgs = []
for i in range(13):
    grail_imgs.append(pygame.image.load(os.path.join("photos", f"grail{i}.png")).convert())

explo_anim = {}    # a list containing explo_anim['lg'], explo_anm['sm'], and explo_anim['player']
explo_anim['lg'] = [] # '' indicates the array's size
explo_anim['sm'] = []
explo_anim['player'] = []
for i in range(5):
    explo_img = pygame.image.load(os.path.join("photos",f"explo{i}.png")).convert()
    explo_anim['lg'].append(pygame.transform.scale(explo_img,(50,50)))
    explo_anim['sm'].append(pygame.transform.scale(explo_img,(25,25)))
    explo_player_img = pygame.image.load(os.path.join("photos", "explo1.png")).convert()
    explo_anim['player'].append(pygame.transform.scale(explo_player_img, (70, 70)))
life_img = pygame.transform.scale(player_img,(20,20))


# sound
attack_sound = pygame.mixer.Sound(os.path.join("soundeffect","shoot.wav"))
boom_sound = pygame.mixer.Sound(os.path.join("soundeffect","boom.ogg"))
suc_sound = pygame.mixer.Sound(os.path.join("soundeffect","attack.ogg"))
pygame.mixer.Sound.set_volume(boom_sound,0.4)
pygame.mixer.Sound.set_volume(attack_sound,0.3)
pygame.mixer.music.load(os.path.join("soundeffect","background1.ogg"))
pygame.mixer.music.set_volume(1.5)
# player sprite
class Player(pygame.sprite.Sprite):
    # define the appearance of the player sprite
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img,(50,60))  # player's figure
        self.rect = self.image.get_rect() # player's location
        self.rect.center = (WIDTH/2,HEIGHT-20)
        self.speed = 3
        self.health = 100
        self.lives = 3
        self.hidden = False
        self.hidden_time = 0

    # define the control of the player sprite
    def update(self):
        if self.hidden and pygame.time.get_ticks() - self.hidden_time > 2000:
            self.hidden = False
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT] or key_pressed[pygame.K_d]:
            self.rect.x += self.speed
        if key_pressed[pygame.K_LEFT] or key_pressed[pygame.K_a]:
            self.rect.x -= self.speed
        if key_pressed[pygame.K_DOWN] or key_pressed[pygame.K_s]:
            self.rect.y += self.speed
        if key_pressed[pygame.K_UP] or key_pressed[pygame.K_w]:
            self.rect.y -= self.speed
        if self.rect.right > WIDTH:
            self.rect.x = 650
        if self.rect.left < 0:
            self.rect.x = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0
    # define this in player class because we don't want ban showing all the time,
    # but only when space is pressed so we need to use event option
    def shoot(self):
           ban = Ban()
           all_sprite.add(ban)
           bans.add(ban)
           attack_sound.play()

    def hide(self):
        self.hidden = True
        self.hidden_time = pygame.time.get_ticks()
        self.rect.right = 900
        self.rect.bottom = 1000


# Cringe sprite
class Cringe(pygame.sprite.Sprite):
    # define the appearance of the cringe sprite
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_old = random.choice(cringe_imgs)
        self.image_og = pygame.transform.scale(self.image_old,(110,90)) # player's figure
        self.image_og.set_colorkey(WHITE)
        self.image = self.image_og.copy()
        self.rect = self.image.get_rect()  # player's location
        self.rect.x = random.randrange(0,WIDTH)
        self.rect.y = random.randrange(-100,-10)
        self.speed = random.randrange(1,3)
        self.speedx = random.randrange(-1,1)
        self.total_angle = 0
        self.rot_angle = random.randrange(-2,2)
    # define the rotating effect
    def rotate(self):
        self.total_angle += self.rot_angle
        self.total_angle = self.total_angle % 360   # % 余数即为除以360还剩多少个 这样结果永远不会超过360反而从头开始 如ele792 lab1
        self.image = pygame.transform.rotate(self.image_og, self.total_angle)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center
    # define the movement of cringe sprite
    def update(self):
        self.rotate()
        self.rect.y += self.speed
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT or self.rect.right < 0 or self.rect.left > WIDTH:
           self.rect.x = random.randrange(0, WIDTH)
           self.rect.y = random.randrange(-100, -10)

class Grail(pygame.sprite.Sprite):
    # define the appearance of the cringe sprite
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_old = random.choice(grail_imgs)
        self.image_og = pygame.transform.scale(self.image_old,(110,100)) # player's figure
        self.image_og.set_colorkey(WHITE)
        self.image = self.image_og.copy()
        self.rect = self.image.get_rect()  # player's location
        self.rect.x = random.randrange(0,WIDTH)
        self.rect.y = random.randrange(-100,-10)
        self.speed = 1
        self.total_angle = 0
        self.rot_angle = random.randrange(-2,2)
    # define the movement of cringe sprite
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
           self.rect.x = random.randrange(0, WIDTH)
           self.rect.y = random.randrange(-100, -10)

# justice sprite
class Ban(pygame.sprite.Sprite):
    # define the appearance of the cringe sprite
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(ban_img,(30,20))# player's figure
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()  # player's location
        self.rect.x = player.rect.centerx
        self.rect.y = player.rect.top
        self.speed = -5

    # define the movement of grail sprite
    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self,center,size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explo_anim[self.size][0]
        self.rect = self.image.get_rect()  # player's location
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 1000

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame:
            now = self.last_update
            self.frame += 1
            if self.frame == len(explo_anim[self.size]):
                self.kill()
            else:
               self.image = explo_anim[self.size][self.frame]
               center = self.rect.center
               self.rect = self.image.get_rect()
               self.rect.center = center


all_sprite = pygame.sprite.Group()
player = Player()
all_sprite.add(player)
cringes = pygame.sprite.Group()
bans = pygame.sprite.Group()
grails = pygame.sprite.Group()
for i in range(9):    # i与cringe本身无关系 只做计数用
    cringe = Cringe()       #每一次的i 都有一个cringe被加进去
    all_sprite.add(cringe)
    cringes.add(cringe)
score = 0
pygame.mixer.music.play(-1)

# main game function

while game_on:
    # limit the processing counts to ensure this can be achieved at same performance level on any device
    clock.tick(FPS)
    # Obtain and check for user action
    if init_display:
        close = draw_init()
        if close:
            break
        all_sprite = pygame.sprite.Group()
        player = Player()
        all_sprite.add(player)
        cringes = pygame.sprite.Group()
        bans = pygame.sprite.Group()
        grails = pygame.sprite.Group()
        for i in range(9):
            cringe = Cringe()
            all_sprite.add(cringe)
            cringes.add(cringe)
        score = 0
        pygame.mixer.music.play(-1)
        init_display = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_on = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
               player.shoot()
    # progress
    all_sprite.update()               # Here is groupcollide since cringes and bans are all groups
    hits1 = pygame.sprite.groupcollide(cringes,bans,True,True) # hits is an array, or the number of content of the array
    for hit in hits1:
        score += 1
        cringe = Cringe()
        all_sprite.add(cringe)
        cringes.add(cringe)
        explosion = Explosion(hit.rect.center, 'lg')
        all_sprite.add(explosion)
        if random.random() > 0.94:
            grail = Grail()
            all_sprite.add(grail)
            grails.add(grail)
    hits3 = pygame.sprite.spritecollide(player, grails, True)
    for hit in hits3:
        suc_sound.play()
        player.health = player.health + 10
        if player.health > 100:
            player.health = 100

    if not player.hidden:
      hits2 = pygame.sprite.spritecollide(player,cringes,True) # here using sprite collide because player is just one sprite not a group
      for hit in hits2:
        player.health = player.health - 20
        boom_sound.play()
        cringe = Cringe()
        all_sprite.add(cringe)
        cringes.add(cringe)
        if player.health <= 0:
            explosion = Explosion(player.rect.center, 'player')
            all_sprite.add(explosion)
            player.lives -= 1
            if player.lives > 0:
              player.health = 100
              player.hide()
            else:
              player.kill()
              init_display = True


    # screen display
    screen.fill(BLOOD)
    all_sprite.draw(screen)
    draw_text(screen, 'SCORE:' + str(score), 24, WIDTH/2, 300)
    draw_text(screen, 'WISH NO CRINGES IN HEAVEN', 12, 500, 650)
    draw_text(screen, 'YOUR CONSCIENCE', 12, 20, 8)
    draw_health(screen, player.health, 20, 30)
    draw_lives(screen,player.lives,life_img,200,5)
    pygame.display.update()

pygame.quit()
