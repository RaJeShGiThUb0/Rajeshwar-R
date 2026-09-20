import pytest
from app.ai_agent import validate_sql

def test_select_is_allowed():
    assert validate_sql("SELECT 1") == "SELECT 1"

@pytest.mark.parametrize("sql", [
    "DROP TABLE x",
    "DELETE FROM x",
    "UPDATE x SET a=1",
    "INSERT INTO x VALUES (1)",
])
def test_mutations_are_rejected(sql):
    with pytest.raises(ValueError):
        validate_sql(sql)
