import os
from datetime import datetime

import click
from loguru import logger
from zenml.client import Client

from chatnews.pipelines.pipelines.extract_from_rss import extract_user_feeds
from chatnews.pipelines.pipelines.features_store import features_store


def get_last_run(client: Client, pipeline_name: str, step_name: str) -> datetime:
    last_run = None
    try:
        last_pipeline_run = client.get_pipeline(pipeline_name).last_successful_run
        last_step_run = last_pipeline_run.steps[step_name]
        last_run = last_step_run.start_time
    except (KeyError, RuntimeError):
        pass
    return last_run or datetime(2025, 1, 1)


@click.command(
    help="""
ChatNews project.

Examples:

  \b
  # Run the rss fetcher pipeline
    python run.py --user-rss-config test.yaml
"""
)
@click.option(
    "--user-rss-config",
    is_flag=False,
    flag_value="test.yaml",
    type=click.STRING,
    help="File config path.",
)
@click.option(
    "--process-documents",
    is_flag=False,
    flag_value="test_process_documents.yaml",
    type=click.STRING,
    help="File config for processing documents.",
)
@click.option(
    "--no-cache",
    is_flag=True,
    default=False,
    help="Disable caching for the pipeline run.",
)
def main(
    user_rss_config: str,
    process_documents: str,
    no_cache: bool = False,
):
    """Main entry point for the pipeline execution.

    This entrypoint is where everything comes together:

      * configuring pipeline with the required parameters
        (some of which may come from command line arguments, but most
        of which comes from the YAML config files)
      * launching the pipeline

    Args:
        user_rss_config: The name of the config file for an user and his feeds.
        no_cache: If `True` cache will be disabled.
    """

    config_folder = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "configs",
    )
    pipeline_args = {}
    if no_cache:
        pipeline_args["enable_cache"] = False

    run_args_feature = {}

    client = Client()

    if user_rss_config:
        logger.info("Info run pipeline for file %s", user_rss_config)
        pipeline_args["config_path"] = os.path.join(config_folder, user_rss_config)
        extract_user_feeds.with_options(**pipeline_args)(**run_args_feature)
    if process_documents:
        logger.info(f"\n{process_documents}")
        logger.info("Info run pipeline for file %s", process_documents)
        pipeline_args["config_path"] = os.path.join(config_folder, process_documents)
        last_run = get_last_run(
            client, pipeline_name="features_store", step_name="query_data_warehouse"
        )
        features_store.with_options(**pipeline_args)(
            last_run=last_run, **run_args_feature
        )

    logger.info("Feature Engineering pipeline finished successfully!\n")


if __name__ == "__main__":
    main()
