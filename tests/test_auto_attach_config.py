"""Persistence tests for remembered USB devices."""

from src.core.config_manager import ConfigManager


def test_auto_attach_rules_survive_a_restart(tmp_path):
    config = ConfigManager(tmp_path)
    config.add_auto_attach_device("1-2", "192.168.1.20")

    assert config.save()

    restored = ConfigManager(tmp_path)
    assert restored.get_auto_attach_devices() == {"1-2": "192.168.1.20"}


def test_saving_same_busid_updates_its_server(tmp_path):
    config = ConfigManager(tmp_path)
    config.add_auto_attach_device("1-2", "192.168.1.20")
    config.add_auto_attach_device("1-2", "192.168.1.21")

    assert config.get_auto_attach_devices() == {"1-2": "192.168.1.21"}


def test_removing_auto_attach_rule_is_idempotent(tmp_path):
    config = ConfigManager(tmp_path)
    config.add_auto_attach_device("1-2", "192.168.1.20")
    config.remove_auto_attach_device("1-2")
    config.remove_auto_attach_device("1-2")

    assert config.get_auto_attach_devices() == {}
