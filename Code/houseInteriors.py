from gdpc import Block
import random

''' This file contains the methods used to decorate the interiors of the house'''

def firstFloorBigger(ED, floorHeight, centerX, centerZ, diameter, height, even, woodColour):
    # First floor in height goes from floorHeight to floorHeight+int(height/2)-1 included
    ceiling = floorHeight+int(height/2)

    ''' Place bed '''
    ED.placeBlock((centerX, floorHeight+1, centerZ-int(diameter/4)), Block("red_bed"))
    ED.placeBlock((centerX+1, floorHeight+1, centerZ-int(diameter/4)), Block("red_bed"))

    ''' Place bed tables '''
    ED.placeBlock((centerX-1, floorHeight+1, centerZ-int(diameter/4)-1), Block("dark_oak_planks"))
    if even == True:
        ED.placeBlock((centerX+2, floorHeight+1, centerZ-int(diameter/4)-1), Block("dark_oak_planks"))

    ''' Place candles on bedTables '''
    ED.placeBlock((centerX-1, floorHeight+2, centerZ-int(diameter/4)-1), Block("white_candle", {"candles":"3", "lit":"true"}))
    if even == True:
        ED.placeBlock((centerX+2, floorHeight+2, centerZ-int(diameter/4)-1), Block("white_candle", {"candles":"3", "lit":"true"}))

    for h in range(floorHeight+3, ceiling-1):
        if even == True:
            zCoord = centerZ-int(diameter/2)+1
        else:
            zCoord = centerZ-int(diameter/2)
        ED.placeBlock((centerX, h, zCoord), Block("glass_pane"))
        if even == True:
            ED.placeBlock((centerX+1, h, zCoord), Block("glass_pane"))


    ''' Desk '''
    ED.placeBlock((centerX+int(diameter/2)-1, floorHeight+1, centerZ), Block("oak_stairs", {"facing":"east", "half":"top"}))
    ED.placeBlock((centerX+int(diameter/2)-1, floorHeight+1, centerZ+1), Block("oak_stairs", {"facing":"east", "half":"top"}))
    ED.placeBlock((centerX+int(diameter/2)-2, floorHeight+1, centerZ), Block("oak_stairs", {"facing":"west"}))
    for h in range(floorHeight+1, floorHeight+5):
        ED.placeBlock((centerX+int(diameter/2)-1, h, centerZ-1), Block("bookshelf"))
    ED.placeBlock((centerX+int(diameter/2)-1, h, centerZ), Block("bookshelf"))
    ED.placeBlock((centerX+int(diameter/2)-1, h, centerZ+1), Block("bookshelf"))
    ED.placeBlock((centerX+int(diameter/2)-1, floorHeight+3, centerZ+1), Block("lantern", {"hanging":"true"}))

    ''' Add windows '''
    for h in range(floorHeight+3, ceiling-1):
        if even == True:
            xCoord = centerX-int(diameter/2)+1
        else:
            xCoord = centerX-int(diameter/2)
        ED.placeBlock((xCoord, h, centerZ), Block("glass_pane"))
        if even == True:
            ED.placeBlock((xCoord, h, centerZ+1), Block("glass_pane"))

    if diameter > 9:
        for z in range(centerZ, centerZ+3):
            ED.placeBlock((centerX-int(diameter/2)+2, floorHeight, z), woodColour)
    if even == True:
        ED.placeBlock((centerX-int(diameter/2)+2, floorHeight+1, centerZ+1), Block("chest", {"facing":"east", "type":"left"}))
    ED.placeBlock((centerX-int(diameter/2)+2, floorHeight+1, centerZ+2), Block("chest", {"facing":"east", "type":"right"}))


def groundFloorBigger(ED, centerX, centerZ, groundFloor, diameter, even, firstFloor):

    if diameter >= 9:
        ED.placeBlock((centerX, groundFloor, centerZ-int(diameter/2)+2), Block("campfire"))
        if even == True:
            ED.placeBlock((centerX+1, groundFloor, centerZ-int(diameter/2)+2), Block("campfire"))
    
        ''' Build fireplace '''
        endFirePlaceZ = centerZ-int(diameter/2)+4
        for z in range(centerZ-int(diameter/2)+2, centerZ-int(diameter/2)+4):
            ED.placeBlock((centerX-1, groundFloor, z), Block("stone_bricks"))
            if even == True:
                ED.placeBlock((centerX+2, groundFloor, z), Block("stone_bricks"))
            else:
                ED.placeBlock((centerX+1, groundFloor, z), Block("stone_bricks"))
            ED.placeBlock((centerX-1, groundFloor+1, z), Block("stone_brick_stairs", {"facing": "east"}))
            if even == True:
                ED.placeBlock((centerX+2, groundFloor+1, z), Block("stone_brick_stairs", {"facing": "west"}))
            else:
                ED.placeBlock((centerX+1, groundFloor+1, z), Block("stone_brick_stairs", {"facing": "west"}))
            ED.placeBlock((centerX, groundFloor+2, z), Block("stone_brick_slab"))
            if even == True:
                ED.placeBlock((centerX+1, groundFloor+2, z), Block("stone_brick_slab"))
    
        ''' Build table '''
        if diameter > 9:
            for x in range(centerX, centerX+2):
                ED.placeBlock((x, groundFloor, endFirePlaceZ+1), Block("oak_fence"))
                ED.placeBlock((x, groundFloor+1, endFirePlaceZ+1), Block("oak_pressure_plate"))
                ED.placeBlock((x, groundFloor, endFirePlaceZ+2), Block("oak_fence"))
                ED.placeBlock((x, groundFloor+1, endFirePlaceZ+2), Block("oak_pressure_plate"))
            for z in range(endFirePlaceZ+1, endFirePlaceZ+3):
                ED.placeBlock((centerX-1, groundFloor, z), Block("oak_stairs", {"facing": "west"}))
                ED.placeBlock((centerX+2, groundFloor, z), Block("oak_stairs", {"facing": "east"}))
        else:
            ED.placeBlock((centerX, groundFloor, endFirePlaceZ+1), Block("oak_fence"))
            ED.placeBlock((centerX, groundFloor+1, endFirePlaceZ+1), Block("oak_pressure_plate"))
            ED.placeBlock((centerX-1, groundFloor, endFirePlaceZ+1), Block("oak_stairs", {"facing": "west"}))
    
def decorateSmallMushroom(ED, centerX, y, centerZ, diameter, even, centerX2, diameter2):
    entranceX = centerX+int(diameter/2)
    entranceZ = centerZ
    for h in range(y, y+2):
        for x in range(entranceX, entranceX+2):
            ED.placeBlock((x, h, entranceZ), Block("air"))
            if even == True:
                ED.placeBlock((x, h, entranceZ+1), Block("air"))

    for h in range(y+1, y+3):
        for z in range(centerZ-int(diameter2/4), centerZ+int(diameter2/2)):
            ED.placeBlock((centerX2+int(diameter2/2), h, z), Block("glass"))
        if diameter > 9:
            z = centerZ-int(diameter2/2)+1
        else:
            z = centerZ-int(diameter2/2)
        for x in range(centerX2-int(diameter2/4), centerX2+int(diameter2/2)):
            ED.placeBlock((x, h, z), Block("glass"))
        z = centerZ+int(diameter2/2)
        if diameter <= 9:
            startX = centerX2-int(diameter2/2)+1
        else:
            startX = centerX2-int(diameter2/2)+2
        for x in range(startX, centerX2+int(diameter2/2)):
            ED.placeBlock((x, h, z), Block("glass"))

    ''' Add plants '''
    for z in range(centerZ-int(diameter2/4), centerZ+int(diameter2/2)):
        ED.placeBlock((centerX2+int(diameter2/2)-1, y, z), Block("rose_bush"))
    if diameter <= 9:
        z = centerZ-int(diameter2/2)+1
    else:
        z = centerZ-int(diameter2/2)+2
    for x in range(centerX2-int(diameter2/4), centerX2+int(diameter2/2)-1):
        ED.placeBlock((x, y, z), Block("white_tulip"))
    z = centerZ+int(diameter2/2)-1
    if diameter <= 9:
        startX = centerX2-int(diameter2/2)+1
    else:
        startX = centerX2-int(diameter2/2)+2
    for x in range(startX, centerX2+int(diameter2/2)-1):
        ED.placeBlock((x, y, z), Block("white_tulip"))


                  
def groundFloorSmaller(ED, centerX, centerZ, groundFloor, diameter, even, firstFloor):
    if even == True:
        zCoord =  centerZ-int(diameter/2)+1
    else:
        zCoord =  centerZ-int(diameter/2)

    probability = random.random()

    ''' We have either candles on the south side, windows on the left and table on the left
        or windows on the south side, table on the south side, candles on the left side'''
    h = groundFloor
    if probability >= 0.5:
        slabCoord = (centerX, h, zCoord+1)
        candlesCoord = (centerX, h+1, zCoord+1)
        slabCoord2 = (centerX+1, h, zCoord+1)
        candlesCoord2 = (centerX+1, h+1, zCoord+1)
        tableLegCoord = (centerX+int(diameter/2)-1, h, centerZ+1)
        tablePlateCoord = (centerX+int(diameter/2)-1, h+1, centerZ+1)
        chairCoord = (centerX+int(diameter/2)-2, h, centerZ+1)
        windowCoord = (centerX+int(diameter/2), h+1, centerZ)
        window2Coord = (centerX+int(diameter/2), h+1, centerZ+1)
        stairs = Block("oak_stairs", {"facing": "west"})
    else:
        slabCoord = (centerX+int(diameter/2)-1, h, centerZ)
        candlesCoord = (centerX+int(diameter/2)-1, h+1, centerZ)
        slabCoord2 = (centerX+int(diameter/2)-1, h, centerZ+1)
        candlesCoord2 = (centerX+int(diameter/2)-1, h+1, centerZ+1)
        tableLegCoord = (centerX, h, zCoord+1)
        tablePlateCoord = (centerX, h+1, zCoord+1)
        chairCoord = (centerX, h, zCoord+2)
        windowCoord = (centerX, h+1, zCoord)
        window2Coord = (centerX+1, h+1, zCoord)
        stairs = Block("oak_stairs", {"facing": "south"})
    ED.placeBlock(slabCoord, Block("dark_oak_slab", {"type": "top"}))
    ED.placeBlock(candlesCoord, Block("white_candle", {"candles":"3", "lit":"true"}))
    if even == True:
            ED.placeBlock(slabCoord2, Block("dark_oak_slab", {"type": "top"}))
            ED.placeBlock(candlesCoord2, Block("white_candle", {"candles":"3", "lit":"true"}))
    
    # Place a table on the right
    ED.placeBlock(tableLegCoord, Block("oak_fence"))
    ED.placeBlock(tablePlateCoord, Block("oak_pressure_plate"))
    ED.placeBlock(chairCoord, stairs)
    if diameter == 8: # Add a bigger table if the house is bigger
        if probability < 0.5:
            ED.placeBlock((tableLegCoord[0]+1, tableLegCoord[1], tableLegCoord[2]), Block("oak_fence"))
            ED.placeBlock((tablePlateCoord[0]+1, tablePlateCoord[1], tablePlateCoord[2]), Block("oak_pressure_plate"))
            ED.placeBlock((chairCoord[0]+1, chairCoord[1], chairCoord[2]), stairs)
        else:
            ED.placeBlock((tableLegCoord[0], tableLegCoord[1], tableLegCoord[2]-1), Block("oak_fence"))
            ED.placeBlock((tablePlateCoord[0], tablePlateCoord[1], tablePlateCoord[2]-1), Block("oak_pressure_plate"))
            ED.placeBlock((chairCoord[0], chairCoord[1], chairCoord[2]-1), stairs)
    
    # Place windows on the right
    for h in range(groundFloor + 1, firstFloor-1):
        ED.placeBlock((windowCoord[0], h, windowCoord[2]), Block("glass_pane"))
        if even == True:
            ED.placeBlock((window2Coord[0], h, window2Coord[2]), Block("glass_pane"))

def addLight(ED, firstFloor, centerX, centerZ):
    ED.placeBlock((centerX, firstFloor-1, centerZ), Block("lantern", {"hanging":"true"}))


def firstFloorSmaller(ED, floorHeight, centerX, centerZ, height, diameter, even):
    if even == True and diameter == 6:
        ceiling = floorHeight+int(height/2)
    else:
        ceiling = floorHeight+int(height/2)-1

    ''' Either flowers on the right and windows on the left, or 
        flowers on the left and windows on the right '''
    probability = random.random()
    for h in range(floorHeight+2, ceiling-1):
        if even == True:
            ED.placeBlock((centerX, h, centerZ-int(diameter/2)+1), Block("glass_pane")) # Place windows at south
        else:
            ED.placeBlock((centerX, h, centerZ-int(diameter/2)), Block("glass_pane")) # Place windows at south
        if probability < 0.5:
            if even == True:
                ED.placeBlock((centerX-int(diameter/2)+1, h, centerZ), Block("glass_pane")) # Place windows on the left
            else:
                ED.placeBlock((centerX-int(diameter/2), h, centerZ), Block("glass_pane")) # Place windows on the left
        else:
            ED.placeBlock((centerX+int(diameter/2), h, centerZ), Block("glass_pane")) # Place windows on the right
        if even == True:
            ED.placeBlock((centerX+1, h, centerZ-int(diameter/2)+1), Block("glass_pane")) # Place windows at south
            if probability < 0.5:
                ED.placeBlock((centerX-int(diameter/2)+1, h, centerZ+1), Block("glass_pane")) # Place windows on the left
            else:
                ED.placeBlock((centerX+int(diameter/2), h, centerZ+1), Block("glass_pane")) # Place windows on the right
            
    ''' Place flowers'''
    if probability < 0.5:
        # Flowers on the right
        slab1Coord = (centerX+int(diameter/2)-1, floorHeight+2, centerZ+1); orchid1Coord = (centerX+int(diameter/2)-1, floorHeight+2, centerZ+1)
        slab2Coord = (centerX+int(diameter/2)-1, floorHeight+2, centerZ);  orchid2Coord = (centerX+int(diameter/2)-1, floorHeight+3, centerZ)
    else:
        if even == True:
            slab1Coord = (centerX-int(diameter/2)+2, floorHeight+2, centerZ+1); orchid1Coord = (centerX-int(diameter/2)+2, floorHeight+3, centerZ+1)
            slab2Coord = (centerX-int(diameter/2)+2, floorHeight+3, centerZ); orchid2Coord = (centerX-int(diameter/2)+2, floorHeight+4, centerZ)
        else:
            slab1Coord = (centerX-int(diameter/2)+1, floorHeight+2, centerZ+1); orchid1Coord = (centerX-int(diameter/2)+1, floorHeight+3, centerZ+1)
            slab2Coord = (centerX-int(diameter/2)+1, floorHeight+3, centerZ); orchid2Coord = (centerX-int(diameter/2)+1, floorHeight+4, centerZ)
    if probability >=0.5:
        ED.placeBlock(slab1Coord, Block("oak_slab", {"type":"top"}))
        ED.placeBlock(orchid1Coord, Block("potted_blue_orchid"))
        ED.placeBlock(slab2Coord, Block("oak_slab", {"type":"top"}))
        ED.placeBlock(orchid2Coord, Block("potted_blue_orchid"))
    else:
        ED.placeBlock(slab2Coord, Block("oak_slab", {"type":"top"}))
        ED.placeBlock(orchid2Coord, Block("potted_blue_orchid"))
    ''' Change bed colour'''
    bedProbability = random.random()
    if bedProbability < 0.5:
        bed = Block("red_bed")
    else:
        bed = Block("light_blue_bed")
    if even == True:
        ED.placeBlock((centerX+1, floorHeight+1, centerZ-int(diameter/2)+3), bed) # Left bed
        ED.placeBlock((centerX+2, floorHeight+1, centerZ-int(diameter/2)+3), bed) # Right bed
    else:
        ED.placeBlock((centerX, floorHeight+1, centerZ-int(diameter/2)+2), bed) # Left bed
        ED.placeBlock((centerX+1, floorHeight+1, centerZ-int(diameter/2)+2), bed) # Right bed
    
    ''' Place  chest'''
    ED.placeBlock((centerX-int(diameter/2)+2, floorHeight+1, centerZ+2), Block("chest", {"facing":"east"}))
    ''' Place bookshelf '''
    if even == True:
        ED.placeBlock((centerX-int(diameter/2)+diameter-1, floorHeight+1, centerZ+2), Block("bookshelf"))
    else:
        ED.placeBlock((centerX-int(diameter/2)+diameter-2, floorHeight+1, centerZ+1), Block("bookshelf"))
    ''' Place lantern '''
    if even == True:
        ED.placeBlock((centerX-int(diameter/2)+diameter-1, floorHeight+2, centerZ+2), Block("lantern"))
    else:
        ED.placeBlock((centerX-int(diameter/2)+diameter-2, floorHeight+2, centerZ+1), Block("lantern"))