import io
import unittest
from unittest.mock import patch
from docx import Document
from output_validation import validate_output
from document_parser import generate_docx_bytes

SOURCE = 'Alex Example\nalex@example.com\nPython, Git\nCSV Cleaner\nBSc 2025'

class AccuracyTests(unittest.TestCase):
    def test_gemini_model_and_text_parts(self):
        import api_router
        from unittest.mock import Mock
        response = Mock(status_code=200)
        response.json.return_value = {'candidates': [{'content': {'parts': [
            {'text': 'internal', 'thought': True}, {'text': 'Resume'}, {'text': 'Details'}]}}]}
        with patch.object(api_router, 'get_key', return_value=''), patch.object(api_router.requests, 'post', return_value=response) as post:
            self.assertEqual(api_router.call_gemini('test-key', 'system', 'input', ''), 'Resume\nDetails')
        self.assertTrue(post.call_args.args[0].endswith('gemini-3.8-flash:generateContent'))
        self.assertNotIn('test-key', post.call_args.args[0])
        self.assertEqual(post.call_args.kwargs['headers']['x-goog-api-key'], 'test-key')
        self.assertNotIn('generationConfig', post.call_args.kwargs['json'])

    def test_managed_secrets_without_local_file(self):
        import api_router
        with patch.dict('os.environ', {}, clear=True), patch.object(api_router.st, 'secrets', {'GEMINI_KEY_1': 'fictional-test-key'}), patch.object(api_router, 'secrets_file_exists', return_value=False):
            self.assertEqual(api_router.get_key('GEMINI_KEY_1'), 'fictional-test-key')

    def test_valid_source_contacts(self):
        self.assertEqual(validate_output(SOURCE, '<h1>Alex Example</h1><p>alex@example.com</p><p>BSc 2025</p>'), [])

    def test_source_profile_link_without_scheme(self):
        self.assertEqual(validate_output(SOURCE + '\ngithub.com/alex-example', '<h1>Alex Example</h1><p>alex@example.com</p><a href="https://github.com/alex-example">GitHub</a>'), [])

    def test_missing_or_invented_email(self):
        for contact in ['', 'alex.other@example.com']:
            self.assertTrue(validate_output(SOURCE, f'<h1>Alex Example</h1><p>{contact}</p>'))

    def test_invented_phone_or_metric(self):
        for claim in ['123-456-7890', 'Improved speed by 40%']:
            self.assertTrue(validate_output(SOURCE, f'<h1>Alex Example</h1><p>alex@example.com {claim}</p>'))

    def test_unsafe_markup(self):
        for markup in ['<script>alert(1)</script>', '<p onclick="bad()">Text</p>', '<img src="https://example.com">', '<a href="#">LinkedIn</a>']:
            self.assertTrue(validate_output(SOURCE, '<h1>Alex Example</h1><p>alex@example.com</p>' + markup))

    def test_nested_docx_preserves_sections(self):
        html = '<div><h1>Alex Example</h1><p>alex@example.com</p><h2>Projects</h2><ul><li>CSV Cleaner</li></ul></div>'
        doc = Document(io.BytesIO(generate_docx_bytes(html)))
        self.assertEqual([p.text for p in doc.paragraphs], ['Alex Example', 'alex@example.com', 'Projects', 'CSV Cleaner'])

if __name__ == '__main__':
    unittest.main()
