import pytest

from venvdir.main import cli
from venvdir.venvs import ManagedVirtualEnvironment


@pytest.fixture
def mock_get_entries(mocker):
    return mocker.patch(_create_patch_str("get_entries"))


@pytest.fixture
def mock_create_entry(mocker):
    return mocker.patch(_create_patch_str("create_entry"))


@pytest.fixture
def mock_add_entry(mocker):
    return mocker.patch(_create_patch_str("add_entry"))


@pytest.fixture
def mock_remove_entry(mocker):
    return mocker.patch(_create_patch_str("remove_entry"))


@pytest.fixture
def mock_get_entry(mocker):
    return mocker.patch(_create_patch_str("get_entry"))



def _create_patch_str(name):
    return "venvdir.main.{}".format(name)


def test_ls_output_all_virtual_environments(runner, mock_get_entries):
    entries = [
        ManagedVirtualEnvironment("name0", {"path": "path/to/name0"}),
        ManagedVirtualEnvironment("name1", {"path": "path/to/name1"}),
        ManagedVirtualEnvironment("name2", {"path": "path/to/name2"})
    ]
    mock_get_entries.return_value = entries
    res = runner.invoke(cli, "ls")
    for entry in entries:
        assert entry.name in res.output
        assert entry.path in res.output
    assert mock_get_entries.call_count == 1


def test_ls_when_no_entries_outputs_nothing(runner, mock_get_entries):
    mock_get_entries.return_value = []
    res = runner.invoke(cli, "ls")
    assert res.output == ""


def test_create_calls_create(runner, mock_create_entry):
    runner.invoke(cli, "create test")
    mock_create_entry.assert_called_once_with("test", None)


def test_create_calls_create_with_path(runner, mock_create_entry):
    runner.invoke(cli, "create test -p path")
    mock_create_entry.assert_called_once_with("test", "path")


def test_add_requires_path(runner, mock_add_entry):
    res = runner.invoke(cli, "add test")
    assert "usage" in res.output.lower()


def test_add_calls_add_entry(runner, mock_add_entry):
    runner.invoke(cli, "add test -p path")
    mock_add_entry.assert_called_once_with("test", "path")


def test_rm_calls_remove_entry(runner, mock_remove_entry):
    runner.invoke(cli, "rm test")
    mock_remove_entry.assert_called_once_with("test")


def test_which_outputs_expected_path(runner, mock_get_entry):
    mock_get_entry.return_value = ManagedVirtualEnvironment(
        "test", {"path": "path/to/test"}
    )
    res = runner.invoke(cli, "which test")
    assert "path/to/test" in res.output