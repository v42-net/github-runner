# Using Azure
Azure offers multiple ways to run a container image. For now only configuration
as an Azure Container Instance through the Azure Portal is documented here.

## Azure Portal
- Login to [Azure Portal](https://portal.azure.com/) and select the correct [Directory](https://portal.azure.com/#settings/directory)
- On the [Home page](https://portal.azure.com/#home) under Azure services click [Create a resource](https://portal.azure.com/#create/hub)
- In the search box type "container instances" followed by `Enter`
- Create a new Microsoft Azure Container Instances Service
  - Select the correct subscription and resource group
  - Select `Container name` = `github-runner-<github-organization>`
    - for instance `github-runner-v42-net`
  - Select your prefered region and optionally other parameters
  - Select `Image source` = `Other registry`
  - Select `Image type` = `Public`
  - Select `Image` = `ghcr.io/v42-net/github-runner:latest`
  - Select `OS type` = `Linux`
  - The default size of 1 vcpu and 1.5 GiB memory should be okay
- Click `Next : Networking >`
  - Select `Networking type` = None
- Click `Next : Monitoring >`
  - I haven't used Insights yet ...
- Click `Next : Advanced >`
  - Select `Restart policy` = `Always`
  - Set the environment variables:
    | Mark as secure | Key | Value | For instance |
    | -------------- | --- | ----- | ------------ |
    | No             | `GITHUB_ORGANIZATION` | `<github-organization>` | `v42-net`       |
    | No             | `GITHUB_RUNNER_NAME`  | `<unique-runner-name>`  | `azure-v42-net` |
    | Yes            | `GITHUB_ACCESS_TOKEN` | `<github-access-token>` | `ghp_********`  |
  - The `GITHUB_RUNNER_NAME` should indicate where it is running, like `azure-<directory>`
  - Optionally add variables for `GITHUB_RUNNER_GROUP` and/or `GITHUB_RUNNER_LABELS`
  - Select `Key management` = `Microsoft-managed keys (MMK)`
- Click `Next : Tags >`
  - I haven't used tags yet ...
- Click `Next : Review + create >`
  - Review all settings ... yes, really ...
- Click `Create`
  - Wait until the deployment is finished, this can take several minutes ...
  - Once the deployment is complete, click `Go to resource` ...
  - 
  - In GitHub, check that the configured organization runner is online



