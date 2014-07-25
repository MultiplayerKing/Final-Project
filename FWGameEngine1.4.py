"""PyGame Game engine: FutureWizardsGameEngine; FWGameEngine
By Danny Peck and Josh Sutton Spring 2014"""

#Imports pygame and any other required modules
import pygame, sys, time, random
from pygame.locals import *
  
pygame.init()

#Global variables
ScreenW = 800
ScreenH = 500
#creates the screen and displays it at correct size
screen = pygame.display.set_mode((ScreenW, ScreenH), 0, 32)

#Color Transparency values
BLACK = ( 0, 0, 0)  
WHITE = ( 255, 255, 255)  
BLUE = ( 0, 0, 255) 
PLATRANS = ( 77, 83, 140)
BULLTRANS = (181, 165, 213)
FRIENDTRANS = (120, 195, 128)

#Raw SpriteSheet position and demension Data
playerPos = [(254, 98, 33, 40), (218, 101, 26, 37), (177, 101, 33, 37),
            (126, 101, 44, 37), (85, 102, 34, 36), (260, 141, 27, 37),
            (226, 143, 25, 35), (190, 141, 26, 37), (146, 143, 37, 35),
            (109, 141, 28, 37), (74, 143, 25, 35)]
    
playerJmpPos = [(261, 236, 26, 40),(226, 228, 30, 48), (188, 225, 29, 51),
                 (150, 223, 31, 53), (111, 222, 30, 54)]

playerShootPos = [(297, 424, 45, 38), (349, 425, 36, 37), (388, 425, 42, 37),
                  (433, 425, 47, 37), (484, 426, 42, 36), (297, 465, 37, 37),
                  (339, 467, 35, 35), (378, 465, 37, 37), (421, 467, 43, 35),
                  (471, 465, 39, 37), (516, 467, 36, 35)]

playerJumpShoot = [(297, 379, 38, 40), (342, 371, 40, 48), (389, 368, 38, 51),
                   (433, 366, 39, 53), (479, 365, 39, 54)]

enemyPos = [(33, 17, 34, 41), (43, 78, 42, 44), (86, 78, 40, 44),
            (131, 78, 42, 44), (176, 79, 41, 43), (218, 83, 42, 43),
            (263, 82, 41, 44), (314, 81, 40, 45), (360, 82, 47, 44),
            (416, 81, 47, 45), (466, 83, 46, 43)]

crabPos = [(177, 1621, 42, 32), (177, 1621, 42, 32), (225, 1619, 42, 34), (225, 1619, 42, 34), (273, 1621, 42, 32),
           (273, 1621, 42, 32),   (322, 1618, 40, 35), (322, 1618, 40, 35), (370, 1620, 40, 33), (370, 1620, 40, 33)]

friendlyPOS = [(195, 76, 23, 20), (195, 76, 23, 20), (195, 76, 23, 20), (227, 75, 23, 21),
            (227, 75, 23, 21), (227, 75, 23, 21), (259, 76, 23, 20), (259, 76, 23, 20),
            (259, 76, 23, 20)]

bulletPos = [(24, 259, 8, 6)]

healthBar = [(324, 0, 62, 9), (252, 0, 62, 9), (181, 0, 63, 9),
             (88, 0, 62, 9), (0, 0, 63, 9)]

#SpriteSheet Dictionary making platform data callable by name
platformData = {'Grass_Middle': (1228, 319, 112, 120), 'Filler': (1228, 319, 112, 120), 'Floating_Platform': (716, 868, 48, 24),
                'Wall_Right': (1053, 1109, 72, 104), 'Wall_Left': (1317, 1109, 72, 104), 'Flower': (733, 1212, 59, 160),
                'end': (217, 96, 47, 168)}

#Sprite sheet class
class SpriteSheet(object):
    #takes a spritesheet file and transparency color code
    def __init__(self, file_name, trans): 
        self.trans = trans
        #converts the file for pygame
        self.sprite_sheet = pygame.image.load(file_name).convert()
    
    #takes position and size information about a sprite and returns the image
    def get_image(self, x, y, width, height): 
        image = pygame.Surface([width, height]).convert()  
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))  
        image.set_colorkey(self.trans) 
        return image
    
#object sprite class ex. Platforms or enemies 
class Objects(pygame.sprite.Sprite):
    #takes a spritesheet, transparent color, and position and size data
    def __init__(self, sheet, trans, data):
        pygame.sprite.Sprite.__init__(self)
  
        sprite_sheet = SpriteSheet(sheet, trans) 
  
        self.image = sprite_sheet.get_image(data[0], data[1], data[2], data[3]) 
        #returns the image as a sprite
        self.rect = self.image.get_rect()

#Class for bullets
class MovingObjects(pygame.sprite.Sprite):
    #Takes the lists of animation sprites
    def __init__(self, Animations):
        pygame.sprite.Sprite.__init__(self)
        #animation frame
        self.frame = 0
        #sets variables for each direction list
        self.FrameLeft = Animations[0]
        self.FrameRight = Animations[1]
        #sets starting image
        self.image = self.FrameLeft[self.frame]
        self.rect = self.image.get_rect()
        #creates basic properties
        self.ChangeX = 0
        self.ChangeY = 0
        #Movement Bounds for Objects
        self.BoundXL = 0
        self.BoundXR = 0
        #gets direction from the Animations perameter
        self.direction = Animations[2]
        
    def update(self):
        #Same as animation for player
        #updates the objects position by the changing X value
        self.rect.x += self.ChangeX

        #Cycles through correct Frame list according to spriteSheet images direction
        #Example: The image is only facing to the left on the image self.direction L will
        #Create the correct lists
        if self.direction == "L": 
            if self.frame < len(self.FrameLeft) - 1: 
                self.frame += 1
                self.image = self.FrameLeft[self.frame]
            else: 
                self.frame = 1

        elif self.direction == "R": 
            if self.frame < len(self.FrameRight) - 1: 
                self.frame += 1
                self.image = self.FrameRight[self.frame] 
            else: 
                self.frame = 1
                
class HealthBars(pygame.sprite.Sprite):
    #Takes the lists of animation sprites
    def __init__(self, Animations):
        pygame.sprite.Sprite.__init__(self)
        #animation frame
        #sets variables for each direction list
        #sets starting image
        self.barAnimations = Animations[0][0]
        self.image = self.barAnimations[Enemies.Health]
        self.rect = self.image.get_rect()

#The main players sprite class
class Player(pygame.sprite.Sprite):
    def __init__(self): 
        pygame.sprite.Sprite.__init__(self)
        self.gravConstant = 6
        #Sets the players movement change variables
        self.ChangeX = 0
        self.ChangeY = 0
        #Players sprite direction
        self.direction = "R"
        self.frameX = 0
        self.Health = 4
        self.frameY = 0
        self.Alone = False

        playerAnimations = self.Animation('mega.png', BLACK, playerPos, "L")
        
        self.playerFrameLeft = playerAnimations[0]
        self.playerFrameRight = playerAnimations[1]
        
        playerJmpAnimations = self.Animation('mega.png', BLACK, playerJmpPos, "R")

        self.jmpFrameRight = playerJmpAnimations[0]
        self.jmpFrameLeft = playerJmpAnimations[1]

        playerShootAnimations = self.Animation('mega.png', BLACK, playerShootPos, "L")

        self.shootFrameRight = playerShootAnimations[0]
        self.shootFrameLeft = playerShootAnimations[1]

        playerJSAnimations = self.Animation('mega.png', BLACK, playerJumpShoot, "L")

        self.jumpShootRight = playerJSAnimations[0]
        self.jumpShootLeft = playerJSAnimations[1]

        self.image = self.playerFrameRight[0] 
        self.rect = self.image.get_rect()
        
        self.rect.x = 250
        self.rect.y = 300
        
        self.grounded = True
        self.motion = "Still"
        self.picture = "rightList"
        self.shoot = False
        self.status = [self.picture, self.direction, self.grounded, self.motion, self.frameX, self.frameY, self.shoot]

    def Animation(self, sheet, trans, lst, direction):
        FrameRight = []
        FrameLeft = []
        sprite_sheet = SpriteSheet(sheet, trans)
        for data in lst:
            if direction == "L":
                image = sprite_sheet.get_image(data[0], data[1], data[2], data[3])
                FrameLeft.append(image)
                image = pygame.transform.flip(image, True, False)
                FrameRight.append(image)
            else:
                image = sprite_sheet.get_image(data[0], data[1], data[2], data[3])
                FrameRight.append(image)
                image = pygame.transform.flip(image, True, False)
                FrameLeft.append(image)
        return (FrameLeft, FrameRight, direction)
                
    def Gravity(self):
        self.ChangeY += self.gravConstant
            
        if self.rect.y >= ScreenH - self.rect.height and self.ChangeY >= 0: 
            self.ChangeY = 0
            self.rect.y = ScreenH - self.rect.height 
    
    def update(self):
        self.Gravity()
        self.rect.x += self.ChangeX

        self.status[1] = self.direction
        self.status[6] = self.shoot
        
        if self.ChangeX > 0:
            self.status[3] = "Right"
        elif self.ChangeX < 0:
            self.status[3] = "Left"
        elif self.ChangeX == 0:
            self.status[3] = "Still"

        if self.ChangeY != self.gravConstant:
            self.grounded = False
            self.status[2] = self.grounded
        else:
            self.grounded = True
            self.status[2] = self.grounded
            self.status[5] = 0

        #Animation Logic Tree for grounded moving player

        if self.status[3] == "Right" and self.status[2] == True:
            if self.frameX < len(self.playerFrameRight) - 1:
                self.status[4] = self.frameX
                self.frameX += 1
                if self.status[6] == False:
                    self.image = self.playerFrameRight[self.frameX]
                else:
                    self.image = self.shootFrameRight[self.frameX]
                self.status[0] = "rightList"
            else:
                self.frameX = 1

        elif self.status[3] == "Left" and self.status[2] == True:
            if self.frameX < len(self.playerFrameLeft) - 1:
                self.status[4] = self.frameX
                self.frameX += 1
                if self.status[6] == False:
                    self.image = self.playerFrameLeft[self.frameX]
                else:
                    self.image = self.shootFrameLeft[self.frameX]
                self.status[0] = "leftList"
            else:
                self.frameX = 1

        #Animation Logic Tree for grounded still player
                
        elif self.status[3] == "Still" and self.status[2] == True:
            if self.status[1] == "L":
                if self.status[6] == False:
                    self.image = self.playerFrameLeft[0]
                else:
                    self.image = self.shootFrameLeft[0]
            else:
                if self.status[6] == False:
                    self.image = self.playerFrameRight[0]
                else:
                    self.image = self.shootFrameRight[0]

       #Animation Logic Tree for jumping player 
            
        elif self.status[2] == False and self.status[1] == "L":
            if self.frameY < len(self.jmpFrameLeft) - 1:
                self.status[5] = self.frameY
                self.frameY += 1
                if self.status[6] == False:
                    self.image = self.playerFrameLeft[self.frameX]
                else:
                    self.image = self.shootFrameLeft[self.frameX]
            else:
                if self.status[6] == False:
                    self.image = self.jmpFrameLeft[(len(self.jmpFrameLeft)-1)]
                else:
                    self.image = self.jumpShootLeft[(len(self.jmpFrameLeft)-1)]

        elif self.status[2] == False and self.status[1] == "R":
            if self.frameY < len(self.jmpFrameRight) - 1:
                self.status[5] = self.frameY
                self.frameY += 1
                if self.status[6] == False:
                    self.image = self.playerFrameRight[self.frameX]
                else:
                    self.image = self.shootFrameRight[self.frameX]
            else:
                if self.status[6] == False:
                    self.image = self.jmpFrameRight[(len(self.jmpFrameLeft)-1)]
                else:
                    self.image = self.jumpShootRight[(len(self.jmpFrameLeft)-1)]
                    
        #platform collision for X
        blockHitList = pygame.sprite.spritecollide(self, self.level.platforms_list, False)
        for block in blockHitList:
            if self.ChangeX > 0:
                self.rect.right = block.rect.left
            elif self.ChangeX < 0:
                self.rect.left = block.rect.right

        self.rect.y += self.ChangeY

        #platform collision for Y
        blockHitList = pygame.sprite.spritecollide(self, self.level.platforms_list, False)
        for block in blockHitList:
            if self.ChangeY > 0:
                self.ChangeY = 0
                self.rect.bottom = block.rect.top
            elif self.ChangeY < 0:
                self.rect.top = block.rect.bottom

                
        enemyHitList = pygame.sprite.spritecollide(self, self.level.enemy_list, False)
        for enemy in enemyHitList:
            self.Health -= 1
            if self.ChangeX > 0:
                self.rect.x += -60
            elif self.ChangeX < 0:
                self.rect.x += 60
            elif self.ChangeX == 0:
                if enemy.direction == "L":
                    self.rect.x += -60
                elif enemy.direction == "R":
                    self.rect.x += 60

        friendHitList = pygame.sprite.spritecollide(self, self.level.friend_list, True)
        for friends in friendHitList:
            self.level.friendCount -= 1
                    
    def Left(self):
        self.direction = "L"
        if self.status[3] != "Left":
            self.ChangeX = -8
  
    def Right(self): 
        self.direction = "R"
        if self.status[3] != "Right":
            self.ChangeX = 8
  
    def Stop(self):
        self.ChangeX = 0

    def Jump(self):
        if self.ChangeY == 0: 
            self.ChangeY = -40

    def Shoot(self):
        self.shoot = True
        if len(self.level.bullet_list) < 1:
            if self.status[1] == "R":
                self.level.spriteGenerate(self.level.bulletAnimations, self.rect.right, self.rect.y + 15, 12, self.rect.right, 1000, None, "Bullet")
            else:
                self.level.spriteGenerate(self.level.bulletAnimations, self.rect.left, self.rect.y + 15, -12, self.rect.left, 1000, None, "Bullet")
            self.level.addBullets()

class Enemies(pygame.sprite.Sprite):
    Health = 4
    def __init__(self, Animations):
        pygame.sprite.Sprite.__init__(self)
        
        self.frame = 0
        self.FrameLeft = Animations[0]
        self.FrameRight = Animations[1]
        
        self.image = self.FrameLeft[self.frame]
        self.rect = self.image.get_rect()
        
        self.ChangeX = 0
        self.ChangeY = 0
        self.BoundXL = 0
        self.BoundXR = 0
        self.direction = Animations[2]
        
    def update(self):
        self.rect.x += self.ChangeX

        if self.direction == "L": 
            if self.frame < len(self.FrameLeft) - 1: 
                self.frame += 1
                self.image = self.FrameLeft[self.frame] 
            else: 
                self.frame = 1

        elif self.direction == "R": 
            if self.frame < len(self.FrameRight) - 1: 
                self.frame += 1
                self.image = self.FrameRight[self.frame] 
            else: 
                self.frame = 1
            
class Level():
    def __init__(self, play):
        self.platforms_list = pygame.sprite.Group()
        self.foreground_list = pygame.sprite.Group()
        self.door_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.friend_list = pygame.sprite.Group()
        self.bar_list = pygame.sprite.Group()
        self.bullet_list = pygame.sprite.Group()

        self.play = play

        self.background = pygame.image.load('FPBackground.jpg')
        self.background.convert()
 
        self.shiftWorld = 0
 
        self.BackH = -405
        self.count = 1
    
        self.plats = []
        self.scenery = []
        self.enemies = []
        self.bullets = []
        self.friendly = []
        self.end = []
        self.healthBarList = []
        self.friendCount = 0

        

        self.enemyAnimations = play.Animation('zero.png', WHITE, enemyPos, "R")
        
        self.enemyCrabAnimations = play.Animation('grass.png', PLATRANS, crabPos, "R")

        self.bulletAnimations = play.Animation('bullet.png', BULLTRANS, bulletPos, "R")

        self.friendlyAnimations = play.Animation('Friendly.png', FRIENDTRANS, friendlyPOS, "L")

        self.healthBarAnimations = play.Animation('HealthBar2.png', BLACK, healthBar, "L")
        
        
        #self.wallGenerate(platformData['Wall_Left'], 72, 104, 998, 428, 1800, 200)
        self.levelGenerate(platformData['Grass_Middle'], 112, 120, -120, 430, 1800, -1800, "Platform", "N")
        self.levelGenerate(platformData['Floating_Platform'], 48, 24, 520, 330, 850, -1800, "Platform", "N")
        self.levelGenerate(platformData['Floating_Platform'], 48, 24, 642, 240, 747, -1800, "Platform", "N")
        self.levelGenerate(platformData['Floating_Platform'], 48, 24, 1100, 240, 1100 + (48 * 4), -1800, "Platform", "N")
        self.levelGenerate(platformData['Floating_Platform'], 48, 24, 965, 140, 902 + (48 * 3), -1800, "Platform", "N")
        self.levelGenerate(platformData['Floating_Platform'], 48, 24, 780, 240, 950, -1800, "Stair", "U")
        self.levelGenerate(platformData['Flower'], 59, 160, 0, 290, None, None, "Scenery", "N")
        self.levelGenerate(platformData['end'], 47, 168, 1800, 315, None, None, "Door", "N")

        self.spriteGenerate(self.enemyAnimations, 800, 390, 5, 800, 1000, self.enemies, "Comp")
        self.spriteGenerate(self.enemyAnimations, 1100, 390, 5, 1100, 1400, self.enemies, "Comp")
        self.spriteGenerate(self.enemyCrabAnimations, 300, 400, 2, 300, 500, self.enemies, "Comp")
        self.spriteGenerate(self.friendlyAnimations, 1200, 415, -2, 800, 1200, self.friendly, "Comp")
        self.spriteGenerate(self.friendlyAnimations, 910, 315, -2, 560, 910, self.friendly, "Comp")
        self.spriteGenerate(self.friendlyAnimations, 1100 + (48 * 4.5), 227, -2, 1150, 1100 + (48 * 4.5), self.friendly, "Comp")
        for i in range(len(self.enemies)):
            self.spriteGenerate(self.healthBarAnimations, None, None, None, None, None, None, "Health")

        self.addPlatforms()
        self.addScenery()
        self.addEnd()
        self.addEnemies()
        self.addFriends()
        self.addHealth()

    def addPlatforms(self):
        for platforms in self.plats:
            block = Objects('grass.png', PLATRANS, platforms[0])
            block.rect.x = platforms[1] 
            block.rect.y = platforms[2]
            block.play = self.play
            self.platforms_list.add(block)

    def addScenery(self):
        for scenery in self.scenery:
            block = Objects('grass.png', PLATRANS, scenery[0])
            block.rect.x = scenery[1]
            block.rect.y = scenery[2]
            block.play = self.play
            self.foreground_list.add(block)

    def addEnd(self):
        for doors in self.end:
            door = Objects('doors.png', WHITE, doors[0])
            door.image = pygame.transform.flip(door.image, True, False)
            door.rect.x = doors[1]
            door.rect.y = doors[2]
            self.door_list.add(door)
            
    def addEnemies(self):    
        for enemy in self.enemies:
            Enemy = Enemies(enemy[0]) 
            Enemy.rect.x = enemy[1]
            Enemy.rect.y = enemy[2]
            Enemy.ChangeX = enemy[3]
            Enemy.BoundXL = enemy[4]
            Enemy.BoundXR = enemy[5]
            Enemy.initXL = enemy[4]
            Enemy.initXR = enemy[5]
            self.enemy_list.add(Enemy)

    def addFriends(self):    
        for friends in self.friendly:
            friend = Enemies(friends[0]) 
            friend.rect.x = friends[1]
            friend.rect.y = friends[2]
            friend.ChangeX = friends[3]
            friend.BoundXL = friends[4]
            friend.BoundXR = friends[5]
            self.friendCount += 1
            self.friend_list.add(friend)

    def addHealth(self):
        for bars in self.healthBarList:
            bar = HealthBars(bars)
            self.bar_list.add(bar)
        
    def addBullets(self):
        for bullets in self.bullets:
            bullet = MovingObjects(bullets[0])
            bullet.rect.x = bullets[1]
            bullet.rect.y = bullets[2]
            bullet.ChangeX = bullets[3]
            bullet.BoundXL = bullets[4]
            bullet.BoundXR = bullets[5]
            self.bullet_list.add(bullet)
            
    #Generates static sprites
    def levelGenerate(self, sprite, spriteX, spriteY, curX, curY, maxpX, maxpY, style, direction):
        if style == "Platform":
            while curX < maxpX and curY > maxpY: 
                curX = curX + spriteX - 2
                newPlat = [sprite, curX, curY]
                self.plats.append(newPlat)
                
        elif style == "Stair":
            if direction == "U":
                while curX < maxpX and curY > maxpY:
                    curX = curX + spriteX - 2
                    curY = curY - spriteY - 1
                    newPlat = [sprite, curX, curY]
                    self.plats.append(newPlat)
            elif direction == "D":
                while curX < maxpX and curY < maxpY:
                    curX = curX + spriteX - 2
                    curY = curY + spriteY - 1
                    newPlat = [sprite, curX, curY]
                    self.plats.append(newPlat)
                    
        elif style == "Wall":
            while curY > maxpY:
                curY = curY - spriteY + 8
                newPlat = [sprite, curX, curY]
                self.plats.append(newPlat)
                
        elif style == "Scenery":
            while curX < 1800:
                space = random.randint(0,5)
                curX = curX + (60 * space)
                newPretty = [sprite, curX, curY]
                self.scenery.append(newPretty)
                
        elif style == "Door":
            newEnd = [sprite, curX, curY]
            self.end.append(newEnd)
        
    #generates moving sprites
    def spriteGenerate(self,Animations, curX, curY, speed, BoundXL, BoundXR, spriteList, style):
        if style == "Comp":
            newComp = [Animations, curX, curY, speed, BoundXL, BoundXR]
            spriteList.append(newComp)
            
        elif style == "Bullet":
            newEnemy = [Animations, curX, curY, speed, BoundXL, BoundXR]
            self.bullets.append(newEnemy)
            
        elif style == "Health":
            newBar = [Animations]
            self.healthBarList.append(newBar)
        
    def update(self):
        self.platforms_list.update()
        self.foreground_list.update()
        self.door_list.update()
        self.enemy_list.update()
        self.friend_list.update()

        enemySprites = self.enemy_list.sprites()
        barSprites = self.bar_list.sprites()
        for i in range(len(self.enemy_list)):
            if enemySprites[i].Health > 0:
                barSprites[i].image = self.healthBarAnimations[0][enemySprites[i].Health]
                barSprites[i].rect.x = enemySprites[i].rect.x - 12
                barSprites[i].rect.y = enemySprites[i].rect.y - 20
            elif enemySprites[i].Health <= 0:
                barSprites[i].image = self.healthBarAnimations[0][enemySprites[i].Health]
                self.enemy_list.remove(enemySprites[i])
                self.bar_list.remove(barSprites[i])
            

        for enemy in self.enemy_list:
            enemyPosition = enemy.rect.x - self.shiftWorld
            if enemyPosition <= enemy.BoundXL:
                enemy.direction = "R"
                enemy.ChangeX *= -1
            elif enemyPosition >= enemy.BoundXR:
                enemy.direction = "L"
                enemy.ChangeX *= -1

        for friend in self.friend_list:
            friendPosition = friend.rect.x - self.shiftWorld
            if friendPosition == friend.BoundXL:
                friend.direction = "R"
                friend.ChangeX *= -1
            elif friendPosition == friend.BoundXR:
                friend.direction = "L"
                friend.ChangeX *= -1
           
        for bullets in self.bullet_list:
            bullets.rect.x += bullets.ChangeX
            bulletPosition = bullets.rect.x
            screenRight = ScreenW
            screenLeft = 0
            if bullets.rect.x > screenRight or bullets.rect.x < screenLeft:
                self.bullets.remove(self.bullets[0])
                self.bullet_list.remove(bullets)

    def draw(self, screen):
        screen.blit(self.background, (self.shiftWorld // 3, self.BackH))
        self.foreground_list.draw(screen)
        self.door_list.draw(screen)
        self.platforms_list.draw(screen)
        self.friend_list.draw(screen)
        self.enemy_list.draw(screen)
        self.bullet_list.draw(screen)
        self.bar_list.draw(screen)
            
    def Shift(self, ShiftX):
        self.shiftWorld += ShiftX

        for plats in self.platforms_list: 
            plats.rect.x += ShiftX

        for scenery in self.foreground_list:
            scenery.rect.x += ShiftX // 3

        for enemy in self.enemy_list:
            enemy.rect.x += ShiftX

        for friend in self.friend_list:
            friend.rect.x += ShiftX

        for bullet in self.bullet_list:
            bullet.rect.x += ShiftX

        for doors in self.door_list:
            doors.rect.x += ShiftX

def Game():
    play = Player()
    level = Level(play)
    
    level_list = []
    level_list.append(level)
    current_level_no = 0
    current_level = level_list[current_level_no]
    
    playerSprites = pygame.sprite.Group()
    play.level = current_level
    playerSprites.add(play)
    
    pygame.display.set_caption('FWGameEngine')
    
    clock = pygame.time.Clock() 

    keepGoing = True
    while keepGoing:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                keepGoing = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                play.Left()

            if event.key == pygame.K_RIGHT: 
                play.Right() 
  
            if event.key == pygame.K_UP:
                play.Jump()

            if event.key == pygame.K_SPACE:
                play.Shoot()
                    
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and play.ChangeX < 0:
                play.Stop()

            if event.key == pygame.K_RIGHT and play.ChangeX > 0:
                play.Stop()

            if event.key == pygame.K_SPACE:
                play.shoot = False
                
        playerSprites.update()
        current_level.update()
        
        if play.rect.x <= 250:
            scroll = 250 - play.rect.x
            if level.shiftWorld < 0:
                play.rect.x = 250
                current_level.Shift(scroll)

        if play.rect.x >= 550: 
            scroll = play.rect.x - 550
            if level.shiftWorld > -1100:
                play.rect.x = 550
                current_level.Shift(-scroll)
            
        if play.rect.x <= 0:
            play.rect.x = 0

        for enemies in level.enemy_list:
            playDist = enemies.rect.x - play.rect.x
            if playDist >= 0:
                if abs(playDist) < 150:
                    enemies.BoundXL += enemies.ChangeX
                    enemies.BoundXR += enemies.ChangeX
            elif playDist < 0:
                if abs(playDist) < 150:
                    enemies.BoundXL += enemies.ChangeX
                    enemies.BoundXR += enemies.ChangeX

        for bullet in level.bullet_list:
            enemyHitList = pygame.sprite.spritecollide(bullet, level.enemy_list, False)
            for enemy in enemyHitList:
                enemy.Health -= 1
                level.bullet_list.remove(bullet)
                level.bullets.remove(level.bullets[0])
                if level.enemy_list.has(enemy) == 0:
                    play.Alone = True
    
        if play.Health == 0:
            playerSprites.remove(play)
            keepGoing = False

        if play.rect.x > 700 and play.Alone and level.friendCount == 0:
            keepGoing = False

        level.draw(screen)
        playerSprites.draw(screen)

        clock.tick(30)

        pygame.display.flip()
  
    pygame.quit()
  
Game()
