
class IndexableDict(dict):
    def __getitem__(self, item: int):
        for i, (k, v) in enumerate(self.items()):
            if i == item:
                return v
        return super(IndexableDict, self).__getitem__(item)
