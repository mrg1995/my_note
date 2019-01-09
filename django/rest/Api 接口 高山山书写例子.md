### Api 接口 高山山书写例子

- resources.py

  ```python
  #!coding=utf-8
  import json

  from django.http.response import HttpResponse
  from django.conf.urls import url
  from django.views.decorators.csrf import csrf_exempt

  from Api.utils import method_not_allowed

  # 为所有的请求 规定一个默认类 方便 且 节省代码量 不用每次判断method
  class Resource(object):
      def __init__(self, name=None):
          # 给 resource 初始名字   如果没有输入name  那么初始名为自己的类名
          self.name = name or self.__class__.__name__.lower()

      def enter(self, request, *args, **kwargs):
          method = request.method
          #判断request的类型是什么,分别进行处理
          if method == 'GET':
              response = self.get(request, *args, **kwargs)
          elif method == 'POST':
              response = self.post(request, *args, **kwargs)
          elif method == 'PUT':
              response = self.put(request, *args, **kwargs)
          elif method == 'DELETE':
              response = self.delete(request, *args, **kwargs)
          elif method == 'HEAD':
              response = self.head(request, *args, **kwargs)
          elif method == "OPTIONS":
              response = self.options(request, *args, **kwargs)
          else:
              response = HttpResponse(json.dumps({
                  "state": 422,
                  "msg": '方法不支持'
              }))
          return response
  	# 因为是默认的resources类里的方法  默认都是返回方法不支持
      def get(self, request, *args, **kwargs):
          return method_not_allowed()   # method_not_allowed 这类经常用到的函数 可以放在一个py文件里 此例子是放在utils.py文件中

      def post(self, request, *args, **kwargs):
          return method_not_allowed()

      def delete(self, request, *args, **kwargs):
          return method_not_allowed()

      def put(self, request, *args, **kwargs):
          return method_not_allowed()

      def options(self, request, *args, **kwargs):
          return method_not_allowed()

      def head(self, request, *args, **kwargs):
          return method_not_allowed()

  # url注册器  register方法将视图类   
  class Register(object):

      def __init__(self, version='v1'):
          self.version = version
          self.resources = []

      def regist(self, resource):
          self.resources.append(resource)
  	
      @property    # property装饰器  可以使函数 通过 register.urls 来获得函数的返回值
      def urls(self):
          urlpatterns = []
          for resource in self.resources:
              urlpatterns.append(
                  url(r'{version}/{name}'.format(version=self.version,
                                                 name=resource.name), csrf_exempt(resource.enter))  #csrf_exempt()装饰器  是为了使enter方法可以不被csrf限制
              )
          return urlpatterns  

  ```

  - views.py

    ```python
    #!coding=utf-8

    import random

    from datetime import datetime

    from django.contrib.auth import authenticate, login, logout

    from Question.models import *

    from Api.resources import Resource

    from Api.utils import *

    from Api.decorators import *

    #以下均为视图的类方法  继承上面的Resource类  只需要写自己需要的方法  不需要写那些限制的重复代码

    #由于浏览器只有get和post两种方式  且django框架只能解析form-data,  json,xml,text均无法自动解析 因此写一个中间件  用来伪增加浏览器的请求方式(实际上还是只有两种请求方式), 并对返回的不同格式的数据进行提取解析, 方便在视图文件中进行操作

    获取注册码

    class ReigstCodeResource(Resource):

        def get(self, request, *args, **kwargs):

            regist_code = random.randint(10000, 100000)

            request.session['regist_code'] = regist_code

            return HttpResponse(json.dumps({

                'regist_code': regist_code

            }), content_type="application/json")

    用户信息

    class UserResource(Resource):

        # 获取用户信息

        def get(self, request, *args, **kwargs):

            if request.user.is_authenticated:

                user = request.user

                # 判断是否是普通用户

                if hasattr(user, 'userinfo'):

                    userinfo = user.userinfo

                    # 构建json字典

                    data = dict()

                    data['user'] = user.id

                    data['age'] = getattr(userinfo, 'age', '')

                    data['name'] = getattr(userinfo, 'name', '')

                    data['gender'] = getattr(userinfo, 'gender', '')

                    data['phone'] = getattr(userinfo, 'phone', '')

                    data['email'] = getattr(userinfo, 'email', '')

                    data['address'] = getattr(userinfo, 'address', '')

                    if userinfo.birthday:

                        data['birthday'] = userinfo.birthday.strftime("%Y-%m-%d")

                    else:

                        data['birthday'] = datetime.now().strftime("%Y-%m-%d")

                    data['qq'] = getattr(userinfo, 'qq', '')

                    data['wechat'] = getattr(userinfo, 'wechat', '')

                    data['job'] = getattr(userinfo, 'job', '')

                    data['salary'] = getattr(userinfo, 'salary', '')

                    # 用json把data转化成字符串,返回给客户端

                    return HttpResponse(json.dumps(data), content_type="application/json")

                # 判断是否是客户

                elif hasattr(user, 'customer'):

                    customer = user.customer

                    # 构建json字典

                    data = dict()

                    data['user'] = user.id

                    data['name'] = getattr(customer, 'name', '')

                    data['email'] = getattr(customer, 'email', '')

                    data['company'] = getattr(customer, 'company', '')

                    data['address'] = getattr(customer, 'address', '')

                    data['phone'] = getattr(customer, 'phone', '')

                    data['mobile'] = getattr(customer, 'mobile', '')

                    data['qq'] = getattr(customer, 'qq', '')

                    data['wechat'] = getattr(customer, 'wechat', '')

                    data['web'] = getattr(customer, 'web', '')

                    data['industry'] = getattr(customer, 'industry', '')

                    data['description'] = getattr(customer, 'description', '')

                    # 用json把data转化称字符串,返回给客户端

                    return HttpResponse(json.dumps(data), content_type="application/json")

                else:

                    # 没有相关用户信息,返回空

                    return HttpResponse(json.dumps({

                        "data": {}

                    }), content_type="application/json")

            # 用户未登录,不允许查看信息

            return HttpResponse(json.dumps({

                "msg": '未登录'

            }), content_type="application/json")

    ```


      # 注册用户
      def put(self, request, *args, **kwargs):
          data = request.PUT
          username = data.get('username', '')
          password = data.get('password', '')
          regist_code = data.get('regist_code', '')
          session_regist_code = request.session.get('regist_code', '')
          category = data.get('category', 'userinfo')
          ensure_password = data.get('ensure_password', '')
      
          # 构建错误信息字典
          errors = dict()
          if not username:
              errors['username'] = '没有提供用户名'
          elif User.objects.filter(username=username):
              errors['username'] = '用户名已存在'
          if len(password) < 6:
              errors['password'] = '密码长度不够'
          if password != ensure_password:
              errors['ensure_password'] = '密码不一样'
          if regist_code != str(session_regist_code):
              errors['regist_code'] = '验证码不对'
          if errors:
              return HttpResponse(json.dumps(errors), content_type='application/json')
          user = User()
          user.username = username
          # 设置密码
          user.set_password(password)
          user.save()
          # 根据用户类型,创建普通用户或者客户
          if category == 'userinfo':
              userinfo = UserInfo()
              userinfo.user = user
              userinfo.name = '姓名'
              userinfo.save()
          else:
              customer = Customer()
              customer.name = '客户名称'
              customer.user = user
              customer.save()
      
          return HttpResponse(json.dumps({
              "msg": "创建成功",
              "user_id": user.id
          }), content_type='application/json')
      
      # 更新用户
      def post(self, request, *args, **kwargs):
          data = request.POST
          user = request.user
          if user.is_authenticated:
              # 判断是否是普通用户
              if hasattr(user, 'userinfo'):
                  userinfo = user.userinfo
                  userinfo.name = data.get('name', '姓名')
                  userinfo.age = data.get('age', '')
                  userinfo.gender = data.get('gender', '')
                  userinfo.phone = data.get('phone', '')
                  userinfo.email = data.get('email', '')
                  userinfo.address = data.get('address', '')
      
                  # 时间特殊处理
                  try:
                      birthday = datetime.strptime(
                          data.get('birthday', '2018-01-01'), "%Y-%m-%d")
                  except Exception as e:
                      birthday = datetime.now()
      
                  userinfo.birthday = birthday
      
                  userinfo.qq = data.get('qq', '')
                  userinfo.wechat = data.get('wechat', '')
                  userinfo.job = data.get('job', '')
                  userinfo.salary = data.get('salary', '')
                  userinfo.save()
              # 判断是否是客户
              elif hasattr(user, 'customer'):
                  customer = user.customer
                  customer.name = data.get('name', '客户名称')
                  customer.email = data.get('email', '')
                  customer.company = data.get('company', '')
                  customer.address = data.get('address', '')
                  customer.phone = data.get('phone', '')
                  customer.mobile = data.get('mobile', '')
                  customer.qq = data.get('qq', '')
                  customer.wechat = data.get('wechat', '')
                  customer.web = data.get('web', '')
                  customer.industry = data.get('industry', '')
                  customer.description = data.get('description', '')
                  customer.save()
              return HttpResponse(json.dumps({
                  'msg': '更新成功'
              }), content_type="application/json")
          return HttpResponse(json.dumps({
              'msg': '还未登录'
          }), content_type="application/json")


  # 用户登录与退出
  class SessionResource(Resource):

      def get(self, request, *args, **kwargs):
          if request.user.is_authenticated:
              return json_response({
                  'msg': '已经登录'
              })
          return json_response({
              'msg': '还未登录'
          })
      
      def put(self, request, *args, **kwargs):
          data = request.PUT
          username = data.get('username', '')
          password = data.get('password', '')
          user = authenticate(username=username, password=password)
          if user:
              login(request, user)
              return json_response({
                  'msg': '登录成功'
              })
          return json_response({
              'msg': '用户名或密码错误'
          })
      
      def delete(self, request, *args, **kwargs):
          logout(request)
          return json_response({
              'msg': '退出成功'
          })


  # 问卷资源
  class QuestionnaireResource(Resource):
​      
      @customer_required
      def get(self, request, *args, **kwargs):
          return json_response({})
      
      @customer_required
      def put(self, request, *args, **kwargs):
          return json_response({})


      @customer_required
      def post(self, request, *args, **kwargs):
          return json_response({})
      
      @customer_required
      def delete(self, request, *args, **kwargs):
          return json_response({})
    
    ​```
      
    ​```

- middleware.py  中间件

  ```python
  import json

  from django.http.multipartparser import MultiPartParser
  from django.middleware.common import MiddlewareMixin


  class DataConvert(MiddlewareMixin):
      """
      # 数据类型转换
      > 因为django只能解析使用post方式上传的formdata
      > 不能够解析通过其他方法上传的json,xml,text格式数据,所以这里面,我们需要手动来解析上传的数据
      """

      def process_request(self, request):
          method = request.method
          if 'application/json' in request.META['CONTENT_TYPE']:
              # 把客户端上传的json数据转化成python字典
              data = json.loads(request.body.decode())
              files = None
          elif 'multipart/form-data' in request.META['CONTENT_TYPE']:
              # 把客户端已formdata上传的数据进行解析,通常客户端会把上传的文件也放在formdata中,
              # 所以下面的解析会把上传的文件也解析出来
              data, files = MultiPartParser(
                  request.META, request, request.upload_handlers).parse()
          else:
              data = request.GET
              files = None

          if 'HTTP_X_METHOD' in request.META:
              method = request.META['HTTP_X_METHOD'].upper()
              setattr(request, 'method', method)

          if files:
              setattr(request, '{method}_FILES'.format(method=method), files)
          setattr(request, method, data)
  ```

- decorators.py   装饰器

  ```python
  from Api.utils import permission_denied

  #因为视图文件中  很多函数需要加用户验证  使用装饰器 减少代码量
  # 在执行制定方法前, 先对用户进行判断  是否已经登陆, 并对其进行分类处理
  def customer_required(func):
      def _wrapper(self, request, *args, **kwargs):
          if request.user.is_authenticated and hasattr(request.user, 'customer'):
              return func(self, request, *args, **kwargs)
          return permission_denied()
      return _wrapper


  def userinfo_required(func):
      def _wrapper(self, request, *args, **kwargs):
          if request.user.is_authenticated and hasattr(request.user, 'userinfo'):
              return func(self, request, *args, **kwargs)
          return permission_denied()
      return _wrapper

  ```

- utils.py   一些常见的response放在这个文件中

  ```python
  #!coding=utf-8
  import json

  from django.http.response import HttpResponse


  def method_not_allowed():
      return HttpResponse(json.dumps({
          "state": 405,
          "msg": '方法不支持',
      }), content_type="application/json")


  def json_response(data):
      json_data = {
          'state': 200,
          'msg': 'OK',
          'data': data
      }
      return HttpResponse(json.dumps(json_data), content_type='application/json')


  def server_error():
      return HttpResponse(json.dumps({
          'state': 500,
          'msg': '服务器发生错误'
      }), content_type='application/json')


  def not_found():
      return HttpResponse(json.dumps({
          'state': 404,
          'msg': '没有找到页面'
      }), content_type='application/json')


  def params_error(data={}):
      return HttpResponse(json.dumps({
          'state': 422,
          'msg': '参数错误',
          'data': data
      }), content_type='application/json')


  def not_authenticated():
      return HttpResponse(json.dumps({
          'state': 401,
          'msg': '未登录'
      }), content_type='application/json')


  def permission_denied():
      return HttpResponse(json.dumps({
          'state': 403,
          'msg': '没有权限'
      }), content_type='application/json')

  ```




