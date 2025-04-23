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
- Start our local runner process and monitor the health of our GitHub runner

## Configuration
This version of the GitHub Action Runner container image uses environment
variables to pass the configuration settings to the container. All `GITHUB_*`
environment variables can be replaced by a `GITHUB_*_FILE` variable pointing
to a file mounted inside the container containing the actual value. This is
the prefered solution for passing the GitHub Access Token to the container.

#### `*_PROXY`
**Optional:** these environment variables are used to pass the proxies to be
used to both the control script and the GitHub Action runner itself.

#### `GITHUB_ORGANIZATION`
**Mandatory:** the GitHub organization to add the runner to.

#### `GITHUB_RUNNER_NAME`
**Mandatory:** the name to use to register the GitHub runner. The example
scripts use the fully qualified hostname of the GitHub Runner host, to make it
easier to identify where each GitHub runner is hosted.

#### `GITHUB_RUNNER_GROUP`
**Optional:** name of the runner group to add this runner to (defaults to the
default runner group). The specified runner group must already exist.

#### `GITHUB_RUNNER_LABELS`
**Optional:** custom labels that will be added to the runner (comma-separated,
no whitespace allowed).

#### `GITHUB_ACCESS_TOKEN`
**Mandatory:** the GitHub Access Token (PAT) used by the control script to
communicate with GitHub to register and monitor the GitHub Runner. The example
scripts prefer the `GITHUB_ACCESS_TOKEN_FILE` notation to prevent the actual
GitHub Access Token to be visible as an environment variable.

## Usage
- For use with Docker see the [`docker`](docker) folder.
- For use with Podman see the [`podman`](podman) folder (*to be documented*).
- For Microsoft Azure see the [`azure`](azure) folder (*partly documented*).
- For Google Cloud Platform see the [`gcp`](gcp) folder (*to be documented*).

I currently have no access to an AWS environment for testing purposes, 
but the principle will probably be the same as for the other environments.
