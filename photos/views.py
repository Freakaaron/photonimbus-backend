from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ImageSerializer
from google.cloud import pubsub_v1
from account.models import Account
import base64
import sys

from .models import Image, SharedImage, Annotation

@api_view(["POST"])
def upload(request):
    try:
        image = request.FILES["image"].file.read()
        username = request.POST.get("username")
        p = Image(image=image, username=username)
        p.save()
        project_id = "photonimbus-app"
        topic_id = "image-queue"
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(project_id, topic_id)
        data = str(p.id).encode("utf-8")
        future = publisher.publish(topic_path, data)
        return Response({
            "message": "Saved image successfully."
        })
    except:
        return Response({
            "message": "Image could not be saved."
        })

@api_view(["GET"])
def get(request):
    username = request.GET.get("username")
    if username == None:
        return Response({
            "message": "Images could not be fetched."
        })
    images = Image.objects.filter(username=username)
    result = []
    for index in range(len(images)):
        if len(images[index].thumbnail) == 0:
            continue
        ref = []
        ref.append(images[index].id)
        ref.append(base64.b64encode(images[index].thumbnail))
        result.append(ref)
    return Response(result)

@api_view(["GET"])
def getImage(request):
    try:
        id = int(request.GET.get("id"))
        image = Image.objects.filter(id=id)[0]
        res = {}
        res["id"] = image.id
        res["image"] = base64.b64encode(image.image)
        return Response(res)
    except:
        return Response({
            "message": "Full screen image could not be fetched"
        })

@api_view(["POST"])
def share(request):
    if request.method == "POST":
        try:
            ref = request.data
            username = ref.get("username")
            friend = ref.get("user")
            if len(Account.objects.filter(username=friend)) == 0:
                return Response({
                    "message": "Entered username does not exist"
                })
            image_id = ref.get("image_id")
            s = SharedImage(username=username, friend=friend, image_id=image_id);
            s.save()
            return Response({
                "message":"Shared image successfully"
            })
        except :
            return Response({
                "message":"Image could not be shared"
            })
    else:
        return Response({
            "message": "The API only supports POST requests"
        })

@api_view(["GET"])
def getSharedImages(request):
    try:
        username = request.GET.get("username")
        ref = SharedImage.objects.filter(friend=username).order_by('-id')
        res = []
        for r in ref:
            ref1 = []
            id = r.image_id
            image = Image.objects.filter(id=id)[0]
            ref1.append(id)
            ref1.append(base64.b64encode(image.thumbnail))
            res.append(ref1);
        return Response(res)
    except:
        return Response({
            "message": "Shared images could not be fetched."
        })

@api_view(["POST"])
def annotate(request):
    try:
        annotation = request.data.get("annotation")
        username = request.data.get("username")
        image_id = request.data.get("image_id")
        if len(Annotation.objects.filter(username=username, image_id=image_id, annotation=annotation)) != 0:
            return Response({
                "message" : "Image annotation already exists"
            })
        a = Annotation(username=username, image_id=image_id, annotation=annotation)
        a.save()
        return Response({
            "message" : "Image annotated"
        })
    except :
        return Response({
            "message": "Image could not be annotated."
        })
    

@api_view(["GET"])
def getAnnotations(request):
    try:
        image_id = request.GET.get("image_id")
        ref = Annotation.objects.filter(image_id=image_id)
        res = []
        for r in ref:
            res.append(r.annotation)
        return Response(res)
    except:
        return Response({
            "message": "Annotations could not be fetched."
        })


@api_view(["GET"])
def getAnnotatedThumbnails(request):
    try:
        annotation = request.GET.get("annotation")
        username = request.GET.get("username")
        ref = Annotation.objects.filter(username=username,annotation=annotation)
        res = []
        for r in ref:
            ref1 = []
            id = r.image_id
            ref1.append(id)
            ref1.append(base64.b64encode(Image.objects.filter(id=id)[0].thumbnail))
            res.append(ref1)
        return Response(res)
    except:
        return Response({
            "message": "Annotated thumbnails could not be fetched."
        })

