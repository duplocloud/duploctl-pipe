from bitbucket_pipes_toolkit import Pipe, yaml, get_variable, get_logger
from duplocloud.client import DuploClient

# some global vars
REQUESTS_DEFAULT_TIMEOUT = 10

# Required vars for updating a service
schema = {
  'DUPLO_TOKEN': {'required': True, 'type': 'string'},
  'DUPLO_HOST': {'required': True, 'type': 'string'},
  'DUPLO_TENANT': {'required': True, 'type': 'string'},
  'RESOURCE': {'required': True, 'type': 'string'},
  'NAME': {'required': False, 'type': 'string'},
  'CMD': {'required': False, 'type': 'string'},
  'ARGS': {'required': False, 'type': 'string'},
  'ADMIN': {'required': False, 'type': bool, 'default': False},
  'OUTPUT': {'required': False, 'type': 'string', 'default': 'yaml'},
  'QUERY': {'required': False, 'type': 'string'},
}

logger = get_logger()

class DuploctlPipe(Pipe):
  """Duplo Deploy Pipe"""
  url = None
  headers = None
  service = None
  image = None
  tenant_name = None

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.duplo = DuploClient(
      host=self.get_variable("HOST"), 
      token=self.get_variable("TOKEN"),
      tenant=self.get_variable("TENANT"))
    self.duplo.admin = self.get_variable("ADMIN")
    self.duplo.output = self.get_variable("OUTPUT")
    self.duplo.query = self.get_variable("QUERY")
    self.resource = self.get_variable("RESOURCE")
    self.cmd = self.get_variable("CMD")
    self.args = self.get_variable("ARGS")
    self.name = self.get_variable("NAME")


  def run(self):
    super().run()
    args = self.args.split(" ")
    if self.args.name:
      args.insert(0, self.name)
    svc = self.duplo.load(self.resource)
    res = svc(self.cmd, self.args*)
    print(res)
    

def main():
  with open('./pipe.yml', 'r') as metadata_file:
    metadata = yaml.safe_load(metadata_file.read())
  pipe = DuploctlPipe(pipe_metadata=metadata, schema=schema)
  pipe.run()

if __name__ == '__main__':
  main()
