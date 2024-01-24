import unittest

from batch_apply import BatchApply


class InitTests(unittest.TestCase):

    @staticmethod
    def test_batch_apply():
        items = []

        def apply(its: list):
            # The list may be empty
            if len(its) == 0:
                return
                pass
            print(f"Saving items {its[0]}...{its[-1]}")
            pass

        ba = BatchApply(apply, items)

        for i in range(500):
            items.append(i)
            ba.check_buffer()
            pass

        ba.check_buffer(done=True)
        pass
