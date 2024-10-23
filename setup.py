# Python package setup for dynft
# 
# Copyright (C) 2024  Dameon Wagner
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup, find_packages

setup(
    name="dynft",
    description="Dynamic ruleset object management for nftables",
    author="Dameon Wagner",
    author_email="dameon.wagner@it.ox.ac.uk",
    package_dir={'':'lib',},
    packages=find_packages('lib'),
    scripts=['bin/dynft',],
    install_requires=[
        'click', 'dnspython', 'netaddr', 'nftables', 'pyyaml',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Intended Audience :: System Administrators',
    ],
    license='GNU GPL',
)
