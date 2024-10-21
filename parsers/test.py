import unittest
from pathlib import Path

import responses
from evewars import parse
from freezegun import freeze_time


class TestCase(unittest.TestCase):
    @responses.activate
    @freeze_time("2024-10-13 00:00:00")
    def test_eve_wars(self):
        responses_path = "testdata/evewars/responses.yaml"
        responses._add_from_file(file_path=responses_path)  # noqa: SLF001

        output = parse()

        expected_path = Path("testdata/evewars/expected.txt")
        with expected_path.open("rb") as expected:
            assert output == {"result.txt": expected.read()}

    @responses.activate
    @freeze_time("2024-10-13 00:00:00")
    def test_eve_wars_real_data(self):
        responses_path = "testdata/evewars/responses-realdata.yaml"
        responses._add_from_file(file_path=responses_path)  # noqa: SLF001

        output = parse()

        expected_path = Path("testdata/evewars/expected-realdata.txt")
        with expected_path.open("rb") as expected:
            assert output == {"result.txt": expected.read()}


if __name__ == "__main__":
    unittest.main()
