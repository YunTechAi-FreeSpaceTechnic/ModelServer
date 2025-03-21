import sys
import glob
import os
import asyncio

from importlib.util import spec_from_file_location, module_from_spec

from common.ModelAPI import Error, ModelHandler, ModelInfo, Package, Predict
from common.protocol.tcp import TCPServer
from common.protocol.byte_buffter import ByteBuffter
from common.logger_config import setup_logger

from logging import getLogger


class ModelServer(TCPServer):
    def __init__(self, host: str, port: int, model_name: str):
        spec = spec_from_file_location(f"model", f"model/{model_name}_model.py")
        if spec is None or spec.loader is None:
            raise FileNotFoundError(
                f"model/{model_name}_model.py not found")
        module = module_from_spec(spec)
        sys.path.append(f"model")
        spec.loader.exec_module(module)

        self.model: ModelHandler = getattr(module, "setup")()
        self.logger = getLogger()

        setup_logger()

        self.logger.info(
            f"Model Server {model_name} is running on {host}:{port}")

        super().__init__(self.logger, host, port, self.callback)

    def callback(self, data: bytearray) -> bytearray:
        request_buf = ByteBuffter(bytes(data))
        try:
            request = Package.decode(request_buf)
            request_data = request.Request.decode(request_buf)
        except:
            self.logger.error(f"Failed to decode request: {data}")
            raise ValueError("Failed to decode request")

        self.logger.info(f"Request: {request_data}")

        try:
            if request == Predict:
                response = self.model.invoke(request_data)
            elif request == ModelInfo:
                response = self.model.model_info()
        except Exception as e:
            response = Error.Response(f"Failed to invoke model: {e}")
            self.logger.error(f"Failed to invoke model: {e}")
        self.logger.info(f"Response: {response}")
        response_buf = ByteBuffter()
        Package.encode(response_buf, response)

        return bytearray(response_buf.to_bytes())


if __name__ == "__main__":
    first_file = glob.glob(os.path.join("model", "*_model.py"))[0]
    model_name = os.path.basename(first_file).replace("_model.py", "")

    host = sys.argv[1]
    port = int(sys.argv[2])

    asyncio.run(ModelServer(host, port, model_name).listen())
