from pathlib import Path
from architecture_blueprint_okf.template_validation import validate_templates

SKILL_ROOT=Path(__file__).resolve().parents[1]

def test_template_set_validates():
    result=validate_templates(SKILL_ROOT)
    assert result.ok, [x.__dict__ for x in result.issues]
