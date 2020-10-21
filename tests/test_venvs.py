import pytest

from venvdir.error import VenvDirBaseError
from venvdir.venvs import add_entry
from venvdir.venvs import create_entry
from venvdir.venvs import get_entries
from venvdir.venvs import get_entry
from venvdir.venvs import ManagedVirtualEnvironment
from venvdir.venvs import remove_entry
from tests.conftest import MockSection

TEST_NAME = "test_name"
TEST_GIVEN_PATH = "given/path"
TEST_DEFAULT_PATH = "default/path"


@pytest.fixture()
def mock_config_parser(mocker):
    return mocker.patch(_create_patch_str("config_parser"))


@pytest.fixture(autouse=True)
def mock_default_venv_path(mocker):
    return mocker.patch(_create_patch_str("get_default_venvs_path"))


@pytest.fixture(autouse=True)
def venv_creator(mocker):
    return mocker.patch(_create_patch_str("create_venv"))


@pytest.fixture(autouse=True)
def mock_path_existence(mocker):
    return mocker.patch(_create_patch_str("does_path_exist"))


@pytest.fixture(autouse=True)
def mock_remove_dir(mocker):
    return mocker.patch(_create_patch_str("remove_directory"))


def _create_patch_str(name):
    return "venvdir.venvs.{}".format(name)


class TestManagedVirtualEnvironment:
    def test_get_uses_lower_for_name(self):
        env = ManagedVirtualEnvironment(TEST_NAME, {})
        assert env.get("NAME") == TEST_NAME

    def test_get_when_not_name_uses_entry(self):
        entry = {"path": TEST_GIVEN_PATH}
        env = ManagedVirtualEnvironment("name", entry)
        assert env.get("path") == TEST_GIVEN_PATH

    def test_items_includes_name_in_items(self):
        entry = {"path": TEST_GIVEN_PATH}
        env = ManagedVirtualEnvironment(TEST_NAME, entry)
        actual = env.items()
        expected = list({"path": TEST_GIVEN_PATH, "name": TEST_NAME}.items())
        assert actual == expected

    def test_keys_includes_name_in_keys(self):
        entry = {"path": TEST_GIVEN_PATH}
        env = ManagedVirtualEnvironment(TEST_NAME, entry)
        actual = env.keys()
        assert "name" in actual
        assert "path" in actual
        assert len(actual) == 2


def test_get_entries_returns_expected_entries(mock_config_parser):
    names = ["testname_0", "testname_1", "testname_2"]
    paths = ["test/path/0", "test/path/1", "test/path/2"]
    sections = [
        MockSection(names[0], {"path": paths[0]}),
        MockSection(names[1], {"path": paths[1]}),
        MockSection(names[2], {"path": paths[2]})
    ]

    def get_section_side_effect(name):
        index = int(name[-1])
        return sections[index]

    mock_config_parser.entries = names
    mock_config_parser.get_entry.side_effect = get_section_side_effect

    entries = get_entries()

    assert len(entries) == 3
    for i in range(0, len(entries)):
        entry = entries[i]
        expected_name = names[i]
        assert entry.name == expected_name
        assert entry.path == paths[i]


def test_create_entry_when_not_given_path_uses_default_path(
    mock_config_parser, mock_default_venv_path, venv_creator, mock_path_existence
):
    mock_path_existence.return_value = False
    mock_default_venv_path.return_value = TEST_DEFAULT_PATH
    create_entry(TEST_NAME)
    expected_path = "{}/{}".format(TEST_DEFAULT_PATH, TEST_NAME)
    venv_creator.assert_called_once_with(expected_path, with_pip=True)
    mock_config_parser.create_entry.assert_called_once_with(TEST_NAME, TEST_DEFAULT_PATH)


def test_create_entry_when_environment_already_exists_raises_error(
    mock_config_parser, mock_default_venv_path, venv_creator, mock_path_existence
):
    mock_default_venv_path.return_value = TEST_DEFAULT_PATH
    with pytest.raises(VenvDirBaseError) as err:
        create_entry(TEST_NAME, path=TEST_GIVEN_PATH)

    assert str(err.value) == "Virtual environment 'given/path/test_name' already exists."


def test_create_entry_when_environment_does_not_exist_succeeds(
    mock_config_parser, mock_default_venv_path, venv_creator, mock_path_existence
):
    new_env_path = "{}/{}".format(TEST_GIVEN_PATH, TEST_NAME)

    def does_path_exist_side_effect(n):
        if n == TEST_GIVEN_PATH:
            return True
        elif n == new_env_path:
            return False

    mock_path_existence.side_effect = does_path_exist_side_effect
    mock_default_venv_path.return_value = TEST_DEFAULT_PATH
    create_entry(TEST_NAME, path=TEST_GIVEN_PATH)
    venv_creator.assert_called_once_with(new_env_path, with_pip=True)
    mock_config_parser.create_entry.assert_called_once_with(TEST_NAME, TEST_GIVEN_PATH)


def test_create_entry_when_given_path_that_does_not_exist_raises_error(
    mock_config_parser, mock_default_venv_path, venv_creator, mock_path_existence
):
    mock_path_existence.return_value = False

    with pytest.raises(VenvDirBaseError) as err:
        create_entry(TEST_NAME, path=TEST_GIVEN_PATH)

    assert str(err.value) == "Base path 'given/path' does not exist."


def test_add_entry_when_path_does_not_exist_raises_error(
    mock_config_parser, mock_default_venv_path, mock_path_existence
):
    mock_path_existence.return_value = False

    with pytest.raises(VenvDirBaseError) as err:
        add_entry(TEST_NAME, path=TEST_GIVEN_PATH)

    assert str(err.value) == "Venv path 'given/path' does not exist."


def test_add_entry_when_path_exists_succeeds(
    mock_config_parser, mock_default_venv_path, mock_path_existence
):
    mock_path_existence.return_value = True
    add_entry(TEST_NAME, path=TEST_GIVEN_PATH)
    mock_config_parser.create_entry.assert_called_once_with(TEST_NAME, TEST_GIVEN_PATH)


def test_get_entry_returns_expected_entry(
    mock_config_parser, mock_default_venv_path, venv_creator
):
    def get_section_side_effect(name):
        if name == TEST_NAME:
            return MockSection(TEST_NAME, {"path": TEST_GIVEN_PATH})

    mock_config_parser.get_entry.side_effect = get_section_side_effect
    actual = get_entry(TEST_NAME)
    assert actual.name == TEST_NAME
    assert actual.path == TEST_GIVEN_PATH


def test_remove_entry_removes_expected_directory(
    mock_config_parser, mock_default_venv_path, venv_creator, mock_remove_dir
):
    def get_section_side_effect(name):
        if name == TEST_NAME:
            return MockSection(TEST_NAME, {"path": TEST_GIVEN_PATH})

    mock_config_parser.get_entry.side_effect = get_section_side_effect
    remove_entry(TEST_NAME)
    mock_remove_dir.assert_called_once_with(TEST_GIVEN_PATH)


def test_remove_entry_removes_expected_entry_from_config(
    mock_config_parser, mock_default_venv_path, venv_creator, mock_remove_dir
):
    def get_section_side_effect(name):
        if name == TEST_NAME:
            return MockSection(TEST_NAME, {"path": TEST_GIVEN_PATH})

    mock_config_parser.get_entry.side_effect = get_section_side_effect
    remove_entry(TEST_NAME)
    mock_config_parser.remove_entry.assert_called_once_with(TEST_NAME)
