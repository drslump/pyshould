from setuptools import setup, find_packages

setup(
    name='pyshould',
    description='Should style asserts based on pyhamcrest',
    version='{VERSION}',
    url='https://github.com/drslump/pyshould',
    author='Ivan -DrSlump- Montes',
    author_email='drslump@pollinimini.net',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['pyhamcrest'],
    tests_requires=['pyhamcrest'],
    test_suite="tests",
    zip_safe=False,
    )
