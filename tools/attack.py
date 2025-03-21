import asyncio
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from common.protocol.tcp import TCPClient
from common.protocol.protocol import Package, ByteBuffter
from common.ModelAPI import ModelInfo, Error as ModelError

async def main(host: str, port: int):
    client = TCPClient(host, port)

    await client.connection()

    while True:
        fn = input("Function: ")

        if fn == "info":
            await info(client)

async def info(client: TCPClient):
    buf = ByteBuffter()
    Package.encode(buf, ModelInfo.Request())
    data = await client.send(buf.to_bytes()) or bytearray()
    response_buf = ByteBuffter(bytes(data))
    Package.decode(response_buf)
    model_info = ModelInfo.Response.decode(response_buf)

    print(model_info)

async def check_error(package: type[Package], buf: ByteBuffter):
    if package == ModelError:
        model_error = ModelError.Response.decode(buf)
        print(model_error.message)

        raise Error(model_error.message)
    else:
        return package

if __name__ == "__main__":
    host = sys.argv[1]
    port = int(sys.argv[2])

    asyncio.run(main(host, port))
