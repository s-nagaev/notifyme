# NotifyMe

NotifyMe is a lightning fast and incredibly simple web service for streamlined notifications. It is requiring minimal setup and **no database** to run. Based on the powerful Apprise Python module, it can send notifications to a wide variety of destinations, including Telegram, Slack, SMS, and email.

NotifyMe can be also easily integrated with [Shepherd](https://github.com/djmaze/shepherd), a Docker swarm service that
automatically updates your services whenever their base image is refreshed.

## Supported platforms

- linux/amd64
- linux/arm64
- linux/arm/v7 *(Yeah! Your Raspberry Pi is supported!)*

## Getting Started

NotifyMe is shipped as a [Docker image](https://hub.docker.com/r/pysergio/notifyme). To use it, you need a Docker Engine
installed on your machine. In addition, Docker Compose is recommended.

Please, check the endpoint API documentation first.

### 1. No configuration is required to quickly start the service

```bash
docker run -p 8000:8000 pysergio/notifyme:latest
```

Please note, that in example above we have to provide the target URL every time we're calling the API endpoint.

### 2. Setting up via Docker Compose and evironment variables

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

In the example above, we have a couple of the environment variables that are setting up different notification targets. Now we may call the endpoint just providing the `title`, `body` and `setting` params, i.e.:

```json
{
  "setting": "NOTIFYME_WEBAPP",
  "title": "Registration",
  "body": "New user account registered: ..."
}
```

Moreover, as fas as we set up the `NOTIFYME_DEFAULT` setting, we can call the endpoint not specifying the `url` or `setting` param at all:

```json
{
  "title": "Registration",
  "body": "New user account registered: ..."
}
```

The approach shown in example above can be handful in case we want to integrate NotifyMe with the [Shepherd](https://github.com/djmaze/shepherd) (just provide the NotifyMe URL using the `APPRISE_SIDECAR_URL` env variable).

### 3. Using NotifyMe in Docker Swarm



- `DATABASE_URL` *(required)*: a URL containing database connection data.
- `SECRET_KEY` *(required)*: a secret key that provides cryptographic signing and should be set to a unique,
unpredictable value.
- `ADMIN_USERNAME` *(required for the first run only)*: a username for an administrative account.
- `ADMIN_PASSWORD` *(required for the first run only)*: a password for an administrative account.
- `ADMIN_EMAIL` *(required for the very first run only)*: an email for an administrative account.
- `DOMAIN_DISPLAY` *(optional)*: a protocol and domain where your application instance hosted, i.e.
`https://mysite.com`, `http://192.168.1.150:8000`. The default value is `http://127.0.0.1:8000`.

2. Then run the command:

```shell
docker-compose up -d
```

Please, note that the parameter `-d` in the command example will tell Docker Compose to run the apps defined in
`docker-compose.yml` in the background.

The site should now be running at <http://0.0.0.0:8000>. To access the service admin panel visit
`http://localhost:8000/admin/` and log in as a superuser.

### Prerequisites

- [Dependency 1]
- [Dependency 2]
- [Dependency 3]

### Installing

A step by step series of examples that tell you how to get a development environment running.

1. Clone the repository

## Deployment

Add additional notes about how to deploy this on a live system.

## Built With

- [Dependency 1]
- [Dependency 2]
- [Dependency 3]

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags).

## Authors

- [Author 1]
- [Author 2]
- [Author 3]

## License

This project is licensed under the [License Name] License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

- [Acknowledgment 1]
- [Acknowledgment 2]
- [Acknowledgment 3]
