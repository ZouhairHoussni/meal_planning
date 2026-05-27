from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_brand_tokens_are_defined_in_base_template():
    content = (ROOT / "templates" / "base.html").read_text()

    assert "#2563EB" in content
    assert "#F4B740" in content
    assert "primary-soft" in content
    assert "canvas" in content


def test_shared_mobile_first_components_exist_in_css():
    content = (ROOT / "static" / "css" / "app.css").read_text()

    assert ".page-hero" in content
    assert ".btn-primary" in content
    assert ".form-panel" in content
    assert ".mobile-bottom-nav" in content
    assert ".shopping-item" in content
