from bitbucket_pipes_toolkit import Pipe, yaml, get_logger
from duplocloud.client import DuploClient
import sys

logger = get_logger()

class DuploctlPipe(Pipe):
    """Duplo Deploy Pipe"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.duplo = DuploClient(
            host=self.get_variable("HOST"),
            token=self.get_variable("TOKEN"),
            tenant=self.get_variable("TENANT"),
            loglevel=self.get_variable("LOG_LEVEL"))
        isadmin = self.get_variable("ADMIN")
        wait = self.get_variable("WAIT")
        # set global duplo vars
        self.duplo.admin = True if isadmin == "true" else False
        self.duplo.output = self.get_variable("OUTPUT")
        self.duplo.query = self.get_variable("QUERY")
        self.duplo.wait = True if wait == "true" else False
        # these are for building the command
        self.kind = self.get_variable("KIND")
        self.cmd = self.get_variable("CMD")
        self.args = self.get_variable("ARGS")
        self.name = self.get_variable("NAME")
        self.output_file = self.get_variable("OUTPUT_FILE")

    def run(self):
        super().run()
        args = [self.kind]
        if self.cmd:
            args.append(self.cmd)
        if self.name:
            args.append(self.name)
        if self.args:
            args.extend(self.args.split())
        o = self.duplo(*args)
        if self.output_file:
            with open(self.output_file, 'w') as f:
                f.write(o)
        print(o)

def build_schema(variables):
    """Transform pipe.yml variables list into the bitbucket schema dict."""
    schema = {}
    for var in variables:
        entry = {'type': 'string', 'required': var.get('required', False)}
        if 'default' in var:
            entry['default'] = var['default']
        schema[var['name']] = entry
    return schema

def main():
    file = sys.argv[1] if len(sys.argv) > 1 else './pipe.yml'
    with open(file, 'r') as metadata_file:
        metadata = yaml.safe_load(metadata_file.read())
    schema = build_schema(metadata.get('variables', []))
    pipe = DuploctlPipe(pipe_metadata=metadata, schema=schema)
    pipe.run()

if __name__ == '__main__':
    main()