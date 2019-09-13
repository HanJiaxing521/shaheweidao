from django.urls import path, include

import wxshahe.views

urlpatterns = [
    path('wxshahe/index/', wxshahe.views.get_diet),
    path('wxshahe/dish/', wxshahe.views.get_diet_content),
    path('wxshahe/rank/praise/', wxshahe.views.get_praise_rank),
    path('wxshahe/rank/cook/', wxshahe.views.get_cook_rank),
    path('wxshahe/login/', wxshahe.views.register),
    path('wxshahe/dish/praise/', wxshahe.views.add_praise),
    path('wxshahe/index/search/', wxshahe.views.get_search),
    path('wxshahe/canteen/', wxshahe.views.get_canteen),
    path('wxshahe/history/', wxshahe.views.get_history),
    path('wxshahe/love/', wxshahe.views.get_love),
    path('wxshahe/feedback/', wxshahe.views.get_feedback),
    path('wxshahe/comment/', wxshahe.views.get_comment),
    path('wxshahe/manager/', wxshahe.views.is_manager)
]
