try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name="thorpy",
      version="0.0.0",
      description="",
      packages = ['thorpy', 'thorpy.comm', 'thorpy.message', 'thorpy.stages'],
      package_data = {'thorpy.stages': ['*.ini']},
      include_package_data = True,
      zip_safe = True,
      author = 'Laurent Fasnacht',
      author_email = 'laurent.fasnacht@unine.ch', 
      install_requires=['pyserial>=2.7',
                        'pyusb>=1.0.0a'
                        ],
      )
