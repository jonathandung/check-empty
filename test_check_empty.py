import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from check_empty import __version__, check
from check_empty.__main__ import _p, main  # ruff: ignore[import-private-name]


class TestModule(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._dir = d = __import__('tempfile').mkdtemp()
        cls._dirp = Path(d)

    @classmethod
    def tearDownClass(cls):
        __import__('shutil').rmtree(cls._dir)

    def test_main(self):
        self.assertEqual(main(('',)), 4)
        b = self._dirp
        p = b / 'foo.dat'
        p.write_bytes(b'stuff')
        n = str(p)
        s = StringIO()
        t = str(b / 'nonexistent.txt')
        with redirect_stdout(s):
            self.assertEqual(main(('--quiet', '--may-not-exist', n)), 1)
        self.assertEqual(
            s.getvalue(),
            'All files were found\n1 offending file\nTotal size: 5 bytes\n',
        )
        s = StringIO()
        with redirect_stdout(s):
            self.assertEqual(main(('--clear', '-V', n, t)), 5)
        v = s.getvalue()
        for x in (
            'Cleared: ',
            '(5 bytes)',
            '1 offending file',
            'nonexistent.txt',
            'foo.dat',
        ):
            self.assertIn(x, v)
        self.assertEqual(p.read_bytes(), b'')
        self.assertEqual(main((t,)), 4)
        self.assertEqual(main(('-m', t, '-QQ')), 0)

    def test_p(self):
        self.assertEqual(_p.prog, 'check-empty')
        with self.assertRaises(SystemExit) as e:
            _p.parse_args(('-h',))
        self.assertEqual(e.exception.code, 0)
        s = StringIO()
        with self.assertRaises(SystemExit) as e, redirect_stdout(s):
            _p.parse_args(('-v',))
        self.assertEqual('check-empty v' + __version__, s.getvalue().strip())
        self.assertEqual(e.exception.code, 0)
        self.assertEqual(_p.parse_args(('-c', '--verbose', '')).clear, True)

    def test_check(self):
        b = self._dirp
        p = b / 'bar.txt'
        p.write_text('spam')
        self.assertEqual(check((str(p),)), 1)
        self.assertEqual(check(i for i in [p]), 1)
        with (b / 'baz.bin').open('wb') as f:
            self.assertIn(check([p, f.fileno(), -1]), {5, 9})
        self.assertEqual(check({p}, clear=True), 1)
        self.assertEqual(check((p, 'what')), 4)


if __name__ == '__main__':
    unittest.main()
