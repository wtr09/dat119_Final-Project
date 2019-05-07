# -*- coding: utf-8 -*-
"""
Tyler Ragan
5/6/2019
Python 1 - Dat-119 - Spring 2019
Final Project

Data file is survey of oil and gas well. Program pulls from CSV survey file to give spatial representation and statistical data. 

"""
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import csv
import numpy as np
import seaborn as sns
import pandas as pd

def avg_list(list_X):
    return round(sum(list_X)/len(list_X),2)

def read(North_List, East_List, TVD_List, TMD_List, DLS_List, Inc_List, Azi_List):
    
    with open('survey1.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            tmd = row[1]
            north = row[6]
            east = row[7]
            tvd = row[5]
            inc = row[2]
            azi = row[3]
            dls = row[8]
            TMD_List.append(float(tmd))
            North_List.append(float(north))
            East_List.append(float(east))
            TVD_List.append(float(tvd))
            Inc_List.append(float(inc))
            Azi_List.append(float(azi))
            DLS_List.append(float(dls))
            #https://docs.python.org/2/library/csv.html
            
def write(DLS_Listxx,TVD_Listxx,lateral_lengthx, aDLS_lateralx, maxinc_lateralx, mininc_lateralx, lengthx, percent_lateralx):
    file_object = open('survey_data.txt', 'w')
    file_object.write('Wellbore Statistics' + '\n')
    file_object.write('---------------------------' + '\n')
    file_object.write('Maximum DLS              ')
    file_object.write(str(max(DLS_Listxx)) + '\n')
    file_object.write('Deepest Point            ')
    file_object.write(str(max(TVD_Listxx)) + '\n')
    file_object.write('Average DLS              ')
    file_object.write(str(avg_list(DLS_Listxx)) + '\n')
    file_object.write('Lateral Length           ')
    file_object.write(str(lateral_lengthx) + '\n')
    file_object.write('Average Lateral DLS      ')
    file_object.write(str(aDLS_lateralx) + '\n')
    file_object.write('Maximum Lateral Inc      ')
    file_object.write(str(maxinc_lateralx) + '\n')
    file_object.write('Minimum Lateral Inc      ')
    file_object.write(str(mininc_lateralx) + '\n')
    file_object.write('Footage off Azimuth      ')
    file_object.write(str(lengthx) + '\n')
    file_object.write('Percent off Azimuth      ')
    file_object.write(str(percent_lateralx) + '\n')
    file_object.close()

def main():
    North_Listx = []
    East_Listx = []
    TVD_Listx = []
    TMD_Listx = []
    DLS_Listx = []
    Inc_Listx = []
    Azi_Listx = []
    read(North_Listx, East_Listx, TVD_Listx, TMD_Listx, DLS_Listx, Inc_Listx, Azi_Listx)
    well_name = input("Enter Well Name:")
    user1 = input("Enter Landing Point (Note: Landing Point Has To Be Survey Point):")
    #validates input is number and in TMD_List (i.e. is a survey point)
    while user1.isdigit() == False or float(user1) not in TMD_Listx:
        if user1.isdigit() == False or float(user1) not in TMD_Listx:
            print("Incorrect Response, Please Enter Landing Point Again:")
            user1 = input("Enter Landing Point (Note: Landing Point Has To Be Survey Point):")
        else:
            user11 = float(user1)
            break
    user2 = input("Enter Target Azimuth (Note: Target Azimuth Needs To Be Integer):")
    #validates target azimuth is between 0 and 360 degrees by whole number
    while user2.isdigit() == False:
        if user2.isdigit() == False:
            print("Incorrect Response, Please Enter Landing Point Again:")
            user2 = input("Enter Target Azimuth (Note: Target Azimuth Needs To Be Integer):")
        else:
            user22 = float(user2)
            
    user11 = float(user1)
    user22 = float(user2)
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(North_Listx, East_Listx, TVD_Listx, c='r')
    ax.set_xlabel('North (ft)')
    ax.set_ylabel('East (ft)')
    ax.set_zlabel('TVD (ft)')
    plt.gca().invert_zaxis()
    ax.set_title(well_name)
    plt.show()
    fig.savefig('Wellbore.png')
    #https://matplotlib.org/
    
    fig1 = plt.figure()
    plt.scatter(North_Listx, East_Listx, c='r')
    plt.xlabel('North (ft)')
    plt.ylabel('East (ft)')
    plt.title(well_name)
    plt.show()
    fig1.savefig('Wellbore Plat.png')


    pazimuth = []

    for item in Azi_Listx[TMD_Listx.index(user11):]:
        pazimuth.append(100*(item-user22)/360)
    #calculates percent off target azimuth below landing point for heat map

    df = pd.DataFrame(pazimuth,TMD_Listx[TMD_Listx.index(user11):], columns=["Percent Deviation Off Target Azimuth"])
    sns.heatmap(df, cmap="Greens")
    plt.savefig('Heat Map.png')
    df = pd.DataFrame(DLS_Listx,TMD_Listx, columns=["Dog Leg Severity"])
    df.plot.hist(bins=20)
    plt.savefig('Histogram.png')
    ax = df.plot()
    fig = ax.get_figure()
    fig.savefig('DLS vs TMD.png')
    #https://seaborn.pydata.org/

    aDLS_lateral = avg_list(DLS_Listx[TMD_Listx.index(user11):])
    mininc_lateral = min(Inc_Listx[TMD_Listx.index(user11):])
    maxinc_lateral = max(Inc_Listx[TMD_Listx.index(user11):])
    lateral_length = max(TMD_Listx)-user11
    #takes statistcs of interval based on Landing Point input

    length = 0

    for item in Azi_Listx[TMD_Listx.index(user11):]:
        if item > (2 + user22) or item < (user22 - 2):
            footage = TMD_Listx[Azi_Listx.index(item)]-TMD_Listx[Azi_Listx.index(item)-1]
            length = length + footage
    #Adds footage to counter if deemed out of target (plus/minus 2 degrees) in target interval based on Landing Point input  
    percent_lateral = round(length/lateral_length,2)
    #calculates percentage out of target for lateral
    write(DLS_Listx,TVD_Listx,lateral_length, aDLS_lateral, maxinc_lateral, mininc_lateral, length, percent_lateral)
    print("Program Complete")
main()
