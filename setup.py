from glob import glob
import os
import sys
from setuptools import setup

if sys.version_info[:2] < (3, 8):
    error = (
        "NetworkG, the NetworkX Graphery Wrapper, 2.7+ "
        "requires Python 3.10 or later (%d.%d detected). \n"
    )
    sys.stderr.write(error + "\n")
    sys.exit(1)


name = "networkg"
description = "A customized version of networkx"
authors = {
    "Hagberg": ("Aric Hagberg", "hagberg@lanl.gov"),
    "Schult": ("Dan Schult", "dschult@colgate.edu"),
    "Swart": ("Pieter Swart", "swart@lanl.gov"),
    "Zeng": ("Larry Zeng", "zengl@reed.edu"),
}
maintainer = "Graphery Developers"
maintainer_email = "graphery@reed.edu"
url = "https://graphery.reedcompbio.org/"
project_urls = {
    "Bug Tracker": "https://github.com/Reed-CompBio/networkx/issues",
    "Documentation": "https://networkx.org/documentation/stable/",
    "Source Code": "https://github.com/Reed-CompBio/networkx",
}
platforms = ["Linux", "Mac OSX", "Windows", "Unix"]
keywords = [
    "Graphery",
    "Networks",
    "Graph Theory",
    "Mathematics",
    "network",
    "graph",
    "discrete mathematics",
    "math",
]
classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: BSD License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3 :: Only",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Scientific/Engineering :: Bio-Informatics",
    "Topic :: Scientific/Engineering :: Information Analysis",
    "Topic :: Scientific/Engineering :: Mathematics",
    "Topic :: Scientific/Engineering :: Physics",
]

with open("networkx/__init__.py") as fid:
    for line in fid:
        if line.startswith("__version__"):
            version = line.strip().split()[-1][1:-1]
            break

packages = [
    "networkx",
    "networkx.algorithms",
    "networkx.algorithms.assortativity",
    "networkx.algorithms.bipartite",
    "networkx.algorithms.node_classification",
    "networkx.algorithms.centrality",
    "networkx.algorithms.community",
    "networkx.algorithms.components",
    "networkx.algorithms.connectivity",
    "networkx.algorithms.coloring",
    "networkx.algorithms.flow",
    "networkx.algorithms.minors",
    "networkx.algorithms.traversal",
    "networkx.algorithms.isomorphism",
    "networkx.algorithms.shortest_paths",
    "networkx.algorithms.link_analysis",
    "networkx.algorithms.operators",
    "networkx.algorithms.approximation",
    "networkx.algorithms.tree",
    "networkx.classes",
    "networkx.classes.components",
    "networkx.generators",
    "networkx.drawing",
    "networkx.linalg",
    "networkx.readwrite",
    "networkx.readwrite.json_graph",
    "networkx.tests",
    "networkx.testing",
    "networkx.utils",
]

docdirbase = "share/doc/networkx-%s" % version
# add basic documentation
data = [(docdirbase, glob("*.txt"))]
# add examples
for d in [
    ".",
    "advanced",
    "algorithms",
    "basic",
    "3d_drawing",
    "drawing",
    "graph",
    "javascript",
    "jit",
    "pygraphviz",
    "subclass",
]:
    dd = os.path.join(docdirbase, "examples", d)
    pp = os.path.join("examples", d)
    data.append((dd, glob(os.path.join(pp, "*.txt"))))
    data.append((dd, glob(os.path.join(pp, "*.py"))))
    data.append((dd, glob(os.path.join(pp, "*.bz2"))))
    data.append((dd, glob(os.path.join(pp, "*.gz"))))
    data.append((dd, glob(os.path.join(pp, "*.mbox"))))
    data.append((dd, glob(os.path.join(pp, "*.edgelist"))))
# add js force examples
dd = os.path.join(docdirbase, "examples", "javascript/force")
pp = os.path.join("examples", "javascript/force")
data.append((dd, glob(os.path.join(pp, "*"))))

# add the tests
package_data = {
    "networkx": ["tests/*.py"],
    "networkx.algorithms": ["tests/*.py"],
    "networkx.algorithms.assortativity": ["tests/*.py"],
    "networkx.algorithms.bipartite": ["tests/*.py"],
    "networkx.algorithms.node_classification": ["tests/*.py"],
    "networkx.algorithms.centrality": ["tests/*.py"],
    "networkx.algorithms.community": ["tests/*.py"],
    "networkx.algorithms.components": ["tests/*.py"],
    "networkx.algorithms.connectivity": ["tests/*.py"],
    "networkx.algorithms.coloring": ["tests/*.py"],
    "networkx.algorithms.minors": ["tests/*.py"],
    "networkx.algorithms.flow": ["tests/*.py", "tests/*.bz2"],
    "networkx.algorithms.isomorphism": ["tests/*.py", "tests/*.*99"],
    "networkx.algorithms.link_analysis": ["tests/*.py"],
    "networkx.algorithms.approximation": ["tests/*.py"],
    "networkx.algorithms.operators": ["tests/*.py"],
    "networkx.algorithms.shortest_paths": ["tests/*.py"],
    "networkx.algorithms.traversal": ["tests/*.py"],
    "networkx.algorithms.tree": ["tests/*.py"],
    "networkx.classes": ["tests/*.py"],
    "networkx.classes.components": ["tests/*.py"],
    "networkx.generators": ["tests/*.py", "atlas.dat.gz"],
    "networkx.drawing": ["tests/*.py", "tests/baseline/*png"],
    "networkx.linalg": ["tests/*.py"],
    "networkx.readwrite": ["tests/*.py"],
    "networkx.readwrite.json_graph": ["tests/*.py"],
    "networkx.testing": ["tests/*.py"],
    "networkx.utils": ["tests/*.py"],
}


def parse_requirements_file(filename):
    with open(filename) as f:
        requires = [li.strip() for li in f.readlines() if not li.startswith("#")]

    return requires


install_requires = []
extras_require = {
    dep: parse_requirements_file("requirements/" + dep + ".txt")
    for dep in ["default", "developer", "doc", "extra", "test"]
}.copy()

with open("README.rst") as fh:
    long_description = fh.read()

if __name__ == "__main__":

    setup(
        name=name,
        version=version,
        maintainer=maintainer,
        maintainer_email=maintainer_email,
        author=authors["Zeng"][0],
        author_email=authors["Zeng"][1],
        description=description,
        keywords=keywords,
        long_description=long_description,
        platforms=platforms,
        url=url,
        project_urls=project_urls,
        classifiers=classifiers,
        packages=packages,
        data_files=data,
        package_data=package_data,
        install_requires=install_requires,
        extras_require=extras_require,
        python_requires=">=3.10",
        zip_safe=False,
    )
