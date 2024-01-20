from setuptools import setup

with open('README.md') as file:
    long_description = file.read()

setup(
    name='PyPitch',
    description='A Python Suite of Algorithms to Detect the Most Prominent Frequency In Audio Chunks',
    version='0.0.3',
    author='Joram Millenaar',
    author_email='joormillenaar@live.nl',
    url='https://github.com/jofoks/PyPitch',
    install_requires=['numpy'],
    packages=['pypitch'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['audio', 'pitch', 'music', 'fft', 'yin', 'pitch-detection'],
    license='MIT'
)
