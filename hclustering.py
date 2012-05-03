import sys
import xml.dom.minidom
from data_types import ClusteringData

class HierarchicalClusterer:
    def __init__(self, cluster_data):
        self.data = cluster_data
        self.document = xml.dom.minidom.Document()

    def cluster():
        clusters = []
        distances = []
            
        i = 0    
        clusters.append([])
        for vec in row.vectors:
            row_items = vec.values
            clusters.append[i].append(row_items)
             
        while len(clusters[i]) > 1:
            for j in range(0, len(clusters[i])):
                for k in range(j+1, len(clusters[i])):
                    distances[j][k] = distance(clusters[i][j],clusters[i][k])
            
            min_index = distance_min(distances)
            clusters.append([])
            for j in range(0, len(clusters[i])):
                if j != min_index[0] and j != min_index[1]:
                    clusters[i+1][j] = clusters[i][j]
                elif j == min_index[1]:
                    clusters[i+1][j] = clusters[i][min_index[0]][min_index[1]] 
    
    def distance(c1, c2):
        return 0
    
    def distance_min(distances):
        min_dist = float("inf") 
        min_pair = []
        for i in range(0, len(distances)):
            for j in range(0, len(distances[i])):
                if distances[i][j] <= min_dist:
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
    cluster_data.parse_vectors();
     

if __name__ == '__main__':
    main()
