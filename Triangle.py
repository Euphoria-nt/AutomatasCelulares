import sys, pygame
import numpy as np
import matplotlib.pyplot as plt
import time
import pylint
import math

pygame.init()

size = width, height = 1000,1000
nxC = 500
nyC = 500

dimCW = (width -1) / nxC
dimCH = (height -1) / nyC

bg = 25,25,25

screen = pygame.display.set_mode((height,width), pygame.RESIZABLE)

screen.fill(bg)

gameState= np.zeros((nxC,nyC))
gameState[int(nxC/2),0] = 1

pauseExec = True
rules = list(np.binary_repr(77,width=8))
rules.reverse()

for y in range(0,nyC):
    for x in range(0,nxC):

        #calculamos la posicion de cada celda
        poly = [((x) * dimCW,(y)*dimCH),
            ((x+1) * dimCW,     (y)*dimCH),
            ((x+1) * dimCW,     (y+1)*dimCH),
            ((x) * dimCW,   (y+1)*dimCH)]
        pygame.draw.polygon(screen,(128,128,128),poly,1)

y=0

while y <nyC:
    
    new_gameState = np.copy(gameState)
    #proceed events
    ev = pygame.event.get()

    for event in ev:
        if event.type == pygame.KEYDOWN:
            pauseExec= not pauseExec
        mouseClick = pygame.mouse.get_pressed()

        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()

            if posX > 0 and posY < width-1 and posY > 0 and posY < height-1:
                new_gameState[math.floor(posX/dimCW),
                math.floor(posY/dimCH)] = mouseClick[0] and not mouseClick[2]

    for x in range(0,nxC):
        #Si no esta pausada la ejecucion
        if not pauseExec:

            ruleIdx = 4 * gameState[(x-1)%nxC,y]+2 * gameState[x,y]+1 * gameState[(x+1)%nxC,y]

            new_gameState[x,(y+1)% nyC] = rules[int(ruleIdx)]

        #Calculamos la posicion de cada celda.
        poly = [((x) * dimCW,(y)*dimCH),
            ((x+1) * dimCW,     (y)*dimCH),
            ((x+1) * dimCW,     (y+1)*dimCH),
            ((x) * dimCW,   (y+1)*dimCH)]

            #Dibujamos el estado calculando en la rejilla.
        if new_gameState[x,y] == 1:
            pygame.draw.polygon(screen,(255,255,255),poly,0)

    time.sleep(0.01) 
    if not pauseExec:
        y =(y+1)

    gameState = np.copy(new_gameState)
    pygame.display.flip()


