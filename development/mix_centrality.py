__author__ = 'stephenlawdesign'

'''
scripts that takes an edgelist and runs centrality and gravitational potential measures
with mixed weights using networkx and pandas
'''

################### Instantiate variables ###################
import os
import sys
import networkx as nx
import csv
import datetime
import numpy as np
import pandas as pd
from collections import Counter
from collections import defaultdict
#import igraph
#PList=[111,112,113,121,131,122,123,132,133,211,212,213,221,231,222,223,232,233,311,312,313,321,331,321,323,332,333]
#PList=[411,511,611,711,811,911]

############################ Numpy-Pandas - shortest angular path matrix  #######################################################
def Nx_Mixed_Centrality(csvFile,PList):

    file=open(csvFile,'r')
    G=nx.read_edgelist(file,delimiter=',',nodetype=int,data=(('Norm_ang',float),('Norm_metric',float),('Norm_slope',float),('metric',float)))

    for x in PList:
        for (i,j,k) in G.edges(data=True):
            k['ASL'+str(x)]=int(list(str(x))[0])*k['Norm_ang']+int(list(str(x))[1])*k['Norm_metric']+int(list(str(x))[2])*k['Norm_slope']

    DF_All=pd.read_csv('hkg_nodelist02.csv')
    DF02 = pd.DataFrame(index=DF_All['EdgeID'])

    # closeness centrality

    t1 = datetime.datetime.now()
    print "Starting time: %s" % (t1)
    for i in PList:
        DF02["TD_ASL"+str(i)] = np.nan
        DF02["NC_ASL"+str(i)] = np.nan
        DF02["CC_ASL"+str(i)] = np.nan
        for j in DF_All['EdgeID']:
            SP_ASL=nx.single_source_dijkstra_path_length(G,j,weight='ASL'+str(i))
            DF=pd.DataFrame({"SP_ASL":SP_ASL})
            DF["Node"]=np.where(DF['SP_ASL']>0,1,0)
            DF=DF.fillna(0)
            DF02['TD_ASL'+str(i)][j]=DF['SP_ASL'].sum(axis=0)
            DF02['NC_ASL'+str(i)][j]=DF['Node'].sum(axis=0)
            DF02['CC_ASL'+str(i)][j]=(DF02['NC_ASL'+str(i)][j]*DF02['NC_ASL'+str(i)][j])/(DF02['TD_ASL'+str(i)][j])
            SP_ASL=[]

    for i in PList:
        del DF02['TD_ASL'+str(i)]
        del DF02['NC_ASL'+str(i)]

    t2 = datetime.datetime.now()
    print "Execution time: %s" % (t2-t1)


    # betweenness centrality
    for i in PList:
        DF02["BC_ASL"+str(i)] = np.nan
        BC_ASL= nx.betweenness_centrality(G,weight='ASL'+str(i),normalized=False,endpoints=True)
        DF=pd.DataFrame({"BC_ASL":BC_ASL})
        DF02["BC_ASL"+str(i)] = DF["BC_ASL"]

    DF02.to_csv('Mix_BC_CC_ASL.csv',index=True)

def Nx_Mixed_shortest_path_BC(csvFile,PList):

    file=open(csvFile,'r')
    G=nx.read_edgelist(file,delimiter=',',nodetype=int,data=(('Norm_ang',float),('Norm_metric',float),('Norm_slope',float),('metric',float)))

    for x in PList:
        for (i,j,k) in G.edges(data=True):
            k['ASL'+str(x)]=int(list(str(x))[0])*k['Norm_ang']+int(list(str(x))[1])*k['Norm_metric']+int(list(str(x))[2])*k['Norm_slope']

    DF_All=pd.read_csv('hkg_nodelist02.csv')
    DF02 = pd.DataFrame(index=DF_All['EdgeID'])

    for i in PList:
        for j in DF_All['EdgeID']:
            DF02["BC_ASL"+str(i)] = np.nan
            AllPath=nx.all_pairs_dijkstra_path(G,weight='ASL'+str(i))

    newList=[]
    for i in AllPath:
        for j in AllPath[i]:
            for k in AllPath[i][j]:
                newList.append(k)


    DF02["Mix_BC_ASL"+str(i)] = DF["BC_ASL"]

    for i in reader1:
        i['Time_Ch '+' R'+str(Radius)+'time']=Counter(newList)[int(i['edgeID'])]


    DF02.to_csv('BC_ASL.csv',index=True)

def Nx_Centrality_Pandas(csvFile,Radius):

    file=open(csvFile,'r')
    G=nx.read_edgelist(file,delimiter=',',nodetype=int,data=(('Norm_ang',float),('Norm_metric',float),('Norm_slope',float),('metric',float)))
    for (i,j,k) in G.edges(data=True):
        if k['speed']>0:
            k['time']=k['length']/k['speed']
        else:
            k['time']=k['length']

    DF_All=pd.read_csv('hkg_nodelist02.csv')
    DF02 = pd.DataFrame(index=DF_All['EdgeID'])
    DF02["TD_Time_RN"] = np.nan
    DF02["TD_Ang_RN"] = np.nan
    DF02["NC_Time_RN"] = np.nan
    DF02["HC_Time_RN"] = np.nan
    DF02["HC_Ang_RN"] = np.nan
    DF02["TD_Time_R60min"] = np.nan
    DF02["TD_Ang_R60min"] = np.nan
    DF02["NC_Time_R60min"] = np.nan
    DF02["HC_Time_R60min"] = np.nan
    DF02["HC_Ang_R60min"] = np.nan
    #DF02["Int_Time"] = np.nan
    #DF02["Int_Ang"] = np.nan


    t1 = datetime.datetime.now()
    print "Starting time: %s" % (t1)


    for i in DF_All['EdgeID']:
        SP_Time01=nx.single_source_dijkstra_path_length(G,i,weight='time')
        SP_Ang01=nx.single_source_dijkstra_path_length(G,i,weight='ang')
        DF=pd.DataFrame({"SP_Time":SP_Time01,"SP_Ang":SP_Ang01})
        DF["Node"]=np.where(DF['SP_Time']>0,1,0)
        DF['DD_Time']=DF['Node']/DF['SP_Time']
        DF['DD_Ang']=DF['Node']/DF['SP_Ang']
        DF=DF.fillna(0)
        DF02['TD_Time_RN'][i]=DF['SP_Time'].sum(axis=0)
        DF02['TD_Ang_RN'][i]=DF['SP_Ang'].sum(axis=0)
        DF02['NC_Time_RN'][i]=DF['Node'].sum(axis=0)
        DF02['HC_Time_RN'][i]=DF['DD_Time'].sum(axis=0)
        DF02['HC_Ang_RN'][i]=DF['DD_Ang'].sum(axis=0)
        DF[DF['SP_Time']>Radius]=0
        DF02['TD_Time_R60min'][i]=DF['SP_Time'].sum(axis=0)
        DF02['TD_Ang_R60min'][i]=DF['SP_Ang'].sum(axis=0)
        DF02['NC_Time_R60min'][i]=DF['Node'].sum(axis=0)
        DF02['HC_Time_R60min'][i]=DF['DD_Time'].sum(axis=0)
        DF02['HC_Ang_R60min'][i]=DF['DD_Ang'].sum(axis=0)
        SP_Time01=[]
        SP_Ang01=[]
        DF=[]



    t2 = datetime.datetime.now()
    print "Execution time: %s" % (t2-t1)

    DF02.to_csv('all_centrality.csv',index=True)


############################ Gravitational Potential #######################################################
def Nx_Gravity_Pandas(nodelistFile,employmentFile,csvFile,Radius):

    # Open files
    file = open(csvFile,'r')
    G=nx.read_edgelist(file,delimiter=',',nodetype=int,data=(('length',float),('ang',float),('speed',int)))

    #create time variable
    for (i,j,k) in G.edges(data=True):
        if k['speed']>0:
            k['time']=k['length']/k['speed']
        else:
            k['time']=k['length']

    DF_All=pd.read_csv(nodelistFile)
    DF_Emp=pd.read_csv(employmentFile)
    DF02 = pd.DataFrame(index=DF_All['EdgeID'])
    DF02["Grav_Time_RN"] = 0
    DF02["Grav_Ang_RN"] = 0
    DF02['jobs1997_RN'] = 0
    DF02['NC_RN'] = 0
    DF02['TD_Time_RN'] = 0
    DF02['TD_Ang_RN'] = 0
    DF02["Grav_Time_R60min"] = 0
    DF02["Grav_Ang_R60min"] = 0
    DF02['jobs1997_R60min'] = 0
    DF02['NC_R60min'] = 0
    DF02['TD_Time_R60min'] = 0
    DF02['TD_Ang_R60min'] = 0

    # Run single source shortest path length
    t1 = datetime.datetime.now()
    print "Starting time: %s" % (t1)

    for i in DF_Emp['Edge_ID']:

        # for all radius
        SP_Time01 = nx.single_source_dijkstra_path_length(G,i,weight='time')
        SP_Ang01 = nx.single_source_dijkstra_path_length(G,i,weight='ang')
        DF=pd.DataFrame({"Edge_ID":DF_All['EdgeID'],"SP_Time":SP_Time01,"SP_Ang":SP_Ang01})
        DF['SP_Ang']=DF['SP_Ang']+1
        DF['SP_Time']=DF['SP_Time']+1
        DF['jobs1997']=int(DF_Emp['jobs1997'][DF_Emp['Edge_ID']==i])
        DF['NC']=1
        DF['DD_Time_RN']=DF['jobs1997']/DF['SP_Time']
        DF['DD_Ang_RN']=DF['jobs1997']/DF['SP_Ang']
        DF02['TD_Time_RN']=DF02['TD_Time_RN']+DF['SP_Time']
        DF02['TD_Ang_RN']=DF02['TD_Ang_RN']+DF['SP_Ang']
        DF02['Grav_Time_RN']=DF02['Grav_Time_RN']+DF['DD_Time_RN']
        DF02['Grav_Ang_RN']=DF02['Grav_Ang_RN']+DF['DD_Ang_RN']
        DF02['jobs1997_RN']=DF02['jobs1997_RN']+DF['jobs1997']
        DF02['NC_RN']=DF02['NC_RN']+DF['NC']

        #For radius cut off
        DF[DF['SP_Time']>Radius]=0
        DF['DD_Time_R60min']=DF['jobs1997']/DF['SP_Time']
        DF['DD_Ang_R60min']=DF['jobs1997']/DF['SP_Ang']
        DF=DF.fillna(0)
        DF02['TD_Time_R60min']=DF02['TD_Time_R60min']+DF['SP_Time']
        DF02['TD_Ang_R60min']=DF02['TD_Ang_R60min']+DF['SP_Ang']
        DF02['Grav_Time_R60min']=DF02['Grav_Time_R60min']+DF['DD_Time_R60min']
        DF02['Grav_Ang_R60min']=DF02['Grav_Ang_R60min']+DF['DD_Ang_R60min']
        DF02['jobs1997_R60min']=DF02['jobs1997_R60min']+DF['jobs1997']
        DF02['NC_R60min']=DF02['NC_R60min']+DF['NC']

        SP_Time01=[]
        SP_Ang01=[]
        DF=[]

    t2 = datetime.datetime.now()
    print "Execution time: %s" % (t2-t1)

    DF02.to_csv('Gravity.csv',index=True)


