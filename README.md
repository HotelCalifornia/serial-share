# serial-share

## Objective
Create a working proof of concept that facilitates bidirectional communication over a serial port by more than one client

## Motivation
When working with peripheral devices that communicate over serial ports, it can sometimes be useful to write to/read from a device from multiple processes on a client computer. However, ports (read: file descriptors) generally do not allow concurrent I/O, as this may give rise to race conditions or file corruption-- neither of which are optimal outcomes.

This project will be developed keeping in mind future interoperability with the [PROS CLI](https://github.com/purduesigbots/pros-cli). One use case of this project on the PROS platform involves simultaneously communicating with a microcontroller from the `pros terminal` command and debugging sensor values using [JINX](https://github.com/purduesigbots/JINX). This is currently impossible due to aforementioned limitations with serial ports.

## Method
The idea behind this project makes heavy use of the [ZeroMQ Project](http://www.zeromq.org/)'s libraries (specifically [pyzmq](https://github.com/zeromq/pyzmq)) that abstract sockets and provide a unified interface for interprocess communication (IPC) across many different languages.

Over two parallel, unidirectional pipelines (each following the publisher/subsriber pattern), a proxy attached to the serial port will broadcast data coming from the serial port through one pipeline, and receive data intended to be sent out over the serial port on the other.
![](https://puu.sh/vd5X8/e1b63f2113.png)
