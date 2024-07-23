from setuptools import setup, find_packages

NAME = 'Charred'
VERSION = '0.1.0'
DESCRIPTION = 'Terminal Graphics Rendering Library'
LONG_DESCRIPTION = 'A library for rendering graphics using "pixels" (Unicode half-block characters) in modern terminals'

setup(
	name=NAME, 
	version=VERSION,
	author="crystaltine",
	author_email="<msh379c@outlook.com>",
	description=DESCRIPTION,
	long_description=LONG_DESCRIPTION,
	packages=find_packages(),
	install_requires=["numpy", "scikit-image", "blessed"],
	keywords=['ascii', 'rendering', 'terminal', 'graphics', 'ansi'],
	classifiers= [
		"Development Status :: 3 - Alpha",
		"Intended Audience :: idk",
		"Programming Language :: Python :: 3",
		"Operating System :: MacOS :: MacOS X",
		"Operating System :: Microsoft :: Windows",
	]
)