"""Stable object identities stored in standard OOXML alternative descriptions.

Names remain human-readable. IDs depend on slide/field, never coordinates or theme.
Metadata records raw values, but the checker also reads native cells, chart XML,
connections, image bytes and interval geometry: metadata alone is not verification.
"""
import json


def identify(shape, object_id, **record):
    record = dict(id=object_id, **record)
    shape._element.xpath('.//p:cNvPr')[0].set('descr', json.dumps({'edu_ppt': record}, ensure_ascii=False))
    return shape


def identity(shape):
    nodes = shape._element.xpath('.//p:cNvPr')
    try:
        return json.loads(nodes[0].get('descr', '{}')).get('edu_ppt', {}) if nodes else {}
    except (ValueError, AttributeError):
        return {}


SERIES_COLORS = ['176B76', 'C46B16', '654A9A', '31834E', 'B44A69', '3265A8']
