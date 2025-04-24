import socket
import errno
from machine import PWM

red_pwm = PWM(("ctimer0", 0), freq=1000, duty_ns=0)
green_pwm = PWM(("ctimer0", 3), freq=1000, duty_ns=0)
blue_pwm = PWM(("ctimer1", 0), freq=1000, duty_ns=0)

CONTENT = b"""\
HTTP/1.0 200 OK
Connection: close
Content-Type: text/html

<html>
<head>
    <title>FRDM-MCXN947</title>
    <script>
        function setColor(event) {
            let color = event.target.value;
            fetch(`/set_color?hex=${encodeURIComponent(color)}`)
                .then(response => console.log(`Color set to ${color}`))
                .catch(error => console.error("Error setting color:", error));
        }

        document.addEventListener("DOMContentLoaded", function() {
            document.getElementById("colorPicker").addEventListener("input", setColor);
        });
    </script>
</head>
<body style="background-color: #333; color: #ffffff;">
    <h1>FRDM-MCXN947</h1>
    
    <input type="color" id="colorPicker">
</body>
</html>

"""
def set_color(hex_color):
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    max_duty_cycle = 500_000
    r = int((r / 255) * max_duty_cycle)
    g = int((g / 255) * max_duty_cycle)
    b = int((b / 255) * max_duty_cycle)
    red_pwm.duty_ns(r)
    green_pwm.duty_ns(g)
    blue_pwm.duty_ns(b)

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
            print("request line:", request_line)
        else:
            path = "/"

        while True:
            h = client_stream.readline()
            if h == b"" or h == b"\r\n":
                break
        
        if path.startswith("/set_color"):
            hex_value = path.split("?hex=%23")[1]
            set_color(hex_value)

            client_stream.write(CONTENT)
        else:
            client_stream.write(CONTENT)

        client_stream.close()
        if not micropython_optimize:
            client_sock.close()
        print()

main()