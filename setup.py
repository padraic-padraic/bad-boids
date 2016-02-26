from setuptools import setup, find_packages

setup(
    name = "Boids",
    version = "1.0.0",
    packages = find_packages(exclude=['*test']),
    author = "Padraic Calpin",
    author_email = "padraic.calpin93@gmail.com",
    license = "GPLv2",
    package_data={
        '': ['*.yml']
    },
    scripts = ['scripts/boids'],
    install_requires = ['PyYaml','numpy','matplotlib','six'],
    setup_requires = ['nose'],
    test_suite = 'nose.collector')
