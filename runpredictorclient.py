import random
import socket
from multiprocessing import Process

import runpredictor
from runpredictor import HOST, PORT, PredictorRequest, PredictorResponse, ConstRequestTypes


def predict_personality(resume_path: str):
    response: PredictorResponse
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        request = PredictorRequest(resume=resume_path,
                                   rtype=ConstRequestTypes.WAIT_FOR_PREDICTION)
        print(f'Sending: {request.__dict__}')
        sock.sendall(request.data())
        response_data = sock.recv(1024)
        response = PredictorResponse.from_data(response_data)
        print("Received: {}".format(response.__dict__))
        pass
    return response
    pass


def test():
    resumes = ["pdf1", "pdf2", "pdf3"]
    processes = [Process(target=predict_personality,
                         args=(random.choice(resumes),)) for _ in range(10)]
    for p in processes:
        p.start()
        pass
    for p in processes:
        p.join()
        pass
    pass


if __name__ == '__main__':
    if runpredictor.ping():
        # test()
        pred = predict_personality(r"C:\Users\Anyona\AWork\Mandela\Unit\Personality "
                                   r"ML\PersonalityPrediction\PersonalityPrediction\data\usecase1\resume.pdf")
        # predict_personality('')
        # predict_personality('pdf2')
        pass
    else:
        print(f'Failed to connect to subprocess (Is it started?)')
        pass

    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    #     sock.connect((HOST, PORT))
    #     request = PredictorRequest(resume='pdf2.pdf', rtype=1)
    #     print(f'Sending: {request.__dict__}')
    #     sock.sendall(request.data())
    #     response_data = sock.recv(1024)
    #     response = PredictorResponse.from_data(response_data)
    #     print("Received: {}".format(response.__dict__))
    #
    #     request = PredictorRequest(resume='pdf1.pdf', rtype=0)
    #     print(f'Sending: {request.__dict__}')
    #     sock.sendall(request.data())
    #     response_data = sock.recv(1024)
    #     response = PredictorResponse.from_data(response_data)
    #     print("Received: {}".format(response.__dict__))
    #     pass
    pass
