# pynb2docker
Library for turning Python Jupyter Notebooks into Docker images.

## Installation (Linux)

* Create a virtual environment:

  ```commandline
  virtualenv -p /usr/bin/python3.7 venv
  ```

* From source:

  ```commandline
  git clone https://github.com/fracpete/pynb2docker.git
  cd pynb2docker
  ../venv/bin/pip install setup.py
  ```

## Coding conventions

You can use the *line magics* in your notebook to define all the required
libraries that your code depends on, e.g., if you need *numpy*, then add this
in a *code* cell: 

```
%pip install numpy
```

Of course, in order to take advantage of this *non-standard* line magic, you need 
to install the [pip-magic](https://github.com/Carreau/pip_magic) library in your 
environment:

```commandline
pip install pip_magic
``` 


## Example

For this example we use the [pandas_filter_pipeline.ipynb](jupyter/pandas_filter_pipeline.ipynb)
notebook and the additional [pandas_filter_pipeline.dockerfile](jupyter/pandas_filter_pipeline.dockerfile)
Docker instructions. This notebook contains a simple Pands filter setup, using
a simple query to remove certain rows from the input CSV file and saving the cleaned 
dataset as a new CSV file.

The command-lines for this example assume this directory structure:

```
/some/where
|
+- venv   // virtual environment with pynb2docker installed
|
+- data
|  |
|  +- notebooks
|  |  |
|  |  +- pandas_filter_pipeline.ipynb       // actual notebook
|  |  |
|  |  +- pandas_filter_pipeline.dockerfile  // additional Dockerfile instructions
|  |
|  +- in
|  |  |
|  |  +- bolts.csv   // raw dataset to filter
|  |
|  +- out
|
+- output
|  |
|  +- pandascsvcleaner  // will contain all the generated data, including "Dockerfile"
```

For our `Dockerfile`, we use the `python:3.7-buster` base image (`-b`), which
contains a Python3.7 installation on top of a [Debian "buster"](https://www.debian.org/releases/buster/)
image. The `pandas_filter_pipeline.ipynb` notebook (`-i`) then gets turned into Python code
using the following command-line:

```commandline
./venv/bin/pynb2docker \
  -i /some/where/data/notebooks/pandas_filter_pipeline.ipynb \ 
  -o /some/where/output/pandascsvcleaner \
  -b python:3.7-buster \
  -I /some/where/data/notebooks/pandas_filter_pipeline.dockerfile  
```

Now we build the docker image called `pandascsvcleaner` from the `Dockerfile`
that has been generated in the output directory `/some/where/output/pandascsvcleaner` 
(`-o` option in previous command-line):

```
cd /some/where/output/pandascsvcleaner
sudo docker build -t pandascsvcleaner .
```

With the image built, we can now push the raw CSV file through for cleaning.
For this to work, we map the in/out directories from our directory structure
into the Docker container (using the `-v` option) and we supply the input
and output files via the `INPUT` and `OUTPUT` environment variables (using 
the `-e` option). In order to see a few more messages, we also turn on the
debugging output that is part of the notebook, using the `VERBOSE` environment
variable:

```
sudo docker run -ti \
  -v /some/where/data/in:/data/in \
  -v /some/where/data/out:/data/out \
  -e INPUT=/data/in/bolts.csv \
  -e OUTPUT=/data/out/bolts-clean.csv \
  -e VERBOSE=true \
  pandascsvcleaner
```

From the debugging messages you can see that the initial dataset with 40 rows
of data gets reduced to 24 rows.

**Disclaimer:** This is just a simple notebook tailored to the UCI dataset
*bolts.csv*.
