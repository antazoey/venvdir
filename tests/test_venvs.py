from venvdir.venvs import ManagedVirtualEnvironment


class TestManagedVirtualEnvironment:
    def test_get_uses_lower_for_name(self, mocker):
        name = "test"
        env = ManagedVirtualEnvironment(name, {})
        assert env.get("NAME") == name

    def test_get_when_not_name_uses_entry(self):
        test_path = "~"
        entry = {"path": test_path}
        env = ManagedVirtualEnvironment("name", entry)
        assert env.get("path") == test_path

    def test_items_includes_name_in_items(self):
        test_name = "name"
        test_path = "~"
        entry = {"path": test_path}
        env = ManagedVirtualEnvironment(test_name, entry)
        actual = env.items()
        expected = list({"path": test_path, "name": test_name}.items())
        assert actual == expected

    def test_keys_includes_name_in_keys(self):
        test_name = "name"
        test_path = "~"
        entry = {"path": test_path}
        env = ManagedVirtualEnvironment(test_name, entry)
        actual = env.keys()
        assert "name" in actual
        assert "path" in actual
        assert len(actual) == 2
