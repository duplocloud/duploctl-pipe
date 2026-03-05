"""Tests for DuploctlPipe and main()."""

import pathlib
import yaml
from unittest.mock import MagicMock, patch, mock_open

from bitbucket_pipes_toolkit import Pipe
from duploctl_pipe.pipe import DuploctlPipe, build_schema, main

from tests.conftest import BASE_ENV

REPO_ROOT = pathlib.Path(__file__).parent.parent


def load_metadata():
    with open(REPO_ROOT / "pipe.yml") as f:
        return yaml.safe_load(f)


def make_pipe(schema, env_overrides=None, mock_duplo=None):
    """Instantiate DuploctlPipe with a controlled env and mocked DuploClient.

    Passes env= directly to Pipe.__init__ so os.environ is never touched.
    """
    env = {**BASE_ENV, **(env_overrides or {})}
    if mock_duplo is None:
        mock_duplo = MagicMock()
    with patch("duploctl_pipe.pipe.DuploClient", return_value=mock_duplo):
        pipe = DuploctlPipe(pipe_metadata=load_metadata(), schema=schema, env=env)
    return pipe, mock_duplo


class TestDuploctlPipeInit:
    """DuploctlPipe.__init__ wires up DuploClient and reads variables."""

    def test_duplo_client_receives_host_token_tenant(self, pipe_schema):
        with patch("duploctl_pipe.pipe.DuploClient") as MockClient:
            MockClient.return_value = MagicMock()
            DuploctlPipe(
                pipe_metadata=load_metadata(),
                schema=pipe_schema,
                env=BASE_ENV,
            )
        MockClient.assert_called_once_with(
            host="https://test.duplocloud.net",
            token="test-token",
            tenant="test-tenant",
            loglevel="WARN",
        )

    def test_kind_is_read_from_env(self, pipe_schema):
        pipe, _ = make_pipe(pipe_schema, env_overrides={"KIND": "tenant"})
        assert pipe.kind == "tenant"

    def test_cmd_is_read_from_env(self, pipe_schema):
        pipe, _ = make_pipe(pipe_schema, env_overrides={"CMD": "list"})
        assert pipe.cmd == "list"

    def test_admin_false_sets_duplo_admin_false(self, pipe_schema):
        _, mock_duplo = make_pipe(pipe_schema, env_overrides={"ADMIN": "false"})
        assert mock_duplo.admin is False

    def test_admin_true_sets_duplo_admin_true(self, pipe_schema):
        _, mock_duplo = make_pipe(pipe_schema, env_overrides={"ADMIN": "true"})
        assert mock_duplo.admin is True

    def test_wait_false_sets_duplo_wait_false(self, pipe_schema):
        _, mock_duplo = make_pipe(pipe_schema)
        assert mock_duplo.wait is False

    def test_wait_true_sets_duplo_wait_true(self, pipe_schema):
        _, mock_duplo = make_pipe(pipe_schema, env_overrides={"WAIT": "true"})
        assert mock_duplo.wait is True

    def test_output_format_forwarded_to_duplo(self, pipe_schema):
        _, mock_duplo = make_pipe(pipe_schema, env_overrides={"OUTPUT": "json"})
        assert mock_duplo.output == "json"

    def test_query_forwarded_to_duplo(self, pipe_schema):
        _, mock_duplo = make_pipe(pipe_schema, env_overrides={"QUERY": "Name"})
        assert mock_duplo.query == "Name"


class TestDuploctlPipeRun:
    """DuploctlPipe.run() assembles the right args and calls DuploClient.__call__."""

    def _run(self, pipe, mock_duplo, return_value="result"):
        """Run the pipe with Pipe.run and print stubbed out."""
        mock_duplo.return_value = return_value
        with patch.object(Pipe, "run"), patch("builtins.print"):
            pipe.run()

    def test_kind_only_passes_single_arg(self, pipe_schema):
        pipe, mock_duplo = make_pipe(pipe_schema, env_overrides={"KIND": "service"})
        self._run(pipe, mock_duplo)
        mock_duplo.assert_called_once_with("service")

    def test_kind_and_cmd_passed_in_order(self, pipe_schema):
        pipe, mock_duplo = make_pipe(
            pipe_schema, env_overrides={"KIND": "service", "CMD": "list"}
        )
        self._run(pipe, mock_duplo)
        mock_duplo.assert_called_once_with("service", "list")

    def test_name_appended_after_cmd(self, pipe_schema):
        pipe, mock_duplo = make_pipe(
            pipe_schema,
            env_overrides={"KIND": "service", "CMD": "find", "NAME": "my-app"},
        )
        self._run(pipe, mock_duplo)
        mock_duplo.assert_called_once_with("service", "find", "my-app")

    def test_args_are_split_on_whitespace(self, pipe_schema):
        pipe, mock_duplo = make_pipe(
            pipe_schema,
            env_overrides={
                "KIND": "service",
                "CMD": "update",
                "ARGS": "--image nginx:latest",
            },
        )
        self._run(pipe, mock_duplo)
        mock_duplo.assert_called_once_with("service", "update", "--image", "nginx:latest")

    def test_output_is_printed(self, pipe_schema):
        pipe, mock_duplo = make_pipe(pipe_schema)
        mock_duplo.return_value = "some yaml output"
        with patch.object(Pipe, "run"), patch("builtins.print") as mock_print:
            pipe.run()
        mock_print.assert_called_once_with("some yaml output")

    def test_output_file_is_written(self, pipe_schema, tmp_path):
        out_file = str(tmp_path / "result.txt")
        pipe, mock_duplo = make_pipe(
            pipe_schema, env_overrides={"OUTPUT_FILE": out_file}
        )
        mock_duplo.return_value = "file content"
        with patch.object(Pipe, "run"), patch("builtins.print"):
            pipe.run()
        assert open(out_file).read() == "file content"

    def test_no_output_file_skips_write(self, pipe_schema):
        pipe, mock_duplo = make_pipe(pipe_schema, env_overrides={"OUTPUT_FILE": ""})
        pipe.output_file = None  # ensure falsy after init
        mock_duplo.return_value = "result"
        with patch.object(Pipe, "run"), patch("builtins.print"), \
                patch("builtins.open") as mock_open_call:
            pipe.run()
        mock_open_call.assert_not_called()

    def test_run_returns_config_when_duplo_called_with_no_resource(self, pipe_schema):
        """DuploClient.__call__ with no resource returns the client config dict.

        The pipe always passes at least KIND, so we simulate this by having the
        mock return a config-shaped string — verifying run() prints whatever
        duplo() returns unchanged.
        """
        config_str = "Host: https://test.duplocloud.net\nTenant: test-tenant"
        pipe, mock_duplo = make_pipe(pipe_schema, env_overrides={"KIND": "service"})
        mock_duplo.return_value = config_str
        with patch.object(Pipe, "run"), patch("builtins.print") as mock_print:
            pipe.run()
        mock_print.assert_called_once_with(config_str)


class TestMain:
    """main() loads pipe.yml, builds the schema from it, and runs the pipe."""

    def test_main_creates_pipe_and_calls_run(self):
        meta_path = REPO_ROOT / "pipe.yml"
        mock_pipe = MagicMock()

        with patch("duploctl_pipe.pipe.DuploctlPipe", return_value=mock_pipe), \
                patch("sys.argv", ["pipe", str(meta_path)]), \
                patch("duploctl_pipe.pipe.DuploClient", return_value=MagicMock()):
            main()

        mock_pipe.run.assert_called_once()

    def test_main_builds_schema_from_pipe_yml_variables(self):
        """The schema passed to DuploctlPipe should include all pipe.yml variable names."""
        meta_path = REPO_ROOT / "pipe.yml"
        captured = {}

        def capture(pipe_metadata, schema, **kwargs):
            captured["schema"] = schema
            m = MagicMock()
            m.run = MagicMock()
            return m

        with patch("duploctl_pipe.pipe.DuploctlPipe", side_effect=capture), \
                patch("sys.argv", ["pipe", str(meta_path)]):
            main()

        for key in ("HOST", "TOKEN", "TENANT", "KIND", "CMD", "OUTPUT"):
            assert key in captured["schema"], f"{key} missing from schema passed to pipe"

    def test_main_defaults_to_pipe_yml_path(self):
        """With no sys.argv[1], main() opens './pipe.yml'."""
        meta_path = REPO_ROOT / "pipe.yml"
        with open(meta_path) as f:
            content = f.read()

        mock_pipe = MagicMock()
        m = mock_open(read_data=content)

        with patch("duploctl_pipe.pipe.DuploctlPipe", return_value=mock_pipe), \
                patch("sys.argv", ["pipe"]), \
                patch("builtins.open", m):
            main()

        m.assert_called_with("./pipe.yml", "r")
        mock_pipe.run.assert_called_once()
