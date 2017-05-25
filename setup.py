from setuptools import setup

setup(
    name='certifi-proxy',
    description='A reverse proxy for certifi.io',
    author='Cory Benfield',
    author_email='cory@lukasa.co.uk',
    packages=['certifiproxy', 'twisted.plugins'],
    package_dir={"": "src"},
    install_requires=[
        'twisted[tls,http2]>=16.4.0',
        'txacme>=0.9.0',
        'rproxy>=16.9.0',
    ],
    zip_safe=False,
)
