import itertools

from graph_tool.all import Graph
from analysis.src.data.data_tools import flatten

class TextCoocurrenceGraph(Graph):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def window(seq, n=3):
	"""window
	Yields a sliding window (of width n) over data from the iterable
	   s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...

        Args:
            seq (:obj:`iter`): Sequence to move the window across.

        Examples:
            >>> doc = ['rockets', 'and', 'moonshots', 'blame', 'it', 'on',
                    'the', 'have', 'nots']

            >>> list(window(doc))
            [('rockets', 'and', 'moonshots'),
             ('and', 'moonshots', 'blame'),
             ('moonshots', 'blame', 'it'),
             ('it, 'on', 'the'),
             ('the', 'have', 'nots),
             ]
	"""
	it = iter(seq)
	result = tuple(itertools.islice(it, n))
	if len(result) == n:
	    yield result
	for elem in it:
	    result = result[1:] + (elem,)
	    yield result

    def seq2coocurrences(self, seq):
        """seq2coocurrences
        Converts an iterable sequence to a list of tuples that represent
        all the possible coocurrences.

        Args:
            seq (:obj:`iter`): List of elements 

        Returns:
            coocurrences (:obj:`list` of :obj:`tuple`): List of tuples. Each
                tuple is sorted.

        Examples:
            >>> doc = ['me', 'myself', 'irene']

            >>> seq2coocurrence(doc)
            [('me', 'myself'), ('irene', 'myself'), ('irene', 'me')]
        """
	combos = list(itertools.combinations(set(seq), r=2))
	coocurrences = list(set([tuple(sorted(c)) for c in combos]))
	return coocurrences

    def sliding_window_coocurrences(docs, n=3):
            """sliding_window_coocurrences
            Converts a documents in a corpus into lists of coocurrence tuples 
            using a sliding window method. The window moves across each 
            document, and on each iteration, links the term at the centre of 
            each window with the terms on either side.
    
            Args:
                docs (:obj:`iter` of :obj:`iter` of :obj:`str`): A corpus of
                    documents.
                n (int): Size of the window.
    
            Returns:
                coocurrences:

            Examples:
                
            """
	coocurrences = []
	for doc in docs:
	    doc_indices = range(len(doc))
	    doc_indices = window(doc_indices, n=n)
	    doc_indices = flatten([seq2coocurrences(t) for t in doc_indices])
	    doc = [sorted((doc[a], doc[b])) for a, b in list(set(doc_indices))]
	    doc = [tuple((a, b)) for a, b in doc if a !=b]
	    coocurrences.append(doc)
	return coocurrences

    def edge_coocurrence_counts(coocurrences):
	"""coocurrence_counts
	Takes a corpus of document coocurrence combinations and returns a
	Counter object for them across the entire corpus.
	
	Args:
	    coocurrences (:obj:`list` of :obj:`list` of :obj:`tuple`): 
		Corpus of documents expressed as their coocurrence pairs.
		
	Returns:
	    coocurrence_counts (:obj:`Counter`): Counter with keys as edges
		and values as number of coocurrences between the two vertices.
	"""
	coocurrence_counts = Counter(flatten(coocurrences))
	return coocurrence_counts

    def vertex_degree_centrality(coocurrence_counts):
	"""vertex_degree_centrality
	Takes a Counter of edge coocurrences and returns the degree centrality
	for each vertex.
	
	Args:
	    coocurrence_counts (:obj:`Counter`): Counter with keys as edges
		and values as number of coocurrences between the two vertices.
		
	Returns: 
	    vertex_degrees (:obj:`Counter`): Counter with keys as vertices
		and values as degree centralities.
	"""
	vertex_degrees = Counter()
	for vertices, count in coocurrence_counts.items():
	    v_0 = vertices[0]
	    v_1 = vertices[1]
	    if v_0 in vertex_degrees:
		vertex_degrees[v_0] += 1
	    else:
		vertex_degrees[v_0] = 1
		
	    if v_1 in vertex_degrees:
		vertex_degrees[v_1] += 1
	    else:
		vertex_degrees[v_1] = 1

            self.n_vertices = 
	return vertex_degrees

    def vertex_coocurrence_centrality(coocurrence_counts):
	"""vertex_coocurrence_centrality
	Takes a Counter of edge cooccurences and returns the coocurrence centrality
	for each vertex. This is a summation of all coocurrences for each vertex.
	
	Args:
	    coocurrence_counts (:obj:`Counter`): Counter with keys as edges
		and values as number of coocurrences between the two vertices.
		
	Returns:
	    vertex_coocurrences (:obj:`Counter`): Counter with keys as vertices
		and values as number of coocurrences.
	"""
	
	vertex_coocurrences = Counter()
	for vertices, count in coocurrence_counts.items():
	    v_0 = vertices[0]
	    v_1 = vertices[1]
	    if v_0 in vertex_coocurrences:
		vertex_coocurrences[v_0] += count
	    else:
		vertex_coocurrences[v_0] = count
	    if v_1 in vertex_coocurrences:
		vertex_coocurrences[v_1] += count
	    else:
		vertex_coocurrences[v_1] = count
            self.vertex_coocurrences = vertex_coocurrences
	return vertex_coocurrences

    def corpus2graph(self, corpus, dictionary, method='window', norm=True, **kwargs):
        id_corpus = [dictionary.doc2idx(d) for d in corpus]
        if method == 'window':
            coocurrences = self.sliding_window_coocurrences(id_corpus, **kwargs)

        edges = list(set(flatten(coocurrences)))
        edge_coocurrences = self.edge_coocurrence_counts(coocurrences)
        vertex_degrees = self.vertex_degree_centralitiy(edge_coocurrences)
        vertex_coocurrences = self.vertex_coocurrence_centrality(coocurrences)

        n_vertices = len(vertex_degrees)
        n_edges = len(coocurrences)
        n_coocurrences = len(flatten(coocurrences))

        self.add_vertex(n_vertices)
        self.add_edge_list(edges)

        if norm:
            association_strength_prop = self.new_edge_property("float")

            for s, t in edges:
                association_strength_prop[self.edge(s, t)] = assoc_strength(
                        n_coocurrences,
                        edge_coocurrences[tuple(sorted([s, t]))],
                        vertex_coocurrences[s],
                        vertex_coocurrences[t]
                        )
                self.edge_properties['association_strength'] = association_strength_prop
