"""Validate the portfolio's deployable files and local references using stdlib."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_FILES = {"index.html", "styles.css", "script.js", ".nojekyll"}


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.references = []
        self.errors = []
        self.h1_count = 0
        self.email_found = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        element_id = attrs.get("id")
        if element_id:
            if element_id in self.ids:
                self.errors.append(f"Duplicate element ID: {element_id}")
            self.ids.add(element_id)
        if tag == "h1":
            self.h1_count += 1
        if tag == "html" and not attrs.get("lang"):
            self.errors.append("Missing document language")
        for attribute in ("href", "src"):
            value = attrs.get(attribute)
            if value:
                self.references.append(value)


def main():
    errors = []
    for filename in PUBLIC_FILES:
        if not (ROOT / filename).is_file():
            errors.append(f"Missing deployment file: {filename}")
    if errors:
        raise SystemExit("\n".join(errors))
    html = (ROOT / "index.html").read_text()
    page = Page()
    page.feed(html)
    errors.extend(page.errors)
    if page.h1_count != 1:
        errors.append("Expected one primary heading")
    for reference in page.references:
        url = urlsplit(reference)
        if url.scheme == "mailto":
            if url.path != "shefazca@gmail.com":
                errors.append("Unexpected public email address")
            page.email_found = True
            continue
        if url.scheme == "tel" or url.path.lower().endswith(".pdf"):
            errors.append("Phone or PDF link requires a separate public-safe review")
            continue
        if url.scheme or url.netloc:
            continue
        if url.path:
            path = unquote(url.path)
            if path.startswith("/"):
                errors.append(f"Root-relative path may break project Pages: {path}")
            elif path not in PUBLIC_FILES:
                errors.append(f"Local reference is not packaged: {path}")
        if url.fragment and not url.path and url.fragment not in page.ids:
            errors.append(f"Missing anchor target: {url.fragment}")
    if not page.email_found:
        errors.append("Confirmed contact email is missing")
    if errors:
        raise SystemExit("\n".join(errors))
    print("Site checks passed: public files, contact, local references, and anchors.")


if __name__ == "__main__":
    main()
