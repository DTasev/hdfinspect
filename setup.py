from distutils.core import setup

from setuptools import find_packages

setup(
    name='hdfinspect',
    description="""GUI to inspect/view HDF files in Qt.""",
    version='0.1dev',
    packages=find_packages(),
    package_data={"hdfinspect.display": ["../ui/*.ui"]},
    license='MIT',
    long_description=open('LICENSE').read(),
    author="Dimitar Tasev",
    author_email="dimitar.tasev@stfc.ac.uk",
    url="https://github.com/dtasev/hdfinspect",
    requires=open('requirements.txt').readlines(),
    entry_points={
        "gui_scripts": ["hdfinspect = hdfinspect.__main__:main"],
    },
)
