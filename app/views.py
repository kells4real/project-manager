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
        # Saved file path
        path = savedFile.file.path
        # Exact folder of the saved file
        folder = f"{settings.MEDIA_ROOT}\\user_files\\{savedFile.slug}"

        # Unzip into the file (zipped)
        with zipfile.ZipFile(path, "r") as zip_ref:
            zip_ref.extractall(folder)  # Extracts the zip file
        lines = []
        extLines = []
        newList = []
        # Gets the file extensions from the frontend as just a text, splits them and them into a list
        EXT = savedFile.fileExt.split(",")
        EXT.pop()  # Removes the last comma

        # Creates a list of dictionaries to be updated on the fly depending on the extension
        for ext in EXT:
            newDict = {"name": str(ext), "lines": 0, "files": 0}
            newList.append(newDict)

        # Walk through the dirs and sub dirs
        for subdir, dirs, files in os.walk(folder):
            # For every file,
            for file in files:
                # store file in filepath variable
                filepath = subdir + os.sep + file

                # Loops through the extensions saved in EXT
                for ext in EXT:
                    # Self explanatory
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
                    extLines = []
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
