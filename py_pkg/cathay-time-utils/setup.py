import os
import sys

from setuptools.command.install import install
from setuptools.command.test import test as TestCommand
from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()


class Install(install):
    """
        custom install command
        usage
            python setup.py install [--pip-args="{pip-args}"]
        notice
            pip-args: use "" to wrap your pip arguments
    """
    description = "install with specific pypi server"
    user_options = install.user_options + [('pip-args=', None, 'args for pip')]

    def initialize_options(self):
        install.initialize_options(self)
        self.pip_args = None

    def finalize_options(self):
        install.finalize_options(self)
        if self.pip_args is None:
            print('pip_args not set, using default https://pypi.org/simple/')

    def run(self):
        for dep in self.distribution.install_requires:
            install_cmd = "pip install {} --disable-pip-version-check --no-cache-dir".format(dep)
            if self.pip_args is not None:
                install_cmd += ' ' + self.pip_args
            os.system(install_cmd)
        install.run(self)


class PyTest(TestCommand):
    """
        pytest
        usage
            python setup.py test [-a {arg}|--pytest-args={arg}] [--pip-args="{pip-args}"]
        notice
            pip-args: use "" to wrap your pip arguments
    """
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test"),
                    ('pip-args=', None, 'args for pip')]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []
        self.pip_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
        if self.pip_args is None:
            print('pip_args not set, using default https://pypi.org/simple/')

    def run(self):
        for dep in self.distribution.install_requires + self.distribution.tests_require:
            install_cmd = "pip install {} --disable-pip-version-check --no-cache-dir".format(dep)
            if self.pip_args is not None:
                install_cmd += ' ' + self.pip_args
            os.system(install_cmd)
        TestCommand.run(self)

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        # pytest should pass list object to main, so turn it to list if there's only one option
        pytest_args = [self.pytest_args] if isinstance(self.pytest_args, basestring) else self.pytest_args
        errno = pytest.main(pytest_args)
        sys.exit(errno)


setup(
    name="cathay-time-utils",
    version="1.0",
    author="",
    author_email="",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=2.7",
    install_requires=['python-dateutil==2.7.3',
                      'pytz==2018.5'],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7"
    ],
    keywords=["time", "date", "utils"],
    entry_points={},
    tests_require=['pytest'],
    zip_safe=False,
    cmdclass={'install': Install,
              'test': PyTest}
)
