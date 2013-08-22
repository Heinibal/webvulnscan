import unittest

import tutil
import webvulnscan.crawler


class CrawlerTest(unittest.TestCase):
    def _assert_crawled(self, crawler, client, expected_raw):
        expected = set(map(client.full_url, expected_raw))
        matched = set(page.url for page in crawler)
        self.assertEqual(matched, set(expected))

    def test_imglink(self):
        client = tutil.TestClient({
            u'/': (
                200,
                b'<html><body><a href="/b">another page</a></body></html>',
                {'Content-Type': 'text/html; charset=utf-8'}),
            u'/b': (
                200,
                b'<html><body><a href="/img">image</a></body></html>',
                {'Content-Type': 'text/html; charset=utf-8'}),
            u'/img': (
                200,
                b'[image]<a href="/donot">resolve this</a>',
                {'Content-Type': 'image/png'}),
        })
        crawler = webvulnscan.crawler.Crawler(
            client.ROOT_URL, tutil.ContainsEverything(), client=client)
        self._assert_crawled(crawler, client, [u'/', u'/b'])


if __name__ == '__main__':
    unittest.main()