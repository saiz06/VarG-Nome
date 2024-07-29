# Cafe Variome Similarity Service

This repository holds the source code for similarity web service, intended to use either as a standalone service or as part of the Cafe Variome API.

## Disclaimer

This repository is under the MIT license. Please see the LICENSE file for more information.

This software is provided "as is", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose and non-infringement. In no event shall the authors or the organizations they represent be liable for any claim, damages or other liability, whether in an action of contract, tort or otherwise, arising from, out of or in connection with the software or the use or other dealings in the software.

Users are not allowed to use this software for commercial purposes, unless a commercial license is acquired from the authors, or explicitly permitted by the authors.

This software is still in development and is not ready for production use. Users are encouraged to test the software and report any issues to the authors. Please be aware that the software is not guaranteed to be stable and may change at any time. It's also worth noting that the software is not guaranteed to be secure in this stage and users should take appropriate measures to secure their installation.

## Installation

This software is written in Python only, and is developed against Python 3.10. It's recommended to use the latest compatible Python version with the given dependencies. To install the dependencies, run the following command:

```shell
pip install -r requirements.txt
```

Then the software can be run in development mode using the following command:

```shell
python main.py
```

## Configuration

There is a ``config.json`` file in the root of the repository. This file contains the configuration for the software. Like this:

```json
{
  "neo4j": {
    "uri": "neo4j://localhost:7687",
    "username": "neo4j",
    "password": "password",
    "authentication": "basic"
  },
  "connection": {
    "concurrency": 30
  }
}
```

They are:

- uri: The URI of the Neo4j database to connect to. Both neo4j:// and bolt:// are supported.
- username: The username to use to connect to the Neo4j database.
- password: The password to use to connect to the Neo4j database.
- authentication: The authentication method to use to connect to the Neo4j database. Currently only basic is supported.
- concurrency: The number of concurrent connections to use to the Neo4j database. This should be adjusted based on your processing power and memory. Setting it too high may cause the software or the database to crash.

## Preparing the database

Similarity service uses Neo4j to store the ontology structure, and relies on a series of pre-calculated values to provide semantic similarity search functions. We provide a database dump containing all necessary data to run the similarity service. The dump can be downloaded [here](https://artifactory.cafevariome.org/repository/neo4j-public/similarity-service/1.0.0/neo4j.dump).

After downloading, load it into a neo4j database. For community edition, this is done via `neo4j-admin`, and needs to be performed when the database is not running:

```shell
sudo systemctl stop neo4j     # Stop the Neo4j service
neo4j-admin database load neo4j --from-path=/path/to/dump/
```

## Deployment

### With production ASGI server

It's recommended to use a production ASGI server to run this software. The server this software is developed against is Hypercorn. To install Hypercorn, run the following command:

```shell
pip install hypercorn
```

Then to run the software, run the following command:

```shell
hypercorn main:app --bind 0.0.0.0:5000
```

### With Docker

The similarity service is packaged into a Docker image, built from the source code in this repository. To build it from source, first switch to `docker` branch, then run the following command in the project root:

```shell
docker build . -t similarity-service
```

Or the image can be pulled from GitHub Container Registry:

```shell
docker pull ghcr.io/cafevariomeuol/similarityservice:docker
```

The similarity service container requires a fully initialized Neo4j database to connect to, just like running from source code. If the neo4j database is running within a docker container, the `neo4j-admin` tool can still be used to load a database dump. Refer to the [official documents](https://neo4j.com/docs/operations-manual/current/docker/dump-load/) for more information. Simply put, stop any container running on the same volume, and run:

```shell
docker run --interactive --tty --rm \
    --volume=$HOME/neo4j/newdata:/data \
    --volume=$HOME/neo4j/backups:/backups \
    neo4j/neo4j-admin:5.19.0 \
neo4j-admin database load neo4j --from-path=/backups
```

Here is an example docker-compose file to start the similarity service with a neo4j database (assume the data is already loaded):

```yaml
services:
  neo4j:
    image: neo4j:5.16.0-community
    container_name: neo4j
    environment:
      NEO4J_AUTH: neo4j/neo4jpass
    volumes:
      - neo4j_data:/data
      - neo4j_logs:/logs
      - neo4j_import:/var/lib/neo4j/import
      - neo4j_plugins:/plugins

  similarity-service:
    image: ghcr.io/cafevariomeuol/similarityservice:docker
    container_name: similarity_service
    environment:
      NEO4J_URI: "neo4j://neo4j:7687"
      NEO4J_USERNAME: "neo4j"
      NEO4J_PASSWORD: "neo4jpass"
      CONCURRENCY: 30
    ports:
      - "5000:5000"
    depends_on:
      - neo4j

volumes:
  neo4j_data:
  neo4j_logs:
  neo4j_import:
  neo4j_plugins:
```

Adjust the volume settings to match your environment. Note the similarity service, when running in docker, can use environment variable to override the configuration file, so there's no need to mount a config file. Or, if the environment variables are not set, the service will fall back to the config file.
