import importlib.util
import unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'skills/bbq-geo-observer/scripts/observe.py'
s=importlib.util.spec_from_file_location('observe',p); m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class ObserveTests(unittest.TestCase):
 def test_not_run_is_unknown_even_if_zero_supplied(self):
  r=m.normalize({'answer_status':'not_run','mentioned':False,'identity_verdict':'accurate'},1)
  self.assertEqual(r['mentioned'],'unknown');self.assertEqual(r['identity_verdict'],'unknown')
 def test_full_text_and_conflicting_review_preserved(self):
  row={'answer_text':'A\nMira Example contradicts a prior source.\n','target_entity':'Mira Example','mentioned':False,'identity_verdict':'contradictory','cited_urls':['https://example.org']}
  r=m.normalize(row,1)
  self.assertEqual(r['raw'],row);self.assertEqual(r['answer_text'],row['answer_text']);self.assertTrue(r['literal_mention_candidate']);self.assertFalse(r['mentioned']);self.assertTrue(r['warnings']);self.assertEqual(r['claim_source_support'],'unknown')
 def test_absence_never_becomes_reviewed_false(self):
  r=m.normalize({'answer_text':'Other advisers','target_entity':'Mira'},1)
  self.assertFalse(r['literal_mention_candidate']);self.assertEqual(r['mentioned'],'unknown')
 def test_record_path_is_not_read(self):
  r=m.normalize({'answer_record':'untrusted-file.md','answer_status':'answered'},1)
  self.assertIsNone(r['answer_text']);self.assertEqual(r['mentioned'],'unknown');self.assertTrue(r['warnings'])
 def test_search_and_identity_are_separate_from_mention(self):
  r=m.normalize({'answer_text':'Mira','target_entity':'Mira','mentioned':True,'search_triggered':False,'target_entity_correctly_identified':False},1)
  self.assertTrue(r['mentioned']);self.assertFalse(r['search_triggered']);self.assertFalse(r['target_entity_correctly_identified']);self.assertEqual(r['identity_verdict'],'unknown')
 def test_csv_boolean_strings(self):
  self.assertFalse(m.tri('false'));self.assertTrue(m.tri('true'));self.assertEqual(m.tri(''),'unknown')
if __name__=='__main__':unittest.main()
