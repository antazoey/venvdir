import pytest
from configparser import ConfigParser

from error import VenvDirBaseError
from venvdir._configparser import VenvsConfigParser


@pytest.fixture
def mock_config_parser(mocker):
    return mocker.MagicMock(spec=ConfigParser)


class MockSection:
    def __init__(self, name, values_dict):
        self.name = name
        self.values_dict = values_dict

    def __getitem__(self, item):
        return self.values_dict[item]

    def __setitem__(self, key, value):
        self.values_dict[key] = value

    def get(self, item):
        return self.values_dict.get(item)

    def items(self):
        return self.values_dict.items()


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
