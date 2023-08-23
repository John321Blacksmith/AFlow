# tasks iterator here
class AsyncIterator:
    def __init__(self, sequence):
        self._sequence = sequence
        self._index = 0

    async def __aiter__(self):
        return self

    async def __anext__(self):
        if self._index < len(self._sequence):
            item = self._sequence[self._index]
            self._index += 1
            return item
        else:
            raise StopAsyncIteration