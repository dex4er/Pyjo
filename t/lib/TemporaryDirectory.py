from contextlib import contextmanager
import errno
import tempfile
import shutil


@contextmanager
def TemporaryDirectory():
    name = tempfile.mkdtemp()
    try:
        yield name
    finally:
        try:
            shutil.rmtree(name)
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise
