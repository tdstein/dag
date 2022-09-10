from unittest import TestCase

from dag import DAG


class CreateTestCase(TestCase):
    def test_single(self):
        arr = [('A', [])]
        dag = DAG(arr)
        self.assertEqual(dag.graph, {'A': []})

    def test_simple(self):
        arr = [
            ('A', []),
            ('B', ['A']),
            ('C', ['B'])
        ]
        dag = DAG(arr)
        self.assertEqual(dag.graph, {
            'A': [],
            'B': ['A'],
            'C': ['B']
        })

    def test_simple_invalid(self):
        arr = [
            ('A', []),
            ('C', ['B']),
            ('B', ['A'])
        ]
        with self.assertRaises(RuntimeError):
            DAG(arr)

    def test_out_of_order(self):
        arr = arr = [
            ('B', ['A']),
            ('C', ['B']),
            ('A', []),
        ]
        with self.assertRaises(RuntimeError):
            DAG(arr)

    def test_complex(self):
        arr = [
            ('A', []),
            ('B', ['A']),
            ('C', ['B']),
            ('D', []),
            ('E', ['D']),
            ('F', ['C', 'E']),
            ('G', ['F']),
            ('H', ['G']),
        ]
        dag = DAG(arr)
        self.assertEqual(dag.graph, {
            'A': [],
            'B': ['A'],
            'C': ['B'],
            'D': [],
            'E': ['D'],
            'F': ['C', 'E'],
            'G': ['F'],
            'H': ['G']
        })

    def test_ambiguous(self):
        dag1 = DAG([
            ('5', []),
            ('7', []),
            ('3', []),
            ('11', ['5', '7']),
            ('8', ['3', '7']),
            ('2', ['11']),
            ('9', ['8', '11']),
            ('10', ['3', '11']),
        ])

        dag2 = DAG([
            ('3', []),
            ('5', []),
            ('7', []),
            ('11', ['5', '7']),
            ('8', ['3', '7']),
            ('2', ['11']),
            ('9', ['8', '11']),
            ('10', ['3', '11']),
        ])

        dag3 = DAG([
            ('5', []),
            ('7', []),
            ('3', []),
            ('8', ['3', '7']),
            ('11', ['5', '7']),
            ('10', ['3', '11']),
            ('9', ['8', '11']),
            ('2', ['11']),
        ])

        dag4 = DAG([
            ('7', []),
            ('5', []),
            ('11', ['5', '7']),
            ('3', []),
            ('10', ['3', '11']),
            ('8', ['3', '7']),
            ('9', ['8', '11']),
            ('2', ['11']),
        ])

        dag5 = DAG([
            ('5', []),
            ('7', []),
            ('11', ['5', '7']),
            ('2', ['11']),
            ('3', []),
            ('8', ['3', '7']),
            ('9', ['8', '11']),
            ('10', ['3', '11']),
        ])

        dag6 = DAG([
            ('3', []),
            ('7', []),
            ('8', ['3', '7']),
            ('5', []),
            ('11', ['5', '7']),
            ('10', ['3', '11']),
            ('9', ['8', '11']),
            ('2', ['11']),
        ])

        self.assertEqual(dag1.graph, dag2.graph)
        self.assertEqual(dag2.graph, dag3.graph)
        self.assertEqual(dag3.graph, dag4.graph)
        self.assertEqual(dag4.graph, dag5.graph)
        self.assertEqual(dag5.graph, dag6.graph)


class GetLeavesTestCase(TestCase):
    def test_single(self):
        arr = [('A', [])]
        dag = DAG(arr)
        leaves = dag.get_leaves()
        self.assertEqual(leaves, {'A'})

    def test_simple(self):
        arr = [
            ('A', []),
            ('B', ['A']),
            ('C', ['B'])
        ]
        dag = DAG(arr)
        leaves = dag.get_leaves()
        self.assertEqual(leaves, {'C'})

    def test_simple_two(self):
        arr = [
            ('A', []),
            ('B', ['A']),
            ('C', ['A'])
        ]
        dag = DAG(arr)
        leaves = dag.get_leaves()
        self.assertEqual(leaves, {'B', 'C'})

    def test_simple_three(self):
        arr = [
            ('A', []),
            ('B', ['A']),
            ('C', ['A']),
            ('D', ['B', 'C'])
        ]
        dag = DAG(arr)
        leaves = dag.get_leaves()
        self.assertEqual(leaves, {'D'})

    def test_complex(self):
        arr = [
            ('A', []),
            ('B', ['A']),
            ('C', ['B']),
            ('D', []),
            ('E', ['D']),
            ('F', ['C', 'E']),
            ('G', ['F']),
            ('H', ['G']),
        ]
        dag = DAG(arr)
        leaves = dag.get_leaves()
        self.assertEqual(leaves, {'H'})


class AncestorsTestCase(TestCase):
    def test_single(self):
        arr = [('A', [])]
        dag = DAG(arr)
        ancestors = dag.get_ancestors('A')
        self.assertEqual(ancestors, {'A'})

    def test_simple(self):
        arr = [
            ('A', []),
            ('B', ['A']),
            ('C', ['A']),
            ('D', ['B', 'C']),
        ]
        dag = DAG(arr)
        self.assertEqual(dag.get_ancestors('A'), {'A'})
        self.assertEqual(dag.get_ancestors('B'), {'A', 'B'})
        self.assertEqual(dag.get_ancestors('C'), {'A', 'C'})
        self.assertEqual(dag.get_ancestors('D'), {'A', 'B', 'C', 'D'})

    def test_complex(self):
        arr = [
            ('A', []),
            ('B', ['A']),
            ('C', ['B']),
            ('D', []),
            ('E', ['D']),
            ('F', ['C', 'E']),
            ('G', ['F']),
            ('H', ['G']),
        ]
        dag = DAG(arr)
        ancestors = dag.get_ancestors('H')
        self.assertEqual(ancestors, {'A', 'B', 'C', 'D', 'E', 'F', 'H', 'G'})

    def test_branching(self):
        arr = [
            ('A', []),
            ('B', ['A']),
            ('C', ['A', 'B']),
            ('D', ['A', 'B', 'C']),
        ]
        dag = DAG(arr)
        self.assertEqual(dag.get_ancestors('A'), {'A'})
        self.assertEqual(dag.get_ancestors('B'), {'A', 'B'})
        self.assertEqual(dag.get_ancestors('C'), {'A', 'B', 'C'})
        self.assertEqual(dag.get_ancestors('D'), {'A', 'B', 'C', 'D'})


class BisectTestCase(TestCase):

    def test_simple(self):
        arr = [
            ('A', []),
            ('B', ['A']),
            ('C', ['A']),
            ('D', ['B', 'C']),
        ]
        dag = DAG(arr)
        bisect = dag.get_bisect()
        self.assertEqual(bisect, {'B', 'C'})

    def test_complex(self):
        arr = [
            ('A', []),
            ('B', ['A']),
            ('C', ['B']),
            ('D', []),
            ('E', ['D']),
            ('F', ['C', 'E']),
            ('G', ['F']),
            ('H', ['G']),
        ]
        dag = DAG(arr)
        bisect = dag.get_bisect()
        self.assertEqual(bisect, {'C'})

    def test_branching(self):
        arr = [
            ('A', []),
            ('B', ['A']),
            ('C', ['A', 'B']),
            ('D', ['A', 'B', 'C']),
        ]
        dag = DAG(arr)
        bisect = dag.get_bisect()
        self.assertEqual(bisect, {'B'})
