#!/bin/python3

#############
# 代码世界 #
#############

#---
＃游戏功能
#---

＃将玩家向左移动1个图块。
def moveLeft():
  global playerX
  if(drawing == False and playerX > 0):
    oldX = playerX
    playerX -= 1
    drawResource(oldX, playerY)
    drawResource(playerX, playerY)
    
＃将玩家向右移动1个图块。
def moveRight():
  global playerX, MAPWIDTH
  if(drawing == False and playerX < MAPWIDTH - 1):
    oldX = playerX
    playerX += 1
    drawResource(oldX, playerY)
    drawResource(playerX, playerY)
    
＃将玩家向上移动1个图块。
def moveUp():
  global playerY
  if(drawing == False and playerY > 0):
    oldY = playerY
    playerY -= 1
    drawResource(playerX, oldY)
    drawResource(playerX, playerY)
    
＃将玩家向下移动1个图块。
def moveDown():
  global playerY, MAPHEIGHT
  if(drawing == False and playerY < MAPHEIGHT - 1):
    oldY = playerY
    playerY += 1
    drawResource(playerX, oldY)
    drawResource(playerX, playerY)
    
＃在玩家的位置捡起资源。
def pickUp():
  global playerX, playerY
  drawing = True
  currentTile = world[playerX][playerY]
  ＃如果用户还没有太多...
  if inventory[currentTile] < MAXTILES:
    #player现在有1个此资源
    inventory[currentTile] += 1
    ＃玩家现在站在泥土上
    world[playerX][playerY] = DIRT
    ＃绘制新的DIRT图块
    drawResource(playerX, playerY)
    #用额外资源重新绘制。
    drawInventory()
    #drawPlayer()

＃将资源放置在玩家的当前位置
def place(resource):
  print('placing: ', names[resource])
  ＃仅在玩家有剩余时才放置...
  if inventory[resource] > 0:
    ＃找到玩家当前位置的资源
    currentTile = world[playerX][playerY]
    ＃在玩家的位置捡起资源。
    #(if it's not DIRT)
    if currentTile is not DIRT:
      inventory[currentTile] += 1
    ＃将资源放置在玩家的当前位置
    world[playerX][playerY] = resource
    ＃将新资源添加到库存
    inventory[resource] -= 1
    ＃更新显示（世界和库存）
    drawResource(playerX, playerY)
    drawInventory()
    #drawPlayer()
    print('   放置', names[resource], '完成')
  #...如果没有剩余...
  else:
    print('   您没有', names[resource], '剩余')

#制作一个新的资源
def craft(resource):
  print('构建中: ', names[resource])
  ＃如果可以制作资源...
  if resource in crafting:
    #保持跟踪我们是否有资源
    #制作这个物品
    canBeMade = True
    ＃针对制作资源所需的每个项目
    for i in crafting[resource]:
      ＃...如果我们没有足够的...
      if crafting[resource][i] > inventory[i]:
      ＃...我们做不到！
        canBeMade = False
        break
    ＃如果我们能制作出来的话（我们拥有所有需要的资源）
    if canBeMade == True:
      ＃从库存中取出每个物品
      for i in crafting[resource]:
        inventory[i] -= crafting[resource][i]
      ＃将制作的物品添加到库存中
      inventory[resource] += 1
      print('   正在构建', names[resource], '完成')
    ＃...否则将无法制作资源...
    else:
      print('   不能构建', names[resource])
    ＃更新显示的库存
    drawInventory()

#创建一个用于放置每个资源的函数
def makeplace(resource):
  return lambda: place(resource)

#附加一个“放置”函数到每个键按下
def bindPlacingKeys():
  for k in placekeys:
    screen.onkey(makeplace(k), placekeys[k])

＃创建用于制作每个资源的函数
def makecraft(resource):
  return lambda: craft(resource)

＃为每个按键附加一个“制作”功能
def bindCraftingKeys():
  for k in craftkeys:
    screen.onkey(makecraft(k), craftkeys[k])

＃在（y，x）位置绘制资源
def drawResource(y, x):
  #this variable stops other stuff being drawn
  global drawing
  #only draw if nothing else is being drawn
  if drawing == False:
    #something is now being drawn
    drawing = True
    #draw the resource at that position in the tilemap, using the correct image
    rendererT.goto( (y * TILESIZE) + 20, height - (x * TILESIZE) - 20 )
    #draw tile with correct texture
    texture = textures[world[y][x]]
    rendererT.shape(texture)
    rendererT.stamp()
    if playerX == y and playerY == x:
      rendererT.shape(playerImg)
      rendererT.stamp()
    screen.update()
    #nothing is now being drawn
    drawing = False
    
#draws the world map
def drawWorld():
  #loop through each row
  for row in range(MAPHEIGHT):
    #loop through each column in the row
    for column in range(MAPWIDTH):
      #draw the tile at the current position
      drawResource(column, row)

#draws the inventory to the screen
def drawInventory():
  #this variable stops other stuff being drawn
  global drawing
  #only draw if nothing else is being drawn
  if drawing == False:
    #something is now being drawn
    drawing = True
    #use a rectangle to cover the current inventory
    rendererT.color(BACKGROUNDCOLOUR)
    rendererT.goto(0,0)
    rendererT.begin_fill()
    #rendererT.setheading(0)
    for i in range(2):
      rendererT.forward(inventory_height - 60)
      rendererT.right(90)
      rendererT.forward(width)
      rendererT.right(90)
    rendererT.end_fill()
    rendererT.color('black')
    #display the 'place' and 'craft' text
    for i in range(1,num_rows+1):
      rendererT.goto(20, (height - (MAPHEIGHT * TILESIZE)) - 20 - (i * 100))
      rendererT.write("place")
      rendererT.goto(20, (height - (MAPHEIGHT * TILESIZE)) - 40 - (i * 100))
      rendererT.write("craft")
    #set the inventory position
    xPosition = 70
    yPostition = height - (MAPHEIGHT * TILESIZE) - 80
    itemNum = 0
    for i, item in enumerate(resources):
      #add the image
      rendererT.goto(xPosition, yPostition)
      rendererT.shape(textures[item])
      rendererT.stamp()
      #add the number in the inventory
      rendererT.goto(xPosition, yPostition - TILESIZE)
      rendererT.write(inventory[item])
      #add key to place
      rendererT.goto(xPosition, yPostition - TILESIZE - 20)
      rendererT.write(placekeys[item])
      #add key to craft
      if crafting.get(item) != None:
        rendererT.goto(xPosition, yPostition - TILESIZE - 40)
        rendererT.write(craftkeys[item])     
      #move along to place the next inventory item
      xPosition += 50
      itemNum += 1
      #drop down to the next row every 10 items
      if itemNum % INVWIDTH == 0:
        xPosition = 70
        itemNum = 0
        yPostition -= TILESIZE + 80
    drawing = False

#generate the instructions, including crafting rules
def generateInstructions():
  instructions.append('Crafting rules:')
  #for each resource that can be crafted...
  for rule in crafting:
    #create the crafting rule text
    craftrule = names[rule] + ' = '
    for resource, number in crafting[rule].items():
      craftrule += str(number) + ' ' + names[resource] + ' '
    #add the crafting rule to the instructions
    instructions.append(craftrule)
  #display the instructions
  yPos = height - 20
  for item in instructions:
    rendererT.goto( MAPWIDTH*TILESIZE + 40, yPos)
    rendererT.write(item)
    yPos-=20

#generate a random world
def generateRandomWorld():
  #loop through each row
  for row in range(MAPHEIGHT):
    #loop through each column in that row
    for column in range(MAPWIDTH):
      #pick a random number between 0 and 10
      randomNumber = random.randint(0,10)
      #WATER if the random number is a 1 or a 2
      if randomNumber in [1,2]:
        tile = WATER
      #GRASS if the random number is a 3 or a 4
      elif randomNumber in [3,4]:
        tile = GRASS
      #otherwise it's DIRT
      else:
        tile = DIRT
      #set the position in the tilemap to the randomly chosen tile
      world[column][row] = tile

#---
#Code starts running here
#---

#import the modules and variables needed
import turtle
import random
from variables import *
from math import ceil

TILESIZE = 20
#the number of inventory resources per row
INVWIDTH = 8
drawing = False

#create a new 'screen' object
screen = turtle.Screen()
#calculate the width and height
width = (TILESIZE * MAPWIDTH) + max(200,INVWIDTH * 50)
num_rows = int(ceil((len(resources) / INVWIDTH)))
inventory_height =  num_rows * 120 + 40
height = (TILESIZE * MAPHEIGHT) + inventory_height

screen.setup(width, height)
screen.setworldcoordinates(0,0,width,height)
screen.bgcolor(BACKGROUNDCOLOUR)
screen.listen()

#register the player image  
screen.register_shape(playerImg)
#register each of the resource images
for texture in textures.values():
  screen.register_shape(texture)

#create another turtle to do the graphics drawing
rendererT = turtle.Turtle()
rendererT.hideturtle()
rendererT.penup()
rendererT.speed(0)
rendererT.setheading(90)

#create a world of random resources.
world = [ [DIRT for w in range(MAPHEIGHT)] for h in range(MAPWIDTH) ]

#map the keys for moving and picking up to the correct functions.
screen.onkey(moveUp, 'w')
screen.onkey(moveDown, 's')
screen.onkey(moveLeft, 'a')
screen.onkey(moveRight, 'd')
screen.onkey(pickUp, 'space')

#set up the keys for placing and crafting each resource
bindPlacingKeys()
bindCraftingKeys()

#these functions are defined above
generateRandomWorld()
drawWorld()
drawInventory()
generateInstructions()


