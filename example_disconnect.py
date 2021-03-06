import asyncio
from xknx import XKNX
from xknx.io.async import ConnectionState, Disconnect
from xknx.io.async import UDPClient, GatewayScanner

xknx = XKNX(start=False)

gatewayscanner = GatewayScanner(xknx)
gatewayscanner.start()
gatewayscanner.stop()

if not gatewayscanner.found:
    raise Exception("No Gateways found")

print("Connecting to {}:{} from {}".format(
    gatewayscanner.found_ip_addr,
    gatewayscanner.found_port,
    gatewayscanner.found_local_ip))

own_ip="192.168.42.1"
gateway_ip="192.168.42.10"
gateway_port=3671

udp_client = UDPClient(
    xknx,
    (gatewayscanner.found_local_ip, 0),
    (gatewayscanner.found_ip_addr, gatewayscanner.found_port))

task = asyncio.Task(
    udp_client.connect())

xknx.loop.run_until_complete(task)

for i in range(0,255):

    conn_state = ConnectionState(
        xknx,
		udp_client,
        communication_channel_id=i)

    conn_state.start()

    if conn_state.success:
        print("Disconnecting ",i)
        disconnect = Disconnect(
            xknx,
            udp_client,
            communication_channel_id=i)

        disconnect.start()

        if disconnect.success:
            print("Disconnected ", i)
