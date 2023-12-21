import pytest
import common


def test_paragraph():
    s = common.paragraph("""
        Foo bar
        baz hello!  
    """)
    assert s == "Foo bar baz hello!"