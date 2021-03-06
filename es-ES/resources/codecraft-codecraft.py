#!/bin/python3

#############
# CodeCraft #
#############

#---
#Funciones del juego
#---

#mueve el jugador 1 ficha a la izquierda.
def moveLeft():
  global jugadorX
  if (jugadorX> 0):
    jugadorX -= 1
    drawPlayer()

#mueve el jugador 1 ficha a la derecha.
def moveRight():
  global jugadorX, ANCHURAMAPA
  if(jugadorX < ANCHURAMAPA - 1):
    jugadorX += 1
    drawPlayer()

#mueve el jugador 1 ficha hacia arriba.
def moveUp():
  global jugadorY
  if (jugadorY> 0):
    jugadorY -= 1
    drawPlayer()

#mueve el jugador 1 ficha hacia abajo.
def moveDown():
  global jugadorY, ALTURAMAPA
  if(jugadorY < ALTURAMAPA - 1):
    jugadorY += 1
    drawPlayer()

#recoge el recurso en la posición del jugador.
def pickUp():
  global jugadorX, jugadorY
  dibujando = True
  casillaActual = mundo[jugadorX][jugadorY]
  #si el usuario no tiene todavía demasiado...
  if inventario[casillaActual] < MAXCASILLAS:
    #ahora el jugador tiene 1 más de este recurso
    inventario[casillaActual] += 1
    #el jugador ahora está de pie en la tierra
    mundo[jugadorX][jugadorY] = TIERRA
    #dibuja la nueva ficha de TIERRA
    drawResource(jugadorX, jugadorY)
    #dibuja de nuevo el inventario con el nuevo recurso.
    drawInventory()

#pon un recurso en la posición actual del jugador
def place(recurso):
  print('posición: ', nombres[recurso])
  #solo ponlo si al jugador todavía le quedan recursos...
  if inventario[recurso] > 0:
    #identifica el recurso en la posición actual del jugador
    casillaActual = mundo[jugadorX][jugadorY]
    #recoge el recurso en el que el jugador está de pie
    #(si no es TIERRA)
    if casillaActual is not TIERRA:
      inventario[casillaActual] += 1
    #pon el recurso en la posición actual del jugador
    mundo[jugadorX][jugadorY] = recurso
    #añade un nuevo recurso al inventario
    inventario[recurso] -= 1
    #actualiza lo que se muestra (el mundo y el inventario)
    drawResource(jugadorX, jugadorY)
    drawInventory()
    print('   Posición', nombres[recurso], 'terminada')
  #...y si no le queda nada...
  else:
    print('   No te queda nada de', nombres[recurso])

#crea un nuevo recurso
def craft(recurso):
  print('Creación: ', nombres[recurso])
  #si se puede crear el recurso...
  if recurso in crafting:
    #mantiene un registro de si tenemos los recursos
    #para crear este objeto
    puedeHacerse = True
    #para cada artículo que se necesita para crear el recurso
    for i in crafting[recurso]:
      #...si no tenemos bastante...
      if crafting[recurso][i] > inventario[i]:
      #...¡no podemos crearlo!
        puedeHacerse = True
        break
    #si podemos crearlo (tenemos todos los recursos que se necesita)
    if puedeHacerse == True:
      #toma cada artículo del inventario
      for i in crafting[recurso]:
        inventario[i] -= crafting[recurso][i]
      #añade el artículo creado al inventario
      inventario[recurso] += 1
      print('   Creación', nombres[recurso], 'terminada')
    #...si no, no se puede crear el recurso...
    else:
      print('   No se puede crear', nombres[recurso])
    #actualiza el inventario mostrado
    drawInventory()

#crea una función para poner cada recurso
def makeplace(recurso):
  return lambda: place(recurso)

#da la función de 'poner' a cada tecla que pulsemos
def bindPlacingKeys():
  for k in teclasParaColocar:
    pantalla.onkey(makeplace(k), teclasParaColocar[k])

#crear una función para crear cada recurso
def makecraft(recurso):
  return lambda: craft(recurso)

#da la función de 'crear' a cada tecla que pulsemos
def bindCraftingKeys():
  for k in teclasParaCrear:
    pantalla.onkey(makecraft(k), teclasParaCrear[k])

#dibuja un recurso en la posición (y,x)
def drawResource(y, x):
  #esta variable evita que se dibujen otras cosas
  global dibujando
  #sólo dibuja si nada más se está dibujando
  if dibujando == False:
    #ahora se está dibujando algo
    dibujando = True
    #dibuja el recurso en esta posición en el mapa cuadriculado, usando la imagen correcta
    renderizadorT.goto( (y * TAMANYOCASILLA) + 20, altura - (x * TAMANYOCASILLA) - 20 )
    #dibuja una ficha con la textura correcta
    textura = texturas[mundo[y][x]]
    renderizadorT.shape(textura)
    renderizadorT.stamp()
    pantalla.update()
    #ahora nada se está dibujando
    dibujando = False

#dibuja al jugador encima del mundo
def drawPlayer():
  jugadorT.goto( (playerX * TAMANYOCASILLA) + 20, altura - (playerY * TAMANYOCASILLA) -20 )

#dibuja el mapa del mundo
def drawWorld():
  #da una vuelta a través de cada fila
  for fila in range(ALTURAMAPA):
    #da una vuelta a través de cada columna en esa fila
    for columna in range(ANCHURAMAPA):
      #dibuja la ficha en la posición actual
      drawResource(columna, fila)

#dibuja el inventario en la pantalla
def drawInventory():
  #esta variable evita que se dibujen otras cosas
  global dibujando
  #sólo dibuja si nada más se está dibujando
  if dibujando == False:
    #ahora se está dibujando algo
    dibujando = True
    #usa un rectángulo para cubrir el inventario actual
    renderizadorT.color(COLORDELFONDO)
    renderizadorT.goto(0,0)
    renderizadorT.begin_fill()
    #renderizadorT.setheading(0)
    for i in range(2):
      rendererizadorT.forward(altura_inventario - 60)
      renderizadorT.right(90)
      renderizadorT.forward(anchura)
      renderizadorT.right(90)
    renderizadorT.end_fill()
    renderizadorT.color('')
    #muestra el texto 'poner' y 'crear'
    for i in range(1,num_filas+1):
      renderizadorT.goto(20, (altura - (ALTURAMAPA * TAMANYOCASILLA)) - 20 - (i * 100))
      renderizadorT.write("poner")
      renderizadorT.goto(20, (altura - (ALTURAMAPA* TAMANYOCASILLA)) - 40 - (i * 100))
      rendererizadorT.write("crear")
    #determina la posición del inventario
    posicionX = 70
    posicionY = altura - (ALTURAMAPA * TAMANYOCASILLA) - 80
    numObjeto = 0
    for i, item in enumerate(recursos):
      #añade la imagen
      renderizadorT.goto(posicionX, posicionY)
      renderizadorT.shape(texturas[objeto])
      renderizadorT.stamp()
      #añade el número en el inventario
      renderizadorT.goto(posicionX, posicionY - TAMANYOCASILLA)
      renderizadorT.write(inventario[objeto])
      #añade la tecla para poner
      renderizadorT.goto(posicionX, posicionY - TAMANYOCASILLA - 20)
      renderizadorT.write(teclasParaColocar[objeto])
      #añade la tecla para crear
      if crafting.get(objeto) != None:
        renderizadorT.goto(posicionX, posicionY - TAMANYOCASILLA - 40)
        renderizadorT.write(teclasParaCrear[objeto])     
      #avanza para poner el próximo artículo del inventario
      posicionX += 50
      numObjeto += 1
      #baja a la próxima fila cada 10 artículos
      if numObjeto % ANCHURAINVENTARIO == 0:
        posicionX = 70
        numObjeto = 0
        posicionY -= TAMANYOCASILLA + 80
    dibujando = False

#genera las instrucciones, incluyendo las reglas para crear
def generateInstructions():
  instrucciones.append('Reglas para crear:')
  #para cada recurso que se puede crear...
  for regla in crafting:
    #crear el texto de reglas para crear
    reglaParaCrear = nombres[regla] + ' = '
    for recurso, numero in crafting[regla].items():
      reglaParaCrear += str(numero) + ' ' + nombres[recurso] + ' '
    #añade las reglas para crear a las instrucciones
    instrucciones.append(reglaParaCrear)
  #muestra las instrucciones
  posY = altura - 20
  for objeto in instrucciones:
    renderizadorT.goto( ANCHURAMAPA*TAMANYOCASILLA + 40, posY)
    renderizadorT.write(objeto)
    posY-=20

#genera un mundo aleatorio
def generateRandomWorld():
  #da una vuelta a través de cada fila
  for fila in range(ALTURAMAPA):
    #da una vuelta a través de cada columna en esa fila
    for columna in range(ANCHURAMAPA):
      #elige un número aleatorio entre 0 y 10
      numeroAleatorio = random.randint(0,10)
      #AGUA si el número aleatorio es 1 o 2
      if numeroAleatorio in [1,2]:
        casilla = AGUA
      #CÉSPED si el número aleatorio es 3 o 4
      elif numeroAleatorio in [3,4]:
        casilla = CESPED
      #si no es TIERRA
      else:
        casilla = TIERRA
      #determina la posición en el mapa cuadriculado a la ficha aleatoria
      mundo[columna][fila] = casilla

#---
#Aquí empieza ejecutándose el código
#---

#importa los módulos y las variables que se necesitan
import turtle
import random
from variables import *
from math import ceil

TAMANYOCASILLA = 20
#el número de recursos de inventario por fila
ANCHURAINVENTARIO = 8
dibujando = False

#crea un objeto de 'pantalla' nuevo
pantalla = turtle.Screen()
#calcula el ancho y la altura
anchura = (TAMANYOCASILLA * ANCHURAMAPA) + max(200,ANCHURAINVENTARIO * 50)
num_filas = int(ceil((len(recursos) / ANCHURAINVENTARIO)))
altura_inventario =  num_filas * 120 + 40
altura = (TAMANYOCASILLA * ALTURAMAPA) + altura_inventario

pantalla.setup(anchura, altura)
pantalla.setworldcoordinates(0,0,anchura,altura)
pantalla.bgcolor(COLORDELFONDO)
pantalla.listen()

#registra la imagen del jugador  
pantalla.register_shape(imgJugador)
#registra cada imagen de recurso
for textura in texturas.values():
  pantalla.register_shape(textura)
  
#crea un objeto de jugador nuevo
jugadorT = turtle.Turtle()
jugadorT.hideturtle()
jugadorT.shape(imgJugador)
jugadorT.penup()
jugadorT.speed(0)

#crea otra tortuga para hacer el dibujo de gráficos
renderizadorT = turtle.Turtle()
renderizadorT.hideturtle()
renderizadorT.penup()
renderizadorT.speed(0)
renderizadorT.setheading(90)

#crea un mundo de recursos aleatorios.
mundo = [ [TIERRA for w in range(ALTURAMAPA)] for h in range(ANCHURAMAPA) ]

#vincula las teclas para mover y recoger a las funciones correctas.
pantalla.onkey(moveUp, 'w')
pantalla.onkey(moveDown, 's')
pantalla.onkey(moveLeft, 'a')
pantalla.onkey(moveRight, 'd')
pantalla.onkey(pickUp, 'espacio')

#establece las teclas para poner y crear cada recurso
bindPlacingKeys()
bindCraftingKeys()

#estas funciones se definen arriba
generateRandomWorld()
drawWorld()
drawInventory()
generateInstructions()
drawPlayer()
jugadorT.showturtle()


