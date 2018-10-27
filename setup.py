from setuptools import setup
setup(
   name='video_steganalysis',
   version='1.0',
   description='Video steganalysis',
   author='Tô Duy Nghĩa',
   author_email='toduynghia@gmail.com',
   packages=[],  #same as name
   install_requires=['pillow', 'opencv-python', 'scikit-image', 'scikit-learn', 'matplotlib', 'pandas', 'scipy', 'numpy'], #external packages as dependencies
)