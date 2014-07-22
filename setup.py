from setuptools import setup, find_packages

setup(
    name='pyshould',
    description='Should style asserts based on pyhamcrest',
    version='0.6.1',
    url='https://github.com/drslump/pyshould',
    author='Ivan -DrSlump- Montes',
    author_email='drslump@pollinimini.net',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['pyhamcrest'],
    tests_require=['nose','pyhamcrest'],
    test_suite="nose.collector",
    zip_safe=False,
    )
