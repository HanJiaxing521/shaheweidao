# -*- coding: utf-8 -*-
import json
# from wxshahe.mode
# from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
# from django.core import serializers
from django.core.cache import cache
from wxshahe.models import Diet
from wxshahe.models import User
from wxshahe.models import Cook
from wxshahe.models import Log
from wxshahe.models import Attribution
from wxshahe.models import Group
from wxshahe.models import Feedback
from django.utils import timezone
# from django.core.paginator import Paginator
# Create your views here.


def register(request):
    # 登录注册
    user_id = request.GET.get('openid')
    is_exist = User.objects.filter(user_id=user_id)
    if len(is_exist) != 0:
        isManager = {'manager': is_exist[0].user_manager}
        return HttpResponse(json.dumps(isManager))
    user_name = request.GET.get('nickName')
    user_image = request.GET.get('image')
    user = User(user_id=user_id, user_name=user_name, user_image=user_image)
    user.save()
    isManager = {'manager': user.user_manager}
    return HttpResponse(json.dumps(isManager))


def get_diet(request):
    # 获取20个菜品对象
    diet_list = Diet.objects.all()[:20]
    diet_short_list = []
    for diet in diet_list:
        single_diet = {'diet_id': diet.diet_id,
                       'diet_name': diet.diet_name,
                       'diet_image': diet.diet_image,
                       'diet_material': diet.diet_material,
                       'diet_nutrient': diet.diet_nutrient,
                       'diet_location': diet.diet_location,
                       'diet_praise': diet.diet_praise,
                       'diet_cook_id': diet.diet_cook_id}
        diet_short_list.append(single_diet)
    return HttpResponse(json.dumps(diet_short_list, ensure_ascii=False),
                        content_type='application/json, charset = utf-8')


def get_praise_rank(request):
    # 获取点赞排行信息
    diet_rank = Diet.objects.order_by('-diet_praise')[:10]
    diet_list = []
    for diet in diet_rank:
        single_diet = {'diet_id': diet.diet_id,
                       'diet_name': diet.diet_name,
                       'diet_image': diet.diet_image,
                       'diet_nutrient': diet.diet_nutrient,
                       'diet_location': diet.diet_location,
                       'diet_praise': diet.diet_praise,
                       'diet_cook_id': diet.diet_cook_id
                       }
        diet_list.append(single_diet)
    return HttpResponse(json.dumps(diet_list, ensure_ascii=False),
                        content_type='application/json, charset = utf-8')


def get_cook_rank(request):
    # 获取大厨排行信息
    cook_rank = Cook.objects.order_by('-cook_praise')[:10]
    cook_list = []
    for cook in cook_rank:
        single_cook = {'cook_id': cook.cook_id,
                       'cook_name': cook.cook_name,
                       'cook_image': cook.cook_image,
                       'cook_brief_content': cook.cook_brief_content,
                       'cook_praise': cook.cook_praise
                       }
        cook_list.append(single_cook)
    return HttpResponse(json.dumps(cook_list, ensure_ascii=False),
                        content_type='application/json, charset = utf-8')


def is_manager(request):
    # 判断当前用户是否为管理员
    user_id = int(request.POST.get('user_id', None))
    user_list = User.objects.all()
    for user in user_list:
        if user.user_id == user_id:
            return JsonResponse({'is_manager': user.is_manager})
    return HttpResponse(u"用户不存在")


def add_praise(request):
    # 增加赞数量
    curr_user_id = request.GET.get('user_id')
    curr_diet_id = request.GET.get('diet_id')
    is_praise = request.GET.get('diet_praise')

    if is_praise == 'true':
        pra = Diet.objects.get(diet_id=curr_diet_id)
        print(pra.diet_praise)
        pra.diet_praise -= 1
        pra.save()
        user = Log.objects.get(log_user_id=curr_user_id,
                               log_diet_id=curr_diet_id)
        user.log_diet_praise = False
        user.save()

    else:
        pra = Diet.objects.get(diet_id=curr_diet_id)
        print(pra.diet_praise)
        pra.diet_praise += 1
        pra.save()
        user = Log.objects.get(log_user_id=curr_user_id,
                               log_diet_id=curr_diet_id)
        user.log_diet_praise = True
        user.save()

    return_json = {'praise_num': pra.diet_praise}
    return HttpResponse(json.dumps(return_json))


def get_diet_content(request):
    # 获取单个菜品信息
    curr_diet_id = request.GET.get('diet_id')
    curr_user_id = request.GET.get('user_id')
    log = Log.objects.filter(log_user_id=curr_user_id,
                             log_diet_id=curr_diet_id)
    if len(log) == 0:
        log = Log(log_user_id=curr_user_id,
                  log_diet_id=curr_diet_id, log_diet_praise=False)
        log.save()
    diet = Diet.objects.get(diet_id=curr_diet_id)
    evaluation_list_json = []
    diet_content = {'diet_id': diet.diet_id,
                    'diet_location': diet.diet_location,
                    'diet_name': diet.diet_name,
                    'diet_image': diet.diet_image,
                    'diet_material': diet.diet_material,
                    'diet_nutrient': diet.diet_nutrient,
                    'diet_praise': Log.objects.get(log_user_id=curr_user_id, log_diet_id=curr_diet_id).log_diet_praise,
                    'praise_num': diet.diet_praise,
                    'diet_evaluation': evaluation_list_json}

    evaluation_list = Log.objects.filter(log_diet_id=curr_diet_id)
    for evaluation in evaluation_list:
        if evaluation.log_diet_evaluation == "":
            continue
        single_evaluation = {'user_id': evaluation.log_user_id,
                             'user_name': User.objects.get(user_id=evaluation.log_user_id).user_name,
                             'user_image': User.objects.get(user_id=evaluation.log_user_id).user_image,
                             'content': evaluation.log_diet_evaluation}
        evaluation_list_json.append(single_evaluation)

    return HttpResponse(json.dumps(diet_content, ensure_ascii=False),
                        content_type='application/json, charset = utf-8')


def get_comment(request):
    # 将评论信息存入数据库
    user_id = request.GET.get('user_id')
    diet_id = request.GET.get('diet_id')
    diet_comment = request.GET.get('diet_comment')
    log = Log.objects.filter(log_user_id=user_id,
                             log_diet_id=diet_id)
    if len(log) == 0:
        log = Log(log_user_id=user_id,
                  log_diet_id=diet_id, log_diet_praise=False, log_diet_evaluation=diet_comment)
        log.save()
    else:
        log[0].log_diet_evaluation = diet_comment
        log[0].save()

    info = {'info': 'success'}
    return HttpResponse(json.dumps(info, ensure_ascii=False), content_type='application/json, charset = utf-8')


def get_recom(request):
    # 获得个性化推荐菜品
    user_id = request.GET.get('user_id')
    user_group = Group(user_id=user_id).group
    if user_group == 0:
        diet_list = Diet.objects.all()[:20]
        diet_short_list = []
        for diet in diet_list:
            single_diet = {'diet_id': diet.diet_id,
                           'diet_name': diet.diet_name,
                           'diet_image': diet.diet_name,
                           'diet_material': diet.diet_material,
                           'diet_nutrient': diet.diet_nutrient,
                           'diet_location': diet.diet_location,
                           'diet_praise': diet.diet_praise,
                           'diet_cook_id': diet.diet_cook_id}
            diet_short_list.append(single_diet)
        return HttpResponse(json.dumps(diet_short_list, ensure_ascii=False),
                            content_type='application/json, charset = utf-8')
    else:
        con_user_list = Group.objects.filter(group=user_group)
        recom_list = []
        for con_user in con_user_list:
            logs = Log.objects.filter(log_user_id=con_user.user_id)
            for log in logs:
                single_rom = {'diet_id': log.log_diet_id,
                              'diet_name': Diet.objects.get(diet_id=log.log_diet_id).diet_name,
                              'diet_image': Diet.objects.get(diet_id=log.log_diet_id).diet_image,
                              'diet_material': Diet.objects.get(diet_id=log.log_diet_id).diet_material,
                              'diet_nutrient': Diet.objects.get(diet_id=log.log_diet_id).diet_nutrient,
                              'diet_location': Diet.objects.get(diet_id=log.log_diet_id).diet_location,
                              'diet_praise': Diet.objects.get(diet_id=log.log_diet_id).diet_praise,
                              'diet_cook_id': Diet.objects.get(diet_id=log.log_diet_id).diet_cook_id}
                recom_list.append(single_rom)
        return HttpResponse(json.dumps(recom_list, ensure_ascii=False),
                            content_type='application/json, charset = utf-8')


def get_search(request):
    # 模糊搜索
    keyword = request.GET.get('keyword')
    nameResult = Diet.objects.filter(diet_name__icontains=keyword)
    materResult = Diet.objects.filter(diet_material__icontains=keyword)
    nutriResult = Diet.objects.filter(diet_nutrient__icontains=keyword)

    results = nameResult | materResult | nutriResult
    results = results.distinct()
    result_list = []
    for result in results:
        single_result = {'diet_id': result.diet_id,
                         'diet_name': result.diet_name,
                         'diet_image': result.diet_image,
                         'diet_material': result.diet_material,
                         'diet_nutrient': result.diet_nutrient,
                         'diet_location': result.diet_location,
                         'diet_praise': result.diet_praise,
                         'diet_cook_id': result.diet_cook_id
                         }
        result_list.append(single_result)

    return HttpResponse(json.dumps(result_list, ensure_ascii=False),
                        content_type='application/json, charset = utf-8')


def get_love(request):
    # 收藏
    user_id = request.GET.get('openid')
    log_list = Log.objects.filter(log_user_id=user_id)
    love_list = []
    for log in log_list:
        if log.log_diet_praise is True:
            diet = Diet.objects.get(diet_id=log.log_diet_id)
            result = {'diet_id': diet.diet_id,
                      'diet_name': diet.diet_name,
                      'diet_image': diet.diet_image,
                      'diet_material': diet.diet_material,
                      'diet_nutrient': diet.diet_nutrient,
                      'diet_location': diet.diet_location,
                      'diet_praise': diet.diet_praise,
                      'diet_cook_id': diet.diet_cook_id
                      }
            love_list.append(result)
    return HttpResponse(json.dumps(love_list, ensure_ascii=False),
                        content_type='application/json, charset = utf-8')


def get_history(request):
    # 历史记录
    user_id = request.GET.get('openid')
    log_list = Log.objects.filter(log_user_id=user_id)
    history_list = []
    for log in log_list:
        diet = Diet.objects.get(diet_id=log.log_diet_id)
        result = {'diet_id': diet.diet_id,
                  'diet_name': diet.diet_name,
                  'diet_image': diet.diet_image,
                  'diet_material': diet.diet_material,
                  'diet_nutrient': diet.diet_nutrient,
                  'diet_location': diet.diet_location,
                  'diet_praise': diet.diet_praise,
                  'diet_cook_id': diet.diet_cook_id
                  }
        history_list.append(result)
    return HttpResponse(json.dumps(history_list, ensure_ascii=False),
                        content_type='application/json, charset = utf-8')


def get_canteen(request):
    # 获得各个餐厅的菜单
    can_name = request.GET.get('keyword')
    diet_list = Diet.objects.filter(diet_location__icontains=can_name)

    fried_list = []  # 炒饭
    veg_list = []  # 炒菜
    wheaten_list = []  # 面食
    soup_list = []  # 汤
    dessert_list = []  # 甜点

    for diet in diet_list:
        single_result = {'diet_id': diet.diet_id,
                         'diet_name': diet.diet_name,
                         'diet_image': diet.diet_image,
                         'diet_material': diet.diet_material,
                         'diet_nutrient': diet.diet_nutrient,
                         'diet_location': diet.diet_location,
                         'diet_praise': diet.diet_praise,
                         'diet_cook_id': diet.diet_cook_id
                         }
        if '饭' in single_result['diet_name']:
            fried_list.append(single_result)
        elif '面' in single_result['diet_name'] or '饺' in single_result['diet_name']:
            wheaten_list.append(single_result)
        elif '汤' in single_result['diet_name']:
            soup_list.append(single_result)
        elif '糕' in single_result['diet_name']:
            dessert_list.append(single_result)
        else:
            veg_list.append(single_result)

    fried_json = {'id': 1,
                  'title': '炒饭',
                  'list': fried_list}
    veg_json = {'id': 2,
                'title': '炒菜',
                'list': veg_list}
    wheaten_json = {'id': 3,
                    'title': '面食',
                    'list': wheaten_list}
    soup_json = {'id': 4,
                 'title': '汤',
                 'list': soup_list}
    dessert_json = {'id': 5,
                    'title': '甜点',
                    'list': dessert_list}
    result_list = [fried_json, veg_json, wheaten_json, soup_json, dessert_json]

    return HttpResponse(json.dumps(result_list, ensure_ascii=False), content_type='application/json, charset = utf-8')


def get_feedback(request):
    # 获取反馈的意见
    class_array = request.GET.get('mesclass')  # 意见类别
    for cla in class_array:
        if cla['checked'] is True:
            mes_class = cla['text']
            break
    mes_time = timezone.localtime(timezone.now()).strftime(
        "%Y-%m-%d %H:%M:%S")  # 提交时间
    mes_text = request.GET.get('mestext')    # 意见内容
    mes_image = request.GET.get('mesimage')  # 图片
    mes_message = request.GET.get('message')  # 联系方式
    feedback = Feedback(que_class=mes_class, que_time=mes_time,
                        que_text=mes_text, que_image=mes_image, que_message=mes_message)
    feedback.save()
    info = {'info': 'success'}
    return HttpResponse(json.dumps(info, ensure_ascii=False), content_type='application/json, charset = utf-8')
