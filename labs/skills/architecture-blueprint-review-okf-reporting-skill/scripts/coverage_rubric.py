from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import yaml

ALLOWED_SCORES = {0.0, 0.25, 0.5, 0.75, 1.0}


def _read_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(value, dict):
        raise ValueError(f"Configuration must be a YAML object: {path}")
    return value


def normalize_rubric(document: dict[str, Any]) -> dict[str, Any]:
    rubric = document.get("coverage_rubric", document)
    if not isinstance(rubric, dict):
        raise ValueError("coverage_rubric must be a YAML object")
    raw = rubric.get("dimensions") or {}
    dimensions: list[dict[str, Any]] = []
    if isinstance(raw, dict):
        for dim_id, value in raw.items():
            item = dict(value or {}) if isinstance(value, dict) else {"weight": value}
            item["id"] = str(dim_id)
            dimensions.append(item)
    elif isinstance(raw, list):
        dimensions = [dict(item) for item in raw if isinstance(item, dict)]
    else:
        raise ValueError("coverage_rubric.dimensions must be a mapping or list")
    return {
        "model_version": str(rubric.get("model_version") or "1.0"),
        "normalize_enabled_weights": bool(rubric.get("normalize_enabled_weights", True)),
        "dimensions": dimensions,
    }


def dimension_map(rubric: dict[str, Any]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for item in rubric.get("dimensions", []):
        dim_id = str(item.get("id") or "").strip()
        if not dim_id:
            raise ValueError("each coverage dimension requires an id")
        if dim_id in result:
            raise ValueError(f"duplicate coverage dimension id: {dim_id}")
        result[dim_id] = item
    return result


def validate_rubric(rubric: dict[str, Any]) -> None:
    dims = dimension_map(rubric)
    if not dims:
        raise ValueError("coverage rubric requires at least one dimension")
    enabled = 0
    for dim_id, item in dims.items():
        if not str(item.get("label") or "").strip():
            raise ValueError(f"coverage dimension {dim_id} requires a label")
        try:
            weight = float(item.get("weight", 0))
        except (TypeError, ValueError) as exc:
            raise ValueError(f"coverage dimension {dim_id} has an invalid weight") from exc
        if weight < 0:
            raise ValueError(f"coverage dimension {dim_id} weight cannot be negative")
        if bool(item.get("enabled", True)):
            enabled += 1
            if weight <= 0:
                raise ValueError(f"enabled coverage dimension {dim_id} must have a positive weight")
    if not enabled:
        raise ValueError("at least one coverage dimension must be enabled")


def load_rubric(defaults_path: Path, override_path: Path | None = None) -> dict[str, Any]:
    defaults = normalize_rubric(_read_yaml(defaults_path))
    validate_rubric(defaults)
    if not override_path:
        return defaults
    override = normalize_rubric(_read_yaml(override_path))
    default_map = dimension_map(defaults)
    override_map = dimension_map(override)
    unknown = sorted(set(override_map) - set(default_map))
    if unknown:
        raise ValueError(f"override contains unknown coverage dimensions: {', '.join(unknown)}")
    result = json.loads(json.dumps(defaults))
    result_map = dimension_map(result)
    for dim_id, item in override_map.items():
        target = result_map[dim_id]
        if "enabled" in item:
            target["enabled"] = bool(item["enabled"])
        if "weight" in item:
            target["weight"] = float(item["weight"])
    result["model_version"] = str(override.get("model_version") or result.get("model_version") or "1.0")
    result["normalize_enabled_weights"] = bool(override.get("normalize_enabled_weights", result.get("normalize_enabled_weights", True)))
    validate_rubric(result)
    return result


def model_hash(rubric: dict[str, Any]) -> str:
    material = {
        "model_version": str(rubric.get("model_version") or "1.0"),
        "normalize_enabled_weights": bool(rubric.get("normalize_enabled_weights", True)),
        "dimensions": [
            {"id": str(item["id"]), "enabled": bool(item.get("enabled", True)), "weight": float(item.get("weight", 0))}
            for item in rubric.get("dimensions", [])
        ],
    }
    blob = json.dumps(material, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()[:16]


def effective_weights(rubric: dict[str, Any], scores: dict[str, Any] | None = None) -> dict[str, float]:
    score_map = scores or {}
    applicable = []
    for item in rubric.get("dimensions", []):
        dim_id = str(item["id"])
        if not bool(item.get("enabled", True)):
            continue
        if scores is not None and score_map.get(dim_id, "__missing__") is None:
            continue
        applicable.append(item)
    total = sum(float(item.get("weight", 0)) for item in applicable)
    if total <= 0:
        return {}
    return {str(item["id"]): 100.0 * float(item.get("weight", 0)) / total for item in applicable}


def validate_dimension_scores(rubric: dict[str, Any], scores: dict[str, Any]) -> None:
    known = set(dimension_map(rubric))
    missing = sorted(known - set(scores))
    unknown = sorted(set(scores) - known)
    if missing:
        raise ValueError(f"coverage dimension scores are incomplete: {', '.join(missing)}")
    if unknown:
        raise ValueError(f"coverage dimension scores contain unknown dimensions: {', '.join(unknown)}")
    for dim_id, value in scores.items():
        if value is None:
            continue
        try:
            score = float(value)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"coverage dimension {dim_id} score must be numeric or null") from exc
        if score not in ALLOWED_SCORES:
            raise ValueError(f"coverage dimension {dim_id} score {score} is invalid; allowed: 0, .25, .5, .75, 1")


def score_category(rubric: dict[str, Any], scores: dict[str, Any]) -> int:
    validate_dimension_scores(rubric, scores)
    weights = effective_weights(rubric, scores)
    if not weights:
        raise ValueError("no enabled and applicable coverage dimensions remain for this category")
    result = sum((weights[dim_id] / 100.0) * float(scores[dim_id]) for dim_id in weights)
    return int(round(result * 100))


def coverage_level(score: int, levels: list[dict[str, Any]]) -> str:
    for item in sorted(levels, key=lambda x: int(x.get("min", 0)), reverse=True):
        if score >= int(item.get("min", 0)):
            return str(item.get("label") or "")
    return ""


def portable_document(rubric: dict[str, Any]) -> dict[str, Any]:
    dims: dict[str, dict[str, Any]] = {}
    for item in rubric.get("dimensions", []):
        weight = float(item.get("weight", 0))
        dims[str(item["id"])] = {
            "label": str(item.get("label") or item["id"]),
            "enabled": bool(item.get("enabled", True)),
            "weight": int(weight) if weight.is_integer() else weight,
            "question": str(item.get("question") or ""),
        }
    return {"coverage_rubric": {"model_version": str(rubric.get("model_version") or "1.0"), "normalize_enabled_weights": bool(rubric.get("normalize_enabled_weights", True)), "dimensions": dims}}
