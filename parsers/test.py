import unittest

import responses
from evewars import parse
from freezegun import freeze_time


class TestCase(unittest.TestCase):
    @responses.activate
    @freeze_time("2024-10-13 00:00:00")
    def test_eve_wars(self):
        responses._add_from_file(file_path="testdata/evewars/responses.yaml")

        output = parse()

        with open("testdata/evewars/expected.txt", "rb") as expected:
            self.assertEqual({"result.txt": expected.read()}, output)

    @responses.activate
    @freeze_time("2024-10-13 00:00:00")
    def test_eve_wars_real_data(self):
        responses._add_from_file(file_path="testdata/evewars/responses-realdata.yaml")

        output = parse()

        with open("testdata/evewars/expected-realdata.txt", "rb") as expected:
            self.assertEqual({"result.txt": expected.read()}, output)


if __name__ == "__main__":
    unittest.main()
