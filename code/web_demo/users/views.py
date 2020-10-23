from django.shortcuts import render, redirect
# from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponse
from users.models import User
from django.views import View
from django.utils.decorators import method_decorator


# Create your views here.


def register(request):
    """注册View视图函数"""
    if request.method == 'GET':
        return render(request, 'index.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.create(username=username, password=password)
        # return JsonResponse({'message': '注册成功'})
        return redirect('/login/')


# def login(request):
#     if request.method == 'GET':
#         # username = request.COOKIES.get('username')
#         # return render(request, 'login.html', context={'username': username})
#         return render(request, 'login.html')
#     else:
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         remember = request.POST.get('remember')
#
#         try:
#
#             # 根据 username 和 password 查询对应的用户是否存在，即进行用户名和密码校验
#
#             # get 方法默认会利用查询到的数据创建一个对应的模型类对象，并将这个模型对象返回
#
#             user = User.objects.get(username=username, password=password)
#
#         except User.DoesNotExist:
#
#             # 如果 get 方法查询不到数据，会出现 `模型类.DoesNotExist` 异常
#             #
#
#             # 用户名或密码错误
#
#             return JsonResponse({'message': 'login failed'})
#
#         else:
#             request.session['user_id'] = user.id
#             request.session['username'] = user.username
#             # response = JsonResponse({'message': 'login success'})
#             # if remember == 'true':
#             #     response.set_cookie('username', username, max_age=3600)
#             # # 用户名和密码正确
#
#             # return response
#             if remember != 'true':
#                 request.session.set_expiry(0)
#             return JsonResponse({'message': 'login success'})
#
#         return response
#
# def login(request):
#     username = request.session.get('username')
#     if username:
#         return  HttpResponse('%s用户已登录'%username)
#     if request.method == 'GET':
#         return  render(request, 'login.html')
#     else:
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         remember = request.POST.get('remember')
#
#     try:
#         user = User.objects.get(username=username,password=password)
#     except User.DoesNotExist:
#         return JsonResponse({'message':'login failed'})
#     else:
#         request.session['user_id'] = user.id
#         request.session['username'] = user.username
#
#         if remember != 'true':
#             request.session.set_expiry(0)
#         return  JsonResponse({'message':'login success'})

def is_login(view_func):
    def inner(request):
        username = request.session.get('username')
        if username:
            return HttpResponse('%s用户已登录'%username)
        return view_func(request)
    return inner


class LoginView(View):
    @method_decorator(is_login)
    def get(self, request):
        # username = request.session.get('username')

        # if username:
        #     return HttpResponse('%s用户已登录' % username)
        return render(request, 'login.html')

    @method_decorator(is_login)
    def post(self, request):

        # username = request.session.get('username')
        #
        # if username:
        #     return HttpResponse('%s用户已登录' % username)
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remember')

        try:
            user = User.objects.get(username=username, password=password)
        except User.DoesNotExist:
            return JsonResponse({'message': 'login failed'})
        else:

            request.session['user_id'] = user.id
            request.session['username'] = user.username

            if remember != 'true':
                request.session.set_expiry(0)
            return JsonResponse({'message': 'login success'})
