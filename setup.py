from distutils.core import setup

setup(
    name='RBU',
    version='0.1dev',
    packages=['rbu', ],
    license='MIT',
    scripts=['bin/rbu-benchmark-prs'],
    install_requires=[
        'gitpython',
        'requests',
        'py-cpuinfo',
        'click'
    ]
)
