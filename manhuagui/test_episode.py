import unittest
from manhuagui.episode import episode


class TestEpisode(unittest.TestCase):
    def setUp(self):
        self.url = 'https://www.manhuagui.com/comic/20515/239686.html'

    def tearDown(self):
        pass

    def test_episode(self):
        result = episode(self.url)
        self.assertTrue(len(result) > 0)
        self.assertEqual(len(result['files']), 51)
        self.assertEqual(result['referer'], self.url)
        self.assertTrue(len(result['bname']) > 0)
        self.assertTrue(len(result['cname']) > 0)
        self.assertTrue(len(result['params']['md5']) > 0)
        self.assertEqual(result['params']['cid'], '239686')


if __name__ == '__main__':
    unittest.main()
