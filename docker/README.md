# Using Docker
Docker offers three ways to run a container image:
- Simply with `docker run`, but without any support for secrets
- Using `docker compose`, with somewhat better support for secrets
- Using `docker service`, to be investigated ...

> *All of the example scripts referenced below expect the GitHub Access Token to be stored in `../secret.txt` (which is obviously not stored in GitHub). Create this file with your own GitHub Access Token (PAT) and update the scripts with the parameters for your environment before using them.*

## `docker run`
`docker run` uses environment variables to pass all configuration settings to
the container, including the GitHub Access Token, so not really secure.

> *See [`run.sh`] for a full example on how to use `docker run`*

## `docker compose`
*To-be-documented...*

## `docker service`
*To-be-documented...*
