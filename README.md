# ChatNews

ChatNews is a small Python project that aggregates news articles from RSS/Atom feeds
and stores them in a feature store (MongoDB) for downstream processing.

## Overview

ChatNews fetches articles from RSS/Atom feeds, performs lightweight processing
(language detection, clean text), and persists results to a MongoDB-backed
store used by the project.

## Features

- Fetch articles from RSS/Atom feeds
- Simple pipeline orchestration for extract/process/store
- MongoDB-backed feature store

## Requirements

- Python 3.12
- MongoDB running locally see documentation: [mongodb](https://www.mongodb.com/docs/v8.0/tutorial/install-mongodb-on-ubuntu/#std-label-install-mdb-community-ubuntu)
- `uv` for package manager
- `ZenML` for pipeline management

**Installation**

1. Clone the repository:

```bash
git clone git@github.com:asapse/chatnews.git
cd chatnews
```
2. Install UV

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

3. Run ZenML
```sh
uv run zenml login --local
```

## Configuration

- Pipeline configs live in `chatnews/pipelines/configs/`.
- Add a YAML config (example below) and pass it to the runner with
  `--user-rss-config`.
- Ensure MongoDB is available
- Create `.env` file like `.env.example`

Example config (`chatnews/pipelines/configs/test.yaml`):

```yaml
parameters:
  user_full_name: Bob Alice
  links:
    - https://maximelabonne.substack.com/feed
```

## Usage

Run the pipeline module directly:

```bash
uv run --env-file .env -m chatnews.pipelines.run --user-rss-config test.yaml
```

Available options used by the runner include `--user-rss-config <file>` and
`--no-cache` to force reprocessing.

## Contributing

Contributions are welcome. Please open issues or pull requests with a clear
description of the change and tests where appropriate.

## License

This project is provided under the terms of the repository license. See the
`LICENSE` file for details.