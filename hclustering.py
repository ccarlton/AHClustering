import sys
import xml.dom.minidom
import random
import math
from data_types import ClusteringData

class Cluster:
    def __init__(self, npoints):
        self.points = npoints

    def size(self):
        print "Points: ", self.points
        size = len(self.points)
        return size 

class Binding:
    def __init__(self, indexes, iteration, height, pair):
        self.indexes = indexes
        self.iteration = iteration
        self.height = height
        self.pair = pair
        
class HierarchicalClusterer:
    def __init__(self, cluster_data):
        self.data = cluster_data
        self.document = xml.dom.minidom.Document()

    def cluster(self):
        clusters = []
        heights = []
        bindings = []
            
        i = 0    
        clusters.append([])
        for vec in self.data.vectors:
            row_items = vec.values
            clusters[i].append(Cluster([row_items]))

        while len(clusters[i]) > 1:
            distances = [None] * len(clusters[i])
            for x in range(len(clusters[i])):
                distances[x] = [None] * len(clusters[i])
            
            for j in range(0, len(clusters[i])):
                for k in range(j+1, len(clusters[i])):
                    distances[j][k] = self.shared_link_dist(clusters[i][j].points, clusters[i][k].points)
            
            min_index = self.distance_min(distances)
            heights.append(distances[min_index[0]][min_index[1]])
            bindings.append(Binding([min_index[0], min_index[1]], i, distances[min_index[0]][min_index[1]], [clusters[i][min_index[0]], clusters[i][min_index[1]]]))
            clusters.append([])
            for j in range(0, len(clusters[i])):
                if j != min_index[0] and j != min_index[1]:
                    clusters[i+1].append(clusters[i][j])
                elif j == min_index[1]:
                    temp = clusters[i][min_index[0]].points + clusters[i][min_index[1]].points
                    clusters[i+1].append(Cluster(temp))
            i += 1  
        
        self.clusters = clusters 
        self.heights = heights
        self.bindings = bindings
        print len(heights)

    def build_xml(self, iteration, ):
        curNode = None
        for i in range(len(self.clusters)-1):
            cluster1 = self.clusters[i][self.bindings[i-1].indexes[0]]
            cluster2 = self.clusters[i][self.bindings[i-1].indexes[1]]
            height = self.bindings[i-1].height
            
            node1 = self.document.createElement('node')
            node1.setAttribute('height', str(height))

            if curNode != None:
                curNode.appendChild(node1)

            curNode = node1
 
            if (len(cluster1.points) == 1):
                leaf1 = self.document.createElement('leaf')
                node1.appendChild(leaf1)
            if (len(cluster2.points) == 1):
                leaf2 = self.document.createElement('leaf')
                node1.appendChild(leaf2)
            
 #   for i in range(len(ahclusterfier.clusters)):
 #       print "\nClusters[",i,"]: "
 #       if i >= 1:
 #           print "Height: ", ahclusterfier.bindings[i-1].height
 #           print "Indexes: ", ahclusterfier.bindings[i-2].indexes
 #       for j in range(len(ahclusterfier.clusters[i])):
 #           print "    ",j,": ", ahclusterfier.clusters[i][j].points
   
#    top_ind = (len(ahclusterfier.clusters)-1)
            #print cluster
            #if len(self.clusters)-1 == iteration:
            #    tree = self.document.createElement('tree')
            #    self.document.appendChild(tree);
            #    
            #    print "len(self.clusters[",iteration,"]: ", len(self.clusters[iteration])
            #    print "len(self.clusters[",iteration-1,"]: ", len(self.clusters[iteration-1])
            #    print "Indexes: ", self.bindings[iteration-1].indexes
            #    cluster1 = self.clusters[iteration-1][self.bindings[iteration-1].indexes[0]]
            #    cluster2 = self.clusters[iteration-1][self.bindings[iteration-1].indexes[1]]
            #    tree.appendChild(self.build_xml(iteration-1, cluster1))
            #    tree.appendChild(self.build_xml(iteration-1, cluster2))

            #elif len(cluster.points) > 1:
              #  node = self.document.createElement('node') 
              #  node.setAttribute('height', str(self.bindings[iteration-1].height))

              #  print "Indexes", self.bindings[iteration-1].indexes
              #  print "len(self.clusters[",iteration,"]: ", len(self.clusters[iteration])
              #  print "len(cluster.points): ", len(cluster.points)
              #  print "custer.points: ", cluster.points
              #  cluster1 = self.clusters[iteration-1][self.bindings[iteration-1].indexes[0]]
              #  cluster2 = self.clusters[iteration-1][self.bindings[iteration-1].indexes[1]]

             #   node.appendChild(self.build_xml(iteration-1, cluster1))
             #   node.appendChild(self.build_xml(iteration-1, cluster2))
             #   return node
            #else:
            #    print str(cluster.points)
            #    return self.document.createElement('test')
         #       print "Indexes", self.bindings[iteration].indexes
         #       #print str(cluster.points)
  # 
   #             leaf = self.document.createElement('leaf')
    #            leaf.setAttribute('height', str(0))
     #           #leaf.setAttribute('data', str(cluster.points))           
      #          return leaf 

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
            print "Height: ", ahclusterfier.bindings[i-1].height
            print "Indexes: ", ahclusterfier.bindings[i-1].indexes
        for j in range(len(ahclusterfier.clusters[i])):
            print "    ",j,": ", ahclusterfier.clusters[i][j].points
   
    #top_ind = (len(ahclusterfier.clusters)-1)
    #ahclusterfier.build_xml(top_ind, ahclusterfier.clusters[top_ind])
    #print ahclusterfier.document.toprettyxml();

if __name__ == '__main__':
    main()
