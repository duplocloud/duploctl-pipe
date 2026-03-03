import pathlib
import pytest
import yaml
from duploctl_pipe.pipe import build_schema

REPO_ROOT = pathlib.Path(__file__).parent.parent


@pytest.fixture(scope="session")
def pipe_metadata():
    with open(REPO_ROOT / "pipe.yml") as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="session")
def pipe_schema(pipe_metadata):
    return build_schema(pipe_metadata.get("variables", []))


# Minimal env dict covering every schema key.
# Passed as env= to Pipe.__init__ so os.environ is never touched.
BASE_ENV = {
    "HOST": "https://test.duplocloud.net",
    "TOKEN": "test-token",
    "TENANT": "test-tenant",
    "KIND": "service",
    "CMD": "",
    "NAME": "",
    "ARGS": "",
    "ADMIN": "false",
    "OUTPUT": "yaml",
    "QUERY": "",
    "WAIT": "false",
    "OUTPUT_FILE": "",
    "LOG_LEVEL": "WARN",
}
