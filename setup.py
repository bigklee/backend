import pathlib
from setuptools import find_packages, setup


here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')


setup(
    name='kleenet',
    version='0.1.0',
    description='Backend for Klee visualization',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="GPLv3",
    author='Martin Obrist, Laurens Inauen',
    packages=find_packages(where='.', exclude=['tests', 'tasks']),
    python_requires='>=3.10, <4',
    include_package_data=True,
    setup_requires=['wheel'],
    install_requires=[
        "pydantic",
        "fastapi",
        "uvicorn",
        "python-multipart",
        "sqlalchemy",
        "jinja2"
    ]
)
