from distutils.core import setup

setup(
    name='Scg Ink lib',
    version='0.1.0',
    author='Michael Yin',
    author_email='gt8442b@yahoo.com',
    packages=['net', 'net.wyun','net.wyun.mer', 'net.wyun.mer.ink'],
    #scripts=['bin/stowe-towels.py','bin/wash-towels.py'],
    url='http://pypi.python.org/pypi/im2markup/',
    license='LICENSE.txt',
    description='scg ink file reading processing.',
    long_description=open('README.md').read(),
    install_requires=[
        "numpy >= 1.13.3",
        "scipy == 1.0.0",
    ],
)