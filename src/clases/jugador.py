import pygame

#Hereda de Sprite de pygame
class Jugador(pygame.sprite.Sprite):

    def __init__(self, escalado, alto, ancho, limites):

        super().__init__()

        self.escalado = escalado
        self.alto = alto
        self.ancho = ancho
        self.limites = limites

        #Atributos del jugador
        self.velocidad_y = 0
        self.gravedad = 1
        self.salto = -20
        self.velocidad = 8        
        self.saltando = False
        self.corriendo = False
        self.atacando = False
        self.gravedad = 1
        self.izq = False
        self.puntos = 0
        self.colision_detectada = False

        #Listas de imagenes
        self.imagenes_quieto_escaladas = []
        self.imagenes_corriendo_escaladas = []
        self.imagenes_atacando_escaladas = []
        self.imagenes_saltando_escaladas = []
        self.imagenes_muriendo_escaladas = []

        # Cargar y escalar las imagenes
        self.cargar_escalar_imagenes()

        # Establecer una imagen de la lista como imagen del sprite
        self.indice_imagen = 0
        self.image = self.imagenes_quieto_escaladas[self.indice_imagen]
        self.rect = self.image.get_rect()

        #Posicion inicial
        self.rect.topleft = (self.ancho // 2, self.alto - self.rect.height)

    def update(self):
        #Cambiar imagen en cada actualizacion

        if self.corriendo:
            self.indice_imagen = (self.indice_imagen + 1) % len(self.imagenes_corriendo_escaladas)
            if self.izq: 
                self.image = pygame.transform.flip(self.imagenes_corriendo_escaladas[self.indice_imagen], True, False)
            else:
                self.image = self.imagenes_corriendo_escaladas[self.indice_imagen]
        elif self.atacando:
            self.indice_imagen = (self.indice_imagen + 1) % len(self.imagenes_atacando_escaladas)
            if self.izq:
                self.image = pygame.transform.flip(self.imagenes_atacando_escaladas[self.indice_imagen], True, False)
            else:
                self.image = self.imagenes_atacando_escaladas[self.indice_imagen]
        elif self.saltando:
            self.indice_imagen = (self.indice_imagen + 1) % len(self.imagenes_saltando_escaladas)
            self.image = self.imagenes_saltando_escaladas[self.indice_imagen]
        else:
            self.indice_imagen = (self.indice_imagen + 1) % len(self.imagenes_quieto_escaladas)
            if self.izq:
                self.image = pygame.transform.flip(self.imagenes_quieto_escaladas[self.indice_imagen], True, False)
            else:
                self.image = self.imagenes_quieto_escaladas[self.indice_imagen]

        #Obtenemos las teclas presionadas
        teclas = pygame.key.get_pressed()

        #Movemos segun la tecla presionada

        if teclas[pygame.K_LEFT]:
            self.rect.x -= self.velocidad
            self.corriendo = True
            self.izq = True
        elif teclas[pygame.K_RIGHT]:
            self.rect.x += self.velocidad
            self.corriendo = True
            self.izq = False
        elif teclas[pygame.K_UP]:

            #Salta si está en el suelo
            if self.rect.y == self.alto - self.rect.height:
                self.velocidad_y = self.salto
                self.saltando = True

        elif teclas[pygame.K_SPACE]:
            self.atacando = True
        else:
            
            self.corriendo = False
            self.atacando = False
        
        #Hacemos caer el jugador
        self.velocidad_y += self.gravedad
        self.rect.y += self.velocidad_y

        # Limitar la caída al suelo
        if self.rect.y > self.alto - self.rect.height:
            self.rect.y = self.alto - self.rect.height
            self.velocidad_y = 0
            self.saltando = False
        
        # Clamp para limitar la posición del jugador dentro de los límites del escenario
        self.rect.clamp_ip(self.limites)


    def cargar_escalar_imagenes(self):
        imagenes_quieto_originales = [
            pygame.image.load('src\\assets\\sprites\\Minotauro\\Parado\\0_Minotaur_Idle_000.png').convert_alpha(),
            pygame.image.load('src\\assets\\sprites\\Minotauro\\Parado\\0_Minotaur_Idle_001.png').convert_alpha(),
            pygame.image.load('src\\assets\\sprites\\Minotauro\\Parado\\0_Minotaur_Idle_002.png').convert_alpha(),
            pygame.image.load('src\\assets\\sprites\\Minotauro\\Parado\\0_Minotaur_Idle_003.png').convert_alpha(),
            pygame.image.load('src\\assets\\sprites\\Minotauro\\Parado\\0_Minotaur_Idle_004.png').convert_alpha(),
            pygame.image.load('src\\assets\\sprites\\Minotauro\\Parado\\0_Minotaur_Idle_005.png').convert_alpha(),
            pygame.image.load('src\\assets\\sprites\\Minotauro\\Parado\\0_Minotaur_Idle_006.png').convert_alpha(),
            pygame.image.load('src\\assets\\sprites\\Minotauro\\Parado\\0_Minotaur_Idle_007.png').convert_alpha()
        ]

        for img in imagenes_quieto_originales:
            imagen_escalada = pygame.transform.scale(img, (int(img.get_width() * self.escalado), int(img.get_height() * self.escalado)))
            self.imagenes_quieto_escaladas.append(imagen_escalada)

        imagenes_corriendo_originales = [
            pygame.image.load('src\\assets\\sprites\\Minotauro\\Corriendo\\0_Minotaur_Running_000.png').convert_alpha(),
            pygame.image.load('src\\assets\\sprites\\Minotauro\\Corriendo\\0_Minotaur_Running_001.png').convert_alpha(),
            pygame.image.load('src\\assets\\sprites\\Minotauro\\Corriendo\\0_Minotaur_Running_002.png').convert_alpha(),
            pygame.image.load('src\\assets\\sprites\\Minotauro\\Corriendo\\0_Minotaur_Running_003.png').convert_alpha(),
            pygame.image.load('src\\assets\\sprites\\Minotauro\\Corriendo\\0_Minotaur_Running_004.png').convert_alpha(),
            pygame.image.load('src\\assets\\sprites\\Minotauro\\Corriendo\\0_Minotaur_Running_005.png').convert_alpha(),
            pygame.image.load('src\\assets\\sprites\\Minotauro\\Corriendo\\0_Minotaur_Running_006.png').convert_alpha(),
            pygame.image.load('src\\assets\\sprites\\Minotauro\\Corriendo\\0_Minotaur_Running_007.png').convert_alpha()
        ]

        for img in imagenes_corriendo_originales:
            imagen_escalada = pygame.transform.scale(img, (int(img.get_width() * self.escalado), int(img.get_height() * self.escalado)))
            self.imagenes_corriendo_escaladas.append(imagen_escalada)

        imagenes_atacando_originales = [
            pygame.image.load('src\\assets\\sprites\\Minotauro\\Atacando\\0_Minotaur_Slashing_000.png').convert_alpha(),
            pygame.image.load('src\\assets\\sprites\\Minotauro\\Atacando\\0_Minotaur_Slashing_001.png').convert_alpha(),
            pygame.image.load('src\\assets\\sprites\\Minotauro\\Atacando\\0_Minotaur_Slashing_002.png').convert_alpha(),
            pygame.image.load('src\\assets\\sprites\\Minotauro\\Atacando\\0_Minotaur_Slashing_003.png').convert_alpha(),
            pygame.image.load('src\\assets\\sprites\\Minotauro\\Atacando\\0_Minotaur_Slashing_004.png').convert_alpha(),
            pygame.image.load('src\\assets\\sprites\\Minotauro\\Atacando\\0_Minotaur_Slashing_005.png').convert_alpha(),
            pygame.image.load('src\\assets\\sprites\\Minotauro\\Atacando\\0_Minotaur_Slashing_006.png').convert_alpha(),
            pygame.image.load('src\\assets\\sprites\\Minotauro\\Atacando\\0_Minotaur_Slashing_007.png').convert_alpha()
        ]

        for img in imagenes_atacando_originales:
            imagen_escalada = pygame.transform.scale(img, (int(img.get_width() * self.escalado), int(img.get_height() * self.escalado)))
            self.imagenes_atacando_escaladas.append(imagen_escalada)

        imagenes_muriendo_originales = [
            pygame.image.load('src\\assets\\sprites\\Minotauro\\Muriendo\\0_Minotaur_Dying_000.png').convert_alpha(),
            pygame.image.load('src\\assets\\sprites\\Minotauro\\Muriendo\\0_Minotaur_Dying_001.png').convert_alpha(),
            pygame.image.load('src\\assets\\sprites\\Minotauro\\Muriendo\\0_Minotaur_Dying_002.png').convert_alpha(),
            pygame.image.load('src\\assets\\sprites\\Minotauro\\Muriendo\\0_Minotaur_Dying_003.png').convert_alpha(),
            pygame.image.load('src\\assets\\sprites\\Minotauro\\Muriendo\\0_Minotaur_Dying_004.png').convert_alpha(),
            pygame.image.load('src\\assets\\sprites\\Minotauro\\Muriendo\\0_Minotaur_Dying_005.png').convert_alpha(),
            pygame.image.load('src\\assets\\sprites\\Minotauro\\Muriendo\\0_Minotaur_Dying_006.png').convert_alpha(),
            pygame.image.load('src\\assets\\sprites\\Minotauro\\Muriendo\\0_Minotaur_Dying_007.png').convert_alpha()
        ]

        for img in imagenes_muriendo_originales:
            imagen_escalada = pygame.transform.scale(img, (int(img.get_width() * self.escalado), int(img.get_height() * self.escalado)))
            self.imagenes_muriendo_escaladas.append(imagen_escalada)

        imagenes_saltando_originales = [
            pygame.image.load('src\\assets\\sprites\\Minotauro\\Saltando\\0_Minotaur_Jump Start_000.png').convert_alpha(),
            pygame.image.load('src\\assets\\sprites\\Minotauro\\Saltando\\0_Minotaur_Jump Start_001.png').convert_alpha(),
            pygame.image.load('src\\assets\\sprites\\Minotauro\\Saltando\\0_Minotaur_Jump Start_002.png').convert_alpha(),
            pygame.image.load('src\\assets\\sprites\\Minotauro\\Saltando\\0_Minotaur_Jump Start_003.png').convert_alpha(),
            pygame.image.load('src\\assets\\sprites\\Minotauro\\Saltando\\0_Minotaur_Jump Start_004.png').convert_alpha(),
            pygame.image.load('src\\assets\\sprites\\Minotauro\\Saltando\\0_Minotaur_Jump Start_005.png').convert_alpha(),
            pygame.image.load('src\\assets\\sprites\\Minotauro\\Saltando\\0_Minotaur_Jump Start_006.png').convert_alpha(),
            pygame.image.load('src\\assets\\sprites\\Minotauro\\Saltando\\0_Minotaur_Jump Start_007.png').convert_alpha(),
            pygame.image.load('src\\assets\\sprites\\Minotauro\\Saltando\\0_Minotaur_Jump Start_008.png').convert_alpha(),
            pygame.image.load('src\\assets\\sprites\\Minotauro\\Saltando\\0_Minotaur_Jump Start_009.png').convert_alpha(),
            pygame.image.load('src\\assets\\sprites\\Minotauro\\Saltando\\0_Minotaur_Jump Start_010.png').convert_alpha()
        ]

        for img in imagenes_saltando_originales:
            imagen_escalada = pygame.transform.scale(img, (int(img.get_width() * self.escalado), int(img.get_height() * self.escalado)))
            self.imagenes_saltando_escaladas.append(imagen_escalada)