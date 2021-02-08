from setuptools import setup


with open('README.md') as f:
    long_description = ''.join(f.readlines())


setup(
    name='swing',
    version='0.1',
    description='An open-source client for creating compounded Docker Swarm deployments',
    long_description=long_description,
    author='Jan Šafařík',
    author_email='cowjen01@gmail.com',
    keywords='docker,swarm,repository',
    license='Apache License 2.0',
    url='https://github.com/docker-swing/swing',
    packages=['swing'],
    install_requires=[
        'pyyaml~=5.4.1',
        'click~=7.1.2',
        'requests~=2.25.1',
        'tabulate~=0.8.7',
        'jinja2~=2.11.3'
    ],
    entry_points={
        'console_scripts': [
            'swing = swing.cli:main',
        ],
    },
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    zip_safe=False,
)
