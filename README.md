# plsmeme


![](static/plsmeme.gif)


## Intallation

1. Build the image

```bash
docker build -t plsmeme .
```

2. Create a `$HOME/.plsmeme.env` file as described in [Environment Variables](#environment-variables)

3. (OPTIONAL) Create a `$HOME/.plsmeme.toml` config file as desribed in [Configuration](#configuration)

4. Place `bin/plsmeme` on your $PATH


## Environment Variables

```
#.env
PLSMEME_REDDIT_CLIENT_ID=
PLSMEME_REDDIT_CLIENT_SECRET=
PLSMEME_REDDIT_USER_AGENT=
PLSMEME_REDDIT_USERNAME=
PLSMEME_REDDIT_PASSWORD=
```


## Configuration

[TOML](https://github.com/toml-lang/toml)

```toml
# This is the list of subreddits used by default
subreddits = [
  "catpictures",
  "dogpictures",
]

# Here you can specify groups of subreddits, you can use any key name you wish
# which is then useable with `-g` e.g. `-g sfw`
[subreddit_groups]
sfw = [
  "catpictures",
  "dogpictures",
]

```


## Developing


## Building

```bash
docker build -t plsmeme .
```


## Running

To work `plsmeme` requires the environment variables listed above, these can
be provided to the container with `-e` flags but this is not recommended as
they are secrets. Instead create a `$HOME/.plsmeme.env` file with those
contents and mount that file into the container at `/plsmeme/.env`.

`plsmeme` reads its from `/plsmeme/config/default.toml` inside the container,
there is a default config present but it will preferentially read from
`/plsmeme/config/.plsmeme.toml` if such a file is mounted.

```bash
docker run \
    -v $HOME/.plsmeme.env:/plsmeme/.env:ro \
    -v $HOME/.plsmeme.toml:/plsmeme/config/.plsmeme.toml \
    -t plsmeme:latest
```


### Committing

Use the `plscommit.sh` script instead of `git commit`. Only `plsmeme` output
should be the content of commit messages.


## git

To set your commit message to the output of `plsmeme` simply:

```bash
plsmeme -a | git commit -F -
```
