from bitbucket_pipes_toolkit import Pipe, yaml, get_logger
from duplocloud.client import DuploClient

# some global vars
REQUESTS_DEFAULT_TIMEOUT = 10

# Required vars for updating a service
schema = {
  'TOKEN': {'required': True, 'type': 'string'},
  'HOST': {'required': True, 'type': 'string'},
  'TENANT': {'required': True, 'type': 'string'},
  'KIND': {'required': True, 'type': 'string'},
  'NAME': {'required': False, 'type': 'string'},
  'CMD': {'required': False, 'type': 'string'},
  'ARGS': {'required': False, 'type': 'string', 'default': ''},
  'ADMIN': {'required': False, 'type': 'string', 'default': 'false'},
  'OUTPUT': {'required': False, 'type': 'string', 'default': 'yaml'},
  'QUERY': {'required': False, 'type': 'string'},
  'WAIT': {'required': False, 'type': 'string', 'default': 'false'}
}

logger = get_logger()

class DuploctlPipe(Pipe):
  """Duplo Deploy Pipe"""
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.duplo = DuploClient(
      host=self.get_variable("HOST"), 
      token=self.get_variable("TOKEN"),
      tenant=self.get_variable("TENANT"))
    isadmin = self.get_variable("ADMIN")
    wait = self.get_variable("WAIT")
    # set global duplo vars
    self.duplo.admin = True if isadmin == "true" else False
    self.duplo.output = self.get_variable("OUTPUT")
    self.duplo.query = self.get_variable("QUERY")
    # these are for building the command
    self.kind = self.get_variable("KIND")
    self.cmd = self.get_variable("CMD")
    self.args = self.get_variable("ARGS")
    self.name = self.get_variable("NAME")
    self.wait = True if wait == "true" else False

  def run(self):
    super().run()
    args = [self.kind]
    if self.cmd:
      args.append(self.cmd)
    if self.name:
      args.append(self.name)
    if self.args:
      args.extend(self.args.split())
    if self.wait:
      args.append("--wait")
    o = self.duplo(*args)
    print(o)
    

def main():
  with open('./pipe.yml', 'r') as metadata_file:
    metadata = yaml.safe_load(metadata_file.read())
  pipe = DuploctlPipe(pipe_metadata=metadata, schema=schema)
  pipe.run()

if __name__ == '__main__':
  main()
