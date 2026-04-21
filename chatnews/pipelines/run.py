import os

import click
from loguru import logger

from chatnews.pipelines.pipelines.extract_from_rss import extract_user_feeds


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
    default="test.yaml",
    type=click.STRING,
    help="File config path.",
)
@click.option(
    "--no-cache",
    is_flag=True,
    default=False,
    help="Disable caching for the pipeline run.",
)
def main(
    user_rss_config: str = "test.yaml",
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
    logger.info("Info run pipeline for file %s", user_rss_config)
    pipeline_args = {}
    if no_cache:
        pipeline_args["enable_cache"] = False
    pipeline_args["config_path"] = os.path.join(config_folder, user_rss_config)
    run_args_feature = {}
    extract_user_feeds.with_options(**pipeline_args)(**run_args_feature)
    logger.info("Feature Engineering pipeline finished successfully!\n")


if __name__ == "__main__":
    main()
