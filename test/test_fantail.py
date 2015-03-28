
import os
import logging
import shutil
import tempfile
import unittest
import yaml

import fantail

lg = logging.getLogger(__name__)
lg.setLevel(logging.DEBUG)

test_set_1 = yaml.load("""
a: 1
b: 2
c:
  d: 3
  e: 4
  f: 5
g: [0, 1, 2, 3,]
h: 
  i: 12
  j:
    k: 14
    l: 15
    m: 16
""")

test_set_2 = yaml.load("""
a: 18
b:
  k: 9
  m: 10
g: [0, 1, 2, 3, 4, 5]
""")


def d():
    return fantail.Fantail(test_set_1)


class BasicFantailTest(unittest.TestCase):

    def test_load(self):
        fantail.Fantail()

    def test_store_dict(self):
        f = fantail.Fantail()
        f['a'] = 1
        self.assertEqual(f['a'], 1)

test_yaml = """
a:
  b1:
    c1: v1
    c2: v2
    c3: v3
  b2: v4
b: v5
"""

test_dict = yaml.load(test_yaml)

class FantailTest(unittest.TestCase):

    def test_load(self):
        y = fantail.Fantail()

    def test_setgetitem(self):
        y = fantail.Fantail()
        y['a'] = 1
        self.assertEqual(y['a'], 1)

    def test_setlevelgetitem(self):
        y = fantail.Fantail()
        y['a']['b'] = 1
        self.assertEqual(y['a.b'], 1)
        y['c.d'] = 1
        self.assertEqual(y['c']['d'], 1)

    def test_nonstringkeys(self):
        y = fantail.Fantail()
        y[1] = 12
        self.assertEqual(y[1], 12)

        
    def test_get(self):
        y = fantail.Fantail()
        y['a'] = 1
        self.assertEqual(y.get('a'), 1)
        self.assertEqual(y.get('a', 2), 1)
        self.assertEqual(y.get('b', 3), 3)
        
    def test_branch_nodes(self):
        y = d()
        self.assertTrue(y.has_key('b'))
        self.assertTrue(y.has_key('c'))
        self.assertFalse(y.has_key('d'))

        self.assertTrue('b' in y)
        self.assertTrue('c' in y)
        self.assertFalse('d' in y)

        self.assertTrue(y.has_key('h.j.k'))
        self.assertTrue(y.has_key('h.j'))
        self.assertFalse(y.has_key('h.j.qq'))


class StackTest(unittest.TestCase):

    def setUp(self):
        self.a = fantail.Fantail()
        self.b = fantail.Fantail()
        self.s = fantail.Fanstack([self.a,self.b])

        self.a['a.b.c'] = 1
        self.a['a.b.d'] = 2
        self.b['a.b.e'] = 3

    def test_basic(self):        
        self.assertEqual(self.s['a.b.c'], 1)
        self.assertEqual(self.s['a.b.d'], 2)
        self.assertEqual(self.s['a.b.e'], 3)

    def test_slice(self):
        s = self.s['a.b']
        self.assertEqual(s, dict(d=2,e=3,c=1))

    def test_in(self):
        self.assertTrue('a.b' in self.s)

    def test_slice_in(self):
        self.assertTrue('b' in self.s['a'])

class LoaderTest(unittest.TestCase):

    def setUp(self):
        self.tf = tempfile.NamedTemporaryFile(delete=False)
        self.tf.write(test_yaml.encode('utf8'))
        self.tf.close()
        self.test_dir = os.path.join(
            os.path.dirname(__file__), 'data')

    def get_empty_yaco(self):
        return fantail.Fantail()

    def test_dict_loader(self):
        y = fantail.dict_loader(test_dict)
        self.assertEqual(y['a']['b1']['c2'], 'v2')
        self.assertEqual(y['b'], 'v5')

    def test_simple_loader_yaml(self):

        lg.critical(str(dir(fantail)))
        lg.critical(str(fantail.load))
        y = fantail.load(test_dict)
        self.assertEqual(y['a']['b1']['c2'], 'v2')
        self.assertEqual(y['b'], 'v5')

    def test_yaml_string_loader(self):
        y = fantail.yaml_string_loader(test_yaml)
        self.assertEqual(y['a']['b1']['c2'], 'v2')
        self.assertEqual(y['b'], 'v5')
        z = fantail.dict_loader(test_dict)
        self.assertEqual(y, z)

    def test_yaml_file_loader(self):
        y = fantail.yaml_file_loader(self.tf.name)
        self.assertEqual(y['a']['b1']['c2'], 'v2')
        self.assertEqual(y['b'], 'v5')
        z = fantail.dict_loader(test_dict)
        self.assertEqual(y, z)

    def test_yaml_file_save(self):
        y = fantail.Fantail()
        y['a']['b']['c'] = 1
        y['d.e'] = '2'

        tf = tempfile.NamedTemporaryFile(delete=False)
        tf.close()
        fantail.yaml_file_save(y, tf.name)
        tf.close()

        z = fantail.yaml_file_loader(tf.name)
        self.assertEqual(y, z)

    def test_dir_loader(self):
        y = fantail.dir_loader(self.test_dir)
        self.assertEqual(y['test']['a'], 1)
        self.assertEqual(y['subdir']['subtest']['e']['g'], 4)
        self.assertEqual(y['subdir']['subsubdir']['subsubtest']['g'], 4)
        self.assertEqual(y['subdir']['subtest']['d'], 'overridden')
        self.assertEqual(y['subdir']['raw'].strip(),
                          'multiline\ntext\nfield')

    def test_package_loader(self):
        y = fantail.package_loader("pkg://fantail/etc")
        #import pprint
        #pprint.pprint(y)
        self.assertEqual(y['Mus'].strip(), 'musculus')
        self.assertEqual(y['sub.Rattus'].strip(), 'swedigicus')
        self.assertEqual(y['sub.Sus'], 'scrofa')
        self.assertEqual(y['sub.test.Gallus'], 'Gallus')

    def tearDown(self):
        os.unlink(self.tf.name)




