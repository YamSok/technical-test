from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import MountainPeak
from .serializer import MountainPeakSerializer
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


# Afficher une carte avec le polygone pour vérifier les zones géographiques
def map_view(request):

    # zone du mont blanc
    polygon_points = [[44.7598, 4.80821], [44.68192, 10.5945], [48.38324, 7.50742]]

    # Europe
    # polygon_points = [
    #     [71.0036, -10.0094],  # Northernmost point in Europe
    #     [36.5697, -5.1406],  # Southernmost point in Europe
    #     [45.4643, 11.1201],  # Easternmost point in Europe
    #     [62.0177, 24.1730],
    # ]

    # Afficher les pics de la base
    queryset = MountainPeak.objects.all().values()

    # Marqueurs pour la carte
    markers = [[q["lat"], q["lon"]] for q in queryset]
    markers_info = [f'{q["name"]} : {q["altitude"]}m' for q in queryset]

    return render(
        request,
        "api/map.html",
        {
            "polygon_points": polygon_points,
            "markers": markers,
            "markers_info": markers_info,
        },
    )


## Vues basiques pour réaliser des opérations CRUD sur le modèle MountainPeak


class MountainPeakList(generics.ListAPIView):
    # Liste de tous les pics
    # Opération : GET (liste)
    queryset = MountainPeak.objects.all()
    serializer_class = MountainPeakSerializer


class MountainPeakCreate(generics.CreateAPIView):
    # Création d'un pic
    # Opération : POST
    queryset = MountainPeak.objects.all()
    serializer_class = MountainPeakSerializer


class CreateMultiplePeaksView(generics.CreateAPIView):
    # Création de plusieurs pics
    # Opération : POST
    serializer_class = MountainPeakSerializer

    # Surcharge de la méthode créate pour ajouter plusieurs objets à la fois
    def create(self, request):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class MountainPeakDetail(generics.RetrieveUpdateDestroyAPIView):
    # Détail, modification et suppréssion d'un pic
    # Opérations : GET, DELETE, PUT
    queryset = MountainPeak.objects.all()
    serializer_class = MountainPeakSerializer


class MountainPeakSearchWithinZone(generics.ListAPIView):
    # Rechercher les pics contenus dans une zone géographique définie par un
    # ensemble de coordonnées GPS (lat, lon)

    def list(self, request):

        # Création d'un polygone à partir des points en entrée
        points = request.data.get("points")
        if len(points) < 3:
            return Response({"Erreur": "Un polygone doit avoir au moins 3 points"})

        polygon = Polygon([(p[0], p[1]) for p in points])

        # Vérification de l'appartenance des pics à la zone définie par le polygone
        queryset = MountainPeak.objects.all().values()
        peaks_in_zone = [
            peak for peak in queryset if Point(peak["lat"], peak["lon"]).within(polygon)
        ]

        # Construction de la réponse
        serializer = MountainPeakSerializer(data=peaks_in_zone, many=True)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data)
