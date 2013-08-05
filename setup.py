from setuptools import setup, find_packages
setup(
    name = "manalang",
    version = "0.1",
    packages = find_packages(),

    # metadata for upload to PyPI
    author = "James Ravenscroft",
    author_email = "ravenscroftj@gmail.com",
    description = """Manalang is a simple metalanguage for parsing tabletop
    game dice roll expressions.""",
    license = "MIT",
)
