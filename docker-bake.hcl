variable "TAG" {
    default = "0.0.1"
}

variable "REGISTRY" {
    default = "duplocloud"
}

group "default" {
    targets = ["duploctl-pipe"]
}

target "duploctl-pipe" {
    tags = [
        "${REGISTRY}/bitbucket-deploy-pipe:latest",
        "${REGISTRY}/bitbucket-deploy-pipe:${TAG}"
    ]
    platforms = [
        "linux/amd64",
        "linux/arm64/v8"
    ]
}