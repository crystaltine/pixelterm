from setuptools import setup, find_packages

NAME = 'pixelterm' # 'charred' taken :(((
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
	install_requires=["numpy", "scikit-image", "pillow"],
	keywords=['ascii', 'rendering', 'terminal', 'graphics', 'ansi', 'cli'],
	classifiers=[
		"Development Status :: 4 - Beta",
		"Intended Audience :: Developers",
		"Programming Language :: Python :: 3",
		"Operating System :: MacOS :: MacOS X",
		"Operating System :: Microsoft :: Windows",
	]
)