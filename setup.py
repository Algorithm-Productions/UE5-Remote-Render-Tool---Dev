from remote_render import __version__
from setuptools import setup

setup(name='UE Remote Render Tool',
      version=__version__,
      description='Unreal Engine Remote Rendering Tool',
      author='Vitor Vicente',
      author_email='vitor@bu.edu',
      url='http://path/to/repo.git',
      packages=['remote_render'],
      install_requires=['python-dotenv', 'flask', 'GPUtil', 'psutil', 'unreal']
      )
