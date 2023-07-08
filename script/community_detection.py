#------------- COMMUNITY DETECTION : HIERARCHICAL CLUSTERING
 #creation de notre base/projet
   
rq1 = """
CALL gds.graph.project(
    'myGraph2',
    'User',
    {
        VOTED: {
            orientation: 'UNDIRECTED'
        }
    },
    {
        
        relationshipProperties: 'valeurvote'
    }
)
"""
graph.run(rq1)


rq2 = """
CALL gds.louvain.stream('myGraph2')
YIELD nodeId, communityId, intermediateCommunityIds
RETURN gds.util.asNode(nodeId).name AS name, communityId, intermediateCommunityIds
ORDER BY name ASC
"""
graph.run(rq2)


#calcule le nombre de communautés
rq3 = """
CALL gds.louvain.stats('myGraph2')
YIELD communityCount
"""
graph.run(rq3)

#rajoute une propriété à mes noeuds : communauté ==> cela permet de visualiser les clusters en mettant de la couleur par exemple
rq4 = """
CALL gds.louvain.write('myGraph2',
{writeProperty:'louv_community'}
)
YIELD communityCount, modularity, modularities
"""
graph.run(rq4)
