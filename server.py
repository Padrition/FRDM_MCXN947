import socket
import errno
import time

CONTENT = b"""\
HTTP/1.0 200 OK

Hello #%d from MicroPython!
"""


def main(micropython_optimize=False):
    print("starting")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    addr = ("0.0.0.0", 8080)

    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        s.bind(addr)
    except OSError as e:
        print("Error:", e.errno, errno.errorcode.get(e.errno, "Unknown Error"))
        return
    s.listen(5)
    print("Listening, connect your browser to http://<this_host>:8080/")

    counter = 0
    time.sleep(5)
    while True:
        print("accepting")
        res = s.accept()
        client_sock = res[0]
        client_addr = res[1]
        print("Client address:", client_addr)
        print("Client socket:", client_sock)

        if not micropython_optimize:
            client_stream = client_sock.makefile("rwb")
        else:
            client_stream = client_sock

        print("Request:")
        req = client_stream.readline()
        print(req)
        while True:
            h = client_stream.readline()
            if h == b"" or h == b"\r\n":
                break
            print(h)
        client_stream.write(CONTENT % counter)

        client_stream.close()
        if not micropython_optimize:
            client_sock.close()
        counter += 1
        print()

main()
