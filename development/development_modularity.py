__author__ = 's.law'

import networkx as nx
import igraph
#import community_test
import community
import csv
from itertools import izip
from itertools import combinations
import pandas as pd
import random
import numpy as np
import datetime

def pandas_functions():

    DF_nodelist['RUN_096'][113543]
    DF_nodelist.iloc[0]['RUN_096']
    DF_nodelist.loc[113543]['RUN_096']
    DF_nodelist.at[113543,'RUN_096']
    pd.unique(DF_nodelist['RUN_096'])
    #for i in DF_nodelist['RUN_096'].isin([155]):
        #if i==True


    DF_nodelist.set_value(113543,'RUN_096',156)
    DF_nodelist.apply(pd.Series.nunique, axis=1)

    grouped = DF_nodelist.groupby('RUN_096')
    for i in grouped:
        for j in i[1]['Depthmap_Ref']:
            for k in i[1]['Depthmap_Ref']:
                Dict[(j,k)]


    from itertools import product
    pd.DataFrame(list(product(i, i)), columns=['i', 'j'])


def igraph_plotting():

    g=igraph.Graph.Read_Ncol('test01.csv',directed=False)
    WT=igraph.Graph.community_walktrap(g,steps=3)
    #WT.summary(verbosity=1,max_leaf_count=40)
    format(WT)
    summary(WT,verbosity=1)
    plot(WT)
    opt_n=WT.optimal_count
    WT_p=WT.as_clustering(n=opt_n)

def nx_Pandas_Graph():
    #Reading Pandas edgelist
    DF_nodelist=pd.read_csv('GLA_nodelist2.csv')
    DF_edgelist=pd.read_csv('GLA_meridian_edgelist_test.csv')
    G2 = nx.Graph()

    for id, row in DF_nodelist.iterrows():
        G2.add_node(str(row['EdgeID']))

    for id, row in DF_edgelist.iterrows():
        G2.add_edge(str(row[0]),str(row[1]))

def nx_Random_Modularity():

    #4 minutes per ten runs = 24 seconds per run
    # 40 minutes per hundred runs or 6.5 hours for 1000 runs
    DF_nodelist=pd.read_csv('GLA_nodelist.csv')
    file=open("GLA_meridian_edgelist_no_weights.csv",'r')
    G=nx.read_weighted_edgelist(file,delimiter=',',nodetype=int)
    #G=nx.read_edgelist(file,delimiter=',',nodetype=int,data=(('weight',float),))

    #t1 = datetime.datetime.now()

    x=1
    Random={}
    while x<31:
        Random_p=community_test.best_partition(G)
        DF_nodelist['RUN_0'+str(x)]=Random_p.values()
        Random_p=[]
        #Random['RUN_0'+str(x)]=Random_p
        x=x+1

    #t2 = datetime.datetime.now()
    #print "Execution time: %s" % (t2-t1)

    #DF02=pd.DataFrame(Random.items())
    #DF02.to_csv('GLA_Random_Mod_Dict.csv',index=True)
    #DF_nodelist.to_csv('GLA_Random_Mod_p.csv',index=True)

    #return Random

def new_nx_fuzzy_membership_02():

    Dict={}

    t1=datetime.datetime.now()
    for i in DF_nodelist.columns.values[1:]:
        grouped=DF_nodelist.groupby(i)
        for j in grouped:
            comb=combinations(j[1]['Depthmap_Ref'],2)
            for i in comb:
                if Dict.has_key(str(i)):
                    Dict[str(i)]=Dict[str(i)]+1
                else:
                    Dict[str(i)]=1
    t2=datetime.datetime.now()

    DF01=pd.DataFrame(Dict.items(),columns=['pairs','weights'])
    DF01=DF01.drop(DF01[DF01.weights<Param].index)
    DF01.to_csv('GLA_Fuzzy_Edgelist03_p.csv', index=True)

def new_nx_fuzzy_membership():

    Dict={}
    #pd.unique(DF_nodelist['RUN_096'])

    for i in DF_nodelist.columns.values[1:]:
        grouped=DF_nodelist.groupby(i)
        for j in grouped:
            for k in j[1]['Depthmap_Ref']:
                for l in j[1]['Depthmap_Ref']:
                    if Dict.has_key((k,l)):
                        Dict[(k,l)]=Dict[(k,l)]+1
                    else:
                        Dict[(k,l)]=1

    DF01=pd.DataFrame(Dict.items(),columns=['pairs', 'weights'])
    Param=5
    DF01 = DF01.drop(DF01[DF01.weights<Param].index)
    DF01.to_csv('GLA_Fuzzy_edgelist_p.csv',index=True)


def old_nx_fuzzy_membership(Random):

    Dict={}
    Param=2
    for i in Random:
        for j in Random[i]:
            for k in Random[i]:
                if Random[i][j]==Random[i][k] and Dict.has_key((j,k)):
                    Dict[(j,k)]=Dict[(j,k)]+1
                else:
                    Dict[(j,k)]=1

    #DF_nodelist=DF_nodelist.drop(DF_nodelist[DF_nodelist.Depthmap_Ref<113500].index)
    DF01=pd.DataFrame(Dict.items(),columns=['pairs', 'weights'])

    DF01 = DF01.drop(DF01[DF01.weights<Param].index)
    DF01.to_csv('GLA_Fuzzy_edgelist_p.csv',index=True)

def nx_fuzzy_membership_write():

    file=open("GLA_Fuzzy_edgelist_p.csv",'r')
    G=nx.read_weighted_edgelist(file,delimiter=',',nodetype=int)
    Component_SG=nx.connected_component_subgraphs(G)

    G2 = nx.Graph()
    x=1
    for i in Component_SG:
        for j in i.nodes():
            G2.add_node(j,attr=x)
        x=x+1

def nx_Subgraph_Modularity():
    #1. Using basic edgelist csv file
    file=open("GLA_meridian_edgelist_no_weights.csv",'r')
    #file=open("test02.csv",'r')
    #G=nx.read_edgelist(file,delimiter=',',nodetype=int,data=(('weight',float),))
    #G=nx.read_weighted_edgelist(file,delimiter=',',nodetype=int)
    G=nx.read_edgelist(file,delimiter=',',nodetype=int)



    #2. create community graphs
    dendo = community.generate_dendogram(G)
    SG04=community.partition_at_level(dendo,4)
    #Mod=community.best_partition(G)
    #{1: 0, 2: 1, 3: 1, 4: 0, 5: 2, 6: 2, 7: 3, 8: 3, 9: 3}
    #{1: 0, 2: 0, 3: 0, 4: 1, 5: 1, 6: 1, 7: 2, 8: 2, 9: 2}

    Dict={}
    for i in SG04:
        Dict[i]=SG04[i]

    #DF02 = pd.DataFrame(Dict)
    DF02 = pd.Series(Dict, name='Mod04')
    DF02.to_csv('GLA_noW_Mod04_p.csv',index=True)



    #f4=open("GLA_G_Mod04_p.txt", 'w')
    #f4.write(str(SG04))
    #f4.close


    #SubG=community.induced_graph(SG04,G)
    #SubG_p=community.best_partition(SubG)
    #Sub4=open("GLA_subG_Mod04_p.txt", 'w')
    #Sub4.write(str(SubG_p))
    #Sub4.close

def nx_modularity():

    #Read edgelist
    file=open("GLA_meridian_edgelist.csv",'r')
    file=open("test01.csv",'r')
    file=open("paris_seg_edgelist_p.csv",'r')
    G=nx.read_edgelist(file,delimiter=',',nodetype=int)
    #G=nx.read_adjlist

    #run best partition that optimise modularity without resolution definition
    file=open("London_Subgraph_Network.csv",'r')
    G=nx.read_edgelist(file,delimiter=',',nodetype=int,data=(('weight',float),))

    SG=community.best_partition(G)

    dendo = community.generate_dendogram(G)
    SG01=community.partition_at_level(dendo,1)
    SG02=community.partition_at_level(dendo,2)
    SG03=community.partition_at_level(dendo,3)
    SG04=community.partition_at_level(dendo,4)
    SG05=community.partition_at_level(dendo,5)
    SG06=community.partition_at_level(dendo,6)


    #open file and save

    f=open("GLA_seg_Mod_p02.txt", 'w')
    f.write(str(SG))
    f.close

    f1=open("GLA_seg_Mod01_p.txt", 'w')
    f1.write(str(SG01))
    f1.close

    f2=open("GLA_seg_Mod02_p.txt", 'w')
    f2.write(str(SG02))
    f2.close

    f3=open("GLA_seg_Mod03_p.txt", 'w')
    f3.write(str(SG03))
    f3.close

    f4=open("GLA_seg_Mod04_p.txt", 'w')
    f4.write(str(SG04))
    f4.close

    f5=open("GLA_seg_Mod05_p.txt", 'w')
    f5.write(str(SG05))
    f5.close

    #f6=open("Boston_Mod06_p.txt", 'w')
    #f6.write(str(SG06))
    #f6.close

def igraph_walktrap():

    g=igraph.Graph.Read_Ncol('GLA_meridian_edgelist02.csv',directed=False)

    WT30=igraph.Graph.community_walktrap(g,steps=30)
    WT30_p=WT30.as_clustering()
    ComDet_WT30_membership = WT30_p.membership
    writer = csv.writer(open("London_WT30_p.csv", "wb"))
    for name, membership in izip(g.vs["name"], ComDet_WT30_membership):
        writer.writerow([name, membership])

    #length = len(WT30_p)
    #i=0
    #CD_WT30_p=[]
    #while i<length:
        #CD_WT30_p.append(g.vs[WT30_p[i]]['name'])
        #i=i+1

    #csv_file = open("London_WT30_p.csv", "wb")
    #writer = csv.writer(csv_file)
    #writer.writerows(CD_WT30_p)
    #csv_file.close()

def igraph_label_propagation():

    g=igraph.Graph.Read_Ncol('GLA_meridian_edgelist02.csv',directed=False)

    # Label Propagation

    ComDet_LP=igraph.Graph.community_label_propagation(g)
    length = len(ComDet_LP)
    i=0
    ComDet_LP_p=[]
    while i<length:
        ComDet_LP_p.append(g.vs[ComDet_LP[i]]['name'])
        i=i+1

    csv_file = open("London_LP_p.txt", "wb")
    writer = csv.writer(csv_file)
    writer.writerows(ComDet_LP_p)

def igraph_infomap():

    g=igraph.Graph.Read_Ncol('GLA_meridian_edgelist02.csv',directed=False)

    # Infomap

    ComDet_IMap10=igraph.Graph.community_infomap(g,trials=5)
    ComDet_IMap10_membership = ComDet_IMap10.membership
    writer = csv.writer(open("London_IMap10_p.csv", "wb"))
    for name, membership in izip(g.vs["name"], ComDet_IMap10_membership):
        writer.writerow([name, membership])


    #length = len(ComDet_IMap10)
    #ComDet_IMap_p=ComDet_IMap.as_clustering()
    #i=0
    #ComDet_InfoMap10_p=[]
    #while i<length:
        #ComDet_InfoMap10_p.append(g.vs[ComDet_IMap10[i]]['name'])
        #i=i+1
    #csv_file = open("London_Info_Map10_p.csv", "wb")
    #writer = csv.writer(csv_file)
    #writer.writerows(ComDet_InfoMap10_p)
    #csv_file.close()

def igraph_spinglass():

    g=igraph.Graph.Read_Ncol('GLA_meridian_edgelist02.csv',directed=False)

    #spinglass

    ComDet_spinglass200=igraph.Graph.community_spinglass(g,spins=200)
    #ComDet_spinglass_p=ComDet_spinglass.as_clustering()

    ComDet_Spinglass200_membership = ComDet_spinglass200.membership
    writer = csv.writer(open("London_spinglass200_p.csv", "wb"))
    for name, membership in izip(g.vs["name"], ComDet_Spinglass200_membership):
        writer.writerow([name, membership])

    #length = len(ComDet_spinglass200)
    #i=0
    #ComDet_spinglass200_p=[]
    #while i<length:
        #ComDet_spinglass200_p.append(g.vs[ComDet_spinglass200[i]]['name'])
        #i=i+1

    #csv_file = open("London_spinglass200_p.txt", "wb")
    #writer = csv.writer(csv_file)
    #writer.writerows(ComDet_spinglass200_p)
    #csv_file.close()

def igraph_multilevel():

    g=igraph.Graph.Read_Ncol('GLA_meridian_edgelist02.csv',directed=False)

    #spinglass

    ComDet_multilevel=igraph.Graph.community_multilevel(g,return_levels=True)

    ComDet_multilevel01_membership = ComDet_multilevel[0].membership
    ComDet_multilevel02_membership = ComDet_multilevel[1].membership
    ComDet_multilevel03_membership = ComDet_multilevel[2].membership
    ComDet_multilevel04_membership = ComDet_multilevel[3].membership
    ComDet_multilevel05_membership = ComDet_multilevel[4].membership
    ComDet_multilevel06_membership = ComDet_multilevel[5].membership

    writer = csv.writer(open("London_multi01_p.csv", "wb"))
    for name, membership in izip(g.vs["name"], ComDet_multilevel01_membership):
        writer.writerow([name, membership])

    writer = csv.writer(open("London_multi02_p.csv", "wb"))
    for name, membership in izip(g.vs["name"], ComDet_multilevel02_membership):
        writer.writerow([name, membership])

    writer = csv.writer(open("London_multi03_p.csv", "wb"))
    for name, membership in izip(g.vs["name"], ComDet_multilevel03_membership):
        writer.writerow([name, membership])

    writer = csv.writer(open("London_multi04_p.csv", "wb"))
    for name, membership in izip(g.vs["name"], ComDet_multilevel04_membership):
        writer.writerow([name, membership])

    writer = csv.writer(open("London_multi05_p.csv", "wb"))
    for name, membership in izip(g.vs["name"], ComDet_multilevel05_membership):
        writer.writerow([name, membership])

    writer = csv.writer(open("London_multi06_p.csv", "wb"))
    for name, membership in izip(g.vs["name"], ComDet_multilevel06_membership):
        writer.writerow([name, membership])

def community_detection_others():
    # leading eigenvector

    # fast greedy doesn't work
    ComDet_FG=igraph.Graph.community_fastgreedy(g)
    # betweenness cut doesn't work
    ComDet_BC=igraph.Graph.community_edge_betweenness(g,directed=False)
    # too long
    ComDet_LE=igraph.Graph.community_leading_eigenvector(g)
    ComDet_OM=igraph.Graph.community_optimal_modularity(g)

def graph_neighbourhood():

    file=open("GLA_meridian_edgelist.csv",'r')
    g=igraph.Graph.Read_Ncol(file)

    g1=igraph.Graph.neighborhood(g,1)
    g1_p=g.vs[g1]['name']

    g2=igraph.Graph.neighbors(g,0)
    g2_p=g.vs[g2]['name']

    length = len(g.vs)
    i=0
    g2_p=[]
    while i<length:
        g2=igraph.Graph.neighbors(g,i)
        g2_p.append(g.vs[g2]['name'])
        i=i+1

    print g.summary

def matrix_edgelist():

    import pandas as pd
    csv01 = open("RUDD_Matrix_9502_index.csv")
    columns = csv01.readline().strip().split(',')[1:]
    f = csv.writer(open("RUDD_9502_Edgelist.csv", "wb+"))

    # this writes the matrix into edgelist
    for i, line in enumerate(csv01):
        tokens = line.strip().split(',')
        row = tokens[0]
        for column, cell in zip(columns[i:],tokens[i+1:]):
            f.writerow([row,column,cell])
            #this only reads
            #print '{},{},{}'.format(row,column,cell)


def combs(a, r):
    """
    Return successive r-length combinations of elements in the array a.
    Should produce the same output as array(list(combinations(a, r))), but
    faster.
    """
    a = np.asarray(a)
    dt = np.dtype([('', a.dtype)]*r)
    b = np.fromiter(combinations(a, r), dt)
    return b.view(a.dtype).reshape(-1, r)

    #dt=np.dtype('i,i,i')
    #a = np.fromiter(combinations([1,2,3],3), np.dtype=dt, np.count=-1)
    #a = np.fromiter(combinations([1,2,3],2),np.dtype=('f2',np.int32))

    #a=[1,2,3]
    #a = np.asarray(a)
    #dt=np.dtype([('',a.dtype)]*2)

    #np.fromiter(itertools.combinations([1,2,3],2),dt)

'''