from architecture_blueprint_okf.markdown import slugify

def test_slugify():
    assert slugify("Funding & Research Insight") == "funding-and-research-insight"
