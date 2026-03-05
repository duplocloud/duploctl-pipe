# Bitbucket Pipe for Duploctl  

A bitbucket wrapper for the [duploctl](https://github.com/duplocloud/duploctl). Implements the bitbucket pipe tools and the duploctl as python libraries to give a nice and integrated kinda feel to it. 

## YAML Definition  

```yaml
- pipe: &duplo docker://duplocloud/pipe:latest
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
| ARGS | Additional arguments to pass to the command |
| ADMIN | Run the command as an admin |
| QUERY | The [JMESPATH](https://jmespath.org/) query to run on the output of the command |
| OUTPUT | The output format (yaml, json) |
| WAIT | Tells duploctl to wait until a process has completed before continuing |
| OUTPUT_FILE | Write the output to a file |
| LOG_LEVEL | Log verbosity for the duploctl client (DEBUG, INFO, WARN, ERROR). Default: WARN |

## Prerequisites  

To make an update to a service you will need a duplo token. 

## References  
  - [This Repo (Bitbucket)](https://bitbucket.org/duplocloud/duploctl-pipe/src/main/)
  - [This Repo (GitHub)](https://github.com/duplocloud/duploctl-pipe)
  - [Bitbucket Pipe Advanced Techniques](https://support.atlassian.com/bitbucket-cloud/docs/advanced-techniques-for-writing-pipes/)
  - [Bitbucket Pipe Tools](https://bitbucket.org/bitbucketpipelines/bitbucket-pipes-toolkit/src/master/)

### GitHub Actions
  - [actions/checkout](https://github.com/actions/checkout)
  - [actions/setup-python](https://github.com/actions/setup-python)
  - [actions/upload-artifact](https://github.com/actions/upload-artifact)
  - [actions/download-artifact](https://github.com/actions/download-artifact)
  - [actions/create-github-app-token](https://github.com/actions/create-github-app-token)
  - [softprops/action-gh-release](https://github.com/softprops/action-gh-release)
  - [peter-evans/dockerhub-description](https://github.com/peter-evans/dockerhub-description)
  - [kentaro-m/auto-assign-action](https://github.com/kentaro-m/auto-assign-action)
  - [tarides/changelog-check-action](https://github.com/tarides/changelog-check-action)
  - [pmeier/pytest-results-action](https://github.com/pmeier/pytest-results-action)
  - [duplocloud/actions](https://github.com/duplocloud/actions)
  - [duplocloud/version-bump](https://github.com/duplocloud/version-bump)
