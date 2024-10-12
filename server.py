from importlib.util import spec_from_file_location, module_from_spec
import sys
from common.ModelAPI import ModelHandler, Request
from common.protocol.tcp import TCPServer
from common.protocol.protocol import BRequest, BResponse
from common.protocol.byte_buffter import ByteBuffter
from common.logger_config import setup_logger
from logging import getLogger

class ModelServer(TCPServer):
    def __init__(self, host: str, port: int, model_name: str):
        spec = spec_from_file_location(f"models.{model_name}_model", f"models/{model_name}_model/{model_name}_model.py")
        if spec is None or spec.loader is None:
            raise FileNotFoundError(f"models/{model_name}_model/{model_name}_model.py not found")
        module = module_from_spec(spec)
        sys.path.append(f"models/{model_name}_model")
        spec.loader.exec_module(module)

        self.model: ModelHandler = getattr(module, "setup")()
        self.logger = getLogger()

        setup_logger()

        self.logger.info(f"Model Server {model_name} is running on {host}:{port}")

        super().__init__(self.logger, host, port, self.callback)

    def callback(self, data: bytes) -> bytes:
        request_buf = ByteBuffter(data)
        try:
            request: Request = BRequest.decode(request_buf).get_data()
        except:
            self.logger.error(f"Failed to decode request: {data}")
            raise ValueError("Failed to decode request")

        try:
            response = self.model.invoke(request)
        except:
            self.logger.error(f"Failed to invoke model: {request}")
            raise ValueError("Failed to invoke model")
        response_buf = ByteBuffter()

        BResponse.encode(response_buf, response)

        return response_buf.to_bytes()

if __name__ == "__main__":
    model_name = sys.argv[1]
    host = sys.argv[2]
    port = int(sys.argv[3])
    server = ModelServer(host, port, model_name)
    server.listen_thread.start()
    server.listen_thread.join()
