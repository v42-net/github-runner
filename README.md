# github-runner
A self-managing version of the official GitHub Action Runner container image.

- https://github.com/v42-net/github-runner/pkgs/container/github-runner

This projects adds a control script to [the official GitHub Actions Runner container image](https://github.com/actions/runner/pkgs/container/actions-runner). This
allows the container to register, run and monitor its own organization action
runner without the need for any additional scripting.

#### DONE:
1. Import the configuration from the environment variables
2. Remove our local runner configuration
3. Connect to our GitHub organization
4. Remove our old runner registration
5. Get a new runner registration token
6. Configure our local runner process
7. Start our local runner process
8. Monitor the health of our GitHub runner

#### TODO:
9. Documentation for use with Docker
10. Documentation for use with Podman
11. Documentation for use with Azure
12. Documentation for use with GCP
