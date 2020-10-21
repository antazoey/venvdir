import pytest
from configparser import ConfigParser

from venvdir.error import VenvDirBaseError
from venvdir._configparser import VenvsConfigParser
from tests.conftest import MockSection


@pytest.fixture(autouse=True)
def mock_saver(mocker):
    return mocker.patch("venvdir._configparser.open")


@pytest.fixture
def mock_config_parser(mocker):
    return mocker.MagicMock(spec=ConfigParser)


class TestVenvsConfigParser:
    def test_entries_returns_sections(self, mock_config_parser):
        mock_sections = ["entry1", "entry2"]
        mock_config_parser.sections.return_value = mock_sections
        venvs_parser = VenvsConfigParser(mock_config_parser)
        assert venvs_parser.entries == mock_sections

    def test_get_entry_returns_expected_entry(self, mock_config_parser):
        name = "test_name"
        mock_section = MockSection(name, {"path": "path/to/venv"})

        def get_item_side_effect(item):
            if item == name:
                return mock_section

        mock_config_parser.__getitem__.side_effect = get_item_side_effect
        venvs_parser = VenvsConfigParser(mock_config_parser)
        assert venvs_parser.get_entry(name) == mock_section.values_dict

    def test_get_entry_when_does_not_exist_raises_error(self, mock_config_parser):
        name = "test_name"

        def get_item_side_effect(item):
            if item == name:
                raise KeyError()

        mock_config_parser.__getitem__.side_effect = get_item_side_effect
        venvs_parser = VenvsConfigParser(mock_config_parser)
        with pytest.raises(VenvDirBaseError) as err:
            venvs_parser.get_entry(name)

        assert err

    def test_create_entry_saves(self, mock_config_parser, mock_saver):
        venvs_parser = VenvsConfigParser(mock_config_parser)
        venvs_parser.create_entry("name", "path")
        assert mock_saver.call_count

    def test_create_entry_adds_new_section(self, mock_config_parser):
        venvs_parser = VenvsConfigParser(mock_config_parser)
        venvs_parser.create_entry("test", "path")
        mock_config_parser.add_section.assert_called_once_with("test")

    def test_create_entry_creates_expected_section_properties(self, mock_config_parser):
        new_name = "new_name"
        new_path = "new/path"
        mock_section = MockSection(new_name, {"path": "Test fail"})
        mock_config_parser.__getitem__.return_value = mock_section
        venvs_parser = VenvsConfigParser(mock_config_parser)
        venvs_parser.create_entry(new_name, new_path)
        expected_path = "{}/{}".format(new_path, new_name)
        assert mock_section["path"] == expected_path

    def test_remove_entry_saved(self, mock_config_parser, mock_saver):
        venvs_parser = VenvsConfigParser(mock_config_parser)
        venvs_parser.remove_entry("test")
        assert mock_saver.call_count

    def test_remove_entry_calls_remove_section(self, mock_config_parser):
        name = "test"
        venvs_parser = VenvsConfigParser(mock_config_parser)
        venvs_parser.remove_entry(name)
        mock_config_parser.remove_section.assert_called_once_with(name)
