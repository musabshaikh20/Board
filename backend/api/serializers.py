from rest_framework import serializers
from .models import Board,List,Card


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("user","id", "title","description", "created_at")
        model = Board

class ListSerializer(serializers.ModelSerializer):
    

    class Meta:
        fields = ("board","id","title","created_at")
        model = List
        

class CardSerializer(serializers.ModelSerializer):


    class Meta:
        fields = ("list","id","title","due_date","attachments","created_at")
        model = Card
            
