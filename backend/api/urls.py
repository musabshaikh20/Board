# from django.urls import path
from django.urls import path
from .views import BoardView,BoardListView,CardView,CardMoveView,RevokeView

urlpatterns = [
    path('boards/',BoardView.as_view(),name="boards" ),
    path('boards/<int:pk>/update', BoardView.as_view(),name="boardupdate"),
    path('boards/<int:pk>/delete', BoardView.as_view(),name="boarddelete"),
    path('boards/<int:pk>/list', BoardListView.as_view(),name="list"),
    path('boards/<int:pk>/list/<int:lk>/update', BoardListView.as_view(),name="updatelist"),
    path('boards/<int:pk>/list/<int:lk>/delete', BoardListView.as_view(),name="deletelist"),
    path('boards/<int:pk>/list/<int:lk>/card', CardView.as_view(),name="cards"),
    path('boards/<int:pk>/list/<int:lk>/card/<int:ck>/update', CardView.as_view(),name="cardsupdate"),
    path('boards/<int:pk>/list/<int:lk>/card/<int:ck>/delete', CardView.as_view(),name="cardsdelete"),
    path('card/move',CardMoveView.as_view(),name="cardsmove"),
    path('revoke', RevokeView.as_view(), name='auth_logout'),
    
]
