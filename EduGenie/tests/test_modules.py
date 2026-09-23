from quiz_module import clean_json_block


def test_clean_json_block():
    raw = """```json
{"questions": []}
```"""
    assert clean_json_block(raw) == '{"questions": []}'
