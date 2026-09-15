import importlib.util
import threading
import unittest
from http.server import BaseHTTPRequestHandler,HTTPServer
from pathlib import Path
s=importlib.util.spec_from_file_location('seo',Path(__file__).resolve().parents[1]/'skills/bbq-multilingual-seo-check/scripts/check.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class Handler(BaseHTTPRequestHandler):
 def log_message(self,*a):pass
 def do_GET(self):
  if self.path=='/redirect':
   self.send_response(302);self.send_header('Location','https://example.org/outside');self.end_headers();return
  if self.path=='/missing':self.send_response(404);self.end_headers();return
  if self.path=='/sitemap.xml':
   body='<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><sitemap><loc>/part.xml</loc></sitemap></sitemapindex>';typ='application/xml'
  elif self.path=='/part.xml':
   body='<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>/en/</loc></url><url><loc>/zh/</loc></url></urlset>';typ='application/xml'
  else:
   lang='en' if self.path=='/en/' else 'zh-CN'
   body=f'<html lang="{lang}"><head><link rel="canonical" href="{self.path}"><link rel="alternate" hreflang="en" href="/en/"><link rel="alternate" hreflang="zh-CN" href="/zh/"></head><body>fixture</body></html>';typ='text/html'
  self.send_response(200);self.send_header('Content-Type',typ);self.end_headers();self.wfile.write(body.encode())
class SEOTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.server=HTTPServer(('127.0.0.1',0),Handler);cls.root=f'http://127.0.0.1:{cls.server.server_port}';cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True);cls.thread.start()
 @classmethod
 def tearDownClass(cls):cls.server.shutdown();cls.server.server_close();cls.thread.join()
 def fetch(self,budget=70):return m.Fetcher({m.origin(self.root)},budget,0)
 def test_live_http_fixture_has_complete_sitemap_and_reciprocal_alternates(self):
  r=m.audit(self.fetch(),[self.root+'/en/',self.root+'/zh/'],[self.root+'/sitemap.xml'])
  self.assertTrue(r['sitemap']['complete']);self.assertEqual(r['sitemap']['url_count'],2);self.assertEqual(r['summary']['checks']['review'],0);self.assertEqual(r['summary']['checks']['unknown'],0)
 def test_budget_exhaustion_does_not_claim_missing_membership(self):
  r=m.audit(self.fetch(1),[self.root+'/en/'],[self.root+'/sitemap.xml'])
  self.assertFalse(r['sitemap']['complete']);self.assertGreater(r['summary']['checks']['unknown'],0)
 def test_missing_page_retains_status(self):
  r=m.audit(self.fetch(),[self.root+'/missing'],[])
  self.assertEqual(r['pages'][0]['checks'][0]['evidence']['status'],404)
 def test_external_redirect_not_followed(self):
  r=self.fetch().get(self.root+'/redirect');self.assertIn('outside allowed',r['error']);self.assertIsNone(r['final_url'])
 def test_language_regions_not_assumed_identical(self):
  self.assertTrue(m.compatible('en','en-US'));self.assertFalse(m.compatible('en-US','en-GB'));self.assertFalse(m.compatible('zh-CN','en'))
if __name__=='__main__':unittest.main()
