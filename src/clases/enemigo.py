import pygame

#Hereda de Sprite de pygame
class Enemigo(pygame.sprite.Sprite):

    def __init__(self, escalado, alto, ancho, limites, jugador):

        super().__init__()

        self.escalado = escalado
        self.alto = alto
        self.ancho = ancho
        self.limites = limites
        self.jugador = jugador
        self.alcance = 100

        #Atributos del Enemigo
        self.velocidad_y = 0
        self.gravedad = 1
        self.velocidad = 3        
        self.corriendo = False
        self.atacando = False
        self.muriendo = False
        self.gravedad = 1
        self.izq = False

        #Listas de imagenes
        self.imagenes_quieto_escaladas = []
        self.imagenes_corriendo_escaladas = []
        self.imagenes_atacando_escaladas = []
        self.imagenes_muriendo_escaladas = []

        # Cargar y escalar las imagenes
        self.imagenes_quieto_escaladas = [self.cargar_escalar_imagen('src\\assets\\sprites\\Orco\\Parado\\0_Orc_Idle_00{}.png'.format(i)) for i in range(8)]
        self.imagenes_corriendo_escaladas = [self.cargar_escalar_imagen('src\\assets\\sprites\\Orco\\Corriendo\\0_Orc_Running_00{}.png'.format(i)) for i in range(8)]
        self.imagenes_atacando_escaladas = [self.cargar_escalar_imagen('src\\assets\\sprites\\Orco\\Atacando\\0_Orc_Slashing_00{}.png'.format(i)) for i in range(8)]
        self.imagenes_muriendo_escaladas = [self.cargar_escalar_imagen('src\\assets\\sprites\\Orco\\Muriendo\\0_Orc_Dying_00{}.png'.format(i)) for i in range(8)]

        # Establecer una imagen de la lista como imagen del sprite
        self.indice_imagen = 0
        self.image = self.imagenes_quieto_escaladas[self.indice_imagen]
        self.rect = self.image.get_rect()

        #Posicion inicial
        self.rect.topleft = (self.ancho, self.alto - self.rect.height)

    def update(self):

        #Calcular distancia al jugador y perseguirlo
        dx = self.jugador.rect.x - self.rect.x
        distancia = abs(dx)

        if self.jugador.rect.x < self.rect.x:
            self.izq = True
        else:
            self.izq = False

        if not self.muriendo:
            if distancia != 0:
                
                if distancia < self.alcance:
                    self.corriendo = False
                    self.atacando = True

                    if self.jugador.atacando and self.izq is not self.jugador.izq:
                        self.corriendo = False
                        self.atacando = False
                        self.muriendo = True
                        self.jugador.puntos += 10
                        self.kill()
                    else:
                        if self.rect.colliderect(self.jugador.rect) and not self.jugador.saltando and not self.jugador.colision_detectada:
                            self.jugador.puntos -= 1
                            self.jugador.colision_detectada = True
                        else:
                            self.jugador.colision_detectada = False
                
                else:
                    self.corriendo = True
                    self.atacando = False
                    dx /= distancia
                    self.rect.x += dx * self.velocidad

            else:
                self.corriendo = False

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
        elif self.muriendo:
            self.indice_imagen = (self.indice_imagen + 1) % len(self.imagenes_muriendo_escaladas)
            if self.izq:
                self.image = pygame.transform.flip(self.imagenes_muriendo_escaladas[self.indice_imagen], True, False)    
            else:
                self.image = self.imagenes_atacando_escaladas[self.indice_imagen]
        else:
            self.indice_imagen = (self.indice_imagen + 1) % len(self.imagenes_quieto_escaladas)
            if self.izq:
                self.image = pygame.transform.flip(self.imagenes_quieto_escaladas[self.indice_imagen], True, False)
            else:
                self.image = self.imagenes_quieto_escaladas[self.indice_imagen]

        
        
        #Hacemos caer el enemigo
        self.velocidad_y += self.gravedad
        self.rect.y += self.velocidad_y

        # Limita la caída al suelo
        if self.rect.y > self.alto - self.rect.height:
            self.rect.y = self.alto - self.rect.height
            self.velocidad_y = 0
        
        # Clamp para limitar la posición del jugador dentro de los límites del escenario
        self.rect.clamp_ip(self.limites)


    def cargar_escalar_imagen(self, ruta):
        imagen_original = pygame.image.load(ruta).convert_alpha()
        return pygame.transform.scale(imagen_original, (int(imagen_original.get_width() * self.escalado), int(imagen_original.get_height() * self.escalado)))
