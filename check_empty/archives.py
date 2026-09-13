"""Functions used to clear files in archives."""

from __future__ import annotations

from .constants import TYPE_CHECKING

if TYPE_CHECKING:
    import tarfile
    import zipfile

    import py7zr
__all__ = ('clear_file_in_zip', 'purge_7z', 'purge_tar')
_ = __import__('io').BytesIO()


def clear_file_in_zip(z: zipfile.ZipFile, i: zipfile.ZipInfo) -> None:
    """Clear the contents of a file in a .zip archive."""
    z.writestr(i, b'')


def purge_7z(z: py7zr.SevenZipFile) -> None:
    """Clear the contents of each file in a .7z archive."""
    x = z.filename
    if x is None:
        raise NotImplementedError
    y = z.namelist()
    with __import__('py7zr').SevenZipFile(x, 'w') as a:
        for n in y:
            a.writef(_, n)


def purge_tar(t: tarfile.TarFile) -> None:
    """Clear the contents of each file in a .tar archive."""
    x = t.name
    if x is None:
        raise NotImplementedError
    import tarfile as z

    with __import__('tempfile').NamedTemporaryFile(
        suffix='.tar.gz', delete=False
    ) as p, z.open(fileobj=p, mode='w:gz') as f:
        a = f.addfile
        for m in t.getmembers():
            a(z.TarInfo(m.name))
    __import__('os').replace(p.name, x)
