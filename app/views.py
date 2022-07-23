from django.shortcuts import render
import shutil
# Create your views here.
from rest_framework.response import Response
from rest_framework.decorators import api_view
import zipfile
from .serializers import FileSerializer
from .models import Project
from django.conf import settings
import os

@api_view(['GET'])
def home(request):
    return Response({"Message": "Welcome Home"})


@api_view(['POST'])
def postFile(request):
    serializer = FileSerializer(data=request.data)

    if serializer.is_valid():
        savedFile = serializer.save()
        path = savedFile.file.path
        folder = f"{settings.MEDIA_ROOT}\\user_files\\{savedFile.slug}"

        with zipfile.ZipFile(path, "r") as zip_ref:
            zip_ref.extractall(folder)
        lines = []
        extLines = []
        summary = []
        newList = []
        EXT = savedFile.fileExt.split(",")
        EXT.pop()
        for ext in EXT:
            newDict = {"name": str(ext), "lines": 0, "files": 0}
            newList.append(newDict)
        for subdir, dirs, files in os.walk(folder):
            for file in files:
                # print os.path.join(subdir, file)

                filepath = subdir + os.sep + file

                for ext in EXT:
                    if filepath.endswith(ext):
                        for i in newList:
                            if i['name'] == str(ext):
                                i["files"] += 1
                        with open(filepath, "rb") as _file:
                            for line in _file:
                                line = line.strip()
                                if line:
                                    lines.append(line)
                                    extLines.append(line)

                    for i in newList:
                        if i['name'] == str(ext):
                            i["lines"] += len(extLines)
                            # i["files"] += 1
                    extLines = []
        # print(f"There is {len(lines)} lines of code in this project.")
        savedFile.delete()
        shutil.rmtree(folder)

        return Response({"codeLines": len(lines), "summary": newList})


@api_view(['GET'])
def testApi(request):
    project = Project.objects.get(slug="forth")

    path = project.file.path
    folder = f"{settings.MEDIA_ROOT}\\user_files\\{project.slug}"

    with zipfile.ZipFile(path, "r") as zip_ref:
        zip_ref.extractall(folder)
    lines = []
    EXT = project.fileExt.split(",")
    EXT.pop()
    for subdir, dirs, files in os.walk(folder):
        for file in files:
            # print os.path.join(subdir, file)
            filepath = subdir + os.sep + file
            for ext in EXT:
                if filepath.endswith(ext):
                    with open(filepath, "rb") as _file:
                        for line in _file:
                            line = line.strip()
                            if line:
                                lines.append(line)
    # print(f"There is {len(lines)} lines of code in this project.")

    return Response({"codeLines": len(lines)})


