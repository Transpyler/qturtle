import pytest
import qturtle


def test_project_defines_author_and_version():
    assert hasattr(qturtle, '__author__')
    assert hasattr(qturtle, '__version__')
