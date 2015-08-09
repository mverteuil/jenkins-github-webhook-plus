import setuptools

setuptools.setup(
    name="jenkins-github-webhook-plus",
    version="0.1.0",
    url="https://github.com/mverteuil/jenkins-github-webhook-plus",

    author="M. de Verteuil",
    author_email="mverteuil@github.com",

    description="Proxy Service for Sidelaunching Python Tasks on GitHub Events",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    install_requires=['Flask>=0.10.1', 'requests>=2.0.0'],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
)
