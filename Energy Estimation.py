import math
import numpy as np
from scipy.stats import beta
import cv2
from matplotlib import pyplot as plt
from PIL import Image as im
from Processing import energyConsumption, image_brightness,rgb_matrix
from gridding import draw_grid
import cv2
import Smart_Report


def overlay(bg,ovl):
    background = cv2.imread(bg)
    overlay = cv2.imread(ovl)

    added_image = cv2.addWeighted(background,0.2,overlay,0.9,0)

    cv2.imwrite('London_Energy+PD+GC.png', added_image)
    cv2.imshow('image', added_image)

    # waits for user to press any key
    # (this is necessary to avoid Python kernel form crashing)
    cv2.waitKey(0)

    # closing all open windows
    cv2.destroyAllWindows()

def population_gridding(image,r,c):
    draw_grid(image,[r,c],(0,255,0),2)
    matrix = rgb_matrix(image,r,c)

    result = [[0]*c for x in range(r)]

    # print(matrix)
    mini = 100000
    maxi = 0
    for x in range(r):
        for y in range(c):
            red = int(matrix[x][y][0][0])
            blue = int(matrix[x][y][0][1])
            green = int(matrix[x][y][0][2])
            factor = red+blue+green
            mini = min(factor,mini)
            maxi = max(factor,maxi)

            if factor>345 and factor<345+102:
                result[x][y] = 5000
            elif factor>345+102 and factor<345+102+102:
                result[x][y] = 500
            else:
                result[x][y] = 50


    return result

def green_cover_gridding(image,r,c):
    draw_grid(image,[r,c],(0,255,0),2)
    matrix = rgb_matrix(image,r,c)

    result = [[0]*c for x in range(r)]

    # print(matrix)
    mini = 100000
    maxi = 0
    for x in range(r):
        for y in range(c):
            red = int(matrix[x][y][0][0])
            blue = int(matrix[x][y][0][1])
            green = int(matrix[x][y][0][2])
            factor = red+blue+green
            mini = min(factor,mini)
            maxi = max(factor,maxi)
    # print(mini,maxi)

            if factor>410 and factor<410+105:
                result[x][y] = 'High'
            elif factor>410+105 and factor<410+105+105:
                result[x][y] = 'Medium'
            else:
                result[x][y] = 'Low'


    return result

Delhi = 'Satellite Images/Delhi/Delhi_SAT1.jpg'
Berlin = 'Satellite Images/Berlin_SAT1.jpg'
test = 'Satellite Images/testimg2.jpg'
SanFrancisco = 'Satellite Images/SanFrancisco_SAT1.jpg'
London_energy = 'Satellite Images/London/London_Energy.jpg'
London_pd = 'Satellite Images/London/London_PD.jpg'
London_GC = 'Satellite Images/London/London_GC.jpg'
London_overlay = 'Satellite Images/London/London_Energy+PD.jpg'


# img = cv2.imread(London_GC)
# green_cover_gridding(img,10,10)

#


img = cv2.imread(London_pd)
img = cv2.resize(img, (960, 540))
cv2.imshow('image', img)
cv2.waitKey(5000)


img = cv2.imread(London_energy)
img = cv2.resize(img, (960, 540))
cv2.imshow('image', img)
cv2.waitKey(5000)


img = cv2.imread(London_overlay)
img = cv2.resize(img, (960, 540))
cv2.imshow('image', img)
cv2.waitKey(5000)
cv2.destroyAllWindows()


img = cv2.imread(London_energy)
ieg = energyConsumption(img)
img = cv2.imread(London_pd)
print('\n Population Density Matrix:\n')
pg = population_gridding(img,10,10)
print(pg)
img = cv2.imread(London_GC)
print('\n Green Cover Matrix:\n')
gcg = green_cover_gridding(img,10,10)
print(gcg)

decisionGrid = [[None]*10 for x in range(10)]
suggestions = [['']*10 for x in range(10)]
for x in range(10):
    for y in range(10):
        if gcg[x][y]=='Medium':
            decisionGrid[x][y] = 100
            suggestions[x][y] = 'Optimal Energy Usage'
            if pg[x][y]==50:
                decisionGrid[x][y] -=25
                suggestions[x][y] = 'Less Population, Reduce Energy Supply or Hike Energy Rates'
            if pg[x][y]==5000:
                decisionGrid[x][y] +=25
                suggestions[x][y] = 'Optimal Energy Usage'

            if ieg[x][y]>=100:
                decisionGrid[x][y] += ieg[x][y]-100
                suggestions[x][y] = 'Optimal Energy Usage, can decrease the supply or deploy renewable energy sources'
            else:
                decisionGrid[x][y] -= 100-ieg[x][y]
                suggestions[x][y] = 'Scarse Energy Supply, Optimally increase or Lower energy Rates'

        if gcg[x][y]=='Low':
            decisionGrid[x][y] = 75
            suggestions[x][y] = 'Optimal Energy Usage, Increase green cover'
            if pg[x][y] == 500:
                decisionGrid[x][y] -= 25
                suggestions[x][y] = 'Optimal Energy Usage'
            if pg[x][y] == 50:
                decisionGrid[x][y] -= 50
                suggestions[x][y] = 'Optimal/ Scarse Energy Usage'

            decisionGrid[x][y]+=ieg[x][y]

        else:
            decisionGrid[x][y] = 125
            suggestions[x][y] = 'Optimal Energy Usage'
            if pg[x][y] == 500:
                decisionGrid[x][y] += 25
                suggestions[x][y] = 'Optimal Energy Usage'
            if pg[x][y] == 5000:
                decisionGrid[x][y] += 50
                suggestions[x][y] = 'Slightly Higher than Optimal Energy Usage. Subjective.'

            decisionGrid[x][y] += ieg[x][y]
# s = []
for x in range(10):
    for y in range(10):
        decisionGrid[x][y] = int(decisionGrid[x][y])-194
        # s.append(decisionGrid[x][y])

# threshold = 194



for x in range(10):
    print(decisionGrid[x])

print(suggestions)

recommendation = [['']*10 for x in range(10)]

for x in range(10):
    for y in range(10):
        recommendation[x][y] = 'EIA Score: '+str(decisionGrid[x][y]) + ' Suggestion: '+ suggestions[x][y]
print('Recommendation:\n\n')
print(recommendation)
Smart_Report.generateReport(recommendation)


