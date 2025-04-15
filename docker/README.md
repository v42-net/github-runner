# Using Docker
Docker offers three ways to run a container image:
- Simply with `docker run`, but without any support for secrets
- Using `docker compose`, with somewhat better support for secrets
- Using `docker service`, requiring a docker swarm, but most secure 

> *All of the example scripts referenced below expect the GitHub Access Token to be stored in `../secret.txt` (which is obviously not stored in GitHub). Create this file with your own GitHub Access Token (PAT) and update the scripts with the parameters for your environment before using them.*

## `docker run`
`docker run` uses environment variables to pass all configuration settings to
the container, including the GitHub Access Token, so not really secure.

> *See [`run.sh`](run.sh) for a full example on how to use `docker run`*

## `docker compose`
`docker compose` uses a compose file anf environment variables to define most
docker settings and the configuration settings to be passed to the container. 
Only the GitHub Access Token is passed as a secret (but docker compose does not
support encrypted secrets).

> *See [`compose.sh`](compose.sh) and [`compose.yaml`](compose.yaml) for a full example on how to use `docker compose`*

## `docker service`
`docker service` uses environment variables to pass most configuration settings
to the container. The GitHub Access Token is passed as an encrypted secret to
the container. This is the most secure docker solution.

> *See [`service.sh`](service.sh) for a full example on how to use `docker service`*
