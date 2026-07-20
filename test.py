import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from check_empty import main


class TestModule(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._dir = d = __import__('tempfile').TemporaryDirectory()
        cls._dirp = Path(d.__enter__())

    @classmethod
    def tearDownClass(cls):
        cls._dir.__exit__(*__import__('sys').exc_info())

    def test_all(self):
        self.assertEqual(main(('-qcm', str(Path(__file__).parent / 'py.typed'))), 0)
        self.assertEqual(main(('--must-exist', '')), 2)
        b = self._dirp
        p = b / 'foo.dat'
        p.write_bytes(b'stuff')
        n = str(p)
        s = StringIO()
        t = str(b / 'nonexistent.txt')
        with redirect_stdout(s):
            self.assertEqual(main(('--quiet', n)), 1)
        self.assertEqual(s.getvalue(), '')
        s = StringIO()
        with redirect_stdout(s):
            self.assertEqual(main(('-m', '--clear', n, t)), 3)
        v = s.getvalue()
        self.assertIn('Cleared: ', v)
        self.assertIn('(5 bytes)', v)
        self.assertIn('1 offending file', v)
        self.assertIn('nonexistent.txt', v)
        self.assertIn('foo.dat', v)
        self.assertIn('1 offending file', v)
        self.assertEqual(p.read_bytes(), b'')
        self.assertEqual(main(('-m', t)), 2)
        self.assertEqual(main((t,)), 0)


if __name__ == '__main__':
    unittest.main()
