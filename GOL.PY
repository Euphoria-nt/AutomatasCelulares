import sys, pygame
import numpy as np
import matplotlib.pyplot as plt
import time
import pylint
import math

pygame.init()

size = width, height = 1000,1000
nxC = 120
nyC = 120

dimCW = (width -1) / nxC
dimCH = (height -1) / nyC

bg = 25,25,25

screen = pygame.display.set_mode((height,width), pygame.RESIZABLE)

screen.fill(bg)

gameState = np.zeros((nxC,nyC))
gameState[21,21] = 1
gameState[22,22] = 1
gameState[22,23] = 1
gameState[21,23] = 1
gameState[20,23] = 1

pauseExec = False

while 1:

    new_gameState = np.copy(gameState)

    # proceed events
    ev = pygame.event.get()

    for event in ev:

        if event.type == pygame.KEYDOWN:
            pauseExec = not pauseExec

        mouseClick = pygame.mouse.get_pressed() 
    
        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()

            if posX > 0  and posX < width -1 and posY > 0 and posX < height-1:
                new_gameState[math.floor(posX / dimCW),
                    math.floor(posY / dimCH)] =mouseClick[0] and not mouseClick[2]
    screen.fill(bg)

    for y in range(0, nyC):
        for x in range(0, nxC):
            #Si no esta pausada la ejecucion:
            if not pauseExec:
                # Calcula el numero de vecinos cercanos.
                n_neigh=gameState[(x-1) % nxC,(y-1) % nyC] + \
                        gameState[(x) % nxC,(y-1) % nyC] +   \
                        gameState[(x+1) % nxC,(y-1) % nyC] + \
                        gameState[(x-1) % nxC,(y) % nyC] +   \
                        gameState[(x+1) % nxC,(y) % nyC] +   \
                        gameState[(x-1) % nxC,(y+1) % nyC] + \
                        gameState[(x) % nxC,(y+1) % nyC] +   \
                        gameState[(x+1) % nxC,(y+1) % nyC] 
                        

            # Una célula muerta con exactamente 3 células vecinas vivas "nace" (es decir, al turno siguiente estará viva).
                if gameState[x,y] == 0 and n_neigh == 3:
                    new_gameState[x,y] = 1
            
            #Una célula viva con 2 o 3 células vecinas vivas sigue viva, en otro caso muere (por "soledad" o "superpoblación").
                elif gameState[x,y] == 1 and (n_neigh <2 or n_neigh >3):
                    new_gameState[x,y] = 0

            #Calculamos la posicion de cada celda.
            poly = [((x) * dimCW,(y)*dimCH),
                ((x+1) * dimCW,     (y)*dimCH),
                ((x+1) * dimCW,     (y+1)*dimCH),
                ((x) * dimCW,   (y+1)*dimCH)]

            #Dibujamos el estado calculando en la rejilla.
            if new_gameState[x,y] == 0:
                pygame.draw.polygon(screen,(128,128,128), poly,1)
            else:
                pygame.draw.polygon(screen,(255,255,255),poly,0)

    time.sleep(1 / 30) 

    gameState = np.copy(new_gameState)
    pygame.display.flip() 
