import setuptools
import os

setuptools.setup(
    name="synkka",
    version="2021.06.07",
    url="https://github.com/Pilperi/Synkka",
    author="Pilperi",
    description="Työkalut datan synkkaamiseen pettanille",
    packages=setuptools.find_packages(),
    install_requires = [
        'tiedostohallinta @ git+https://github.com/Pilperi/Tiedostohallinta'
    ],
	python_requires=">=3.8, <4",
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
)
