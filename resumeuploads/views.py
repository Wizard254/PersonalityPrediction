import dataclasses
import json
import threading

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponseNotFound, StreamingHttpResponse
# Create your views here.
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
# from django.http import Http404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from resumeuploads.forms import DocumentForm
from resumeuploads.models import Document, JobDescription
from resumeuploads.serializers import JobDescriptionSerializer


@login_required
def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document: Document = form.save(commit=False)
            document.user = request.user
            document.save()
            return redirect('resume-home')
        pass
    else:
        form = DocumentForm()
        pass
    return render(request, 'resumeuploads/upload_document.html', {'form': form})


@login_required
def resume_home(request):
    user_documents = Document.objects.filter(user=request.user).order_by('-created_at')
    if user_documents.count() == 0:
        return redirect('upload')
        pass
    return render(request, 'resumeuploads/resume-home.html', {'user_documents': user_documents})


running_jobs = []


def perform_background_task(resume_id):
    # Define the task to be performed in the background
    def background_task():
        print("Background task started.")
        # time.sleep(20)  # Simulating a 20-second task
        rs = Document.objects.filter(pk=int(resume_id))
        doc: Document = rs.first()

        print("[TASK] Loading modules...")
        from old.personalityprediction import predict_mbti_category
        print("[TASK] Done.")

        print("[TASK] Getting Predictions...")
        doc.mbti, doc.category = predict_mbti_category(doc.file.name)
        print("[TASK] Done.")

        # doc.mbti = 'ENTP'
        doc.save()
        print("Background task completed.")
        pass

    # Create and start the background thread
    background_thread = threading.Thread(target=background_task)
    background_thread.start()
    pass


@csrf_exempt
@login_required
def resume_mbti(request):
    if request.method == 'POST':
        data = request.json()
        # key = data.get('key')
        # name = data.get('name')

        resume_id = data.get('resume_id')
        rs = Document.objects.filter(pk=int(resume_id))
        mbti = rs.first().mbti

        if resume_id not in running_jobs and mbti is None:
            perform_background_task(resume_id)
            pass

        return JsonResponse({'mbti': mbti})  # return JsonResponse({'message': f'Key: {key}, Name: {name}'})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    pass


@login_required
@ensure_csrf_cookie
def tmp_view(request):
    return render(request, 'resumeuploads/tmp.html')


@api_view(['POST'])
def resume_info(request, format=None):
    """
    Get the details of a given resume
    """
    # user = request.user
    #
    # # Access user properties
    # username = user.username
    # email = user.email
    #
    # print(f"Current User: {username}, Email: {email}")
    if request.method == 'POST':
        resume_id = request.data.get('resume_id')
        rs = Document.objects.filter(pk=int(resume_id))
        doc = rs.first()

        if resume_id not in running_jobs and doc.mbti is None:
            running_jobs.append(resume_id)
            perform_background_task(resume_id)
            pass
        return Response({'mbti': doc.mbti})
        pass


@api_view(['POST'])
def resume_jobs(request):
    """
    Get the details of a given resume
    """
    if request.method == 'POST':
        resume_id = request.data.get('resume_id')
        rs = Document.objects.filter(pk=int(resume_id))
        doc: Document = rs.first()

        if resume_id not in running_jobs and (doc.mbti is None or doc.category is None):
            running_jobs.append(resume_id)
            perform_background_task(resume_id)
            pass

        response = {'ok': False}
        jobs = []
        if doc.mbti is not None and doc.category is not None:
            for i, j in enumerate(JobDescription.objects.filter(category=doc.category)):
                jobs.append({'title': j.title, 'description': j.description})
                if i >= 100:
                    break
                pass
            response['ok'] = True
            pass
        response['jobs'] = jobs

        # serializer = DocumentSerializer(doc)
        # return Response(serializer.data)
        response['mbti'] = doc.mbti
        response['category'] = doc.category
        return Response(response)
        pass


def sse_view(request):
    resume_id = request.GET.get('id')
    rs = Document.objects.filter(pk=int(resume_id))
    doc: Document = rs.first()

    if doc is None:
        return HttpResponseNotFound()

    response = StreamingHttpResponse(streaming_content=sse_event_generator(resume_id), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    response['Connection'] = 'keep-alive'
    response['Access-Control-Allow-Origin'] = '*'
    return response


def sse_event_generator(resume_id):
    # SSE events format: "event: eventName\ndata: someData\n\n"
    import runpredictor
    import runpredictorclient

    rs = Document.objects.filter(pk=int(resume_id))
    doc: Document = rs.first()

    @dataclasses.dataclass
    class EventPrediction:
        mbti: str
        category: str
        pass

    def event(name: str, data) -> str:
        return f"event: {name}\ndata: {json.dumps(data)}\n\n"
        pass

    def check_doc() -> bool:
        return doc.mbti is not None and doc.category is not None
        pass

    def get_job_recommendations():
        jobs = []
        for jd in JobDescription.objects.filter(category=doc.category)[:100]:
            jobs.append({'title': jd.title, 'description': jd.description})
            pass
        return jobs
        pass

    def get_job_recommendations_json():
        rec_jobs = get_job_recommendations()
        return event('recommendations', rec_jobs)
        pass

    def get_personality_category() -> str:
        return event('prediction', EventPrediction(doc.mbti, doc.category).__dict__)
        pass

    # Do some work here
    if check_doc():
        yield get_personality_category()
        yield get_job_recommendations_json()
        return
        pass

    elif runpredictor.ping():
        # f = (r"C:\Users\Anyona\AWork\Mandela\Unit\Personality "
        #      r"ML\PersonalityPrediction\PersonalityPrediction\data\usecase1\resume.pdf")
        prediction = runpredictorclient.predict_personality(doc.file.path)
        if prediction is None:
            return
            pass

        # Save this prediction to database
        doc.mbti, doc.category = prediction.mbti, prediction.category
        doc.save()

        yield get_personality_category()
        if check_doc():
            yield get_job_recommendations_json()
            pass
        return
        pass
    else:
        yield event('error', {'detail': "Server prediction subprocess not running "
                                        "Was it started? Did it die?"})
        return
        pass


# Django Rest framework class-based views
def api_return400(message: str):
    return Response({'detail': message},
                    status=status.HTTP_400_BAD_REQUEST)
    pass


class JobDescriptionSearch(APIView):
    """
    Search for key instances of recorded Job Descriptions
    """

    @staticmethod
    def get(request, format=None):
        if request.GET.get('format') == 'api':
            return Response({
                "count": 102,
                "page": 1,
                "pages": 2,
                "results": []
            })
            pass
        return Response(status=405)
        pass

    @staticmethod
    def post(request, format=None):
        query_: str = request.data['query']
        limit_str: str = request.data['limit']
        page_str: str = request.data['page']

        page = 1
        if limit_str is not None:
            field = None
            try:
                field = 'limit'
                limit = int(limit_str)

                if page_str is not None:
                    field = 'page'
                    page = int(page_str)
                    pass
                pass
            except ValueError:
                return api_return400(f"The field, {field}, needs a valid integer")
                pass
            pass
        else:
            limit = 20
            pass

        if query_ is None or len(query_) == 0:
            return api_return400("The field, query, can't be null or empty")
            pass

        contact_list = JobDescription.objects.filter(title__icontains=query_).order_by('id')
        # Show `limit` job descriptions per page.
        paginator = Paginator(contact_list, limit)
        page_obj = paginator.get_page(page)
        jds: list[JobDescription] = page_obj.object_list

        serializer = JobDescriptionSerializer(jds, many=True)
        return Response({
            "count": paginator.count,
            "page": page,
            "pages": paginator.num_pages,
            "results": serializer.data
        })
