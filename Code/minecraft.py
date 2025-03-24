import logging
from random import randint

from termcolor import colored

from gdpc import Block, Editor
from gdpc import geometry as geo
from find_location import getBestRegion
import random
from houseInteriors import firstFloorBigger, groundFloorBigger, groundFloorSmaller, decorateSmallMushroom, addLight, firstFloorSmaller


def main():
    # To visualize errors
    logging.basicConfig(format=colored("%(name)s - %(levelname)s - %(message)s", color="yellow"))

    # Construct the Editor object
    ED = Editor(buffering=True)
    try:
        # Here we read start and end coordinates of our build area
        BUILD_AREA = ED.getBuildArea()  # BUILDAREA
        # X-axis = west-east: increasing values = east, decreasing values = west
        # Y-axis = up or down: increasing values = higher, decreasing values = lower
        # Z-axi: north-south: increasing values = south, decreasing values = north
        STARTX, STARTY, STARTZ = BUILD_AREA.begin
        LASTX, LASTY, LASTZ = BUILD_AREA.last
        WORLDSLICE = ED.loadWorldSlice(BUILD_AREA.toRect(), cache=True)
        #heights = WORLDSLICE.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
        heights = WORLDSLICE.heightmaps["MOTION_BLOCKING"]


        # Find a good location for the house
        houseLocation= getBestRegion(ED, STARTX, STARTZ, LASTX, LASTZ, STARTY, LASTY, heights)
        if houseLocation == False:
            print("No area found")
            return 

        if houseLocation == -1:
            print("Too many buildings: could not find a place to build the house")
            
        else:
            print("Clearing region...")
            terrainBlock = clearRegion(ED, houseLocation, heights, STARTX, STARTZ)
            entranceGateCoord = buildPerimeter(ED, houseLocation)
            print("Building house...")
            buildHouse(ED, houseLocation, terrainBlock, entranceGateCoord)

            print("Done!")

    except KeyboardInterrupt:
        print("Pressed Ctrl-C to kill program.")



def clearRegion(ED, region, heights, STARTX, STARTZ):
    ((startX, startZ), (endX, endZ), avgHeight) = region
    avgHeight -= 1
    done = 0
    for x in range(startX, endX+1):
        for z in range(startZ, endZ+1):
            cornerX = x-STARTX
            cornerZ = z - STARTZ
            block = ED.getBlock((x, heights[cornerX][cornerZ]-1, z)) 
            block_string = str(block)
            block_name = block_string.split("[")[0]
            if block != Block("minecraft:air") and done == 0:
                if "leaves" not in block_name:
                    terrainBlock = block # get name of terrain block used in the area
                    done = 1
            if heights[cornerX][cornerZ] > avgHeight:
                # Remove blocks at position (x, z) from height avgHeight + 1 to heights[x][z]
                for h in range(avgHeight+1, heights[cornerX][cornerZ]+1):
                    ED.placeBlock((x, h, z), Block("air"))

    # Add blocks in order to flatten the area
    for x in range(startX, endX+1):
        for z in range(startZ, endZ+1):
            h = avgHeight
            while ED.getBlock((x, h, z)) == Block("minecraft:air"):
                ED.placeBlock((x, h, z), terrainBlock)
                h -= 1
            # On last layer add grass_block because it will be the garden of the house
            ED.placeBlock((x, avgHeight, z), Block("grass_block"))
    print("Terrain block type: ", terrainBlock)
    return terrainBlock


def buildPerimeter(ED, houseLocation):
    ((startX, startZ), (lastX, lastZ), y) = houseLocation
    for x in range(startX, lastX + 1):
        geo.placeCuboid(ED, (x, y, startZ), (x, y, startZ), Block("spruce_fence"))
        geo.placeCuboid(ED, (x, y, lastZ), (x, y, lastZ), Block("spruce_fence"))
        if x == startX + int((lastX-startX)/3+1):
            ED.placeBlock((x, y, lastZ), Block("spruce_fence_gate"))

    for z in range(startZ, lastZ + 1):
        geo.placeCuboid(ED, (startX, y, z), (startX, y, z), Block("spruce_fence"))
        geo.placeCuboid(ED, (lastX, y, z), (lastX, y, z), Block("spruce_fence"))
    entranceGateCoord = (startX + int((lastX-startX)/3+1), y, lastZ)
    return entranceGateCoord
    
def buildHouse(ED, houseLocation, terrainBlock, entranceGateCoord):
    (startX, startZ), (lastX, lastZ), y = houseLocation
    # Calculate the center within the perimeter
    centerX = startX + (lastX - startX) // 2
    centerZ = startZ + (lastZ - startZ) // 2
    y+=1
 
    ''' Two main houses types:
        1. House with diamater smaller than 9, high, without smaller mushroom 
        2. House with diameter > 9, less high, with smaller mushroom '''

    diameter = random.randint(6, 10)
    centerX = centerX-3
    centerZ = centerZ-3
    print("Diameter house = ", diameter)
    if diameter % 2 == 0:
        even = True
    else:
        even = False
    probabilityMushroomColour = random.random()
    if probabilityMushroomColour < 0.5 :
        mushroomColour = Block("mushroom_stem")
        woodColour = Block("dark_oak_planks")
        fenceColour = Block("dark_oak_fence")
        slabColour = Block("dark_oak_slab")
    else:
        mushroomColour = Block("brown_mushroom_block")
        woodColour = Block("oak_planks")
        fenceColour = Block("oak_fence")
        slabColour = Block("oak_slab")
    mushroomType = 'default'

    if diameter >= 9 and diameter <=13:
        height = int(3/2 * diameter)
        ''' Build smaller mushroom '''# 5, 6 
        diameter2 = int(5/8*diameter)
        height2 = int(6/5*diameter2)
        centerX2 = centerX + diameter2 + 2
        centerY = y
        buildMushroom(ED, centerX2, centerY, centerZ, diameter2, height2, mushroomType, mushroomColour)
        buildPlatform(ED, centerX2, centerZ, centerY, diameter2, even, True, woodColour, terrainBlock)
    elif diameter >= 14:
        mushroomType = 'big'
        height = int(diameter/2)
    else:
        height = int(7/4 * diameter)

    ''' Build bigger mushroom '''
    buildMushroom(ED, centerX, y, centerZ, diameter, height, mushroomType, mushroomColour)

    ''' Building upper floor '''
    floorHeight = y + int(height/4+1)
    buildFloor(ED, centerX, floorHeight, y, diameter, centerZ, even, woodColour)
    ''' Building ground floor '''
    buildPlatform(ED, centerX, centerZ, y, diameter, even, False, woodColour, terrainBlock)

    ''' Windows on left side'''
    # Ground floor
    leftGroundWindowCorners = addSideWindows(ED, y+1, y+3, centerX-int(diameter/2)+1, centerZ, even)

    ''' Build main entrance '''
    buildEntrance(ED, centerX, y, centerZ, diameter, even, woodColour, slabColour)

    ''' Build patio '''
    heightBalcony = buildPatio(ED, centerX, centerZ, y, diameter, mushroomType, even, height, leftGroundWindowCorners, woodColour, fenceColour, terrainBlock)
    startPatio = centerZ+int(diameter/2+1)
    endPatio = startPatio+3
    stairsCoord = (centerX, y-1, endPatio+1)

    ''' Add path into the garden '''
    addPath(ED, houseLocation, entranceGateCoord, stairsCoord, even)

    ''' Build entrance at upper balcony '''
    buildEntrance(ED, centerX, heightBalcony+1, centerZ, diameter, even, woodColour, slabColour)

    # Place ladder to reach upper floor
    for h in range(y, y + int(height/2.5)):
        if even == True:
            ED.placeBlock((centerX - int(diameter/2)+2, h, centerZ-1), Block("ladder", {"facing":"east"}))
        else:
            ED.placeBlock((centerX - int(diameter/2)+1, h, centerZ-1), Block("ladder", {"facing":"east"}))
    
    if diameter >= 9 and diameter <= 13:
        decorateSmallMushroom(ED, centerX, y, centerZ, diameter, even, centerX2, diameter2)
        # Remove blocks of the small mushroom roof that are inside the house 
        removeSmallMushroomInside(ED, floorHeight, height, y, centerX, centerZ, diameter, probabilityMushroomColour)
    
    addLight(ED, floorHeight, centerX, centerZ)
    
    if even == True:
        ED.placeBlock((centerX+1, y, centerZ + diameter/2 +1), Block("dark_oak_door", {"facing": "south"}))
        # Left door
        ED.placeBlock((centerX, y, centerZ + diameter/2+1), Block("dark_oak_door", {"facing": "south", "hinge": "right"}))


    ''' Decorate house '''
    if diameter >= 9:
        firstFloorBigger(ED, floorHeight, centerX, centerZ, diameter, height, even, woodColour)
        groundFloorBigger(ED, centerX, centerZ, y, diameter, even, floorHeight)
    else:
        groundFloorSmaller(ED, centerX, centerZ, y, diameter, even, floorHeight)
        firstFloorSmaller(ED, floorHeight, centerX, centerZ, height, diameter, even)

    ''' Decorate garden '''
    decorateGarden(ED, houseLocation, centerZ, diameter, even, woodColour, fenceColour, slabColour)

def buildMushroom(ED, centerX, y, centerZ, diameter, height, mushroomType, mushroomColour):
    # Build the cylinder at the calculated center
    geo.placeCylinder(ED, (centerX, y, centerZ), int(diameter), height, mushroomColour, tube=True)
    if mushroomType == 'big':
        heightRoof = int(height*3/2)
        center = (centerX, y+heightRoof, centerZ)
    else:
        heightRoof = int((height / 3) * 2)
        center = (centerX, y+height, centerZ)
    sideRoof = int(diameter*1.85)

    diameters = (sideRoof, heightRoof, sideRoof)  # Diameters along x, y, z axes
    block = Block("red_mushroom_block")  # Block type for the ellipsoid
    hollow = True  # Whether the ellipsoid should be hollow
    replace = None  # Blocks to replace, if any
    geo.placeEllipsoid(ED, center, diameters, block, hollow, replace)

def buildPlatform(ED, centerX, centerZ, y, diameter, even, smallMushroom, woodColour, terrainBlock):
    ''' Build stone platform '''
    if smallMushroom == False:
        blockToPlace = Block("stone_bricks")
    else:
        blockToPlace = Block("moss_block")
    if even == True:
        startX = centerX - int(diameter/2)+1
    else:
        startX = centerX - int(diameter/2)
    endX = centerX + int(diameter/2+1)
    for x in range(startX, endX):
        for z in range(centerZ-int(diameter/2)+1, centerZ+int(diameter/2+1)):
            block = ED.getBlock((x, y-1, z))
            target = woodColour
            if block != target:
                ED.placeBlock((x, y-1, z), blockToPlace)
            if even == False:
                ED.placeBlock((centerX - int(diameter/2), y-1, z), blockToPlace)
                ED.placeBlock((x, y-1, centerZ-int(diameter/2)), blockToPlace)

    for z in range(centerZ-int(diameter/2)+1, centerZ+int(diameter/2+1)):
        x = startX
        ED.placeBlock((x, y-1, z), Block(blockToPlace))
        
def buildPatio(ED, centerX, centerZ, y, diameter, mushroomType, even, height, leftGroundWindowCorners, woodColour, fenceColour, terrainBlock):
    windowX,windowY, windowZ = leftGroundWindowCorners
    if even == True:
        startX = centerX - int(diameter/2)+1
    else:
        startX = centerX - int(diameter/2)
    startZ = centerZ-int(diameter/2)
    endZ = centerZ+int(diameter/2)
    endX = centerX + int(diameter/2+1)
    for x in range(startX, endX):
        for z in range(startZ, endZ+1):
            if x == startX or x == endX-1:
                if even == True:
                    limit = windowZ+2
                else:
                    limit = windowZ+1
                if z > limit:
                    ED.placeBlock((x, y, z), fenceColour)
        
        if mushroomType != "big":
            startPatio = centerZ+int(diameter/2+1)
            endPatio = startPatio+3
            for z in range(startPatio, endPatio+1):
                ED.placeBlock((x, y-1, z), Block("stone_bricks"))
                h = y-2
                while ED.getBlock((x, h, z)) == Block("minecraft:air"):
                    ED.placeBlock((x, h, z), terrainBlock)
                    h -= 1
                if z == endPatio:
                    ED.placeBlock((x, y, z), fenceColour)
                if x == startX or x == endX-1: 
                    ED.placeBlock((x, y, z), fenceColour)

    #Remove central fence for entrance
    ED.placeBlock((centerX, y, endPatio), Block("air"))
    if even == True:
        ED.placeBlock((centerX+1, y, endPatio), Block("air"))
    # Add central stairs            
    ED.placeBlock((centerX, y-1, endPatio+1), Block("stone_brick_stairs"))
    h = y-2
    while ED.getBlock((x, h, z)) == Block("minecraft:air"):
        ED.placeBlock((x, h, z), terrainBlock)
        h -= 1
    if even == True:
        ED.placeBlock((centerX+1, y-1, endPatio+1), Block("stone_brick_stairs"))
        h = y-2
        while ED.getBlock((x, h, z)) == Block("minecraft:air"):
            ED.placeBlock((x, h, z), terrainBlock)
            h -= 1
    
    ''' For the balcony '''
    # Add 4 pillars
    for h in range(y+1, y+1+int(height/4)):
        if even == True:
            limit = windowZ+3
        else:
            limit = windowZ+2
        ED.placeBlock((startX, h, limit), fenceColour)
    for h in range(y+1, y+1+int(height/4)):
        ED.placeBlock((endX-1, h, limit), fenceColour)
    for h in range(y+1, y+1+int(height/4)):
        ED.placeBlock((startX, h, endPatio), fenceColour)
    for h in range(y+1, y+1+int(height/4)):
        ED.placeBlock((endX-1, h,endPatio), fenceColour)
    
    # Build balcony floor
    if diameter != 6:
        endZ -= 1
    if diameter >=9:
        endZ -= 1
    for x in range(startX, endX):
        for z in range(endZ, endPatio+1):
            if ED.getBlock((x, h+1, z)) == Block('minecraft:air'):
                ED.placeBlock((x, h+1, z), woodColour)

    # Add fence to balcony
    for x in range(startX, endX):
        for z in range(startPatio, endPatio):
            if x == startX or x == endX-1:
                ED.placeBlock((x, h+2, z), fenceColour)  
        ED.placeBlock((x, h+2, z+1), fenceColour)
    
    if even == True:
        limit = windowZ+3
    else:
        limit = windowZ+2
    for z in range(limit, startPatio):
        ED.placeBlock((startX, h+2, z), fenceColour)  
        ED.placeBlock((endX-1, h+2, z), fenceColour)  

    return h+1

def addPath(ED, perimeter, entranceGateCoord, stairsCoord, even):
    (startX, startZ), (endX, endZ), y = perimeter
    for z in range(stairsCoord[2]+1, entranceGateCoord[2]):
        ED.placeBlock((stairsCoord[0], stairsCoord[1]-1, z), Block("dirt_path"))
        if even == True:
            ED.placeBlock((stairsCoord[0]+1, stairsCoord[1]-1, z), Block("dirt_path"))
    # Path on the front of the house
    for x in range(startX+2, endX-1):
        ED.placeBlock((x, y-1, entranceGateCoord[2]-2), Block("dirt_path"))
    
    # Path on the left side of the house
    for z in range(startZ+2, entranceGateCoord[2]-1):
        ED.placeBlock((startX+2, y-1, z), Block("dirt_path"))
    
    # Path at the back of the house
    for x in range(startX+2, endX-1):
        ED.placeBlock((x, y-1, startZ+2), Block("dirt_path"))
    
    # Path on the right side of the house
    for z in range(startZ+2, entranceGateCoord[2]-1):
        ED.placeBlock((endX-2, y-1, z), Block("dirt_path"))

def buildFloor(ED, centerX, floorHeight, y, diameter, centerZ, even, woodColour):
    if even == True:
        endX = centerX-int(diameter/4)
        startZ = centerZ-int(diameter/4)
    else:
        endX = centerX-int(diameter/4)-2
        startZ = centerZ-int(diameter/4)-1
    for z in range(startZ, centerZ+int(diameter/2)):
        for x in range(centerX, endX-1, -1):
            if ED.getBlock((x, floorHeight, z)) != Block("minecraft:air") and ED.getBlock((x, floorHeight, z)) != Block("minecraft:stone_bricks"):
                break
            
            ED.placeBlock((x, floorHeight, z), woodColour)
        for x in range(centerX+1, centerX+int(diameter/2)):
            if ED.getBlock((x, floorHeight, z)) != Block("minecraft:air"):
                break
            ED.placeBlock((x, floorHeight, z), woodColour)


            
def addFrontWindows(ED, startY, endY, startX, startZ, even):
    if even == False:
        startZ -=1
    for h in range(startY, endY): 
        ED.placeBlock((startX, h, startZ), Block("glass_pane"))
        if even == True:
            ED.placeBlock((startX+1, h, startZ),Block("glass_pane")) 
    return startX, startY, startZ

def addSideWindows(ED, startY, endY, startX, startZ, even):
    if even == False:
        startX -= 1
    for h in range(startY, endY):
        ED.placeBlock((startX, h, startZ), Block("glass_pane"))
        if even==True:
            ED.placeBlock((startX, h, startZ+1), Block("glass_pane")) 
    return startX, startY, startZ

def buildEntrance(ED, centerX, y, centerZ, diameter, even, woodColour, slabColour):
    if even == True:
        # Remove block
        ED.placeBlock((centerX+1, y, centerZ + diameter/2), Block("air"))
        ED.placeBlock((centerX+1, y+1, centerZ + diameter/2), Block("air"))
        # Remove block
        ED.placeBlock((centerX, y, centerZ + diameter/2), Block("air"))
        ED.placeBlock((centerX, y+1, centerZ + diameter/2), Block("air"))
    else:
        # Remove block
        ED.placeBlock((centerX, y, centerZ + diameter/2-1), Block("air"))
        ED.placeBlock((centerX, y+1, centerZ + diameter/2-1), Block("air"))

    ''' Frame around the door '''
    for h in range(y, y+2):
        ED.placeBlock((centerX-1, h, centerZ+int(diameter/2)+1), woodColour)
        if even == True:
            ED.placeBlock((centerX+2, h, centerZ+int(diameter/2)+1), woodColour)
        else:
            ED.placeBlock((centerX+1, h, centerZ+int(diameter/2)+1), woodColour)
 
    ED.placeBlock((centerX-1, h+1, centerZ+int(diameter/2)+1), slabColour)
    ED.placeBlock((centerX, h+1, centerZ+int(diameter/2)+1), woodColour)
    if even == True:
        ED.placeBlock((centerX+2, h+1, centerZ+int(diameter/2)+1), slabColour)
        ED.placeBlock((centerX+1, h+1, centerZ+int(diameter/2)+1), woodColour)
    if even == False:
        ED.placeBlock((centerX+1, h+1, centerZ+int(diameter/2)+1), slabColour)
    if even == True:
        # Right door
        ED.placeBlock((centerX+1, y, centerZ + diameter/2 +1), Block("dark_oak_door", {"facing": "south"}))
        # Left door
        ED.placeBlock((centerX, y, centerZ + diameter/2+1), Block("dark_oak_door", {"facing": "south", "hinge": "right"}))
    else:
        # Left door
        ED.placeBlock((centerX, y, centerZ + diameter/2), Block("dark_oak_door", {"facing": "north", "hinge": "right"}))


def removeSmallMushroomInside(ED, floorHeight, height, y, centerX, centerZ, diameter, mushroomColourProbability):
    ''' Remove blocks of the small mushroom roof that are inside the house ''' 
    for h in range(floorHeight+1, y+int(height/1.5)):
        for x in range(centerX, centerX+int(diameter/2)):
            for z in range(centerZ, centerZ-int(diameter/2)+1, -1):
                if mushroomColourProbability < 0.5:
                    target1 = Block("minecraft:mushroom_stem", {"down":"false", "east":"true", "north":"true", "south":"true", "up":"false", "west":"false"})
                    target2 = Block("minecraft:mushroom_stem", {"down":"false", "east":"true", "north":"true", "south":"true", "up":"false", "west":"true"})
                else:
                    target1 = Block("minecraft:brown_mushroom_block", {"down":"false", "east":"true", "north":"true", "south":"true", "up":"false", "west":"false"})
                    target2 = Block("minecraft:brown_mushroom_block", {"down":"false", "east":"true", "north":"true", "south":"true", "up":"false", "west":"true"})
                if ED.getBlock((x, h, z)) != target1 and ED.getBlock((x, h, z)) != target2:
                    ED.placeBlock((x, h, z), Block("air"))
                else:
                    break
            for z in range(centerZ, centerZ+int(diameter/2)):
                if mushroomColourProbability < 0.5:
                    target1 = Block("minecraft:mushroom_stem", {"down":"false", "east":"true", "north":"true", "south":"true", "up":"false", "west":"false"})
                    target2 = Block("minecraft:mushroom_stem", {"down":"false", "east":"true", "north":"true", "south":"true", "up":"false", "west":"true"})
                else:
                    target1 = Block("minecraft:brown_mushroom_block", {"down":"false", "east":"true", "north":"true", "south":"true", "up":"false", "west":"false"})
                    target2 = Block("minecraft:brown_mushroom_block", {"down":"false", "east":"true", "north":"true", "south":"true", "up":"false", "west":"true"})
                if ED.getBlock((x, h, z)) != target1 and ED.getBlock((x, h, z)) != target2:
                    ED.placeBlock((x, h, z), Block("air"))
                else:
                    break

def decorateGarden(ED, perimeter, centerZHouse, diameter, even, woodColour, fenceColour, slabColour):
    flowers = ["red_tulip", "orange_tulip", "white_tulip", "pink_tulip"]
    (startX, startZ), (endX, endZ), y = perimeter
    hortusSize = 5
    endHortusX = endX-3
    hortusOrPool = random.random()
    startHortusX = endHortusX-hortusSize+1
    if diameter >= 9:
        endHortusZ = endZ-3
        startHortusZ = endZ-3-hortusSize
    else:
        startHortusZ = centerZHouse
        endHortusZ = startHortusZ+hortusSize
    for z in range(startHortusZ, endHortusZ+1):
        # Add path
        ED.placeBlock((startHortusX-1, y-1, z), Block("dirt_path"))
        ED.placeBlock((startHortusX, y, z), woodColour)
        ED.placeBlock((endHortusX, y, z), woodColour)
        # Add grass and flowers
        if hortusOrPool < 0.5:
            for x in range(startHortusX+1, endHortusX):
                ED.placeBlock((x, y, z), Block("grass_block"))
                ED.placeBlock((x, y+1, z), Block(random.choice(flowers)))
        else:
            for x in range(startHortusX+1, endHortusX):
                ED.placeBlock((x, y, z), Block("water"))
    for x in range(startHortusX, endHortusX+1):
        # Add path 
        ED.placeBlock((x, y-1, startHortusZ-1), Block("dirt_path"))

        ED.placeBlock((x, y, startHortusZ), woodColour)
        ED.placeBlock((x, y, endHortusZ), woodColour)
    if hortusOrPool < 0.5:
        # Add pillars
        for h in range(y+1, y+3):
            ED.placeBlock((startHortusX, h, endHortusZ), fenceColour) # front left corner
            ED.placeBlock((startHortusX, h, startHortusZ), fenceColour) # back left corner
            ED.placeBlock((endHortusX, h, startHortusZ), fenceColour) # back right corner
            ED.placeBlock((endHortusX, h, endHortusZ), fenceColour) # front right corner
        # Add hortus roof
        for x in range(startHortusX, endHortusX+1):
            for z in range(startHortusZ, endHortusZ+1):
                ED.placeBlock((x, y+3, z), slabColour)
        # Add 8 lanterns
        ED.placeBlock((startHortusX+1, y+2, endHortusZ), Block("lantern", {"hanging":"true"})) # front left corner
        ED.placeBlock((startHortusX, y+2, endHortusZ-1), Block("lantern", {"hanging":"true"})) # front left corner
        ED.placeBlock((startHortusX, y+2, startHortusZ+1), Block("lantern", {"hanging":"true"})) # back left corner
        ED.placeBlock((startHortusX+1, y+2, startHortusZ), Block("lantern", {"hanging":"true"})) # back left corner
        ED.placeBlock((endHortusX-1, y+2, startHortusZ), Block("lantern", {"hanging":"true"})) # back right corner
        ED.placeBlock((endHortusX, y+2, startHortusZ+1), Block("lantern", {"hanging":"true"})) # back right corner
        ED.placeBlock((endHortusX, y+2, endHortusZ-1), Block("lantern", {"hanging":"true"})) # front right corner
        ED.placeBlock((endHortusX-1, y+2, endHortusZ), Block("lantern", {"hanging":"true"})) # front right corner

    # Complete path
    ED.placeBlock((startHortusX-1, y-1, startHortusZ-1), Block("dirt_path"))
    if diameter <= 8:
        for x in range(startHortusX-1, endHortusX+1):
            ED.placeBlock((x, y-1, endHortusZ+1), Block("dirt_path"))

    # Flowerbeds
    lengthFlowerBed = 3
    widthFlowerBed = 2
    addFlowerBed(ED, startX+4, endZ-3, y, lengthFlowerBed, widthFlowerBed, flowers)
    if even == False:
        addFlowerBed(ED, startX+4+lengthFlowerBed+2, endZ-3, y, lengthFlowerBed, widthFlowerBed, flowers)
    else:
        addFlowerBed(ED, startX+4+lengthFlowerBed+3, endZ-3, y, lengthFlowerBed, widthFlowerBed, flowers)

def addFlowerBed(ED, startX, endZ, y, length, width, flowers):
    for x in range(startX, startX+length+1):
        for z in range(endZ-width+1, endZ+1):
            ED.placeBlock((x, y, z), Block(random.choice(flowers)))


if __name__ == '__main__':
    main()