from distutils.core import setup
setup(name='amqp', version='0.1', py_modules=['consumer', 'producer'],
      install_requires=['pika'])
