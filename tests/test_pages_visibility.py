"""Check discoverable Pages artifacts without promising indexing or AI rankings."""

from html.parser import HTMLParser
import json
from pathlib import Path
import re
import tempfile
import unittest
from urllib.parse import unquote, urljoin, urlsplit
import xml.etree.ElementTree as ET

import yaml


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
SITE = "https://chiefinnovator.github.io/inventingfirewithai_skills/"
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


class Element:
    def __init__(self, tag="document", attrs=()):
        self.tag, self.attrs, self.children = tag, dict(attrs), []

    def find(self, tag=None, **attrs):
        result = []
        if (tag is None or self.tag == tag) and all(self.attrs.get(k) == v for k, v in attrs.items()):
            result.append(self)
        for child in self.children:
            if isinstance(child, Element):
                result.extend(child.find(tag, **attrs))
        return result

    def text(self, raw=False):
        if not raw and (self.tag in {"head", "script", "style", "template"} or "hidden" in self.attrs):
            return ""
        return " ".join(child.text(raw) if isinstance(child, Element) else child for child in self.children)


class Document(HTMLParser):
    def __init__(self, content):
        super().__init__(convert_charrefs=True)
        self.root = Element()
        self.stack = [self.root]
        self.feed(content)

    def handle_starttag(self, tag, attrs):
        element = Element(tag, attrs)
        self.stack[-1].children.append(element)
        if tag not in VOID:
            self.stack.append(element)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                del self.stack[index:]
                break

    def handle_data(self, data):
        self.stack[-1].children.append(data)


def normalized(value):
    return " ".join(value.split())


def only(elements, label):
    require(len(elements) == 1, f"Expected one {label}, found {len(elements)}")
    return elements[0]


def metadata(document, key):
    matches = [node.attrs.get("content", "") for node in document.find("meta")
               if node.attrs.get("name", node.attrs.get("property")) == key]
    value = only(matches, f"metadata {key}")
    require(bool(value.strip()), f"Empty metadata: {key}")
    return value


def canonical(document):
    value = only(document.find("link", rel="canonical"), "canonical").attrs.get("href")
    require(value == SITE, f"Unexpected canonical URL: {value}")
    return value


def markdown_anchors(content):
    counts, anchors = {}, set()
    for text in re.findall(r"^ {0,3}#{1,6}\s+(.+?)\s*#*\s*$", content, re.MULTILINE):
        slug = re.sub(r"[^\w\- ]", "", text.lower()).replace(" ", "-")
        count = counts.get(slug, 0)
        anchors.add(slug + (f"-{count}" if count else ""))
        counts[slug] = count + 1
    return anchors


def local_file(docs, link, base=SITE, fragments=True):
    """Resolve the project subpath and established Jekyll Markdown HTML URLs."""
    parsed = urlsplit(urljoin(base, link))
    site = urlsplit(SITE)
    if parsed.scheme == "mailto":
        return None
    require(parsed.scheme == "https", f"Non-HTTPS or machine-specific URL: {link}")
    if parsed.netloc != site.netloc:
        return None
    if urlsplit(link).scheme and re.fullmatch(r"/[\w.-]+/", parsed.path) and parsed.path != site.path:
        return None  # absolute link to a sibling project site root on the same Pages host
    require(parsed.path.startswith(site.path), f"URL escapes project site: {link}")
    relative = unquote(parsed.path[len(site.path):]) or "index.html"
    require(".." not in Path(relative).parts and "\\" not in relative, f"Unsafe project URL: {link}")
    target = (docs / relative).resolve()
    require(target.is_relative_to(docs.resolve()), f"URL escapes docs source: {link}")
    if not target.is_file() and target.suffix == ".html":
        target = target.with_suffix(".md")
    require(target.is_file(), f"Missing local URL target: {link}")
    if fragments and parsed.fragment:
        if target.suffix == ".html":
            ids = {node.attrs["id"] for node in Document(target.read_text()).root.find() if "id" in node.attrs}
        elif target.suffix == ".md":
            ids = markdown_anchors(target.read_text())
        else:
            ids = set()
        require(unquote(parsed.fragment) in ids, f"Missing local fragment: {link}")
    return target


def entities(document):
    result = []
    def visit(value):
        if isinstance(value, dict):
            if "@type" in value:
                result.append(value)
            for item in value.values():
                visit(item)
        elif isinstance(value, list):
            for item in value:
                visit(item)
    for script in document.find("script", type="application/ld+json"):
        value = json.loads(script.text(raw=True))
        require(isinstance(value, dict) and value.get("@context") == "https://schema.org", "Missing Schema.org context")
        visit(value)
    require(bool(result), "Missing structured data")
    return result


def kind(entity, name):
    value = entity.get("@type", [])
    return name in ([value] if isinstance(value, str) else value)


def check_head(document, docs):
    url = canonical(document)
    title = normalized(only(document.find("title"), "page title").text())
    require(bool(title), "Empty page title")
    description = metadata(document, "description")
    require(metadata(document, "og:title") == title == metadata(document, "twitter:title"), "Conflicting social titles")
    require(metadata(document, "og:description") == description == metadata(document, "twitter:description"), "Conflicting descriptions")
    require(metadata(document, "og:url") == url, "Open Graph URL differs from canonical")
    twitter_url = [node for node in document.find("meta") if node.attrs.get("name") == "twitter:url"]
    if twitter_url:
        require(metadata(document, "twitter:url") == url, "Twitter URL differs from canonical")
    image = metadata(document, "og:image")
    require(metadata(document, "twitter:image") == image, "Conflicting social images")
    require(local_file(docs, image) is not None, "Social image must be a deployed asset")
    require(bool(metadata(document, "author")), "Missing author")
    for node in document.find("meta"):
        if node.attrs.get("name", "").lower() in {"robots", "googlebot"}:
            directives = node.attrs.get("content", "").lower().split(",")
            require(not {item.strip() for item in directives} & {"noindex", "none"}, "Public page blocks indexing")


def check_structured_data(document, docs):
    data = entities(document)
    website = only([node for node in data if kind(node, "WebSite")], "WebSite")
    page = only([node for node in data if kind(node, "CollectionPage")], "CollectionPage")
    require(website.get("url") == page.get("url") == SITE, "Structured site/page URL differs from canonical")
    visible = normalized(document.text())
    authors = [node for node in data if kind(node, "Person")]
    require(bool(authors) and all(node.get("name") in visible for node in authors), "Structured author is absent from visible content")
    items = only([node for node in data if kind(node, "ItemList")], "skill ItemList").get("itemListElement", [])
    articles = {node.attrs["id"]: node for node in document.find("article") if "skill-card" in node.attrs.get("class", "").split()}
    families = {path.name for path in (ROOT / "skills" / "codex").iterdir() if (path / "SKILL.md").is_file()}
    require(set(articles) == families, "Visible skill articles differ from repository skill families")
    require(len(items) == len(families), "Structured skill inventory differs from visible inventory")
    seen = set()
    for index, entry in enumerate(items, 1):
        require(entry.get("position") == index, "Invalid skill list ordering")
        item = entry.get("item", {})
        require(kind(item, "SoftwareSourceCode"), "Skill is not described as source code")
        slug = urlsplit(item.get("url", "")).fragment
        require(slug in articles and slug not in seen, "Structured skill URL is missing or duplicated")
        seen.add(slug)
        local_file(docs, item["url"])
        name = normalized(only(articles[slug].find("h3"), f"heading for {slug}").text())
        require(item.get("name") == name, f"Structured skill name differs from visible heading: {slug}")
        require(bool(item.get("description")) and normalized(item["description"]) in normalized(articles[slug].text()), f"Structured skill description differs from visible content: {slug}")
        require(urlsplit(item.get("codeRepository", "")).scheme == "https", f"Missing source repository: {slug}")


class PagesVisibilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = (DOCS / "index.html").read_text()
        cls.document = Document(cls.html).root

    def test_search_and_social_metadata_identify_the_same_public_page(self):
        check_head(self.document, DOCS)

    def test_raw_html_contains_library_installation_and_test_evidence(self):
        heading = only(self.document.find("h1"), "main heading")
        self.assertTrue(normalized(heading.text()))
        for section in ("skills", "install", "tests"):
            node = only(self.document.find(id=section), f"{section} section")
            self.assertTrue(normalized(node.text()))
        install = normalized(only(self.document.find(id="install"), "install section").text())
        for client in ("Codex", "Claude", "Copilot"):
            self.assertIn(client, install)
        test_links = only(self.document.find(id="tests"), "tests section").find("a")
        self.assertTrue(any("evaluation" in node.attrs.get("href", "") for node in test_links))

    def test_navigation_assets_and_project_links_resolve_without_javascript(self):
        for node in self.document.find():
            for attr in ("href", "src"):
                value = node.attrs.get(attr)
                if value:
                    with self.subTest(tag=node.tag, link=value):
                        local_file(DOCS, value)

    def test_structured_skill_inventory_matches_visible_repository_facts(self):
        check_structured_data(self.document, DOCS)

    def test_visible_faq_answers_are_available_without_javascript(self):
        faq = only(self.document.find(id="faq"), "FAQ section")
        questions, answers = faq.find("dt"), faq.find("dd")
        self.assertTrue(questions)
        self.assertEqual(len(questions), len(answers))
        visible = {normalized(question.text()): normalized(answer.text()) for question, answer in zip(questions, answers)}
        self.assertEqual(len(visible), len(questions), "Duplicate FAQ questions")
        self.assertTrue(all(visible.keys()) and all(visible.values()))
        for entity in entities(self.document):
            if kind(entity, "FAQPage"):
                actual = {item["name"]: normalized(item["acceptedAnswer"]["text"]) for item in entity["mainEntity"]}
                self.assertEqual(actual, visible)

    def test_sitemap_contains_only_unique_deployed_project_pages(self):
        tree = ET.parse(DOCS / "sitemap.xml")
        namespace = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        self.assertEqual(tree.getroot().tag, "{" + namespace["s"] + "}urlset")
        urls = [element.text for element in tree.findall("s:url/s:loc", namespace)]
        self.assertIn(SITE, urls)
        self.assertEqual(len(urls), len(set(urls)))
        for url in urls:
            with self.subTest(url=url):
                parsed = urlsplit(url)
                self.assertFalse(parsed.fragment or parsed.query)
                self.assertIsNotNone(local_file(DOCS, url))

    def test_optional_llms_overview_links_to_real_public_sources(self):
        path = DOCS / "llms.txt"
        if not path.exists():
            return
        content = path.read_text()
        self.assertTrue(content.startswith("# "))
        links = re.findall(r"\[[^\]]+\]\(([^\s)]+)\)", content)
        self.assertTrue(links, "Overview must point to maintained source material")
        for link in links:
            with self.subTest(link=link):
                local_file(DOCS, link)

    def test_jekyll_configuration_uses_the_same_canonical_host_and_project_path(self):
        config = yaml.safe_load((DOCS / "_config.yml").read_text())
        site = urlsplit(SITE)
        self.assertEqual(config.get("url"), f"{site.scheme}://{site.netloc}")
        self.assertEqual(config.get("baseurl", "").rstrip("/") + "/", site.path)
        for name in ("title", "description", "lang", "author"):
            self.assertTrue(config.get(name), f"Missing Jekyll {name}")

    def test_public_documentation_links_stay_inside_the_site_or_point_to_external_sources(self):
        pattern = re.compile(r"!?\[[^\]\n]*\]\(\s*(?:<([^>\n]+)>|([^\s)]+))")
        for document in DOCS.rglob("*.md"):
            text = re.sub(r"(?ms)^\s*(`{3,}|~{3,})[^\n]*\n.*?^\s*\1\s*$", "", document.read_text())
            base = urljoin(SITE, document.relative_to(DOCS).with_suffix(".html").as_posix())
            for match in pattern.finditer(text):
                link = match.group(1) or match.group(2)
                with self.subTest(document=document.relative_to(DOCS), link=link):
                    local_file(DOCS, link, base=base)

    def test_checks_detect_missing_or_contradictory_discovery_metadata(self):
        for before, after in ((f'rel="canonical"', 'rel="alternate"'),
                              (f'property="og:url"', 'property="unused"')):
            with self.subTest(before=before), self.assertRaises(ValueError):
                check_head(Document(self.html.replace(before, after, 1)).root, DOCS)

    def test_url_validation_handles_jekyll_pages_and_rejects_project_escapes(self):
        with tempfile.TemporaryDirectory() as directory:
            docs = Path(directory)
            (docs / "guide.md").write_text("# Installation\n")
            self.assertEqual(local_file(docs, "guide.html#installation"), (docs / "guide.md").resolve())
            for link in ("https://chiefinnovator.github.io/outside.html", "../outside.html", "file:///tmp/private.txt", "guide.html#missing"):
                with self.subTest(link=link), self.assertRaises(ValueError):
                    local_file(docs, link)


if __name__ == "__main__":
    unittest.main()
