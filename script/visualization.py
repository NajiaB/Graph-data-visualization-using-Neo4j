import matplotlib.pyplot as plt
from py2neo import *
import pandas as pd
from pandas import DataFrame
import datetime
from datetime import datetime


#SCHEMA : visualisation :
rq = 'call db.schema.visualization()'
graph.run(rq)

#nominations mutuelles : Est-ce que les wiki-users se nominent mutuellement ?
rq = """
Match (nominee1:User)-[n1:NOMINATED]-(nominee2:User),
      (nominee2:User)-[n2:NOMINATED]-(nominee1:User)
      return (nominee1)--(nominee2)
  """
data = graph.run(rq).data()
len(data) # contient 20 elements : 20 nominations 2 par 2 ==> 10 personnes se sont 'entrenominées' deux par deux (voir graphe car plus clair)










#----------------ceux qui ont le plus participé à une élection (nominés) :
rq="""
MATCH (user)-[v:VOTED]->()
WITH user, count(DISTINCT v.IdElection) AS nb_voting ,collect(DISTINCT v.IdElection) AS election_number
MATCH ()-[p:VOTED]->(user)
WITH user, nb_voting,election_number, count(DISTINCT p.IdElection) AS nb_participation ,collect(DISTINCT p.IdElection) AS election_participation
RETURN user.name,nb_voting,election_number,nb_participation,election_participation
ORDER BY nb_participation DESC limit 10
"""
data = graph.run(rq).to_data_frame()
ax = data.plot(x='user.name',y='nb_participation',kind="bar") #c'est encore l'utilisateur silva1979 qui a participé le plus de fois (5 fois)  ==> utilisateur très actif


# ---------les users qui ont le plus voté : 
rq="""
MATCH (user)-[v:VOTED]->()
WITH user, count(v.IdElection) AS nb_voting 

RETURN user.name,nb_voting
ORDER BY nb_voting DESC limit 10
"""
data = graph.run(rq).to_data_frame()
ax = data.plot(x='user.name',y='nb_voting',kind="bar") #c'est encore l'utilisateur silva1979 qui a participé le plus de fois (5 fois)  ==> utilisateur très actif


#----------les users qui ont le plus nominés d'autres users
rq ="""
MATCH (user)-[n:NOMINATED]->()
RETURN user.name,count(n) AS nb_nomi
ORDER BY nb_nomi DESC limit 10
"""
data = graph.run(rq).to_data_frame()
ax = data.plot(x='user.name',y='nb_nomi',kind="bar") 

#-------------------ceux qui ont le plus voté ET participé
rq="""
MATCH (user)-[v:VOTED]->()
WITH user, count(DISTINCT v.IdElection) AS nb_voting ,collect(DISTINCT v.IdElection) AS election_number
MATCH ()-[p:VOTED]->(user)
WITH user, nb_voting,election_number, count(DISTINCT p.IdElection) AS nb_participation ,collect(DISTINCT p.IdElection) AS election_participation
RETURN user.name,nb_voting,election_number,nb_participation,election_participation
ORDER BY nb_voting DESC limit 5
"""
data = graph.run(rq).to_data_frame()
ax = data.plot(x='user.name',kind="bar") #ac'est l'utilisateur silva qui a voté le plus de fois


#----------------nominateur qui nomine des gagnants 
rq = "MATCH (n1:User)-[r1:NOMINATED]-(n2:User) WHERE EXISTS { MATCH (n2:User)-[r:WON]->()} RETURN (n1)   "
data = graph.run(rq).to_data_frame()

#-------------nombre d’election WON/LOST
rq = "MATCH (u1:User)-[r1:WON]->(e1:Election)  MATCH (u2:User)-[r2:LOST]->(e2:Election) RETURN DISTINCT   COUNT(DISTINCT r1) AS Election_Won , count(DISTINCT r2) AS Election_Lost"
data = graph.run(rq).to_data_frame()
data2 = pd.DataFrame({'won_lost': ['Election_Won','Election_Lost'],
                   'Election': [data.iat[0,0],data.iat[0,1]]})
ax = data2.groupby(['won_lost']).sum().plot(kind="pie",y='Election',autopct='%1.0f%%',
                                colors = ['red', 'pink', 'steelblue']) 

#n-----------ominations mutuelles : Est-ce que les wiki-users se nominent mutuellement ? amitiés ?
rq = """
Match (nominee1:User)-[n1:NOMINATED]-(nominee2:User),
      (nominee2:User)-[n2:NOMINATED]-(nominee1:User)
      return (nominee1)--(nominee2)
  """
data = graph.run(rq).data()
len(data) # contient 20 elements : 20 nominations 2 par 2 ==> 10 personnes se sont 'entrenominées' deux par deux (voir graphe car plus clair)




#-------nombre d’election par annee 👍
rq="MATCH (n:User)-[r:VOTED]->() WITH r.DateElection AS DateElection, count(DISTINCT n) AS NombreElection RETURN DateElection AS DateElection, NombreElection ORDER BY DateElection"
df = graph.run(rq).to_data_frame()
df['DateElection']=[int(i) for i in df['DateElection']]

df.plot(kind='bar',x='DateElection',y='NombreElection') #bar plot
plt.plot(df['DateElection'],df['NombreElection'])

