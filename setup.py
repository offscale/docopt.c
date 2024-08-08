# -*- coding: utf-8 -*-

"""
setup.py implementation, interesting because it parsed the first __init__.py and
    extracts the `__author__` and `__version__`
"""

import sys
from ast import Assign, Name, parse
from functools import partial
from operator import attrgetter

from os import listdir, path
from os.path import extsep

from setuptools import find_packages, setup

if sys.version_info[:2] >= (3, 12):
    from ast import Del as Str
else:
    from ast import Str

    if sys.version_info[0] == 2:
        from itertools import ifilter as filter
        from itertools import imap as map

if sys.version_info[:2] > (3, 7):
    from ast import Constant
else:
    from ast import expr

    # Constant. Will never be used in Python < 3.8
    Constant = type("Constant", (expr,), {})


package_name = "docopt_c"

with open(
    path.join(path.dirname(__file__), "README{extsep}md".format(extsep=extsep)), "rt"
) as fh:
    long_description = fh.read()


def gen_join_on_pkg_name(*paths):
    """
    Create a function that joins on `os.path.join` from the package name onward

    :param paths: one or more str, referring to relative folder names
    :type paths: ```*paths```

    :return: function that joins on `os.path.join` from the package name onward
    :rtype: ```Callable[tuple[str, ...], str]```
    """
    return partial(path.join, path.dirname(__file__), package_name, *paths)


def main():
    """Main function for setup.py; this actually does the installation"""
    with open(
        path.join(
            path.abspath(path.dirname(__file__)),
            "{package_name}{extsep}py".format(package_name=package_name, extsep=extsep),
        )
    ) as f:
        parsed_init = parse(f.read())

    __author__, __version__, __description__ = map(
        lambda node: node.value if isinstance(node, Constant) else node.s,
        filter(
            lambda node: isinstance(node, (Constant, Str)),
            map(
                attrgetter("value"),
                filter(
                    lambda node: isinstance(node, Assign)
                    and any(
                        filter(
                            lambda name: isinstance(name, Name)
                            and name.id
                            in frozenset(
                                ("__author__", "__version__", "__description__")
                            ),
                            node.targets,
                        )
                    ),
                    parsed_init.body,
                ),
            ),
        ),
    )

    _data_join = partial(path.join, package_name, "_data")
    package_data = {
        "": list(map(_data_join, listdir(_data_join())))
    }

    setup(
        name=package_name,
        author=__author__,
        author_email="807580+SamuelMarks@users.noreply.github.com",
        version=__version__,
        url="https://github.com/docopt/docopt.c",
        description=__description__,
        long_description=long_description,
        long_description_content_type="text/markdown",
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Environment :: Console",
            "Intended Audience :: Developers",
            "License :: OSI Approved",
            "License :: OSI Approved :: MIT License",
            "Natural Language :: English",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Programming Language :: Python :: 3.12",
            "Programming Language :: Python :: 3.13",
            "Programming Language :: Python :: Implementation",
            "Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator",
            "Topic :: Software Development",
            "Topic :: Software Development :: Build Tools",
            "Topic :: Software Development :: Code Generators",
            "Topic :: Software Development :: Compilers",
            "Topic :: Software Development :: Pre-processors"
        ],
        license="MIT",
        license_files=["LICENSE-MIT"],
        py_modules=[package_name],
        scripts=["docopt.py", "docopt_c.py"],
        packages=find_packages(),
        package_data=package_data,
        include_package_data=True,
    )


def setup_py_main():
    """Calls main if `__name__ == '__main__'`"""
    if __name__ == "__main__":
        main()


setup_py_main()
