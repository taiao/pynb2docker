# generator.py
# Copyright (C) 2020 Fracpete (fracpete at gmail dot com)

import argparse
import logging
import traceback

# logging setup
logger = logging.getLogger("pynb2docker.generator")


def generate(input, docker_base_image, docker_instructions, output_dir):
    """

    :param input: the Jupyter notebook to convert
    :type input: str
    :param docker_base_image: the name of the Docker base image to use
    :type docker_base_image: str
    :param docker_instructions: the file with the additional docker instructions to insert
    :type docker_instructions: str
    :param output_dir: the output directory for the generated files, like Dockerfile
    :type output_dir: str
    """

    pass


def main(args=None):
    """
    Runs the .nfo generation.
    Use -h/--help to see all options.

    :param args: the command-line arguments to use, uses sys.argv if None
    :type args: list
    """

    parser = argparse.ArgumentParser(
        description='Converts Python Jupyter notebooks into Docker images.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        prog="pynb2docker")
    parser.add_argument("-i, --input", metavar="NOTEBOOK", dest="input", required=True, help="the Python notebook to convert")
    parser.add_argument("-b, --docker_base_image", metavar="IMAGE", dest="docker_base_image", required=True, help="the Docker base image to use, e.g., 'python:3.7-buster'")
    parser.add_argument("-I, --docker_instructions", metavar="FILE", dest="docker_instructions", required=False, help="file with additional docker instructions to use for generating the Dockerfile.")
    parser.add_argument("-o, --output_dir", metavar="DIR", dest="pattern", required=False, default="*.imdb", help="the pattern for the files that contain the movie IDs")
    parser.add_argument("--verbose", action="store_true", dest="verbose", required=False, help="whether to output logging information")
    parser.add_argument("--debug", action="store_true", dest="debug", required=False, help="whether to output debugging information")
    parsed = parser.parse_args(args=args)
    # configure logging
    if parsed.debug:
        logging.basicConfig(level=logging.DEBUG)
    elif parsed.verbose:
        logging.basicConfig(level=logging.INFO)
    logger.debug(parsed)
    generate(input=parsed.input, docker_base_image=parsed.docker_base_image,
             docker_instructions=parsed.docker_instructions, output_dir=parsed.output_dir)


def sys_main():
    """
    Runs the main function using the system cli arguments, and
    returns a system error code.

    :return: 0 for success, 1 for failure.
    :rtype: int
    """

    try:
        main()
        return 0
    except Exception:
        logger.info(traceback.format_exc())
        return 1


if __name__ == "__main__":
    try:
        main()
    except Exception:
        logger.info(traceback.format_exc())
