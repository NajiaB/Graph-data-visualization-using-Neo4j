
# -----------------LINK DETECTION : LOGISTIC REGRESSION / RANDOM FOREST / MLP

#creation de notre base/projet
rq0="""CALL gds.graph.project('MonGraph2',
['User'],
[{VOTED: {orientation: 'UNDIRECTED', properties: ['idUser']}}]
);"""
graph.run(rq0)


rq1= """CALL gds.beta.pipeline.linkPrediction.create('lp-pipeline');"""
graph.run(rq1)

rq2="""CALL gds.beta.pipeline.linkPrediction.addNodeProperty('lp-pipeline',
'fastRP', {
  mutateProperty:     'embedding',
  embeddingDimension: 56,
  randomSeed:         42
}) YIELD nodePropertySteps;"""
graph.run(rq2)

#on rajouter une propriété : le degré (nbre de edges) et autres
rq3="""CALL gds.beta.pipeline.linkPrediction.addNodeProperty('lp-pipeline',
'degree', {
  mutateProperty: 'degree'
}) YIELD nodePropertySteps;"""
graph.run(rq3)

rq4="""CALL gds.beta.pipeline.linkPrediction.addNodeProperty('lp-pipeline',
'alpha.scaleProperties', {
  nodeProperties: ['degree'],
  mutateProperty: 'scaledDegree',
  scaler:         'MinMax'
}) YIELD nodePropertySteps;
"""
graph.run(rq4)

rq5="""CALL gds.beta.pipeline.linkPrediction.addFeature('lp-pipeline',
'HADAMARD', {
  nodeProperties: ['embedding']
}) YIELD featureSteps;"""
graph.run(rq5)


rq6="""CALL gds.beta.pipeline.linkPrediction.addFeature('lp-pipeline',
'HADAMARD', {
  nodeProperties: ['scaledDegree']
}) YIELD featureSteps;"""
graph.run(rq6)

#split des donnees

rq7="""CALL gds.beta.pipeline.linkPrediction.configureSplit('lp-pipeline', {
  testFraction:    0.1,
  trainFraction:   0.1,
  validationFolds: 3
}) YIELD splitConfig;"""
graph.run(rq7)

#rajouter une regression logistique au modèle
rq8="""CALL gds.beta.pipeline.linkPrediction.addLogisticRegression('lp-pipeline')
YIELD parameterSpace;"""

graph.run(rq8)

#rajouter un random forest (n=10)
rq9="""
CALL gds.alpha.pipeline.linkPrediction.addRandomForest('lp-pipeline', {numberOfDecisionTrees: 10})
YIELD parameterSpace;

"""
graph.run(rq9)

#rajouter un reseau de neurones multicouches
rq10="""
CALL gds.alpha.pipeline.linkPrediction.addMLP('lp-pipeline',
{hiddenLayerSizes: [4, 2], penalty: 1, patience: 2})
YIELD parameterSpace;"""
graph.run(rq10)

#memoire necessaire
rq11="""CALL gds.beta.pipeline.linkPrediction.train.estimate('MonGraph2', {
pipeline:  'lp-pipeline',
modelName: 'lp-pipeline-model',
targetRelationshipType: 'VOTED'
}) YIELD requiredMemory;"""
graph.run(rq11)

#entrainer le modèele et renvoie le meilleur modele (ici : random forest)

rq12="""CALL gds.beta.pipeline.linkPrediction.train('MonGraph2', {
  pipeline:   'lp-pipeline',
  modelName:  'lp-pipeline-model2',
  metrics:    ['AUCPR'],
  targetRelationshipType: 'VOTED',

  randomSeed: 42
}) YIELD modelInfo, modelSelectionStats
RETURN
  modelInfo.bestParameters AS winningModel,
  modelInfo.metrics.AUCPR.train.avg AS avgTrainScore,
  modelInfo.metrics.AUCPR.outerTrain AS outerTrainScore,
  modelInfo.metrics.AUCPR.test AS testScore,
  [candidate IN modelSelectionStats.modelCandidates | candidate.metrics.AUCPR.validation.avg] AS validationScores;"""
graph.run(rq12)

#prédire des links en utilisant notre pipeline:

rq13="""CALL gds.beta.pipeline.linkPrediction.predict.mutate('MonGraph', {
  modelName:              'lp-pipeline-modell',
  mutateRelationshipType: '2VOTED_APPROX_PREDICTED',
  topN:                   10000,
  threshold:              0.45
}) YIELD relationshipsWritten, samplingStats;"""
graph.run(rq13)
