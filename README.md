
# Overview

Smart utilities for smart python programmers.

Docs are coming, just hang in there.

# Installation and setup

## Automatic Setup

1. Clone the repository with your favorite git client.

2. Prerequisites

The package is mostly automated using Make, but in order for the Makefile to work, the following tools must be available on the `$PATH`:

    + git
    + python
    + pip
    + virtualenv

The presence of these tools are checked by the Makefile. If your build fails with ```error: invalid environment configuration.``` please follow steps in the **Installing prerequisites** section below.

4. Use `make install` to install the package.

3. Use `make setup` to setup local development environment. Dependencies will be installed to a local virtualenv. You can start an interactive demo using `make shell`.


## Manual setup

## Installing prerequisites

The following command are required for this package to build/work. Each command is checked during execution of the Makefile. The results of the check is saved to the `.environment` file. Environment is only re-checked if the environment does not exist. Re-check can be enforced using `make checkenv`.

If there are missing tools, the output of `make *` will look something like: 

    ```
    checking environment....
    checking git...ok
    checking python...ok
    checking pip...NOT FOUND
    checking virtualenv...NOT FOUND
    error: invalid environment configuration.
    ```

Please follow the guides below to install tools labeled `NOT FOUND`.

### git

Download and install platform specific version from [https://git-scm.com/download].

### python

Download an install platfrom specific version from [https://www.python.org/downloads/].

### pip

Use `easy_install` to install pip.

    sudo easy_install pip

### virtualenv

Use `pip` to install `virtualenv`

    sudo pip install virtualenv

### Multiple versions of the same tool

The contents of the .environment file contains paths to where each tool was found. If you have multiple versions of a tool you can verify which one is going to be used by looking into the `.environment` file using `cat .environment`. You should see something like:

    ```
    cat .environment
    git is /usr/bin/git
    python is /usr/bin/python
    pip is /usr/local/bin/pip
    virtualenv is /usr/local/bin/virtualenv
    ```

### Virtualenv

Create the virtualenv using `make .virtualenv` or using the alias `make activate`.

Activate the virtualenv using `source activate`.

### Dependencies 

Dependencies are specified in the `requirements-.txt` files. 

Dependencies can be installed from these files into the local virtualenv using the following commands.

- `make deps`: install runtime dependencies from `requirements.txt`
- `make deps-test`: install test dependencies from `requirements-test.txt`
- `make deps-build`: install build dependencies from `requirements-build.txt`

The `make setup` executes all three targets above with a single command.

## Building and releasing

Use `make build` to build a version from the current source.

Use `make release-patch`, `make release-minor` or `make release-major` to test, build and release a new version of the package. The release includes bumping the specified version and making a new commit/tag with it.


# Demo mode

1. Use `make shell` to execute an interactive demo. Please see look for further documentation in `./shell.py`


# Usage

*TODO: Please document package specific usage here*

