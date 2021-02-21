import pytest
from redscript_docgen.parser import parse


@pytest.mark.parametrize("source", (
    r"""
func t(p: t, opt p: t) -> t {}
    """,
    r"""
class t {}
    """,
    r"""
class t {
  let f: t;
}
    """,
    """
class t {
  func t() -> t {}
}
    """,
    r"""
@one()
func t() -> t {}
    """,
    r"""
@one()
@two()
func t() -> t {}
    """,
    r"""
@one(param, param)
@two(param, "param")
func t() -> t {}
    """,
))
def test_transform_annotationlist(source):
    assert parse(source) is not None
