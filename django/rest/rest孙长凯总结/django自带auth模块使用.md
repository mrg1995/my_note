## 创建用户

```python
>>> from django.contrib.auth.models import User
>>> user = User.objects.create_user(username='john',
...                                 email='jlennon@beatles.com',
...                                 password='glass onion')
```

## 修改密码

```
>>> user = User.objects.get(username='john')
>>> user.set_password('goo goo goo joob')
>>> user.save()
```

## User属性

| username     | 必需的，不能多于30个字符。 仅用字母数字式字符（字母、数字和下划线）。     |
| ------------ | ---------------------------------------- |
| first_name   | 可选; 少于等于30字符。                            |
| last_name    | 可选; 少于等于30字符。                            |
| email        | 可选。 邮件地址。                                |
| password     | 必需的。 密码的哈希值（Django不储存原始密码）。 See the Passwords section for more about this value. |
| is_staff     | 布尔值。 用户是否拥有网站的管理权限。                      |
| is_active    | 布尔值. 设置该账户是否可以登录。 把该标志位置为False而不是直接删除账户。 |
| is_superuser | 布尔值 标识用户是否拥有所有权限，无需显式地权限分配定义。            |
| date_joined  | 账号被创建的日期时间 当账号被创建时，它被默认设置为当前的日期/时间。      |
| last_login   | 用户上次登录的时间日期。 它被默认设置为当前的日期/时间。            |

## User方法

| 方法                      | 描述                                       |
| ----------------------- | ---------------------------------------- |
| is_authenticated()      | 对于真实的User对象，总是返回`True` 。这是一个分辨用户是否已被鉴证的方法。 它并不意味着任何权限，也不检查用户是否仍是活动的。 它仅说明此用户已被成功鉴证。 |
| get_full_name()         | 返回`first_name` 加上`last_name` ，中间插入一个空格。  |
| set_password(passwd)    | 设定用户密码为指定字符串（自动处理成哈希串）。 实际上没有保存`User`对象。 |
| check_password(passwd)  | 如果指定的字符串与用户密码匹配则返回`True`。 比较时会使用密码哈希表。   |
| get_group_permissions() | 返回一个用户通过其所属组获得的权限字符串列表。                  |
| get_all_permissions()   | 返回一个用户通过其所属组以及自身权限所获得的权限字符串列表。           |
| has_perm(perm)          | 如果用户有指定的权限，则返回`True` ，此时`perm` 的格式是`"package.codename"` 。如果用户已不活动，此方法总是返回`False` 。 |
|                         |                                          |

## 登陆和退出

Django 提供内置的视图(view)函数用于处理登录和退出 (以及其他奇技淫巧)，但在开始前，我们来看看如何手工登录和退出。 Django提供两个函数来执行django.contrib.auth\中的动作 : authenticate()和login()。

认证给出的用户名和密码，使用 authenticate() 函数。它接受两个参数，用户名 username 和 密码 password ，并在密码对给出的用户名合法的情况下返回一个 User 对象。 如果密码不合法，authenticate()返回None。

```python
>>> from django.contrib import auth
>>> user = auth.authenticate(username='john', password='secret')
>>> if user is not None:
...     print "Correct!"
... else:
...     print "Invalid password."
```

authenticate() 只是验证一个用户的证书而已。 而要登录一个用户，使用 login() 。该函数接受一个HttpRequest 对象和一个 User 对象作为参数并使用Django的会话（ session ）框架把用户的ID保存在该会话中。

下面的例子演示了如何在一个视图中同时使用 authenticate() 和 login() 函数：

#### 登陆

```python
from django.contrib import auth

def login_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        # Correct password, and the user is marked "active"
        auth.login(request, user)
        # Redirect to a success page.
        return HttpResponseRedirect("/account/loggedin/")
    else:
        # Show an error page
        return HttpResponseRedirect("/account/invalid/")
```

#### 登出

```python
from django.contrib import auth

def logout_view(request):
    auth.logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/account/loggedout/")
```

 它接受一个HttpRequest对象并且没有返回值。

即使用户没有登录， logout() 也不会抛出任何异常。



## 限制未登陆用户的访问

```python
from django.http import HttpResponseRedirect

def my_view(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login/?next=%s' % request.path)
    # ...
```

也可以使用login_required修饰符

```python
from django.contrib.auth.decorators import login_required

@login_required
def my_view(request):
    # ...
```

login_required 做下面的事情:

- 如果用户没有登录, 重定向到 /accounts/login/ , 把当前绝对URL作为 next 在查询字符串中传递过去, 例如： /accounts/login/?next=/polls/3/ 。
- 如果用户已经登录, 正常地执行视图函数。 视图代码就可以假定用户已经登录了。



## 对于不同权限的访问限制

限制访问可以基于某种权限，某些检查或者为login视图提供不同的位置，这些实现方式大致相同。

一般的方法是直接在视图的 request.user 上运行检查。 例如，下面视图确认用户登录并是否有polls.can_vote权限：

```python
def vote(request):
    if request.user.is_authenticated() and request.user.has_perm('polls.can_vote')):
        # vote here
    else:
        return HttpResponse("You can't vote in this poll.")
```

并且Django有一个称为 user_passes_test 的简洁方式。它接受参数然后为你指定的情况生成装饰器。

```python
def user_can_vote(user):
    return user.is_authenticated() and user.has_perm("polls.can_vote")

@user_passes_test(user_can_vote, login_url="/login/")
def vote(request):
    # Code here can assume a logged-in user with the correct permission.
    ...
```

user_passes_test 使用一个必需的参数： 一个可调用的方法，当存在 User 对象并当此用户允许查看该页面时返回True 。 注意 user_passes_test 不会自动检查 User是否认证，你应该自己做这件事。