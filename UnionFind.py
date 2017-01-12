"""
Generic union-find data structure
"""
class UnionFind:
    def __init__(self, vertices):
        self.components = dict()

        for vertex in vertices:
            self.components[vertex] = vertex

    """ Parent access with path compression """
    def find(self, vertex):
        if self.components[vertex] == vertex:
            return vertex

        # Path compression
        else:
            self.components[vertex] = self.find( self.components[vertex] )
            return self.components[vertex]

    """ Provides merging functionality """
    def merge(self, u, v):
        cu = self.find(u)
        cv = self.find(v)

        self.components[cu] = cv

    """ Generator for all roots """
    def roots(self):
        for vertex in sorted( self.components.keys() ):
            if self.find(vertex) == vertex:
                yield vertex

    """ Gets all vertices of a specific connected component """
    def vertices(self, root):
        result = list()

        for vertex in self.components.keys():
            if self.find(vertex) == root:
                result.append( vertex )

        return sorted(result)
