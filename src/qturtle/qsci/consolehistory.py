class HistoryItem:
    def __init__(self, command, is_complete=True):
        self.command = str(command)
        self.is_complete = is_complete

    def __str__(self):
        return self.command

    def __repr__(self):
        return ('' if self.is_complete else '*') + repr(self.command)

    def __hash__(self):
        return hash(self.command)

    def __eq__(self, other):
        if isinstance(other, HistoryItem):
            return self.command == other.command
        elif isinstance(other, str):
            return self.command == other.command
        else:
            return NotImplemented


class History:
    def __init__(self):
        self._data = [HistoryItem('')]
        self.index = 0
        self.browsing = False

    def add(self, element, is_complete=None, reset_index=True, clean=True):
        # Prepare history
        if clean:
            self.clean()
        if reset_index:
            self.index = 0

        # Add element
        elem = HistoryItem(element)
        try:
            del self._data[self._data.index(elem)]
            is_present = True
        except ValueError:
            is_present = False

        if is_complete is not None:
            elem.is_complete = is_present or is_complete
        self._data.append(elem)

    def incr(self):
        self.index += 1

    def decr(self):
        self.index -= 1

    def clean(self):
        self._data = [x for x in self._data if x.is_complete]
        self.browsing = False

    def get(self):
        N = len(self._data)
        return self._data[(N - self.index) % N].command

    def __str__(self):
        return str(self._data)

    def __len__(self):
        return len(self._data)