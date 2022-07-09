setuptools.setup(
    name='magnetizationfitting',
    version='0.1',
    author='Elliot Wadge',
    author_email='ewadge@sfu.ca',
    description='Package for quickly fitting normalized magnetic moment of coupled magnetic layers',
    url='https://github.com/Elliot-Wadge/Mink',
    license='MIT',
    packages=["magnetizationfitting"],
    install_requires=['numpy', 'scipy>=1.7.1'],
)
