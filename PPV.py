# programme avec python qui fait la classification en utilisant la methode des k plus proche voisin
 
import csv
import random
import math
import operator
 
 # une fonction qui prepare le data set iris et le shuflling ou bien le random
def loadDataset(filename, split, trainingSet=[] , testSet=[]):
	with open(filename, 'rt') as csvfile:
	    lines = csv.reader(csvfile)
	    dataset = list(lines)
	    for x in range(len(dataset)-1):
	        for y in range(4):
	            dataset[x][y] = float(dataset[x][y])
	        if random.random() < split:
	            trainingSet.append(dataset[x])
	        else:
	            testSet.append(dataset[x])
 
 
 #une fonction qui calcule la distance entre deux noeuds donnee
def euclideanDistance(instance1, instance2, length):
	distance = 0
	for x in range(length):
		distance += pow((instance1[x] - instance2[x]), 2)
	return math.sqrt(distance)
 

 #une fonction qui nous retourne les k voisin 
def getNeighbors(trainingSet, testInstance, k):
	distances = []
	length = len(testInstance)-1
	for x in range(len(trainingSet)):
		dist = euclideanDistance(testInstance, trainingSet[x], length)
		distances.append((trainingSet[x], dist))
	distances.sort(key=operator.itemgetter(1))
	neighbors = []
	for x in range(k):
		neighbors.append(distances[x][0])
	return neighbors
 
 #voir le correct vote ou bien reponse de chaque voisin 
def getResponse(neighbors):
	classVotes = {}
	for x in range(len(neighbors)):
		response = neighbors[x][-1]
		if response in classVotes:
			classVotes[response] += 1
		else:
			classVotes[response] = 1
	sortedVotes = sorted(classVotes.items(), key=operator.itemgetter(1), reverse=True)
	return sortedVotes[0][0]
 

 #fonction qui calcule la precition de la classification
def getAccuracy(testSet, predictions):
	correct = 0
	for x in range(len(testSet)):
		if testSet[x][-1] == predictions[x]:
			correct += 1
	return (correct/float(len(testSet))) * 100.0
	

#le main qui contient le tt
def main():
	# prepare data
	trainingSet=[]
	testSet=[]
	split = 0.67
	loadDataset('iris.data', split, trainingSet, testSet)
	print('Train set: ' + repr(len(trainingSet)))
	print('Test set: ' + repr(len(testSet)))
	# generate predictions
	predictions=[]
	#on pris les 3 plus proche voisin 
	k = 3
	for x in range(len(testSet)):
		#on recupere les 3 plus proche voisin du noeud courant 
		neighbors = getNeighbors(trainingSet, testSet[x], k)
		#on prend la reponse de chaque voisin sa validité
		result = getResponse(neighbors)
		#on calcule la precision de la prediction
		predictions.append(result)
		#un printf du resultat , esq on a bien classe le noeud ou pas
		print('> predicted=' + repr(result) + ', actual=' + repr(testSet[x][-1]))
	#la precision total
	accuracy = getAccuracy(testSet, predictions)
	print('Accuracy: ' + repr(accuracy) + '%')
	
#notre point d'entree
main()