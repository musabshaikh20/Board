from typing import OrderedDict
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
# Python Libraries
from collections import defaultdict
import logging
import os
#models
from .models import Board,List,Card
from jwtauth.models import UserProfile
#serializers
from .serializers import BoardSerializer,ListSerializer,CardSerializer
# other imports
from .utilities import swap_objects
from .config import LOG_FILE,MAX_BOARD_COUNT,PREMIUM





logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(name)-12s %(levelname)-8s %(message)s'
        },
        'file': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': f'{LOG_FILE}'
        }
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        }
    }
})

# This retrieves a Python logging instance (or creates it)
logger = logging.getLogger(__name__)


class RevokeView(APIView):
    """
    Revoke Token
    """
  
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message":"Logout Succesfully"},status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            logger.debug(e)
            
            return Response({"error":"server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)






class BoardView(APIView):


    """
    Crud For Board
    """
    
  
	
    serializer_class =  BoardSerializer
    permission_classes = ( IsAuthenticated,)
    
    
	
    def get(self, request, format=None):
        try:
            user = self.request.user
            board_instance = Board.objects.filter(user=user)
            serializer = BoardSerializer(board_instance, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.debug(e)

            return Response({"error":f"server error {e}"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def post(self, request, format=None):

        try:
        
            user = self.request.user
            user_type = UserProfile.objects.get(id=user.id).user_type 
            count_of_boards = Board.objects.filter(user=user).count()
            
            if user_type != PREMIUM and count_of_boards > MAX_BOARD_COUNT:
                return Response({"error":"free plan consists of 10 boards switch to Premium for more boards"}, status=status.HTTP_402_PAYMENT_REQUIRED)
            if Board.objects.filter(user=user,title=request.data['title']).exists():
                return Response({"error":"Board with Title Already Exists"}, status=status.HTTP_403_FORBIDDEN)
            
            request.data['user'] = user.id
            try:
                serializer = BoardSerializer(data=request.data)
            except Exception as e:
                logger.debug(e)
                return Response({"error":f"server error {e} pls check id's or data input"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if serializer.is_valid():
            
                serializer.save()
                return Response({"message":"succesfully created"},
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.debug(e)
            
            return Response({"error":f"server error {e}"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def patch(self, request, pk, format=None):
        try:
            try:
                board_instance = get_object_or_404(Board,id=pk)
                serializer = BoardSerializer(board_instance,
                                                data=request.data,
                                                partial=True)
            except Exception as e:
                logger.debug(e)
                return Response({"error":f"server error {e} pls check id's or data input"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


            if serializer.is_valid():
                serializer.save()
                
                return Response({"message":"update sucessfully"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error":f"server error {e}"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)



    def delete(self, request, pk, format=None):
        try:
            board_instance = get_object_or_404(Board,id=pk)
            board_instance.delete()
            return Response({"message":"deleted succesfully"},status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.debug(e)
            return Response({"error":f"server error {e}"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class BoardListView(APIView):

    """
    Crud For LIST
    """
	
    serializer_class = ListSerializer
    permission_classes = ( IsAuthenticated,)
    
    
	
    def get(self, request,pk, format=None):
        try:
            try:
                board_instance = Board.objects.get(id=pk)
            except Exception as e:
                logger.debug(e)
                return Response({"error":f"server error {e} pls check id's"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            list_instance = List.objects.filter(board=board_instance)
            try:
                serializer = ListSerializer(list_instance, many=True)
            except Exception as e:
                logger.debug(e)
                return Response({"error":f"server error {e} pls check input datatype"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


            return Response(serializer.data)
        except Exception as e:
            logger.debug(e)
            return Response({"error":f"server error {e}"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def post(self, request,pk, format=None):
        
        try:
            try:
                 board_instance = Board.objects.get(id=pk)
            except Exception as e:
                logger.debug(e)
                return Response({"error":f"server error {e} pls check id's"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


            if List.objects.filter(board=board_instance,title=request.data['title']).exists():
                return Response({"error":"List with Title Already Exists"}, status=status.HTTP_403_FORBIDDEN)
            
            request.data['board'] = pk
            try:
                serializer = ListSerializer(data=request.data)
            except Exception as e:
                logger.debug(e)
                return Response({"error":f"server error {e} pls check input datastructure"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            if serializer.is_valid():
            
                serializer.save()
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.debug(e)
            return Response({"error":f"server error {e}"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)



    def patch(self, request, pk,lk, format=None):
        try:
            try:
                list_instance = get_object_or_404(List,id=lk)
                serializer = BoardSerializer(list_instance,
                                                data=request.data,
                                                partial=True)
            except Exception as e:
                logger.debug(e)
                return Response({"error":f"server error {e} pls check id's or input datatype"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


            if serializer.is_valid():
                serializer.save()
                
                return Response({"message":"update sucessfully"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error":f"server error {e}"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)



    def delete(self, request, pk,lk, format=None):
        try:
            try:
                list_instance = get_object_or_404(List,id=lk)
            except Exception as e:
                logger.debug(e)
                return Response({"error":f"server error {e} pls check id's"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


            list_instance.delete()
            return Response({"message":"deleted succesfully"},status=status.HTTP_204_NO_CONTENT)
        
        except Exception as e:
            logger.debug(e)
            return Response({"error":f"server error {e}"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class CardView(APIView):
    """
    Crud For Card
    """
	
    serializer_class = CardSerializer
    permission_classes = ( IsAuthenticated,)
    parser_classes = (MultiPartParser, )
    
    
	
    def get(self, request,pk,lk, format=None):
        try:
            try:
                list_instance = List.objects.get(id=lk)
            except Exception as e:
                logger.debug(e)
                return Response({"error":f"server error {e} pls check id's"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


            card_instance = Card.objects.filter(list=list_instance)
            try:
                serializer = CardSerializer(card_instance, many=True)
            except Exception as e:
                logger.debug(e)
                return Response({"error":f"server error {e} pls check input Datatype and structure"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(serializer.data)
        except Exception as e:
            logger.debug(e)
            return Response({"error":"server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request,pk,lk, format=None):
        
        try:
            try:
            
                 list_instance = List.objects.get(id=lk)
            except Exception as e:
                logger.debug(e)
                return Response({"error":f"server error {e} pls check id's"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


            title_dict =eval(request.data["data"])
            attachments = request.data["attachments"]

            dict_to_serialize ={
                "list":lk,
                "title":title_dict['title'],
                "due_date":title_dict['due_date'],
                "attachments":attachments,
            } 
            if Card.objects.filter(list=list_instance,title=dict_to_serialize['title']).exists():
                return Response({"error":"Card with Title Already Exists"}, status=status.HTTP_403_FORBIDDEN)
            
            request.data['list'] = lk
            try:
                serializer = CardSerializer(data=dict_to_serialize)
            except Exception as e:
                logger.debug(e)
                return Response({"error":f"server error {e} pls check input data type and structure"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if serializer.is_valid():
            
                serializer.save()
                return Response({"message":serializer.data,"message":"succesfully created"},
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.debug(e)
            return Response({"error":"server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def patch(self, request, pk,lk,ck, format=None):

        try:
            try:
                list_instance = List.objects.get(id=lk)
                card_instance = get_object_or_404(Card,id=ck)
            except Exception as e:
                logger.debug(e)
                return Response({"error":f"server error {e} pls check id's"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)   
            try:
                title_dict =eval(request.data["data"])
            except:
                title_dict = defaultdict()
            try:
                if "attachments" in request.data.keys():
                    attachments = request.data["attachments"]
                elif "attachments" not in request.data.keys():
                     attachments = None
            except:
                attachments = None
                
            dict_to_serialize = defaultdict()
            if title_dict:
                if 'title' in title_dict.keys():
                    if Card.objects.filter(list=list_instance,title=title_dict['title']).exists():
                        return Response({"error":"Card with Title Already Exists"}, status=status.HTTP_403_FORBIDDEN)
            
                    dict_to_serialize['title'] = title_dict['title']

                if 'due_date' in title_dict.keys():
                    dict_to_serialize['due_date'] = title_dict['due_date']
            if attachments is not None:
                dict_to_serialize['attachments'] = attachments
           
            try:
                serializer = CardSerializer(card_instance,
                                                data=dict_to_serialize,
                                                partial=True)
            except Exception as e:
                logger.debug(e)
                return Response({"error":f"server error {e} pls check input data type and field"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


            if serializer.is_valid():
                serializer.save()
                
                return Response({"message":"update sucessfully"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.debug(e)
            return Response({"error":"server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def delete(self, request, pk,lk,ck, format=None):
        try:
            try:
                card_instance = get_object_or_404(Card,id=ck)
            except Exception as e:
                logger.debug(e)
                return Response({"error":f"server error {e} pls check id's"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


            card_instance.delete()
            return Response({"message":"deleted succesfully"},status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.debug(e)
            return Response({"error":f"server error {e}"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class CardMoveView(APIView):
    """
    Card Move View
    """
	
    serializer_class = CardSerializer
    permission_classes = ( IsAuthenticated,)
   
    
    
	
    def get(self, request, format=None):
        try:
        
            data = request.data
            a,b = swap_objects(data)
            if a:
                return Response({"message":"moved sucessfully"}, status=status.HTTP_201_CREATED)
            elif not a:
                logger.debug(b)
                return Response({"error":"server error pls check id's"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            logger.debug(e)
            return Response({"error":f"server error {e}"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
