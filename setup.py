import ast
import os
import re
from setuptools import setup

current_dir = os.path.abspath(os.path.dirname(__file__))
_version_re = re.compile(r'__version__\s+=\s+(?P<version>.*)')

with open(os.path.join(current_dir, 'flake8_if_checker.py'), 'r') as f:
    version = _version_re.search(f.read()).group('version')
    version = str(ast.literal_eval(version))


setup(
    name='flake8_if_checker',
    license='GPL',
    version=version,
    description='flake8 if statement linter',
    long_description=open('README.rst').read(),
    author='Daniel Kuruc',
    author_email='dnk@dnk.net.pl',
    url='https://github.com/danie1k/flake8_if_checker',
    py_modules=[
        'flake8_if_checker',
    ],
    zip_safe=False,
    python_requires='>=3.5',
    tests_require=['pytest'],
    install_requires=[
        'flake8 > 3.0.0',
    ],
    entry_points={
        'flake8.extension': [
            'IF0 = flake8_if_checker:IfChecker',
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Framework :: Flake8",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
    ],
)
