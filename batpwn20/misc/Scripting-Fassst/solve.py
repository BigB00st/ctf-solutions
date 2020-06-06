from websocket import create_connection
from datetime import datetime, timezone
ws = create_connection("ws://challenges.ctfd.io:30065/")
print(ws.recv())
ws.send("y")
while True:
    a = ws.recv()
    print(a)
    dt = datetime.strptime(a, "%Y-%m-%d %H:%M:%S")
    ws.send(str(int(dt.replace(tzinfo=timezone.utc).timestamp())))
ws.close()
