#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Final Project. WR KNN Program"""
__author__ = "Samran Mirza"
import csv
import sys
import math


lName = []
fName = []
team = []
year = []
games = []
rec = []
yards = []
tds = []
avg = []
std = []

def zscore(arr,line):
    global games, rec, yards, tds, avg, std
    r = len(arr)
    c = len(arr[0])
    games = [0] * line
    rec = [0] * line
    yards = [0] * line
    tds = [0] * line
    avg = [0] * 4
    std = [0] * 4
    for i in range(line):
        avg[0] = avg[0] + arr[i][0]
        games[i] = arr[i][0]
        avg[1] = avg[1] + arr[i][1]
        rec[i] = arr[i][1]
        avg[2] = avg[2] + arr[i][2]
        yards[i] = arr[i][2]
        avg[3] = avg[3] + arr[i][3]
        tds[i] = arr[i][3]
    for i in range(len(avg)):
        avg[i] = avg[i] / line


    for i in range(line):
        for j in range(len(std)):
            std[j] = std[j] + ((arr[i][j] - avg[j]) * (arr[i][j] - avg[j]))

    for j in range(len(std)):
        std[j] = std[j] / line
        std[j] = math.sqrt(std[j])


    arrNorm = []
    for i in range(r):
        row = []
        for j in range(c):
            value = (arr[i][j] - avg[j]) / std[j]
            row.append(value)
        arrNorm.append(row)    

    return(arrNorm)

def distance(user, players):
    sim = []
    r = len(players)
    c = len(user)
    for i in range(r):
        ed = 0
        for j in range(c):
            ed = ed + ((user[j] - players[i][j]) * (user[j] - players[i][j]))
        ed = math.sqrt(ed)
        sim.append(ed)   
    return(sim) 

def userZScore(arr):
    global avg, std
    
    r = len(arr)
    arrNorm = []
    for i in range(r):
        value = (int(arr[i]) - avg[i]) / std[i]
        arrNorm.append(value)    
    #print(arrNorm)
    return(arrNorm)

def printScore(k, names, scores, stats):
    r = len(scores)
    for i in range(r):
        for j in range(r - 1):
            if(scores[j] > scores[j + 1]):
                temp = scores[j]
                scores[j] = scores[j + 1]
                scores[j + 1] = temp
                for l in range(len(names[0])):
                   temp = names[j][l]
                   names[j][l] = names[j + 1][l]
                   names[j + 1][l] = temp
                   temp = stats[j][l]
                   stats[j][l] = stats[j + 1][l]
                   stats[j + 1][l] = temp
    k = int(k)
    
    for i in range(k):
        print(i + 1,". Last Name:", names[i][0], "First Name:", names[i][1], "Team:", names[i][2],  "Year:", names[i][3], 
        "Games:", stats[i][0], "Receptions:", stats[i][1], "Yards:", stats[i][2], "Touchdowns:", stats[i][3])

                

def start():
    global games, rec, yards, tds, lName, fName, team, year


    data = csv.DictReader(open("WR_DB.csv"))
  
    line_count = 0
    name = []
    value = []
    stats = []
    for row in data:
        
        value = []
        
        value.append([row['\ufeffLast Name']])
        value.append([row['First Name']])
        value.append([row['Team']])
        value.append([row['Year']])
        name.append(value)
        value = []
        games = ([row['Games']])
        value.append(int(games[0]))
        rec =[row['REC']]
        value.append(int(rec[0]))
        yards = [row["Yards"]]
        value.append(int(yards[0]))
        tds= [row['TDS']]
        value.append(int(tds[0]))
        stats.append(value)
        line_count += 1  

    statsNorm = zscore(stats, line_count)

    user = []
    print("Enter the amount of closest players you would like to view")
    k = input()    
    print("Enter the amount of games played")
    games = input()
    user.append(games)
    print("Enter the amount of receptions")
    rec = input()
    user.append(rec)
    print("Enter the amount receiving yards")
    yards = input()
    user.append(yards)
    print("Enter the amount of touchdowns")
    tds = input()
    user.append(tds)
    userNorm = userZScore (user)
    print("Games played:", user[0], " receptions: ", user[1], " yards: ", user[2], "touchdowns:", user[3] ) #print statement
    sim = distance(userNorm, statsNorm)
    printScore(k, name, sim, stats)
 

if __name__ == "__main__":         
    start()     