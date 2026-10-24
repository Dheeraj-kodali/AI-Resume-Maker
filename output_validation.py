"""Deterministic safeguards; these do not prove semantic factual accuracy."""
import re
from bs4 import BeautifulSoup


def validate_output(source, html):
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text(' ', strip=True)
    issues = []
    if not text or not soup.find('h1'):
        issues.append('Missing resume content or name heading')
    if soup.find(['script', 'iframe', 'object', 'embed', 'img', 'style', 'link']):
        issues.append('Unsafe or unsupported HTML elements')
    if any(k.lower().startswith('on') or k.lower() == 'style' for tag in soup.find_all(True) for k in tag.attrs):
        issues.append('Unsupported active content or inline styling')
    emails = lambda value: set(re.findall(r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}', value))
    if emails(source) != emails(text):
        issues.append('Contact email was changed, omitted or invented')
    numbers = lambda value: set(re.findall(r'\b\d+(?:[.,]\d+)*%?', value))
    if numbers(text) - numbers(source):
        issues.append('Unsupported numbers, dates or contact details')
    for link in soup.find_all('a'):
        href = link.get('href', '')
        target = href.removeprefix('mailto:').removeprefix('tel:')
        if not target or target == '#' or target not in source or not href.startswith(('https://', 'http://', 'mailto:', 'tel:')):
            issues.append('Unsupported or unsafe link')
            break
    return issues
