#Imports
import random
from src.clases.jugador import Jugador
from src.clases.enemigo import Enemigo
import sys
#Importamos el paquete de pygame
import pygame

#Configuramos pygame
pygame.init()
anchoP = 900
altoP = 600
pantalla = pygame.display.set_mode((anchoP,altoP))
reloj = pygame.time.Clock()
escala = 0.30
fuente = pygame.font.Font(None, 36)
juego_iniciado = False
opcion_seleccionada = 0


#Opciones de juego

opciones = ['Iniciar Supervivencia', 'Salir']

#Fondo
fondoOriginal = pygame.image.load('src\\assets\\background\\forest bridge.png').convert_alpha()
fondo = pygame.transform.scale(fondoOriginal, (int(fondoOriginal.get_width() * escala), int(fondoOriginal.get_height() * escala)))
fondo_rect = fondo.get_rect()

#Camara de jugador
camara = pygame.Rect(0,0, anchoP, altoP)

#Limites del escenario
limites = pygame.Rect(0,0, fondo_rect.width, fondo_rect.height)

#Metodos adicionales
def mostrar_Texto(texto, x, y, color):
    texto_sf = fuente.render(texto, True, color)
    texto_rect = texto_sf.get_rect(center=(x,y))
    pantalla.blit(texto_sf, texto_rect) 

#Menu de pausa
def poner_pausa():
    #Opciones de pausa

    opciones_pausa = ['Reanudar juego', 'Menu principal', 'Salir']
    opcion_pausa = 0
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    if opcion_pausa == 0:
                        print("Juego reanudado")
                        return False, opcion_pausa

                    elif opcion_pausa == 1:
                        print("Yendo a menu principal")
                        return False, opcion_pausa

                    elif opcion_pausa == 2:
                        print("Salir")
                        pygame.quit()
                        sys.exit()
                elif evento.key == pygame.K_UP:
                    opcion_pausa = (opcion_pausa - 1) % len(opciones_pausa)
                elif evento.key == pygame.K_DOWN:
                    opcion_pausa = (opcion_pausa + 1) % len(opciones_pausa)
        
        pantalla.fill('white')
         #Dibujar fondo
        pantalla.blit(fondo, (0,0), area=camara)

        for i, opcion in enumerate(opciones_pausa):
                if i == opcion_pausa:
                     color = (255,255,255)
                else:
                     color = (150, 150, 150)
        
                mostrar_Texto(opcion, anchoP // 2, altoP // 2 + i * 50, color)
        
        pygame.display.flip()
        #Limitamos la tasa de cuadros por segundo
        reloj.tick(30)

#Menu de juego finalizado
def fin_juego(puntos):
    #Opciones de pausa

    opciones_menu = ['Menu principal', 'Salir']
    opcion_menu = 0
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    if opcion_menu == 0:
                        print("Juego finalizado")
                        return

                    elif opcion_menu == 1:
                        print("Salir")
                        pygame.quit()
                        sys.exit()
                elif evento.key == pygame.K_UP:
                    opcion_menu = (opcion_menu - 1) % len(opciones_menu)
                elif evento.key == pygame.K_DOWN:
                    opcion_menu = (opcion_menu + 1) % len(opciones_menu)
        
        pantalla.fill('white')
         #Dibujar fondo
        pantalla.blit(fondo, (0,0), area=camara)

        mostrar_Texto('Recolectaste: '+str(puntos) + ' puntos', anchoP // 2, 60, (255, 255, 255))

        for i, opcion in enumerate(opciones_menu):
                if i == opcion_menu:
                     color = (255,255,255)
                else:
                     color = (150, 150, 150)
        
                mostrar_Texto(opcion, anchoP // 2, altoP // 2 + i * 50, color)
        
        pygame.display.flip()
        #Limitamos la tasa de cuadros por segundo
        reloj.tick(30)

#Iniciar modo supervivencia
def iniciar_supervivencia():
    #Sprites
    lista_sprites = pygame.sprite.Group()

    jugador = Jugador(escala, altoP, anchoP, limites)

    orco = Enemigo(escala, altoP, anchoP, limites, jugador)

    lista_sprites.add(jugador)
    lista_sprites.add(orco)
    tiempo_total_supervivencia = 180000
    tiempo_inicio_supervivencia = pygame.time.get_ticks()
    pausa = False

    tiempo_entre_enemigos = 10000
    tiempo_ultima_aparicion = tiempo_inicio_supervivencia
    while True:
        #Capturamos los eventos que se producen
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    pausa = True
                    pausa, opcion = poner_pausa()

                    if opcion == 1:
                        return False

        if not pausa:
            tiempo_actual = pygame.time.get_ticks()
            tiempo_transcurrido = tiempo_actual - tiempo_inicio_supervivencia
            tiempo_restante = max(0, tiempo_total_supervivencia - tiempo_transcurrido)


            #Actualizamos los sprites
            lista_sprites.update()
    
            #Ajustamos la camara a la posicion del jugador
            camara.x = jugador.rect.x
            camara.clamp_ip(limites)

            pantalla.fill('white')
            #Dibujar fondo
            pantalla.blit(fondo, (0,0), area=camara)

            segundos_restantes = tiempo_restante // 1000
            minutos = segundos_restantes // 60
            segundos = segundos_restantes % 60
            tiempo_texto = f'Tiempo restante: {minutos:02d}:{segundos:02d}'
            mostrar_Texto(tiempo_texto, anchoP // 2, 30, (255, 255, 255))
            mostrar_Texto('Puntos: '+str(jugador.puntos), anchoP // 2, 60, (255, 255, 255))

            lista_sprites.draw(pantalla)
            #Colocamos objetos en la pantalla
            pygame.display.flip()
            #Limitamos la tasa de cuadros por segundo
            reloj.tick(30)

            if tiempo_restante > 0:
                tiempo_transcurrido_aparicion = tiempo_actual - tiempo_ultima_aparicion
                if tiempo_transcurrido_aparicion >= tiempo_entre_enemigos:
                    tiempo_ultima_aparicion = tiempo_actual
                    x_nueva_enemigo = random.randint(limites.left, limites.right)
                    nuevo_enemigo = Enemigo(escala, altoP, anchoP, limites, jugador)
                    nuevo_enemigo.rect.x = x_nueva_enemigo
                    lista_sprites.add(nuevo_enemigo)

            else:
                fin_juego(jugador.puntos)
                return False;


#Bucle principal
while True:
    #Capturamos los eventos que se producen
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if not juego_iniciado:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    if opcion_seleccionada == 0:
                        print("Modo supervivencia iniciado")
                        juego_iniciado = iniciar_supervivencia()
                    elif opcion_seleccionada == 1:
                        print("Salir")
                        pygame.quit()
                        sys.exit()
                elif evento.key == pygame.K_UP:
                    opcion_seleccionada = (opcion_seleccionada - 1) % len(opciones)
                elif evento.key == pygame.K_DOWN:
                    opcion_seleccionada = (opcion_seleccionada + 1) % len(opciones)

    if not juego_iniciado:
        
            pantalla.fill('white')
            #Dibujar fondo
            pantalla.blit(fondo, (0,0), area=camara)

             #Mostrar opciones de juego
            for i, opcion in enumerate(opciones):
                if i == opcion_seleccionada:
                     color = (255,255,255)
                else:
                     color = (150, 150, 150)
        
                mostrar_Texto(opcion, anchoP // 2, altoP // 2 + i * 50, color)

            pygame.display.flip()
            #Limitamos la tasa de cuadros por segundo
            reloj.tick(30)
