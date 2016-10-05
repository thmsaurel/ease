# EASE Project

## Description

This project is a python exploit/vulnerability framework written in python.
Like metasploit, it provide many default exploits and vulnerabilities which
targeted OT or IT platforms.

### Protocol Target
#### IT Protocols

- TCP       (OSI Model: Transport)

#### OT Protocols

- Modbus    (OSI Model: Application)    (TCP port: 502)

## Usage

### Requirements
Before launch this tool, you have to be sure to have python2 installed.

#### Scapy
The only dependency for this project is the Python network library, **scapy**.
To be sure to have all functionalities available, we recommand you to use a
version with modbus (version 2.3.2-dev available on the [main scapy
repository](https://github.com/secdev/scapy)).

> ##### Note:
> For a more modbus functionalities, we recommand to use the version available
> on https://github.com/thmsaurel/scapy. We had some functionalities usefull
> for some Modbus exploit.

```bash
$ git clone https://github.com/secdev/scapy
# you can also cloned the other repository with the command:
# $ git clone https://github.com/thmsaurel/scapy
$ cd scapy
$ python setup.py install
```

#### ConfigParser
Config parser is used to parse configuration files of the application.

```bash
$ pip install configparser
```

#### Path.py
A library that improved the path management by creating Path object for a
easier manipulation of path.

```bash
$ pip install path.py
```

## Developers

You can add your own scripts inside the tool or into a dedicated personal
folder (work in progress)

### Requirements
We demand you to use this tools before to try to commit on our repository:
- ``pep8``: a python style convention
- ``isort``: a tool to sort import

We also recommand to use ``pyflakes`` to check your python code for error (if
you are using an IDE, this tool or an equivalent is already used).

### Advices/Tutorial
* https://www.concise-courses.com/hacking-tools/packet-crafting-tools/scapy/
* http://www.secdev.org/projects/scapy/
