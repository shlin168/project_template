from __future__ import print_function
import os
import sys
from io import open

from setuptools import setup, Command, find_packages
from setuptools.command.install import install
from setuptools.command.test import test as TestCommand


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


class InstallLibs(Command):
    """
        install packages in py_pkg
        usage:
            python setup.py lib [-p py_pkg | --lib-path=py_pkg] [--pip-args="{pip-args}"]
        notice
            pip-args: use "" to wrap your pip arguments
    """
    description = "Install py_pkg libs"
    user_options = [('lib-path=', 'p', "Arguments to install libs in py_pkg"),
                    ('pip-args=', None, 'args for pip')]

    def initialize_options(self):
        self.lib_path = None
        self.pip_args = None

    def finalize_options(self):
        if self.pip_args is None:
            print('pip-args not set, using: https://pypi.org/simple/')

    def run(self):
        install_cmd = "python setup.py install"
        if self.pip_args is not None:
            install_cmd += ' --pip-args="{}"'.format(self.pip_args)

        project_dir = os.getcwd()
        if self.lib_path is not None:
            for pkg in os.listdir(self.lib_path):
                print(os.path.join(project_dir, self.lib_path, pkg))
                os.chdir(os.path.join(project_dir, self.lib_path, pkg))
                os.system(install_cmd)
        else:
            print('set py_pkg path')


class InstallExtra(Command):
    """
        install packages in extra_requires
        usage:
            python setup.py extra -k <key> [-p py_pkg | --lib-path=py_pkg] [--pip-args="{pip-args}"]
        notice
            pip-args: use "" to wrap your pip arguments
    """
    description = "Install extra_requires with key"
    user_options = [('key=', 'k', "key in extra_requires to install libs"),
                    ('pip-args=', None, 'args for pip')]

    def initialize_options(self):
        self.key = None
        self.pip_args = None

    def finalize_options(self):
        if self.pip_args is None:
            print('pip-args not set, using: https://pypi.org/simple/')

    def run(self):
        if self.key is not None:
            if self.key in self.distribution.extras_require:
                cmd_list = ["pip install {} --disable-pip-version-check --no-cache-dir".format(
                    pkg) for pkg in self.distribution.extras_require[self.key]]
            else:
                raise ValueError('key is not in extras_require, available key: {}'.format(
                    self.distribution.extras_require.keys()))
        else:
            pkg_list = [pkg for pkgs in self.distribution.extras_require.values() for pkg in pkgs]
            cmd_list = [
                "pip install {} --disable-pip-version-check --no-cache-dir".format(pkg) for pkg in pkg_list]
        if self.pip_args is not None:
            cmd_list = map(lambda v: ' '.join([v, self.pip_args]), cmd_list)

        for cmd in cmd_list:
            print(cmd)
            os.system(cmd)


class Clean(Command):
    """
        custom clean command
        usage:
            python setup.py clean [-e|--egg]
    """
    description = "Cleans build files"
    user_options = [('egg', 'e', "Arguments to clean with .eggs folder")]

    def initialize_options(self):
        self.egg = None

    def finalize_options(self):
        if self.egg is None:
            print('not deleting .eggs folder')

    def run(self):
        cmd = dict(
            build="find ./ -name 'build' -exec rm -rf {} +",
            egg_info="find . -name '*.egg-info' -not -path './venv/*' -exec rm -rf {} +",
            dist="find ./ -name 'dist' -exec rm -rf {} +"
        )
        if self.egg is not None:
            cmd['eggs'] = "find ./ -name '.eggs' -exec rm -rf {} +"

        for key in cmd:
            print('remove {} folder ...'.format(key))
            os.system(cmd[key])


python_2 = sys.version_info[0] == 2
app_home = os.path.dirname('__file__')


def read(fname):
    with open(fname, 'rU' if python_2 else 'r') as f:
        return f.read()


with open(os.path.join(app_home, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

install_req_path = os.path.join(app_home, 'docs/requirements.txt')
install_require = [req.strip() for req in read(install_req_path).splitlines() if req.strip()]

dev_req_path = os.path.join(app_home, 'docs/requirements-dev.txt')
dev_require = [req.strip() for req in read(dev_req_path).splitlines() if req.strip()]

extras_require = {"dev": dev_require}

setup(
    name="cathay",
    version="1.0",
    author="Cathay",
    description="python project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7"
    ],
    keywords=["pyspark", "template"],
    packages=find_packages(),
    python_requires=">=2.7",
    install_requires=install_require,
    tests_require=dev_require,
    extras_require=extras_require,
    zip_safe=False,
    cmdclass={'install': Install,
              'test': PyTest,
              'lib': InstallLibs,
              'extra': InstallExtra,
              'clean': Clean}
)
