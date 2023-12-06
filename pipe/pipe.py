from bitbucket_pipes_toolkit import Pipe, yaml, get_variable, get_logger
from duplocloud.client import DuploClient

# some global vars
REQUESTS_DEFAULT_TIMEOUT = 10

# Required vars for updating a service
schema = {
  'DUPLO_TOKEN': {'required': True, 'type': 'string'},
  'DUPLO_HOST': {'required': True, 'type': 'string'},
  'DUPLO_TENANT': {'required': True, 'type': 'string'}
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
    self.duploctl = DuploClient(
      host=self.get_variable("DUPLO_HOST"), 
      token=self.get_variable("DUPLO_TOKEN"),
      tenant=self.get_variable("DUPLO_TENANT"))

  def run(self):
    super().run()
    svc = self.duploctl.load("tenant")
    res = svc.list()
    logger.info("Tenant list: %s", res)
    

def main():
  with open('./pipe.yml', 'r') as metadata_file:
    metadata = yaml.safe_load(metadata_file.read())
  pipe = DuploctlPipe(pipe_metadata=metadata, schema=schema)
  pipe.run()

if __name__ == '__main__':
  main()
