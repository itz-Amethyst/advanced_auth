from rest_framework.generics import GenericAPIView
from .serializers import GoogleAuthSerializer
from rest_framework.response import Response
from rest_framework import status



class GoogleAuthView(GenericAPIView):
    serializer_class = GoogleAuthSerializer

    def post( self, request ):
        print(request.data)
        serializer = self.serializer_class(data = request.data, context = {"request": request})
        if serializer.is_valid(raise_exception = True):
            data = (serializer.validated_data['access_token'])
            return Response(data, status = status.HTTP_200_OK)

        return Response(serializer.errors, status = status.HTTP_406_NOT_ACCEPTABLE)

