"""Static accessibility regressions; browser/assistive-technology checks are separate."""

from pathlib import Path
import re
import unittest
from urllib.parse import unquote, urlsplit

from test_pages_visibility import Document, Element, normalized, only, require


PAGE = Path(__file__).resolve().parents[1] / "docs" / "index.html"
IDREFS = {"aria-labelledby", "aria-describedby", "aria-controls", "aria-owns",
          "aria-activedescendant", "aria-details", "aria-errormessage", "aria-flowto"}
NATIVE_NAMED = {"a", "button", "img", "input", "select", "textarea", "nav", "main",
                "header", "footer", "aside", "section", "article", "form", "fieldset",
                "figure", "table", "ul", "ol", "dialog", "summary", "h1", "h2", "h3",
                "h4", "h5", "h6"}


def walk(node, ancestors=()):
    yield node, ancestors
    for child in node.children:
        if isinstance(child, Element):
            yield from walk(child, (*ancestors, node))


def ids(document):
    result = {}
    for node in document.find():
        if "id" in node.attrs:
            value = node.attrs["id"]
            require(bool(value) and not re.search(r"\s", value), "Empty or whitespace-containing ID")
            require(value not in result, f"Duplicate ID: {value}")
            result[value] = node
    return result


def content_name(node):
    if ("hidden" in node.attrs or node.attrs.get("aria-hidden") == "true"
            or node.tag in {"head", "script", "style", "template"}):
        return ""
    if node.tag == "img":
        return node.attrs.get("alt") or ""
    return normalized(" ".join(content_name(child) if isinstance(child, Element) else child
                               for child in node.children))


def accessible_name(node, index, content=True):
    if "aria-labelledby" in node.attrs:
        references = (node.attrs["aria-labelledby"] or "").split()
        require(bool(references), "Empty aria-labelledby")
        require(all(value in index for value in references), "Unresolved accessible-name reference")
        return normalized(" ".join(content_name(index[value]) for value in references))
    if (node.attrs.get("aria-label") or "").strip():
        return normalized(node.attrs["aria-label"])
    return (content_name(node) if content else "") or (node.attrs.get("title") or "").strip()


def interactive(node):
    return ((node.tag == "a" and "href" in node.attrs)
            or node.tag in {"button", "input", "select", "textarea", "summary", "iframe"}
            or node.attrs.get("role") in {"button", "link", "checkbox", "radio", "switch", "textbox", "combobox"}
            or node.attrs.get("contenteditable") == "true")


def tab_focusable(node, ancestors):
    if any("hidden" in item.attrs or item.attrs.get("aria-hidden") == "true"
           for item in (*ancestors, node)):
        return False
    if "disabled" in node.attrs or node.attrs.get("type") == "hidden":
        return False
    if "tabindex" in node.attrs:
        return int(node.attrs["tabindex"]) >= 0
    return interactive(node)


def check_ids_and_labels(document):
    index = ids(document)
    for node, ancestors in walk(document):
        for attribute in IDREFS & node.attrs.keys():
            references = (node.attrs[attribute] or "").split()
            require(bool(references) and all(value in index for value in references),
                    f"Unresolved {attribute}: {node.attrs[attribute]}")
        if "aria-label" in node.attrs or "aria-labelledby" in node.attrs:
            require(bool(accessible_name(node, index, content=False)), f"Empty name on {node.tag}")
            contextual_generic = node.tag in {"header", "footer"} and any(
                ancestor.tag in {"article", "aside", "main", "nav", "section"}
                or ancestor.attrs.get("role") in {"article", "complementary", "main", "navigation", "region"}
                for ancestor in ancestors)
            if node.tag not in NATIVE_NAMED or contextual_generic:
                require(node.attrs.get("role") not in {None, "none", "presentation", "generic"},
                        f"Name on generic {node.tag} needs appropriate semantics")
        if node.attrs.get("role") == "region":
            require(bool(accessible_name(node, index, content=False)), "Unnamed region")
        if ("client-links" in node.attrs.get("class", "").split()
                and ("aria-label" in node.attrs or "aria-labelledby" in node.attrs)):
            require(node.attrs.get("role") == "group", "Named package links need group semantics")


def check_landmarks_and_skip(document):
    index = ids(document)
    mains = [node for node in document.find() if node.tag == "main" or node.attrs.get("role") == "main"]
    main = only(mains, "main landmark")
    navs = [node for node in document.find() if node.tag == "nav" or node.attrs.get("role") == "navigation"]
    require(bool(navs), "Missing navigation landmark")
    require(all(accessible_name(node, index, content=False) for node in navs), "Navigation needs a name")
    focusable = [node for node, ancestors in walk(document) if tab_focusable(node, ancestors)]
    require(bool(focusable), "No keyboard entry point")
    skip = focusable[0]
    target = urlsplit(skip.attrs.get("href", ""))
    require(skip.tag == "a" and not target.scheme and not target.netloc and not target.path
            and bool(target.fragment), "First focusable element must skip to the main content")
    require(index.get(unquote(target.fragment)) is main, "Skip link must target the main landmark")
    require("tabindex" in main.attrs and int(main.attrs["tabindex"]) <= 0,
            "Skip target must be programmatically focusable without positive tabindex")
    require(bool(accessible_name(skip, index)), "Skip link needs a name")


def check_controls_and_focus(document):
    index = ids(document)
    for node, ancestors in walk(document):
        if node.tag == "img":
            require("alt" in node.attrs, "Image is missing alt text or an explicit decorative alt")
        if node.tag == "button" or (node.tag == "a" and "href" in node.attrs):
            require(bool(accessible_name(node, index)), f"Unnamed {node.tag}")
        if node.tag == "a" and "href" in node.attrs:
            href = (node.attrs["href"] or "").strip()
            require(bool(href) and href != "#" and not href.lower().startswith("javascript:"),
                    "Links need real destinations")
        if "tabindex" in node.attrs:
            try:
                value = int(node.attrs["tabindex"])
            except (TypeError, ValueError) as error:
                raise ValueError("tabindex must be an integer") from error
            require(value <= 0, "Positive tabindex disrupts document keyboard order")
        if interactive(node):
            require(not any(interactive(ancestor) for ancestor in ancestors), "Nested interactive elements")


def check_scorecard(document):
    target = only(document.find(id="scorecard-table"), "scorecard region")
    require(target.attrs.get("role") == "region", "Scorecard needs region semantics")
    require(target.attrs.get("aria-busy") == "true", "Scorecard must expose initial loading state")
    index = ids(document)
    require(bool(accessible_name(target, index, content=False)), "Scorecard region needs a name")
    statuses = [node for node in document.find() if node.attrs.get("role") == "status"]
    require(bool(statuses), "Missing persistent scorecard status")
    outside = [node for node in statuses if node not in target.find()]
    require(any(node.attrs.get("aria-live") == "polite" and "id" in node.attrs
                and bool(content_name(node)) for node in outside),
            "Status must remain outside replaced scorecard content and announce politely")
    scripts = "\n".join(node.text(raw=True) for node in document.find("script")
                        if node.attrs.get("type") != "application/ld+json")
    require(re.search(r"<caption\b[^>]*>\s*[^<]+</caption>", scripts), "Rendered table needs a caption")
    headers = re.findall(r"<th\b[^>]*>", scripts)
    require(bool(headers) and all(re.search(r"\bscope\s*=\s*['\"]col['\"]", value) for value in headers),
            "Rendered column headers need scope=col")
    require(re.search(r"setAttribute\(\s*['\"]aria-busy['\"]\s*,\s*['\"]false['\"]\s*\)", scripts),
            "Loader must clear aria-busy")
    require(re.search(r"\.textContent\s*=", scripts), "Loader must update persistent status text")


VALID = """<body><a href="#main">Skip to content</a>
<nav aria-label="Primary"><a href="https://example.invalid/">Home</a></nav>
<main id="main" tabindex="-1"><h1 id="title">Library</h1>
<div role="group" aria-labelledby="title"><a href="#title"><img alt="">Skills</a></div>
<section aria-label="Details"><img src="mark.png" alt="Brand mark"></section>
<p id="scorecard-status" role="status" aria-live="polite">Loading.</p>
<div id="scorecard-table" role="region" aria-label="Scorecard" aria-busy="true"></div>
</main><script>function render() { return `<table><caption>Scores</caption><thead><tr><th scope="col">Skill</th></tr></thead></table>`; }
target.setAttribute("aria-busy", "false"); status.textContent = "Loaded";</script></body>"""


class PagesAccessibilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.document = Document(PAGE.read_text()).root

    def test_page_ids_and_aria_references_have_valid_named_semantics(self):
        check_ids_and_labels(self.document)

    def test_page_keyboard_entry_reaches_a_focusable_main_landmark(self):
        check_landmarks_and_skip(self.document)

    def test_page_images_controls_and_keyboard_order_are_accessible(self):
        check_controls_and_focus(self.document)

    def test_scorecard_preserves_live_loading_and_table_semantics(self):
        check_scorecard(self.document)

    def test_valid_native_elements_and_explicit_decorative_images_need_no_extra_aria(self):
        document = Document(VALID).root
        for check in (check_ids_and_labels, check_landmarks_and_skip, check_controls_and_focus, check_scorecard):
            check(document)
        check_ids_and_labels(Document('<header aria-label="Site">Library</header>').root)
        check_ids_and_labels(Document('<main><header role="group" aria-label="Introduction">Library</header></main>').root)

    def test_duplicate_ids_and_dangling_aria_references_are_rejected(self):
        for change in ('<div id="title"></div>', '<div role="group" aria-labelledby="missing">Group</div>',
                       '<button aria-controls="missing">Expand</button>'):
            with self.subTest(change=change), self.assertRaises(ValueError):
                check_ids_and_labels(Document(VALID.replace("</main>", change + "</main>")).root)

    def test_missing_landmarks_or_broken_keyboard_entry_are_rejected(self):
        cases = [("<nav aria-label=\"Primary\">", "<nav>"),
                 ('href="#main"', 'href="#title"'), ('tabindex="-1"', ""),
                 ('<a href="#main">Skip to content</a>', '<a href="https://example.invalid/">Home</a>')]
        for before, after in cases:
            with self.subTest(before=before), self.assertRaises(ValueError):
                check_landmarks_and_skip(Document(VALID.replace(before, after, 1)).root)

    def test_missing_image_names_and_unnamed_or_placeholder_controls_are_rejected(self):
        for content in ('<img src="logo.png">', '<a href="/home"><img alt=""></a>',
                        '<button><span aria-hidden="true">Go</span></button>', '<a href="#">Placeholder</a>'):
            with self.subTest(content=content), self.assertRaises(ValueError):
                check_controls_and_focus(Document(content).root)

    def test_nested_interactive_elements_and_positive_tabindex_are_rejected(self):
        for content in ('<a href="/home"><button>Open</button></a>',
                        '<button><a href="/home">Open</a></button>',
                        '<a href="/home" tabindex="2">Home</a>'):
            with self.subTest(content=content), self.assertRaises(ValueError):
                check_controls_and_focus(Document(content).root)

    def test_generic_named_containers_and_unnamed_regions_are_rejected(self):
        for content in ('<div aria-label="Packages">Links</div>', '<div role="region">Details</div>',
                        '<div class="client-links" aria-label="Packages" role="region">Links</div>',
                        '<main><header aria-label="Introduction">Title</header></main>',
                        '<section><footer aria-label="Footnotes">Notes</footer></section>'):
            with self.subTest(content=content), self.assertRaises(ValueError):
                check_ids_and_labels(Document(content).root)

    def test_broken_loading_announcements_or_table_markup_are_rejected(self):
        cases = [('aria-busy="true"', ""), ('aria-live="polite"', 'aria-live="off"'),
                 ('<caption>Scores</caption>', ""), ('scope="col"', ""),
                 ('setAttribute("aria-busy", "false")', 'setAttribute("data-loaded", "true")'),
                 ('status.textContent = "Loaded"', 'status.dataset.loaded = "yes"')]
        for before, after in cases:
            with self.subTest(before=before), self.assertRaises(ValueError):
                check_scorecard(Document(VALID.replace(before, after, 1)).root)
        inside = VALID.replace('<p id="scorecard-status" role="status" aria-live="polite">Loading.</p>', "")
        inside = inside.replace('aria-busy="true"></div>', 'aria-busy="true"><p id="status" role="status" aria-live="polite">Loading.</p></div>')
        with self.assertRaises(ValueError):
            check_scorecard(Document(inside).root)


if __name__ == "__main__":
    unittest.main()
