from dataclasses import dataclass
from typing import Any


@dataclass
class BatchApply:
    apply: Any
    buffer: list
    batch_size = 100

    @staticmethod
    def check_not_none(var, identifier=None, message: str = None):
        if var is None:
            if message is None:
                message = f"{identifier} wasn't set"
                pass
            raise ValueError(message)
        pass

    def check_buffer(self, done=False):
        buffer: list = self.buffer
        apply = self.apply
        self.check_not_none(buffer, "buffer")
        self.check_not_none(apply, "apply")

        size = len(buffer)
        if size >= self.batch_size or done:
            apply(buffer)
            buffer.clear()
            return True
            pass

        return False
        pass
    pass
