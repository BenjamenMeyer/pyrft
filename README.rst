=====
PyRFT
=====

Python Reliable File Transfer (PyRFT) is an FTP replacement with the ability
to do fast, reliable file transfer operations. PyRTF provides several interfaces:

- pyrtf API - a Python-API package
- pyrtf - a python-based program that provides a client user interface implementatio
- pyrtfd - a python-based daemon that provides the server implementation

A GUI interface is not presently planned.

Design
------

The PyRTF reference applications provided (pyrtf, pyrtfd) utilize a TCP-based network
server design that consists of:

- an encrypted command channel that communicates using JSON formatted messages
- multiple encrypted binary data channels based on the negotiations of the client and server

PyRFT also includes a mechanism to negotiate a restart location should the connection
be lost. This mechanism guarantees that no data is lost during the transfer.

For each file transfer that is:
- 1 File reader
- 1 File writer
- N Data transfer connections

Options
-------

PyRFT has many options:
- Max Total Transfer Bandwidth Utilization (default: None)
- Max Per File Bandwidth Utilization (default: None)
- Max Per Connection Bandwidth Utilization (default: None)
- Max Number of Data Connections (default: 10)
- Number of connection retries (default: None)
- Data Block Size

The design of PyRFT is such that it will automatically consume any extra bandwidth
available, allowing it to easily overcome the standard AI/MD configuration of TCP
connections. Therefore transfer rates limitations are provided on both client and
servers so they can negotiate the actual usage, always going to the lower of the
two.

PyRFT dedicates itself to transferring one file at a time in order to transfer it
as quickly as possible. As a file transfer finishes, the data connection may be
transferred from one file transfer transaction to another file transfer  transaction.
