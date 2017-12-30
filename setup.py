from setuptools import setup

setup(name='toripy',
      version='0.1',
      description='Lightweight python interface to easily make HTTP(s) requests over the Tor network.',
      url='http://github.com/nikoferro/toripy',
      author='Nicolas Ferro',
      author_email='nicolaspatricioferro@gmail.com',
      license='MIT',
      packages=['toripy'],
      install_requires=[
          'PySocks>=1.6.7',
          'requests>=2.13.0',
          'stem>=1.5.4',
      ],
      zip_safe=False)
