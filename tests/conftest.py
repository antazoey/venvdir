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
