# dicc

`dicc` is a simple terminal front end to Merriam-Webster's dictionary and thesaurus API.

## Features
For now, `dicc` only supports the Merriam-Webster Collegiate Dictionary API. Support for the Thesaurus API is planned.

I do not yet know how this will behave on Windows, though I can check in the near future.

### Caching
To save API requests, `dicc` caches the response from a given query. When searching for the same query again, it will use the cached response.

### User Configuration
Colors, cache location, and logging support are all exposed to the user to change in a user configuration file. This file is located in one of the common configuration locations:
- $XDG_CONFIG_HOME/dicc/config.toml
- .config/dicc/config.toml
- $HOME/dicc/config.toml

`dicc` searches for the configuration in this order, and will stop when it finds a user configuration file.

## Installation
`dicc` is written in python and is available on pypi, so is most easily installed with `pipx`.

```sh
pipx install dicc
```

You can, of course, install it with `pip`, though `pipx` is the preferred way to install python command line tools.

Once installed, an API key from Merriam-Webster is required. One can be acquired here: https://dictionaryapi.com/. They only provide you with access to two services per personal account.

A minimal user configuration is required, in one of the file locations specified above:
```toml
[api_keys]
collegiate_key = API_KEY
thesaurus_key = API_KEY
...
```

Keys are obviously only required for the service you wish to use. For now, I have no plans to implement any API responses other than the Collegiate API and the Thesaurus API, but am open to Pull Requests.

## Usage

Search for a word:
```sh
dicc search WORD
```
Search for a word in the thesaurus: (support in progress)
```sh
dicc search --method thesaurus WORD
dicc search -m t WORD
```
