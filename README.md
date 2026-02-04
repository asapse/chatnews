# ChatNews

## News Aggregator from feeds

ChatNews is a news aggregator from feeds.  
## Installation

### Package Manager

UV is the package manager for the repository. You can install UV with:
```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### MongoDB

The project use MongoDB in local for Feature store. See [https://www.mongodb.com/docs/v8.0/tutorial/install-mongodb-on-ubuntu/#std-label-install-mdb-community-ubuntu](MongoDB) documentation to install it.


### ZenML

The project use ZenML for pipeline.  
You can start ZenML with the command:  
```sh
uv run zenml login --local
```


## How to run
You can run the pipeline to fetch articles from RSS with:
```sh
uv run -m chatnews.pipelines.run
```