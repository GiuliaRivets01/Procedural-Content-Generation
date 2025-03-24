
import numpy as np
import matplotlib.pyplot as plt
from gdpc import Block


def getAllRegions(ED, STARTX, STARTZ, LASTX, LASTZ, STARTY, LASTY, heights):
    allRegions = []
    allScores = []
    size = 23
    print("Build area from ({}, {}, {}) to ({}, {}, {})" .format(STARTX, STARTY, STARTZ, LASTX, LASTY, LASTZ))
    endX = LASTX-size+1
    for x in range(STARTX, endX+1):
        endZ = LASTZ-size+1
        for z in range(STARTZ, endZ+1):
            cornerX = x-STARTX
            cornerZ = z - STARTZ
            heightsOfRegion = [row[cornerZ:cornerZ+size] for row in heights[cornerX:cornerX+size]]
            avgHeight = int(np.mean(heightsOfRegion)) # get average height of the region
            water = False
            if avgHeight == 63: 
                water = checkForWater(ED, x, z, x+size-1, z+size-1, avgHeight)
            if water == False:
                if avgHeight >= STARTY and avgHeight <= LASTY:
                    avgHeight = int(avgHeight)
                    region = ((x, z), (x+size-1, z+size-1), avgHeight)
                    score = computeBlocksToModify(ED, region, heights, STARTX, STARTZ)
                    if score >= 0:
                        allRegions.append(region)
                        allScores.append(score)

    return allRegions, allScores
        
def computeBlocksToModify(ED, region, heights, STARTX, STARTZ):
    ((startX, startZ), (endX, endZ), avgHeight) = region
    numBlocksToRemove = 0
    numBlocksToAdd = 0
    for x in range(startX, endX + 1):
        for z in range(startZ, endZ + 1):
            cornerX = x - STARTX
            cornerZ = z - STARTZ
            if heights[cornerX][cornerZ] > avgHeight:
                numBlocksToRemove += 1
            if heights[cornerX][cornerZ] < avgHeight:
                numBlocksToAdd += (avgHeight - heights[cornerX][cornerZ])  # Blocks below average height need to be filled in or removed
                
    return numBlocksToAdd + numBlocksToRemove

def checkForWater(ED, startX, startZ, endX, endZ, avgHeight):
    for x in range(startX, endX+1):
        for z in range(startZ, endZ+1):
            if ED.getBlock((x, avgHeight-1, z)) == Block("minecraft:water", {"level": "0"}):
                return True
    return False


def getBestRegion(ED, STARTX, STARTZ, LASTX, LASTZ, STARTY, LASTY, heights):
    allRegions, allScores = getAllRegions(ED, STARTX, STARTZ, LASTX, LASTZ, STARTY, LASTY, heights)
    ''' Uncomment this if you want to visualize the heightmap '''
    #createHeatMap(STARTX, STARTZ, LASTX, LASTZ, allRegions, allScores)
    
    # We search for the minimum value of modified blocks
    if len(allRegions) == 0:
        return False
    indexMin = allScores.index(min(allScores))
    bestRegion = allRegions[indexMin]

    while checkForExistingBuildings(ED, bestRegion, heights, STARTX, STARTZ, STARTY, LASTY) == True:
        print("A building is already here, search for another region...")

        allScores.pop(indexMin)
        allRegions.pop(indexMin)
        if len(allRegions) > 0:
            indexMin = allScores.index(min(allScores))
            bestRegion = allRegions[indexMin]
        else: return -1

    # Before selecting the region as being actually 
    start, end, height = bestRegion
    print("Build region found: from {} to {} at height {} with score {}" .format(start, end, height, allScores[indexMin]))
    return bestRegion


def checkForExistingBuildings(ED, bestRegion, heights, STARTX, STARTZ, STARTY, LASTY):
    ((startX, startZ), (endX, endZ), y) = bestRegion
    for x in range(startX, endX+1):
        for z in range(startZ, endZ+1):
            if isBlockFence(ED, (x, y, z)) == True:
                return True
            cornerX = x-STARTX
            cornerZ = z - STARTZ
            # Check at higher blocks
            if heights[cornerX][cornerZ] > y:
                for h in range(y+1, heights[cornerX][cornerZ]+1):
                    if isBlockFence(ED, (x, h, z)) == True:
                        print("True")
                        return True
            
            # Check at lower blocks
            if heights[cornerX][cornerZ] < y:
                for h in range(heights[cornerX][cornerZ]-1, y):
                    if isBlockFence(ED, (x, h, z)) == True:
                        return True 
    return False
        
def isBlockFence(ED, position):
    target = ED.getBlock(position)
    block_string = str(target)
    if "fence" in block_string:
        return True
    if "mushroom" in block_string:
        return True
    return False


def createHeatMap(STARTX, STARTZ, LASTX, LASTZ, allRegions, allScores):
    print("Creating heatmap...")
    # Initialize heatmap with zeros
    heatmap = [[0] * (LASTZ - STARTZ + 1) for _ in range(LASTX - STARTX + 1)]
    # Count how many times each cell appears in the regions
    count_map = [[0] * (LASTZ - STARTZ + 1) for _ in range(LASTX - STARTX + 1)]

    # Iterate through all regions
    for region, score in zip(allRegions, allScores):
        (x1, z1), (x2, z2), _ = region
        for x in range(x1, x2 + 1):
            for z in range(z1, z2 + 1):
                heatmap[x - STARTX][z - STARTZ] += score
                count_map[x - STARTX][z - STARTZ] += 1

    # Calculate the average score for each cell
    for i in range(len(heatmap)):
        for j in range(len(heatmap[0])):
            if count_map[i][j] > 0:
                heatmap[i][j] /= count_map[i][j]

    # Plot heatmap
    heatmap = np.array(heatmap)
    plt.imshow(heatmap, cmap='hot', interpolation='nearest')
    plt.colorbar(label='Average Blocks to Modify')
    plt.title('Heatmap of Average Blocks to Modify')
    plt.xlabel('X')
    plt.ylabel('Z')
    plt.show()
