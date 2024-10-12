import unittest
import responses
from evewars import parse
from freezegun import freeze_time

class TestCase(unittest.TestCase):
  @responses.activate
  @freeze_time("2024-10-13 00:00:00")
  def test_eve_wars(self):
    responses._add_from_file(file_path="test-evewars-responses.yaml")
    expected = {'result.txt': str.encode("War ID 3: Alliance 1 (AID1) declared war to Corporation 2 (CID2) 5 hours ago\nWar ID 2: Corporation 2 (CID2) declared war to Alliance 1 (AID1) 11 hours ago\n")}

    output = parse()

    self.assertEqual(expected, output)
    
  @responses.activate
  @freeze_time("2024-10-13 00:00:00")
  def test_eve_wars_real_data(self):
    responses._add_from_file(file_path="test-evewars-responses-realdata.yaml")
    expected = {'result.txt': str.encode("War ID 745134: BLACKFLAG. (S4LTY) declared war to Les deux mousquetaires (LDM.) 4 hours ago\nWar ID 745130: BLACKFLAG. (S4LTY) declared war to 2 Unicorns et a Obelisk (2UEO) 9 hours ago\nWar ID 745129: C A P S T E X T . (CAP) declared war to Friendly LoneWolf Corporation (FLW C) 10 hours ago\nWar ID 745128: Bully Brigade (BULLY) declared war to Friendly LoneWolf Corporation (FLW C) 10 hours ago\nWar ID 745127: Bully Brigade (BULLY) declared war to Codex Signal Prism (CSPHG) 13 hours ago\nWar ID 745126: Smart Deploy (5MART) declared war to Rim Worlds Republic (RIM W) 13 hours ago\nWar ID 745125: C A P S T E X T . (CAP) declared war to Codex Signal Prism (CSPHG) 14 hours ago\nWar ID 745124: C A P S T E X T . (CAP) declared war to Job's Done. (.JD.) 21 hours ago\nWar ID 745123: Bully Brigade (BULLY) declared war to Job's Done. (.JD.) 21 hours ago\nWar ID 745122: BLACKFLAG. (S4LTY) declared war to Blood Drive (BLUD) 22 hours ago\n")}

    output = parse()

    self.assertEqual(expected, output)

if __name__ == '__main__':
    unittest.main()