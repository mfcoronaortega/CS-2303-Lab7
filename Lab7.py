#Course: CS 2302 Data Structures | Spring 2019
#Author: Maria Fernanda Corona Ortega
#Assignment: Lab 7
#Instructor: Olac Fuentes
#Purpose of Code: Starting point for program to build and draw a maze
# Modify program using disjoint set forest to ensure there is exactly one
# simple path joiniung any two cells
#Last Modification: 4/1/2019

import matplotlib.pyplot as plt
import numpy as np
import random
from scipy import interpolate 
import timeit 

def DisjointSetForest(size):
    return np.zeros(size,dtype=np.int)-1

def find(S,i):
    # Returns root of tree that i belongs to
    if S[i]<0:
        return i
    return find(S,S[i])

def find_c(S,i): #Find with path compression 
    if S[i]<0: 
        return i
    r = find_c(S,S[i]) 
    S[i] = r 
    return r

def union(S,i,j):
    # Joins i's tree and j's tree, if they are different
    ri = find(S,i) 
    rj = find(S,j)
    if ri!=rj:
        S[rj] = ri
        
def union_c(S,i,j):
    # Joins i's tree and j's tree, if they are different
    # Uses path compression
    ri = find_c(S,i) 
    rj = find_c(S,j)
    if ri!=rj:
        S[rj] = ri


def draw_maze(walls,maze_rows,maze_cols,cell_nums=False):
    fig, ax = plt.subplots()
    for w in walls:
        if w[1]-w[0] ==1: #vertical wall
            x0 = (w[1]%maze_cols)
            x1 = x0
            y0 = (w[1]//maze_cols)
            y1 = y0+1
        else:#horizontal wall
            x0 = (w[0]%maze_cols)
            x1 = x0+1
            y0 = (w[1]//maze_cols)
            y1 = y0  
        ax.plot([x0,x1],[y0,y1],linewidth=1,color='k')
    sx = maze_cols
    sy = maze_rows
    ax.plot([0,0,sx,sx,0],[0,sy,sy,0,0],linewidth=2,color='k')
    if cell_nums:
        for r in range(maze_rows):
            for c in range(maze_cols):
                cell = c + r*maze_cols   
                ax.text((c+.5),(r+.5), str(cell), size=10,
                        ha="center", va="center")
    ax.axis('off') 
    ax.set_aspect(1.0)

def wall_list(maze_rows, maze_cols):
    # Creates a list with all the walls in the maze
    w =[]
    for r in range(maze_rows):
        for c in range(maze_cols):
            cell = c + r*maze_cols
            if c!=maze_cols-1:
                w.append([cell,cell+1])
            if r!=maze_rows-1:
                w.append([cell,cell+maze_cols])
    return w

plt.close("all") 

n = 10
maze_rows = n
maze_cols =  n
walls = wall_list(maze_rows,maze_cols)
size = maze_rows*maze_cols
S = DisjointSetForest(size)

#draw_maze(walls,maze_rows,maze_cols,cell_nums=True) 

def buildMaze(walls, S, size, m):
    start = timeit.default_timer()  
    for i in range(m):#While S has more than one set
        ran = random.randint(0,len(walls)-1)
        if find_c(S, walls[ran][0]) != find_c(S, walls[ran][1]):
#           print('root of', walls[ran][0],'is',find_c(S, walls[ran][0]))
#           print('root of', walls[ran][1],'is',find_c(S, walls[ran][1]))
#           print('removing wall ',walls[ran])
#           print('union between sets', walls[ran][0], 'and ', walls[ran][1])
        
            union_c(S,walls[ran][0],walls[ran][1])
#           print('root of', walls[ran][0],'is NOW',find_c(S, walls[ran][0]))
#           print('root of', walls[ran][1],'is NOW',find_c(S, walls[ran][1]))
            walls.pop(ran)
#           print()
#           print(len(walls))
#           print(walls)   
#           print(S)

    stop = timeit.default_timer()
#   print(walls)
    print('Standard Union running time', stop-start, 'for size n', n ,' in and nxn matrix')
    print()
    draw_maze(walls,maze_rows,maze_cols)
    return walls, S

#def maze_toAl(walls, S):
##    for i in range(len(walls)):
##        if find_c(S, walls[i][0]) != find_c(S, walls[i]][1])
##            print(' ') 
#        
#    print(walls)
#    print(S)
#    
#
#
#
#newWalls, newSet = buildMaze(walls, S, size, size*2 + 1)
#
#maze_toAl(newWalls,newSet)

print('The curren number of cells in this maze is', size)
user = input('What is the numer of walls m you would like to remove?')
m = int(user)
print()
print('Choice = ', m)
print()

if m < size-1:
    buildMaze(walls, S, size,m*2)
    print('A path from source to destination is not guaranteed to exist (when m < n − 1)')
if m == size-1:
    buildMaze(walls, S, size,m*2)
    print('The is a unique path from source to destination (when m = n − 1)')
if m > size-1:
    buildMaze(walls, S, size,m*2)
    print('There is at least one path from source to destination (when m > n − 1)')

