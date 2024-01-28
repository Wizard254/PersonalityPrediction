import argparse
import json
import pathlib
import socket
import socketserver
import threading
from dataclasses import dataclass

from loguru import logger

import constants
import heavyimport


@dataclass
class PredictorResponse:
    status: int
    mbti: str
    category: str

    def data(self) -> bytes:
        return json.dumps(self.__dict__).encode()
        pass

    def ok(self):
        return self.status == 200
        pass

    @staticmethod
    def from_data(data: bytes):
        return PredictorResponse(**json.loads(data))
        pass

    pass


@dataclass
class PredictorRequest:
    resume: str
    rtype: int = 0

    def data(self) -> bytes:
        return json.dumps(self.__dict__).encode()
        pass

    @staticmethod
    def from_data(data: bytes):
        return PredictorRequest(**json.loads(data))
        pass

    pass


HOST, PORT = "localhost", 10051

STATUS_DICT = {0: 'idle', 1000: 'loading model', 1001: 'waiting for model load', 400: 'bad request',
               500: 'error loading model', 501: 'error making prediction', 200: 'ok', -1: 'unprocessed', 1: '', }


@dataclass
class ConstRequestTypes:
    PING: int = 1
    WAIT_FOR_PREDICTION: int = 2
    REFRESH_PREDICTION: int = 3
    NORMAL: int = 0
    pass


def ping() -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(10)
        try:
            sock.connect((HOST, PORT))
            pass
        except ConnectionError:
            return False
            pass

        request = PredictorRequest(resume='', rtype=ConstRequestTypes.PING)
        print(f'Pinging: {request.__dict__}')

        try:
            sock.sendall(request.data())
            response_data = sock.recv(1024)
            pass
        except ConnectionError:
            return False
            pass

        response = PredictorResponse.from_data(response_data)
        print("Ping Received: {}".format(response.__dict__))
        return response.ok()
    pass


status: int = 0


def main():
    global status
    prediction_queue = []
    prediction_cache: dict[str, list] = {}

    lock = threading.Lock()
    queue_lock = threading.Lock()

    class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

        def handle(self):
            """
            :return: status 1000 if the model is still loading
            """
            global status
            data = self.request.recv(1024)
            request = PredictorRequest.from_data(data)
            response = PredictorResponse(status=-1, mbti='', category='')

            if request.rtype == ConstRequestTypes.PING:
                response.status = 200
                return self.request.sendall(response.data())
                pass
            elif request.rtype == ConstRequestTypes.WAIT_FOR_PREDICTION:
                @logger.catch
                def its_dangerous():
                    import time
                    # Load the model
                    start = time.time()
                    logger.info("[WAIT] Loading Model..")
                    # print(f'[WAIT] Loading model...')
                    heavyimport.load_model()
                    # print(f'[WAIT] Model Loaded ({time.time() - start} ms)')
                    logger.info(f'[WAIT] Model Loaded ({time.time() - start} seconds)')
                    # Wait for predictions
                    mbti, category = heavyimport.predict(request.resume)
                    # Return prediction
                    response.category = category
                    response.mbti = mbti
                    response.status = 200
                    return self.request.sendall(response.data())
                    pass

                its_dangerous()
                # try:
                # except Exception:
                # except ImportError:
                #     response.status = 500
                #     return self.request.sendall(response.data())
                #     pass
                pass

            lock.acquire()
            if status == 0:
                # Load the model
                status = 1
                lock.release()

                try:
                    response.status = 1000
                    self.request.sendall(response.data())
                    heavyimport.load_model()
                    lock.acquire()
                    status = 2
                    lock.release()
                    pass
                except ImportError:
                    # We failed to load the model, restore initial status
                    lock.acquire()
                    status = 1
                    lock.release()

                    response.status = 500
                    return self.request.sendall(response.data())
                    pass
                pass
            elif status == 1:
                lock.release()
                response.status = 1001
                return self.request.sendall(response.data())
                pass
            elif status == 2 and len(request.resume) > 0:
                # We have loaded the model, we can make predictions now
                lock.release()
                try:
                    queue_lock.acquire()
                    if request.resume in prediction_queue:
                        # TODO: Another thread is currently processing the prediction for this resume
                        logger.warning('Another thread is currently processing the prediction for this resume')
                        queue_lock.release()
                        pass
                    else:
                        queue_lock.release()
                        pass

                    if request.resume in prediction_cache.keys():
                        # We had predicted the prediction for this resume,
                        # respond from cache
                        mbti, category = prediction_cache[request.resume]
                        pass
                    else:
                        queue_lock.acquire()
                        prediction_queue.append(request.resume)
                        queue_lock.release()
                        mbti, category = heavyimport.predict(request.resume)
                        queue_lock.acquire()
                        prediction_cache[request.resume] = [mbti, category]
                        try:
                            prediction_queue.remove(request.resume)
                            pass
                        except ValueError:
                            pass
                        queue_lock.release()
                        pass

                    response.category = category
                    response.mbti = mbti
                    response.status = 200
                    self.request.sendall(response.data())
                    pass
                except ImportError:
                    try:
                        prediction_queue.remove(request.resume)
                        pass
                    except ValueError:
                        pass
                    response.status = 501
                    self.request.sendall(response.data())
                    return
                    pass
                pass
            else:
                lock.release()
                self.request.sendall(response.data())
                return
                pass
            pass

    class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
        pass

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)

    try:
        ip, port = server.server_address
        logger.info(f'Server running at https://{ip}:{port} (Press CTRL+C to quit)')
        server.serve_forever()
        pass
    except KeyboardInterrupt:
        logger.info(f'Shutting down')
        server.shutdown()
        pass

    pass


if __name__ == '__main__':
    # Create the argument parser
    parser = argparse.ArgumentParser()

    # Add the command-line switch
    parser.add_argument('--load_model',
                        action='store_true',
                        help='Run as a client to load the prediction model')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Check if the verbose switch was specified
    is_load_model = args.load_model

    # Print whether the verbose switch was specified
    if is_load_model:
        # Write logs in the mounted docker volume
        logger.add(pathlib.Path(constants.DOCKER_VOLUME) / "log.runpredictor.load_model.log",
                   rotation="500 MB")
        if ping():
            response: PredictorResponse
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((HOST, PORT))
                request = PredictorRequest(resume='')
                logger.info(f'Sending: {request.__dict__}')
                sock.sendall(request.data())
                response_data = sock.recv(1024)
                response = PredictorResponse.from_data(response_data)
                logger.info(f"Received: {response.__dict__}")
                pass
            pass
        else:
            logger.warning('Failed to connect to subprocess (Is it started?)')
            pass
        pass
    else:
        # Write logs in the mounted docker volume
        logger.add(pathlib.Path(constants.DOCKER_VOLUME) / "log.runpredictor.log",
                   rotation="500 MB")
        main()
        pass

    pass
