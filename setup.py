import setuptools
from setuptools.command.test import test as TestCommand
import sys


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setuptools.setup(
    name="jenkins-github-webhook-plus",
    version="0.1.0",
    url="https://github.com/mverteuil/jenkins-github-webhook-plus",

    author="M. de Verteuil",
    author_email="mverteuil@github.com",

    description="Proxy Service for Sidelaunching Python Tasks on GitHub Events",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    install_requires=['Flask>=0.10.1', 'requests>=2.0.0'],
    tests_require=['pytest'],
    cmdclass={'test': PyTest},

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
)
