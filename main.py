import serial.tools.list_ports
import multiprocessing
import time
import zmq
from sys import argv

port_pub = "6969"
port_sub = "6970"
if len(argv) > 1:
    port_pub = argv[1]
    int(port_pub)  # I think this fails when port is not an int
    if len(argv) > 2:
        port_sub = argv[2]
        int(port_sub)

ctx = zmq.Context()

uni_pub = ctx.socket(zmq.PUB)
uni_pub.bind('tcp://*:%s'.format(port_pub))

uni_sub = ctx.socket(zmq.SUB)
uni_sub.bind('tcp://*:%s'.format(port_sub))


def pub(p):
    while True:
        uni_pub.send(p.read_all())
        time.sleep(0.001)


def sub(p):
    while True:
        p.write(uni_sub.recv())
        time.sleep(0.001)

port = [x for x in serial.tools.list_ports.comports() if x.vid is not None and
        (x.vid in [0x4d8, 0x67b] or 'vex' in x.product.lower())][0]
processes = [multiprocessing.Process(target=pub, args=(port,))] + [multiprocessing.Process(target=sub, args=(port,))]
for process in processes:
    process.start()

for process in processes:
    process.join()
