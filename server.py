import socket
import errno
from machine import Pin

red = Pin(("gpio0", 10), Pin.OUT)

CONTENT = b"""\
HTTP/1.0 200 OK
Connection: close
Content-Type: text/html

<html>
<head>
    <title>FRDM-MCXN947</title>
    <script>
        function turnOnRed() {
            fetch("/red_on").then(response => console.log("Red LED ON"));
        }
    </script>
</head>
<body style="background-color: #333;color: #ffffff">
    <h1>FRDM-MCXN947</h1>
    <p>Current tempreture: %s</p>
    <button onclick="turnOnRed()">Turn Red LED %s</button>
</body>
</html>
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
    while True:
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

        request_line = req.decode().split()
        if len(request_line) > 1:
            path = request_line[1]
        else:
            path = "/"

        while True:
            h = client_stream.readline()
            if h == b"" or h == b"\r\n":
                break
            print(h)
        
        if path == "/red_on":
            red.value(red.value() ^ 1)

            new_value = "ON" if red.value() > 0 else "OFF"
            client_stream.write(CONTENT % new_value)
        else:
            value = "ON" if red.value() > 0 else "OFF"
            client_stream.write(CONTENT % value)

        client_stream.close()
        if not micropython_optimize:
            client_sock.close()
        counter += 1
        print()

main()
