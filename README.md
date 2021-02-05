# Swing

Swing is an open-source client for creating compounded Docker Swarm deployments using already prepared services called Swing Charts. The charts can be installed from public repositories served by the Swing Server application.

```
[swing]
server = http://localhost:5000
email = user123@gmail.com
password = pass123
```

## Functional Requirements

- Downloading charts from the repository.
- Listing available charts and versions.
- Packaging and uploading a new version of the chart.
- Merging charts and project services into a single compose file.

## Nonfunctional Requirements

- Charts can be installed by name or using the dependencies file.
- The client should be configurable using a config file.
- Before uploading the chart, secrets have to be set in the config file.
- The client should support the help command.
