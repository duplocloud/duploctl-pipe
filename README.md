# Bitbucket Pipe for Duploctl  

A bitbucket wrapper for the [duploctl](https://github.com/duplocloud/duploctl). Implements the bitbucket pipe tools and the duploctl as python libraries to give a nice and integrated kinda feel to it. 

## YAML Definition  

```yaml
- pipe: &duploctl docker://duplocloud/duploctl-pipe:1.0.0
  variables: &duplovars
    TOKEN: <string>
    HOST: <string>
    TENANT: <string>
    KIND: service
    NAME: my-app
    CMD: update_image
    ARGS: registry.com/my-app:latest
- pipe: *duploctl
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

## Prerequisites  

To make an update to a service you will need a duplo token. 
