import sys
import xml.dom.minidom
import random
import math
from data_types import ClusteringData

class HierarchicalClusterer:
    def __init__(self, cluster_data):
        self.data = cluster_data
        self.document = xml.dom.minidom.Document()

    def cluster(self):
        clusters = []
        heights = []
            
        i = 0    
        clusters.append([])
        for vec in self.data.vectors:
            row_items = vec.values
            clusters[i].append([row_items])

        while len(clusters[i]) > 1:
            distances = [None] * len(clusters[i])
            for x in range(len(clusters[i])):
                distances[x] = [None] * len(clusters[i])
            
            for j in range(0, len(clusters[i])):
                for k in range(j+1, len(clusters[i])):
                    distances[j][k] = self.shared_link_dist(clusters[i][j],clusters[i][k])
            
            min_index = self.distance_min(distances)
            heights.append(distances[min_index[0]][min_index[1]])

            clusters.append([])
            for j in range(0, len(clusters[i])):
                if j != min_index[0] and j != min_index[1]:
                    clusters[i+1].append(clusters[i][j])
                elif j == min_index[1]:
                    test =clusters[i][min_index[0]] + clusters[i][min_index[1]]
                    clusters[i+1].append(test) 
            i += 1  
        self.clusters = clusters 
        self.heights = heights
        print len(heights)

    def build_xml(self, currentNode, c_ind):

        print "Heights: ", self.heights
        print "Last cluster: ", self.clusters[-1]
        print "cind: ", c_ind
        print self.clusters[c_ind]
        print self.heights[c_ind]
        #self.build_xml(currentNode, c_ind-1)

        #if c_ind == len(self.heights)-1:
        #    node = ahclusterfier.document.createElement('tree')
        #    node.setAttribute('height', ahclusterfier.heights[c_ind])
            
       
       # node = self.document.createElement('tree')
       # node.setAttribute('height', self.heights[i])
       # currentNode.appendChild(node)

    def ndistance(self, p1, p2):
        dist = 0;
        for i in range(len(p1)):
            dist += (float(p2[i]) - float(p1[i]))*(float(p2[i]) - float(p1[i]))
        dist = math.sqrt(dist)
        return dist
 
    def shared_link_dist(self, c1, c2):
        min_dist = float("inf")

        for i in range(len(c1)):
            ele_c1 = c1[i]
            for j in range(len(c2)):
                ele_c2 = c2[j]
                dist = self.ndistance(c1[i], c2[j])
                if dist <= min_dist:
                    min_dist = dist
        return min_dist   
    
    def distance_min(self, distances):
        min_dist = float("inf") 
        min_pair = [-1,-1]
        for i in range(0, len(distances)):
            for j in range(0, len(distances[i])):
                if distances[i][j] != None and distances[i][j] <= min_dist:
                    min_dist = distances[i][j]
                    min_pair[0] = i
                    min_pair[1] = j
                 
        return min_pair                                      

def main():
    filename = 0
    threshold = 0

    if len(sys.argv) > 3 or len(sys.argv) < 2:
        print "Usage: python hclustering.py <filename> [<threshold>]"
        return    
    
    if len(sys.argv) == 3:
        threshold = float(sys.argv[2])

    cluster_data = ClusteringData(sys.argv[1])
    cluster_data.parse_vectors()
     
    ahclusterfier = HierarchicalClusterer(cluster_data)
    ahclusterfier.cluster()

    for i in range(len(ahclusterfier.clusters)):
        print "\nClusters[",i,"]: "
        if i >= 1:
            print "Height: ", ahclusterfier.heights[i-1]
        for j in range(len(ahclusterfier.clusters[i])):
            print "    ",j,": ", ahclusterfier.clusters[i][j]
    
    #ahclusterfier.build_xml(ahclusterfier.document, len(ahclusterfier.heights)-1);

if __name__ == '__main__':
    main()
