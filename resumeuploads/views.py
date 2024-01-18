import threading
# import time

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
# Create your views here.
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from rest_framework.decorators import api_view
from rest_framework.response import Response

from resumeuploads.forms import DocumentForm
from resumeuploads.models import Document, JobDescription
# from .serializers import DocumentSerializer
# import json
# from snippets.models import Snippet
# from snippets.serializers import SnippetSerializer


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
    return render(request, 'resumeuploads/resume-home.html',
                  {'user_documents': user_documents})


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

        return JsonResponse({'mbti': mbti})
        # return JsonResponse({'message': f'Key: {key}, Name: {name}'})
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

        # serializer = DocumentSerializer(doc)
        # return Response(serializer.data)
        return Response({'mbti': doc.mbti})
        pass

    #
    # if request.method == 'GET':
    #     snippets = Snippet.objects.all()
    #     serializer = SnippetSerializer(snippets, many=True)
    #     return Response(serializer.data)
    #
    # elif request.method == 'POST':
    #     serializer = SnippetSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
