# github-runner
A self-managing version of the official GitHub Action Runner container image.

- https://github.com/v42-net/github-runner/pkgs/container/github-runner

This projects adds a control script to [the official GitHub Actions Runner 
container image](https://github.com/actions/runner/pkgs/container/actions-runner).
This allows the container to register, run and monitor its own organization
action runner without the need for any additional scripting.

The control script performs the following tasks:
- Import the configuration from the environment variables
- Remove our local runner configuration (only relevant on restarts)
- Connect to our GitHub organization and remove our old runner registration
- Get a new runner registration token and configure our local runner process
- Start our local runner process an monitor the health of our GitHub runner

#### TODO:
- Documentation about `secret.env`
- Documentation for use with Docker
- Documentation for use with Podman
- Documentation for use with Azure
- Documentation for use with GCP
