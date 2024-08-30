# Bitbucket Pipe for Duploctl  

A bitbucket wrapper for the [duploctl](https://github.com/duplocloud/duploctl). Implements the bitbucket pipe tools and the duploctl as python libraries to give a nice and integrated kinda feel to it. 

## YAML Definition  

```yaml
- pipe: &duplo docker://duplocloud/pipe:1.0.0
  variables: &duplovars
    TOKEN: <string>
    HOST: <string>
    TENANT: <string>
    KIND: service
    NAME: my-app
    CMD: update_image
    ARGS: registry.com/my-app:${BITBUCKET_TAG}
    WAIT: 'true' # waits for deploy to finish
- pipe: *duplo
  variables:
    <<: *duplovars
    KIND: lambda
    NAME: my-lambda
    ARGS: registry.com/my-lambda:latest

```

## Variables  

| Variable | Usage |  
| -------- | ----- |  
| TOKEN | Auth token for Duplo |  
| HOST | The domain of your Duplo instance |  
| TENANT | The tenant where the service is in |  
| KIND | The kind of the service (service, lambda) |
| NAME | The name of the service |
| CMD | The command to run on the service |
| ARGS | The arguments to the command |
| QUERY | The [JMESPATH](https://jmespath.org/) query to run on the output of the command |
| OUTPUT | The output of the command, json, yaml, string |
| WAIT | Tells duploctl to wait until a process has completed before continuing |

## Prerequisites  

To make an update to a service you will need a duplo token. 

## References  
  - [This Repo](https://bitbucket.org/duplocloud/duploctl-pipe/src/main/)
  - [Bitbucket Pipe Advanced Techniques](https://support.atlassian.com/bitbucket-cloud/docs/advanced-techniques-for-writing-pipes/)
  - [Bitbucket Pipe Tools](https://bitbucket.org/bitbucketpipelines/bitbucket-pipes-toolkit/src/master/)
