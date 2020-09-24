from setuptools import setup, find_packages

setup(
    name='RlGlue',
    url='https://github.com/andnp/coursera-rl-glue.git',
    author='Andy Patterson',
    author_email='ap3@ualberta.com',
    packages=find_packages(exclude=['tests*']),
    install_requires=[],
    version=0.1,
    license='MIT',
    description='The rl-glue library used in the RL Specialization on Coursera',
    long_description='todo',
)
