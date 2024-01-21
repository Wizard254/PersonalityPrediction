predict = None


def load_model():
    global predict
    from old.personalityprediction import predict_mbti_category
    predict = predict_mbti_category
    pass


#
# def load_model():
#     if predict is None:
#         pass
#     else:
#         pass
#     sleep(10)
#     pass
#
#
# def predict(file: str):
#     # import ghostpackage
#     sleep(10)
#     return 'ENTP', 'Technical Jobs'
#     pass
