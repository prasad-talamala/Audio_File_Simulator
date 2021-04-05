import json

from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from audioapp.models import Song, Podcast, Audiobook


def format_object_to_json_data(object_data, audioFileType):
    json_data = {}
    print("object_data: {}".format(object_data))
    print("type of object_data: {}".format(type(object_data)))
    if isinstance(object_data, object):
        for each_obj in object_data:
            if audioFileType == "audiobook":
                dict_values = {"title": each_obj.title, "author": each_obj.author, "narrator": each_obj.narrator,
                               "duration": each_obj.duration, "uploaded_time": each_obj.uploaded_time}
            else:
                dict_values = {"name": each_obj.name, "duration": each_obj.duration,
                               "uploaded_time": each_obj.uploaded_time}
                if audioFileType == "podcast":
                    dict_values.update({"host": each_obj.host, "participants": each_obj.participants})
            json_data[each_obj.id] = dict_values
    return json_data


@csrf_exempt
def add_file(request, audioFileType):
    audioFileMetadata = json.loads(request.body)
    audioFileMetadata.update({"uploaded_time": timezone.localtime().now()})

    if request.method == 'POST':
        if audioFileType == "song":
            new_instance = Song.objects.create(name=audioFileMetadata["name"], duration=audioFileMetadata["duration"],
                                               uploaded_time=audioFileMetadata["uploaded_time"])

        elif audioFileType == "podcast":
            new_instance = Podcast.objects.create(name=audioFileMetadata["name"],
                                                  duration=audioFileMetadata["duration"],
                                                  uploaded_time=audioFileMetadata["uploaded_time"],
                                                  host=audioFileMetadata["host"],
                                                  participants=audioFileMetadata["participants"])

        elif audioFileType == "audiobook":
            new_instance = Audiobook.objects.create(title=audioFileMetadata["title"],
                                                    author=audioFileMetadata["author"],
                                                    narrator=audioFileMetadata["narrator"],
                                                    duration=audioFileMetadata["duration"],
                                                    uploaded_time=audioFileMetadata["uploaded_time"])
        else:
            return HttpResponse("The request is invalid.")

        return HttpResponse("{} added successfully with id: {}.".format(audioFileType, new_instance.id))

    else:
        return HttpResponse("Invalid Request.")


@csrf_exempt
def update_file(request, audioFileType, audioFileID):
    print("inside")
    audioFileMetadata = json.loads(request.body)
    audioFileMetadata.update({"uploaded_time": timezone.localtime().now()})

    if request.method == "POST":
        if audioFileType == "song":
            try:
                instance = Song.objects.get(id=audioFileID)
            except Exception as e:
                return HttpResponse(str(e))

            instance.name = audioFileMetadata["name"]
            instance.duration = audioFileMetadata["duration"]
            instance.uploaded_time = audioFileMetadata["uploaded_time"]

        elif audioFileType == "podcast":
            try:
                instance = Podcast.objects.get(id=audioFileID)
            except Exception as e:
                return HttpResponse(str(e))

            instance.name = audioFileMetadata["name"]
            instance.duration = audioFileMetadata["duration"],
            instance.uploaded_time = audioFileMetadata["uploaded_time"],
            instance.host = audioFileMetadata["host"],
            instance.participants = audioFileMetadata["participants"]

        elif audioFileType == "audiobook":
            try:
                instance = Audiobook.objects.get(id=audioFileID)
            except Exception as e:
                return HttpResponse(str(e))

            instance.title = audioFileMetadata["title"],
            instance.author = audioFileMetadata["author"],
            instance.narrator = audioFileMetadata["narrator"],
            instance.duration = audioFileMetadata["duration"],
            instance.uploaded_time = audioFileMetadata["uploaded_time"]

        else:
            return HttpResponse("The request is invalid.")

        instance.save()
        return HttpResponse("{} {} updated successfully.".format(audioFileType, instance.id))

    else:
        return HttpResponse("Invalid Request.")


def get_file(request, audioFileType, audioFileID):
    if request.method == "GET":
        try:
            if audioFileType == "song":
                if audioFileID:
                    request_data = Song.objects.get_queryset()
                    request_data = request_data.filter(id__exact=audioFileID)
                else:
                    request_data = Song.objects.get_queryset()

            elif audioFileType == "podcast":
                if audioFileID:
                    request_data = Podcast.objects.get_queryset()
                    request_data = request_data.filter(id__exact=audioFileID)
                else:
                    request_data = Podcast.objects.get_queryset()

            elif audioFileType == "audiobook":
                if audioFileID:
                    request_data = Audiobook.objects.get_queryset()
                    request_data = request_data.filter(id__exact=audioFileID)
                else:
                    request_data = Audiobook.objects.get_queryset()
            else:
                return HttpResponse("The request is invalid.")

        except Exception as e:
            return HttpResponse(str(e))

        return JsonResponse(format_object_to_json_data(request_data, audioFileType))


    else:
        return HttpResponse("Invalid Request.")


@csrf_exempt
def delete_file(request, audioFileType, audioFileID):
    if request.method == "DELETE":
        if audioFileType == "song":
            data = Song.objects.filter(id=audioFileID)
            if data:
                data.delete()
            else:
                return HttpResponse("{} {} not exists.".format(audioFileType, audioFileID))

        elif audioFileType == "podcast":
            data = Podcast.objects.filter(id=audioFileID)
            if data:
                data.delete()
            else:
                return HttpResponse("{} {} not exists.".format(audioFileType, audioFileID))

        elif audioFileType == "audiobook":
            data = Audiobook.objects.filter(id=audioFileID)
            if data:
                data.delete()
            else:
                return HttpResponse("{} {} not exists.".format(audioFileType, audioFileID))

        return HttpResponse("{} {} deleted successfully.".format(audioFileType, audioFileID))
    else:
        return HttpResponse("Invalid Request.")
