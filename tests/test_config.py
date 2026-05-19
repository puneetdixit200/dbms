from expense_tracker.config import get_config


def test_get_config_reads_current_environment(monkeypatch):
    monkeypatch.setenv("DB_PORT", "3307")
    monkeypatch.setenv("DB_NAME", "test_expense_tracker")

    config = get_config()

    assert config["DB_PORT"] == 3307
    assert config["DB_NAME"] == "test_expense_tracker"

