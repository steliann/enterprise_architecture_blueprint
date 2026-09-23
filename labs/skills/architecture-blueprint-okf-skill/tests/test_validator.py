from pathlib import Path
import tempfile
from architecture_blueprint_okf.initializer import initialize
from architecture_blueprint_okf.validator import Validator

SKILL_ROOT=Path(__file__).resolve().parents[1]

def test_initialized_package_has_only_placeholder_warnings():
    with tempfile.TemporaryDirectory() as d:
        bp=Path(d)/"blueprint"
        initialize(SKILL_ROOT,bp,"Example Organisation","Example Solution")
        result=Validator(SKILL_ROOT).validate(bp,strict=False)
        assert result.ok, [x.__dict__ for x in result.errors]

def test_strict_rejects_placeholders():
    with tempfile.TemporaryDirectory() as d:
        bp=Path(d)/"blueprint"
        initialize(SKILL_ROOT,bp,"Example Organisation","Example Solution")
        result=Validator(SKILL_ROOT).validate(bp,strict=True)
        assert not result.ok
        assert any(x.code=="placeholder" for x in result.errors)
