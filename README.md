# Swing
Swing is an open-source client for creating compounded Docker Swarm deployments using already prepared services called Swing Charts.
The charts can be installed from public repositories served by the Swing Server application.

## Installation

The application can be installed from the PyPI repository using the next command.

```shell
pip install swing-cli
```

## Requirements

For creating and publishing Swing Charts, you have to have access to the [Swing Server](https://pypi.org/project/swing-server/),
which can be installed from the PyPI repository.

## Configuration

For communication with the Swing Server, you have to provide server URL and login credentials.
This information has to be set using a configuration file, which has to be placed at the home folder
under `~/.swing` file or provided using `--config` parameter of the client tool.

```
[swing]
server = http://localhost:5000
email = user123@gmail.com
password = pass123
```

## Client Commands

The client can be used using command line command.

```
Usage: swing [OPTIONS] COMMAND [ARGS]...

  Client for the communication with the Swing Server respository.

Options:
  -c, --config FILENAME  Swing configuration file.
  --help                 Show this message and exit.

Commands:
  build    Build the installed charts to the final docker compose file.
  delete   Delete the chart or specific release from the repository server.
  install  Install requirements specified in the dependency file.
  publish  Upload the local chart to the remote respository.
  search   Search for available charts.
  show     Show releases of the specific chart.
```

### Chart List

You can list all uploaded charts using the search command. If you want to filter the charts, append the keyword to the command.

```shell
swing search KEYWORD
```

### Release Detail

If you want to show releases of the specific chart, use the show command.

```shell
swing show CHART
```

### Chart Delete

To delete the chart from the server, call the delete command. You can only delete the charts you have uploaded using your account.
If you want to just delete a specific release of the chart, you can pass `--version` argument.

```shell
swing delete [OPTIONS] CHART

Options:
  -v, --version VERSION  Version of the release to delete.
```

### Chart Publish

You can easily create new charts and then upload them to the repository server. You can provide some details about
the release using `--notes` argument.

```shell
swing publish [OPTIONS] PATH

Options:
  -n, --notes MESSAGE  Some release notes.
```

First, create a new directory, and the following files: `chart.yaml`, `deployment.yaml` and `values.yaml`.

#### Chart Definition

Every chart has to have the definition file, where are the name and the description. Also, when you are publishing
the chart, you have to specify the version. Example of the Redis chart:

```yaml
description: Basic redis chart
name: redis
version: 1.0.0
```

#### Deployment Specification

Next, you have to create a deployment specification using Docker Compose notation. You can use [Jinja2](https://jinja.palletsprojects.com/en/2.11.x/)
templating language to prepare complex and generic deployments.

```yaml
version: '3.8'

services:
  {{ Values.serviceName }}:
    image: redis:{{ Values.image.tag }}
    command: redis-server {% if Values.usePassword %}--requirepass {{ Values.password }}{% endif %}
    deploy:
      mode: replicated
      replicas: 1
```

#### Default Values

Finally, you have to provide default values for the chart deployment specification. You can make configurable parameters
like a number of replicas, service passwords, or image tags.

```yaml
serviceName: redis

image:
  tag: 6

usePassword: false
password: null
```

### Requirements Installation

If you want to use the published Swing Charts, you have to install them using `requirements.yaml` file.

```shell
swing install [OPTIONS]

Options:
  -r, --requirements FILENAME  Chart dependencies file.
```

The requirement can be both downloaded from the remote repository (in this case, you have to provide the chart name, and the release
version) or loaded from the local filesystem (in this case, you have to provide the path to this directory).

```yaml
dependencies:
  - name: redis
    version: 2.1
  - name: psql
    file: ../charts/postgresql
```

### Chart Build

If you have already installed the dependencies, you can build the charts to the final Docker Compose file.
Before that, make sure you have installed the `docker-compose` command.

```shell
swing build [OPTIONS] PATH

Options:
  -o, --output PATH  Docker compose output path.
```

To override the installed charts' default values, you can create `values.yaml` file where will be provided custom values.

```yaml
redis:
  usePassword: true
  password: password234
  
psql:
  username: root
  database: main
  password: secret432
```

## Project Requirements

### Functional Requirements
- Downloading charts from the repository.
- Listing available charts and versions.
- Packaging and uploading a new version of the chart.
- Merging charts and project services into a single compose file.

### Nonfunctional Requirements
- Charts can be installed by name or using the dependencies file.
- The client should be configurable using a config file.
- Before uploading the chart, secrets have to be set in the config file.
- The client should support the help command.

