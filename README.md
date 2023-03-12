# NotifyMe

NotifyMe is a tiny, lightning-fast, and incredibly simple web service for streamlined notifications. It requires minimal setup and **no database** to run. Based on the powerful Apprise Python module, it can send notifications to a wide variety of destinations, including Telegram, Slack, SMS, and email.

NotifyMe can also be easily integrated with [Shepherd](https://github.com/djmaze/shepherd), a Docker swarm service that automatically updates your services whenever their base image is refreshed.

## Supported platforms

- linux/amd64
- linux/arm64
- linux/arm32/v7 *(Yeah! Your Raspberry Pi is supported!)*

## Getting Started

NotifyMe is shipped as a [Docker image](https://hub.docker.com/r/pysergio/notifyme). To use it, you need a Docker Engine
installed on your machine. In addition, Docker Compose is recommended.

Please, check the [endpoint API documentation first](https://s-nagaev.github.io/notifyme/#/group-send-noification/).

### Quick start (no configuration is required)

```bash
docker run -p 8000:8000 pysergio/notifyme:latest
```

Please note that in the example above, we must provide the target URL every time we call the API endpoint.

### Setting up via Docker Compose and environment variables

Create the file `docker-compose.yml` in any directory of your choice:

```yaml
version: '3'

services:
  notifyme:
    restart: unless-stopped
    image: pysergio/notifyme:latest
    environment:
      NOTIFYME_DEFAULT: tgram://12345678910:DKFJDHKDS-DKwsksdpORUjdsiYerk/-987654321/
      NOTIFYME_WEBAPP: mailto://server.com?smtp=smtp.server.com&from=noreply@server.com&to=myemail@server.com
      NOTIFYME_MONITOR: discord://4174216298/JHMHI8qBe7bk2ZwO5U711o3dV_js,mailto://server.com?smtp=smtp.server.com&from=noreply@server.com&to=myemail@server.com
```

Then run the command:

```bash
docker-compose up -d
```

In the example above, we have several environment variables that set up different notification targets. Now we may call the endpoint just providing the `title`, `body` and `setting` params, i.e.:

```json
{
  "setting": "NOTIFYME_WEBAPP",
  "title": "Registration",
  "body": "New user account registered: ..."
}
```

Moreover, as far as we set up the `NOTIFYME_DEFAULT` setting, we can call the endpoint not specifying the `url` or `setting` param at all:

```json
{
  "title": "Registration",
  "body": "New user account registered: ..."
}
```

The approach shown in the example above can be a handful if we want to integrate NotifyMe with the [Shepherd](https://github.com/djmaze/shepherd) (provide the NotifyMe URL using the `APPRISE_SIDECAR_URL` env variable).

### Using NotifyMe in Docker Swarm

Using the Docker Swarm, you may want to store the application settings in the docker secrets. The decrypted secrets are mounted into the container in an in-memory filesystem. The location of the mount point within the container defaults to `/run/secrets/<secret_name>`.

You still may set up NotifyMe using the data stored in the docker secret files. Let's say you have a docker secret named `tgram_notofocation_url`, and you want to keep it in the setting named `NOTIFYME_TGRAM`. All you need is to provide the environment variable named `NOTIFYME_TGRAM_FILE` containing the path to the docker secret, i.e., `NOTIFYME_TGRAM_FILE=/run`/secrets/tgram_notofocation_url. That's all. Now, you can call the endpoint using the `NOTIFYME_TGRAM`  setting in the body:

```json
{
  "setting": "NOTIFYME_TGRAM",
  "title": "Some Title",
  "body": "Message body here"
}
```

### Other settings

In case you want to integrate NotifyMe with the Sentry, you may optionally provide two additional environment variables:

- `SENTRY_DSN` - should contain a valid Sentry DSN string.
- `ENVIRONMENT` - should contain environment name (`production` by default).

## Authorization and authentication

The service is designed to be as simple as possible, running without database integration. So no authorization and authentication functionality is expected. 

Suppose you need such functionality or want to restrict access to the service in any way. In that case, you should set it up via firewall, web server, reverse proxy settings or use security groups or any resource-level permissions and conditions provided by your cloud provider.

## Built With

- Python 3.9+
- [FastAPI](https://github.com/tiangolo/fastapi)
- [Apprise](caronc/apprise)

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags).

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
