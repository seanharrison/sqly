import pytest

from sqly import queries
from tests import fixtures


@pytest.mark.parametrize(
    "fields,filters,orderby,limit",
    [
        (None, None, None, None),
        (["a", "b"], None, None, None),
        (None, ["a = :a", "b < :b"], None, None),
        (None, None, "a", None),
        (None, None, None, 5),
        ([], [], [], []),
        (["a", "b"], [], [], []),
        ([], ["a = :a", "b < :b"], [], []),
        ([], [], "a", []),
        ([], [], [], 5),
    ],
)
def test_select(fields, filters, orderby, limit):
    tablename = "tablename"
    kwargs = {
        name: value
        for name, value in {
            "fields": fields,
            "filters": filters,
            "orderby": orderby,
            "limit": limit,
        }.items()
        if value
    }
    q = queries.SELECT(tablename, **kwargs)
    print(q)
    assert isinstance(q, str)
    assert f"FROM {tablename}" in q
    # The presence of certain clauses is based on the inclusion of those clauses
    assert ("SELECT *" not in q) is bool(fields)
    assert ("ORDER BY" in q) is bool(orderby)
    assert ("LIMIT" in q) is bool(limit)


@pytest.mark.parametrize("fields", fixtures.fields)
def test_insert(fields):
    tablename = "tablename"
    q = queries.INSERT(tablename, fields)
    print(q)
    assert isinstance(q, str)
    assert f"INSERT INTO {tablename}" in q
    assert q.count(",") == (len(fields) - 1) * 2


def test_update():
    tablename = "tablename"
    fields = ["a", "b", "c"]
    filters = ["a = :a"]
    q = queries.UPDATE(tablename, fields, filters)
    assert isinstance(q, str)
    assert "UPDATE" in q
    assert tablename in q
    assert "SET" in q
    assert "WHERE" in q
    print(q)
    assert q.count("=") == len(fields) + len(filters)


def test_delete():
    tablename = "tablename"
    filters = ["a = :a"]
    q = queries.DELETE(tablename, filters)
    print(q)
    assert isinstance(q, str)
    assert "DELETE FROM" in q
    assert tablename in q
    assert "WHERE" in q
    assert q.count("=") == len(filters)


@pytest.mark.parametrize(
    "fields,returning",
    [
        ([], "*"),
        (None, "*"),
        (["a", "b", "c"], "a, b, c"),
    ],
)
def test_delete_returning(fields, returning):
    tablename = "tablename"
    filters = ["a = :a"]
    q_delete = queries.DELETE(tablename, filters)
    q_returning = queries.DELETE_RETURNING(tablename, filters, fields)
    print(q_returning)
    assert isinstance(q_returning, str)
    assert q_delete in q_returning
    assert f"RETURNING {returning}" in q_returning
