from rest_framework import generics, status
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import Project, Measurement
from .serializers import ProjectSerializer, MeasurementSerializers


class ProjectViewSet(ListAPIView):
    """ViewSet для проекта."""
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class MeasurementViewSet(ModelViewSet):
    """ViewSet для измерения."""
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializers


class Project_one(RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class MeasurementUpdate(generics.UpdateAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializers


class MeasurementPut(APIView):
    def put(self, request, pk):
        device = self.get_object(pk)
        serializer = MeasurementSerializers(device, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



