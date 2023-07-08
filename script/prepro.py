# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 11:14:29 2022

@author: BOUADDOUCH Najia
"""
import pandas as pd

df = pd.read_csv("C:/Users/BOUADDOUCH Najia/Documents/Neo4j/wikivoteBRUTE.csv",sep=';',encoding="ISO-8859-1",header=None)


         

L=[]
for i in range(len(df[0])):
    if pd.isna(df[0][i]) :
        L.append(i)


df=df.drop(df.columns[5],axis=1)

dfs=[]
k=0
for i in L :
    dfs.append(df.iloc[k:i,:])
    k=i+1


 
k=1
for dataframe in dfs:
    y=dataframe.index[0]
    dataframe['IdElection'] = k
    dataframe['DateElection']=dataframe[1][y+1]
    dataframe['Electedornot'] = dataframe[1][y]
    dataframe['IdNominated'] = dataframe[1][y+2]
    dataframe['nominated'] = dataframe[2][y+2]
    dataframe['nominator'] = dataframe[2][y+3]
    dataframe['IdNominator'] = dataframe[1][y+3]
    k=k+1
    

    dataframe=dataframe.drop([y,y+1,y+2,y+3],axis=0,inplace=True)
    
a=pd.concat(dfs,axis=0)    
len(a)

a.to_csv(r'C:/Users/BOUADDOUCH Najia/Documents/Neo4j/newcsv.csv')

#creation dun csv users 
data=pd.read_csv('C:/Users/BOUADDOUCH Najia/Documents/Neo4j/newcsv.csv',sep=';')


df1=data.iloc[:,[1,4]]
df1.drop_duplicates(inplace=True)

df2=data.iloc[:,[6,7]]
df2.drop_duplicates(inplace=True)

df3=data.iloc[:,[9,8]]
df3.drop_duplicates(inplace=True)
L_dfs=[df1,df2,df3]

df_users=pd.concat(L_dfs,axis=0,ignore_index=True)
df_users.to_csv(r'C:/Users/BOUADDOUCH Najia/Documents/Neo4j/users.csv')

df_users=pd.read_csv('C:/Users/BOUADDOUCH Najia/Documents/Neo4j/users.csv',sep=';')

df_users.drop_duplicates(inplace=True)
df_users.to_csv(r'C:/Users/BOUADDOUCH Najia/Documents/Neo4j/usersfinal.csv')


data=pd.read_csv('C:/Users/BOUADDOUCH Najia/Documents/Neo4j/wikivote.csv',sep=';')

#csv elections

df1=data.iloc[:,[0,6,7,8]]
df1.drop_duplicates(inplace=True)
df1.to_csv(r'C:/Users/BOUADDOUCH Najia/Documents/Neo4j/election.csv')
