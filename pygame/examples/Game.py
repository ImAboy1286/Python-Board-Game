#Import pygame
import pygame
#Import random
import random
#Import os
import os
#Import math
import math
#import sys
import sys

def IfExp(bool: bool, true, false):
    if bool:
        return true
    else:
        return false





class Unit:
    #Constants
    UnitToFilePath = {
    "Soldier": "UnitImages\BasicSoldier\{}\\",
    "Tank": "UnitImages\BasicTank\{}\\",
    "Infantry": "UnitImages\BasicInfantry\{}\\",
    "Airplane": "UnitImages\BasicAir\{}\\",
    "Soldier Barracks": "UnitImages\BasicSoldierHousing\{}\\",
    "Tank Storage": "UnitImages\BasicTankStorage\{}\\",
    "Infantry Barracks": "UnitImages\BasicInfantryHousing\{}\\",
    "Airplane Storage": "UnitImages\BasicAirStorage\{}\\",
    }
    #Class for the units
    def __init__(self, name: str, health: int, attack: int, defense: int, speed: int, x: int, y: int, images: dict, team: str, attackRange: int):
        self.name = name
        self.health = health
        self.MaxHealth = health
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.x = x
        self.y = y
        self.image = images
        self.state = 'Default'
        self.img = pygame.image.load(self.UnitToFilePath[name].format(team) + self.image[self.state])
        self.rect = self.img.get_rect()
        self.rect.x = self.x * 256
        self.rect.y = self.y * 256
        self.alive = True
        self.HasMove = False
        self.HasAttack = False
        self.team = team
        self.attackRange = attackRange
    def Move(self, x: int, y: int):
        if not self.HasMove:
            self.x = x
            self.y = y
            self.rect.x = self.x * 256 * zoom + cameraLocation[0]
            self.rect.y = self.y * 256 * zoom + cameraLocation[1]
            self.HasMove = True
            self.PlaySound('Move')
            for Unit in Units:
                if not Unit.alive:
                    if Unit.x == self.x and Unit.y == self.y:
                        Units.remove(Unit)
    def Attack(self, target: 'Unit'):
        if not self.HasAttack:
            target.health -= max(self.attack - target.defense, 0)
            if target.health <= 0:
                target.alive = False
            self.HasAttack = True
    def SetState(self, state: str):
        if state in self.image:
            self.state = state
            self.img = pygame.image.load(self.UnitToFilePath[self.name].format(self.team) + self.image[self.state])
    def IsHover(self):
        global SelectedUnit
        if self.alive:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                return True
            else:
                return False
        elif(SelectedUnit == self):
            return True
        return False
    def Render(self, screen):
        self.rect = pygame.transform.scale(self.img, (256 * zoom, 256 * zoom)).get_rect()
        self.rect.x = self.x * 256 * zoom + cameraLocation[0]
        self.rect.y = self.y * 256 * zoom + cameraLocation[1]
        if self.name == 'Soldier':
            if self.health < self.MaxHealth / 3:
                self.SetState("Scared")
        if not self.alive:
            self.SetState("Dead")
        hoverSize = IfExp(self.IsHover(), 320, 256)
        hoverOffset = IfExp(self.IsHover(), -16, 0)
        screen.blit(pygame.transform.scale(self.img, (hoverSize * zoom, hoverSize * zoom)), (self.x * 256 * zoom + cameraLocation[0] + (hoverOffset * zoom), self.y * 256 * zoom + cameraLocation[1] + (hoverOffset * zoom)))
        if self.IsHover():
            self.ShowDescription()
    def ShowDescription(self):
        font = pygame.font.SysFont('bahnschrift.ttf', 30)
        UnitDescText = font.render("HP: {}/{}   Atk: {}  Def: {}  Spd: {}".format(self.health,self.MaxHealth,self.attack,self.defense,self.speed), True, (0, 0, 0))
        UnitDescRect = UnitDescText.get_rect()
        UnitDescRect.x = self.x * 256 * zoom + cameraLocation[0] + (320 * zoom) + 16
        UnitDescRect.y = self.y * 256 * zoom + cameraLocation[1] + (256 * zoom) - 16
        screen.blit(UnitDescText, UnitDescRect)
    def Update(self):
        self.HasMove = False
        self.HasAttack = False
    def UpdateState(self):
        if not self.alive:
            self.SetState("Dead")
            return
        if self.name == 'Soldier':
            if self.health < self.MaxHealth / 3:
                self.SetState("Scared")
        if not self.name in ['Soldier', 'Infantry'] and self.health < self.MaxHealth / 3:
            self.SetState("Damaged")
    def PlaySound(self, sound: str, usesName: bool = True):
        footstep = True if self.name in ['Soldier', 'Infantry'] and sound == 'Move' else False
        if footstep:
            global MapStyle
            pygame.mixer.Channel(0).play(pygame.mixer.Sound("Sounds\\" + 'Footstep' + MapStyle + '.wav'))
        else:
            name = self.name if usesName else ''
            pygame.mixer.Channel(0).play(pygame.mixer.Sound("Sounds\\" + sound + name + '.wav'))

        
#Spawner Unit Class
class Spawner(Unit):
    def __init__(self, name: str, health: int, attack: int, defense: int, speed: int, x: int, y: int, images: dict, team: str, attackRange: int):
        super().__init__(name, health, attack, defense, speed, x, y, images, team, attackRange)
        self.spawned = False
        self.spawnTimer = 0
        self.spawnTime = 10
        self.spawnUnit = None
    def Spawn(self):
        if not self.spawned:
            self.spawned = True
            self.spawnUnit = Unit(self.spawnUnit, self.x, self.y, self.team)
            Units.append(self.spawnUnit)
            self.PlaySound('Spawn')
    def Update(self):
        super().Update()
        if self.spawned:
            self.spawnUnit.Update()
        if self.spawnTimer >= self.spawnTime:
            self.Spawn()
            self.spawnTimer = 0
        else:
            self.spawnTimer += 1
    def Render(self, screen):
        super().Render(screen)
        if self.spawned:
            self.spawnUnit.Render(screen)


Imgs = {
    "Soldier": {
        "Default": "SoldierBasicNeutral.png",
        "Scared": "SoldierBasicScared.png",
        "Dead": "SoldierBasicDead.png",
        "Angry": "SoldierBasicAngry.png",
    },
    "Tank": {
        "Default": "TankBasicNeutral.png",
        "Dead": "TankBasicDead.png",
        "Damaged": "TankBasicDamaged.png",
    },
    "Infantry": {
        "Default": "InfantryBasicNeutral.png",
        "Scared": "InfantryBasicScared.png",
        "Dead": "InfantryBasicDead.png",
        "Angry": "InfantryBasicAngry.png"
    },
    "Airplane": {
        "Default": "AirBasicNeutral.png",
        "Dead": "AirBasicDead.png",
        "Damaged": "AirBasicDamaged.png"
    },
    "Soldier Barracks": {
        "Default": "SoldierHousingBasicNeutral.png",
        "Dead": "SoldierHousingBasicDead.png",
        "Damaged": "SoldierHousingBasicDamaged.png"
    },
    "Tank Storage": {
        "Default": "TankStorageBasicNeutral.png",
        "Dead": "TankStorageBasicDead.png",
        "Damaged": "TankStorageBasicDamaged.png"
    },
    "Infantry Barracks": {
        "Default": "InfantryHousingBasicNeutral.png",
        "Dead": "InfantryHousingBasicDead.png",
        "Damaged": "InfantryHousingBasicDamaged.png"
    },
    "Airplane Storage": {
        "Default": "AirStorageBasicNeutral.png",
        "Dead": "AirStorageBasicDead.png",
        "Damaged": "AirStorageBasicDamaged.png"
    }
}

UnitSounds = {
    "Soldier": {
        "Move": "SoldierMove.wav",
        "Attack": "SoldierAttack.wav",
        "Dead": "SoldierDead.wav",
        "Hurt": "SoldierHurt.wav"
    },
    "Tank": {
        "Move": "TankMove.wav",
        "Attack": "TankAttack.wav",
        "Dead": "TankDead.wav",
        "Hurt": "TankHurt.wav"
    },
    "Infantry": {
        "Move": "InfantryMove.wav",
        "Attack": "InfantryAttack.wav",
        "Dead": "InfantryDead.wav",
        "Hurt": "InfantryHurt.wav"
    },
    "Airplane": {
        "Move": "AirMove.wav",
        "Attack": "AirAttack.wav",
        "Dead": "AirDead.wav",
        "Hurt": "AirHurt.wav"
    }
}




BackgroundImgs = []
screen = pygame.display.set_mode((1920,1080))
camera = [0,0]
zoom = .4
cameraLocation = [0,0]
Units = [
Unit("Soldier", 100, 70, 10, 2, 0, 0, Imgs["Soldier"], "Red", 2),
Unit("Soldier", 100, 70, 10, 2, 0, 1, Imgs["Soldier"], "Blue", 2),
Unit("Soldier", 100, 70, 10, 2, 1, 0, Imgs["Soldier"], "Red", 2),
Unit("Soldier Barracks", 150, 0, 10, 0, 1, 1, Imgs["Soldier Barracks"], "Blue", 2)
]
SelectedUnit = None
MapStyle = ""



def DrawMap():
    for y in BackgroundImgs:
        Y = BackgroundImgs.index(y)
        for x in y:
            X = y.index(x)
            screen.blit(pygame.transform.scale(x, (256 * zoom, 256 * zoom)), (X * 256 * zoom + cameraLocation[0], Y * 256 * zoom + cameraLocation[1]))
    for Unit in Units:
        Unit.Render(screen)



def main():
    
    # initialize the pygame module
    pygame.init()
    pygame.mixer.init()
    # load and set the logo
    logo = pygame.image.load("logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Combat Board Game")
     
     
    # define a variable to control the main loop
    running = True

    #Define clock
    clock = pygame.time.Clock()

    
    #Choose Map Style
    global MapStyle
    MapStyle = ["Grass", "Snow"][random.randint(0,1)]
    #Create base floor
    for y in range(30):
        BackgroundImgs.append([])
        for x in range(30):
            BackgroundImgs[y].append(pygame.image.load("Terrain\BaseFloor\\" + MapStyle + ".png"))
    
    global zoom
    global camera
    global SelectedUnit

    WarnTime = -1

    # main loop
    while running:
        text = None
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_UP:
                    camera[1] += 1
                if event.key == pygame.K_DOWN:
                    camera[1] -= 1
                if event.key == pygame.K_LEFT:
                    camera[0] += 1
                if event.key == pygame.K_RIGHT:
                    camera[0] -= 1
                if event.key == pygame.K_z:
                    zoom += .2
                    zoom = min(zoom, 1)
                    cameraLocation[0] = cameraLocation[0] * zoom
                    cameraLocation[1] = cameraLocation[1] * zoom
                if event.key == pygame.K_x:
                    zoom -= .2
                    zoom = max(zoom, .2)
                    cameraLocation[0] = cameraLocation[0] * zoom
                    cameraLocation[1] = cameraLocation[1] * zoom
                if event.key == pygame.K_SPACE:
                    for Unit in Units:
                        Unit.Update()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    camera[1] -= 1
                if event.key == pygame.K_DOWN:
                    camera[1] += 1
                if event.key == pygame.K_LEFT:
                    camera[0] -= 1
                if event.key == pygame.K_RIGHT:
                    camera[0] += 1
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for Unit in Units:
                        if Unit.IsHover():
                            SelectedUnit = Unit
                            break
                if event.button == 3:
                    for Unit in Units:
                        if Unit.IsHover():
                            Unit.PlaySound("Move")
                            break
            if event.type == pygame.MOUSEBUTTONUP:
                if SelectedUnit != None:
                    if event.button == 1:
                        for Unit in Units:
                            if Unit.IsHover():
                                SelectedUnit.Attack(Unit)
                                SelectedUnit.HasAttack = True
                                SelectedUnit = None
                                break
                        else:
                            if abs(round((pygame.mouse.get_pos()[0] - cameraLocation[0]) / (256 * zoom)) + round((pygame.mouse.get_pos()[1] - cameraLocation[1]) / (256 * zoom))) - SelectedUnit.x - SelectedUnit.y <= SelectedUnit.speed:
                                SelectedUnit.Move(round((pygame.mouse.get_pos()[0] - cameraLocation[0]) / (256 * zoom)), round((pygame.mouse.get_pos()[1] - cameraLocation[1]) / (256 * zoom)))
                                SelectedUnit.HasMove = True
                                SelectedUnit = None
                            else:
                                WarnTime = 5
                                SelectedUnit = None
        #Moving Camera
        cameraLocation[0] += camera[0] * 32
        cameraLocation[1] += camera[1] * 32
        # fill the screen with black
        screen.fill((0, 0, 0))
        #Draw Map
        DrawMap()
        if WarnTime >= 0:
            WarnTime -= 1/clock.get_fps()
            font = pygame.font.Font('bahnschrift.ttf', 20)
            text = font.render("Cannot move that far", True, (255,0,0))
            screen.blit(text, (pygame.mouse.get_pos()[0] - text.get_width()/2, pygame.mouse.get_pos()[1] - text.get_height()/2 + 20))
        if SelectedUnit != None:
            temp = SelectedUnit.img.copy()
            temp.set_alpha(32 if round((pygame.mouse.get_pos()[0] - cameraLocation[0]) / (256 * zoom)) + round((pygame.mouse.get_pos()[1] - cameraLocation[1]) / (256 * zoom)) - SelectedUnit.x - SelectedUnit.y > SelectedUnit.speed or SelectedUnit.HasMove else 128)
            screen.blit(pygame.transform.scale(temp, (256 * zoom, 256 * zoom)), (round((pygame.mouse.get_pos()[0] - cameraLocation[0]) / (256 * zoom)) * 256 * zoom + cameraLocation[0], round((pygame.mouse.get_pos()[1] - cameraLocation[1]) / (256 * zoom)) * 256 * zoom + cameraLocation[1]))
        # update the screen
        pygame.display.flip()
        # limit to 120 frames per second
        clock.tick(120)

     
     

# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()






