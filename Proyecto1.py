import pygame
import random
import ConfigParser
ANCHO=1024
ALTO=640
VERDE=(0,255,0)
BLANCO=(255,255,255)
NEGRO=(0,0,0)
ROJO=(255,0,0)
AZUL=(0, 0, 255)
AMARILLO=(255, 255, 0)
CIAN=(0, 255, 255)
MAGNETA=(255, 0, 255)
ROSADO=(234,137,154)
FUCSIA=(222,076,138)
GRIS=(215,215,215)
#Juego gallinas
'''
anc ancho de corte
alc alto de corte
'''
def Recortar(archivo,anc,alc):
    matriz=[]
    imagen=pygame.image.load(archivo).convert_alpha()
    i_ancho, i_alto=imagen.get_size()
    #print i_ancho, '', i_alto
    for x in range(i_ancho/anc):
        linea=[]
        for y in range(0,i_alto/alc):
            cuadro=(x*anc,y*alc,anc,alc)
            linea.append(imagen.subsurface(cuadro))
        matriz.append(linea)
    return matriz
class Jugador(pygame.sprite.Sprite):
    bloques=None
    def __init__(self, img_sprite):
        pygame.sprite.Sprite.__init__(self)
        self.image=img_sprite
        self.rect=self.image.get_rect()
        self.rect.x=100
        self.rect.y=100
        self.var_x=2
        self.var_y=0
        self.con=0
        self.dir=6
    def update(self):
        self.rect.x+=self.var_x
        self.rect.y+=self.var_y
        ls_choqueb=pygame.sprite.spritecollide(self,self.bloques,False)
        for b in ls_choqueb:
                if self.var_x>0:
                    self.rect.right=b.rect.left
                if self.var_x<0:
                    self.rect.left=b.rect.right
        self.rect.y+=self.var_y
        ls_choqueb=pygame.sprite.spritecollide(self,self.bloques,False)
        for b in ls_choqueb:
                if self.var_y>0:
                    self.rect.bottom=b.rect.top
                if self.var_y<0:
                    self.rect.top=b.rect.bottom
        if self.con<2:
            self.con+=1
        else:
            self.con=0
class Bala(pygame.sprite.Sprite):
    def __init__(self, archivo):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load(archivo).convert_alpha()
        self.rect=self.image.get_rect()
        self.rect.x=0
        self.rect.y=0
        self.var_x=0
        self.var_y=0
        self.dir=0
    def update(self):
        if self.dir==6:
            self.var_x+=10
            self.var_y=0
        if self.dir==5:
            self.var_x-=10
            self.var_y=0
        if self.dir==4:
            self.var_y+=10
            self.var_x=0
        if self.dir==7:
            self.var_y-=10
            self.var_x=0
        self.rect.x+=self.var_x
        self.rect.y+=self.var_y
class Enemigo(pygame.sprite.Sprite):
    def __init__(self, img_sprite):
        pygame.sprite.Sprite.__init__(self)
        self.image=img_sprite
        self.rect=self.image.get_rect()
        self.rect.x=100
        self.rect.y=100
        self.var_x=2
        self.var_y=0
        self.con=0
        self.dir=6
        self.disparar=False
        self.tiempo=random.randrange(10,40)
        self.vida=3
    def update(self):
        self.rect.x+=self.var_x
        self.rect.y+=self.var_y
        self.tiempo-=1
        '''if self.tiempo==0:
            self.disparar=True
            self.tiempo=random.randrange(20)'''
        if self.con<2:
            self.con+=1
        else:
            self.con=0
class Bloque(pygame.sprite.Sprite):
    def __init__(self, img_sprite):
        pygame.sprite.Sprite.__init__(self)
        self.image=img_sprite
        self.rect=self.image.get_rect()
        self.rect.x=0#ubicacion
        self.rect.y=0#ubicacion
        self.var_x=0
        self.var_y=0
    def update(self):
        self.rect.x+=self.var_x
        self.rect.y+=self.var_y

if __name__ == '__main__':
    #Configuracion del videojuego
    pygame.init()
    reloj=pygame.time.Clock()
    pantalla=pygame.display.set_mode([ANCHO,ALTO])
    todos=pygame.sprite.Group()
    enemigos=pygame.sprite.Group()
    balas=pygame.sprite.Group()
    bloques=pygame.sprite.Group()
    animal=Recortar('animales.png',32,32)
    jp=Jugador(animal[3][4])
    #print type (animal[3][4])
    #Creacion de 5 enemigos en posiciones aleatorias
    for i in range(5):
        en=Enemigo(animal[0][1])
        en.rect.x=random.randrange(ANCHO)
        en.rect.y=random.randrange(ALTO)
        en.var_x=(-1)*random.randrange(1,10)
        en.var_y=0#random.randrange(3,10)
        enemigos.add(en)
        todos.add(en)
    todos.add(jp)
    conenemi=50

    interprete=ConfigParser.ConfigParser()
    interprete.read('nivel.map')
    ar_origen=interprete.get("nivel","origen")
    mapa=interprete.get("nivel","mapa").split("\n")
    al=int(interprete.get("nivel","corte_alto"))
    an=int(interprete.get("nivel","corte_ancho"))
    fondo=Recortar(ar_origen,al,an)


    fin=False
    while not fin:
        #Control de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin=True
            if event.type == pygame.KEYDOWN:
                #Eventos con las teclas para movimientos y acciones del jugador
                if event.key == pygame.K_RIGHT:
                    jp.var_x=3.5
                    jp.var_y=0
                    jp.dir=6
                if event.key == pygame.K_LEFT:
                    jp.var_x=-3.5
                    jp.var_y=0
                    jp.dir=5
                if event.key == pygame.K_UP:
                    jp.var_y=-3.5
                    jp.var_x=0
                    jp.dir=7
                if event.key == pygame.K_DOWN:
                    jp.var_y=3.5
                    jp.var_x=0
                    jp.dir=4
                if event.key == pygame.K_SPACE:
                    jp.var_y=0
                    jp.var_x=0
                if event.key == pygame.K_c:
                    b=Bala('image.png')
                    b.rect.x=jp.rect.x+5
                    b.rect.y=jp.rect.y+10
                    b.dir=jp.dir
                    balas.add(b)
                    todos.add(b)
            if event.type == pygame.KEYUP:
                if event.key==pygame.K_c:
                    b.dir=0
                if event.key == pygame.K_RIGHT:
                    jp.var_x=0
                    jp.var_y=0
                    jp.dir=6
                if event.key == pygame.K_UP:
                    jp.var_y=0
                    jp.var_x=0
                    jp.dir=7
                if event.key == pygame.K_LEFT:
                    jp.var_x=0
                    jp.var_y=0
                    jp.dir=5
                if event.key == pygame.K_DOWN:
                    jp.var_y=0
                    jp.var_x=0
                    jp.dir=4

        #Choques entre el jugador y el enemigo
        ls_choque=pygame.sprite.spritecollide(jp,enemigos, True)
        for elemento in ls_choque:
            print 'Golpe'
        #Choques entre balas del jugador y el enemigo con 3 balas mata
        for bl in balas:
            ls_impac=pygame.sprite.spritecollide(bl,enemigos,False)
            for im in ls_impac:
                balas.remove(bl)
                todos.remove(bl)
                im.vida-=1
                if im.vida==0:
                    ls_impac=pygame.sprite.spritecollide(bl,enemigos,True)
        #Para ir borrando los enemigos que salen de la pantalla
        for enemigo in enemigos:
            if en.rect.x < -50:
                enemigos.remove(en)
        #Creacion de mas enemigos
        if conenemi==0:
            en1=Enemigo(animal[0][1])
            en1.rect.x=random.randrange(ANCHO)
            en1.rect.y=random.randrange(ALTO)
            en1.var_x=(-1)*random.randrange(1,10)
            en1.var_y=0#random.randrange(3,10)
            enemigos.add(en1)
            todos.add(en1)
            conenemi=50
        else:
            conenemi-=1
        #Dibujar mapa
        vary=0
        for fila in mapa:
            varx=0
            for col in fila:
                px=int(interprete.get(col,"x"))
                py=int(interprete.get(col,"y"))
                pantalla.blit(fondo[px][py],(varx,vary))
                varx+=an
                if col=="#":
                    #for b in range(640):
                    b=Bloque(fondo[px][py])
                    b.rect.x=varx
                    b.rect.y=vary
                    todos.add(b)
                    bloques.add(b)
                jp.bloques=bloques
                    #print "calor"
                #print col
                #print type (fondo[px][py])
                #print varx
                #print vary
            vary+=al
        #en.image=animal[0+en.con][en.dir]
        jp.image=animal[3+jp.con][jp.dir]
        #Limitar el jugador con la pantalla 4 direcciones
        if jp.rect.x>ANCHO-jp.rect.width:
            jp.rect.x=ANCHO-jp.rect.width
            jp.var_x=0
        if jp.rect.x<0:
            jp.rect.x=0
            jp.var_x=0
        if jp.rect.y>ALTO-jp.rect.height:
            jp.rect.y=ALTO-jp.rect.height
            jp.var_y=0
        if jp.rect.y<0:
            jp.rect.y=0
            jp.var_y=0

        #pantalla.fill(BLANCO)
        todos.update() # Con este update refresca todos los incluidos en el grupo todos.
        todos.draw(pantalla)
        pygame.display.flip()
        reloj.tick(20)
