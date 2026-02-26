import pytest
from duploctl_pipe.pipe import build_schema


class TestBuildSchema:
    def test_empty_variables_returns_empty_dict(self):
        assert build_schema([]) == {}

    def test_variable_name_becomes_schema_key(self):
        schema = build_schema([{"name": "FOO"}])
        assert "FOO" in schema

    def test_type_is_always_string(self):
        schema = build_schema([{"name": "FOO"}])
        assert schema["FOO"]["type"] == "string"

    def test_required_true_is_preserved(self):
        schema = build_schema([{"name": "FOO", "required": True}])
        assert schema["FOO"]["required"] is True

    def test_required_false_is_preserved(self):
        schema = build_schema([{"name": "FOO", "required": False}])
        assert schema["FOO"]["required"] is False

    def test_required_defaults_to_false_when_absent(self):
        schema = build_schema([{"name": "FOO"}])
        assert schema["FOO"]["required"] is False

    def test_default_value_is_included(self):
        schema = build_schema([{"name": "FOO", "default": "bar"}])
        assert schema["FOO"]["default"] == "bar"

    def test_no_default_key_when_not_in_variable(self):
        schema = build_schema([{"name": "FOO"}])
        assert "default" not in schema["FOO"]

    def test_description_is_excluded(self):
        """pipe.yml descriptions are human-facing only — not part of the schema."""
        schema = build_schema([{"name": "FOO", "description": "help text"}])
        assert "description" not in schema["FOO"]

    def test_multiple_variables_all_present(self):
        variables = [
            {"name": "A", "required": True},
            {"name": "B", "required": False, "default": "x"},
            {"name": "C"},
        ]
        schema = build_schema(variables)
        assert set(schema.keys()) == {"A", "B", "C"}
        assert schema["A"]["required"] is True
        assert schema["B"]["default"] == "x"
        assert schema["C"]["required"] is False

    def test_dollar_sign_default_preserved_as_literal(self):
        """$VAR_NAME defaults from pipe.yml should pass through unchanged."""
        schema = build_schema([{"name": "HOST", "default": "$DUPLO_HOST"}])
        assert schema["HOST"]["default"] == "$DUPLO_HOST"


class TestSchemaFromPipeYml:
    """Verify the schema derived from the real pipe.yml has the right shape."""

    def test_required_vars_are_marked_required(self, pipe_schema):
        for key in ("HOST", "TOKEN", "TENANT", "KIND"):
            assert pipe_schema[key]["required"] is True, f"{key} should be required"

    def test_optional_vars_are_not_required(self, pipe_schema):
        for key in ("CMD", "NAME", "ARGS", "ADMIN", "OUTPUT", "QUERY", "WAIT", "OUTPUT_FILE"):
            assert pipe_schema[key]["required"] is False, f"{key} should not be required"

    def test_defaults_match_pipe_yml(self, pipe_schema):
        assert pipe_schema["KIND"]["default"] == "service"
        assert pipe_schema["ADMIN"]["default"] == "false"
        assert pipe_schema["OUTPUT"]["default"] == "yaml"
        assert pipe_schema["WAIT"]["default"] == "false"
        assert pipe_schema["ARGS"]["default"] == ""

    def test_all_entries_have_string_type(self, pipe_schema):
        for key, entry in pipe_schema.items():
            assert entry["type"] == "string", f"{key} should have type='string'"
