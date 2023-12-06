# Bitbucket Pipe for Duploctl  

A bitbucket wrapper for the [duploctl](https://github.com/duplocloud/duploctl). Implements the bitbucket pipe tools and the duploctl as python libraries to give a nice and integrated kinda feel to it. 

## YAML Definition  

```yaml
- pipe: docker://duplocloud/duploctl-pipe:1.0.0
  variables:
    DUPLO_TOKEN: '<string>'
    DUPLO_HOST: '<string>'
    DUPLO_TENANT: '<string>'
```

## Variables  

| Variable | Usage |  
| -------- | ----- |  
| DUPLO_TOKEN | Auth token for Duplo |  
| DUPLO_HOST | The domain of your Duplo instance |  
| DUPLO_TENANT | The tenant where the service is in |  

## Prerequisites  

To make an update to a service you will need a duplo token. 
