### Django URL name详解

```python
# 在 urls.py文件中
urlpatterns = [
    url(r'^$', calc_views.index, name='home'),
    url(r'^add/$', calc_views.add, name='add'),
    url(r'^add/(\d+)/(\d+)/$', calc_views.add2, name='add2'),
    url(r'^admin/', admin.site.urls),
]
```

```html
// 在html中
<a href="{% url 'add2' 4 5 %}">link</a>
```

```python
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
def old_add2_redirect(request, a, b):
    return HttpResponseRedirect(
        reverse('add2', args=(a, b))  # reverse 方法可以导出地址  具体如下
    )
#>>> reverse('add2', args=(4,5))
# u'/add/4/5/'
```

#### 命名空间 namespace

```python
#  project.urls.py
from django.conf.urls import url,include
urlpatterns = [
    url(r'^a/', include('app01.urls', namespace='author-polls')),
    url(r'^b/', include('app01.urls', namespace='publisher-polls')),
]
```

```python
# app01.urls.py
from django.conf.urls import url
from app01 import views
 
app_name = 'app01'
urlpatterns = [
    url(r'^(?P<pk>\d+)/$', views.detail, name='detail')
]
```

```python
# app01.views.py
def detail(request, pk):
    print(request.resolver_match)
    return HttpResponse(pk)
```

以上定义带命名空间的url之后,生成url如下

- v=reverse('author-polls:detail', kwargs={'pk':11})
- {%  url 'author-polls:detail' pk=11 %}

### Django 表单模块

- tempelate里的表单控件的name(html里) 需要 和 创建的表单类 的 属性名一致
- ​

**Form表单的功能**

- 自动生成HTML表单元素
- 检查表单数据的合法性
- 如果验证错误，重新显示表单（数据不会重置）
- 数据类型转换（字符类型的数据转换成相应的Python类型）

**Form相关的对象包括**

- Widget：用来渲染成HTML元素的工具，如：forms.Textarea对应HTML中的<textarea>标签
- Field：Form对象中的一个字段，如：EmailField表示email字段，如果这个字段不是有效的email格式，就会产生错误。
- Form：一系列Field对象的集合，负责验证和显示HTML元素
- Form Media：用来渲染表单的CSS和JavaScript资源。



```python
# 实例化一个Form对象
# 直接继承Form
from django import forms
class ContactForm(forms.Form):
     subject = forms.CharField(max_length=100,label='主题')
     message = form.CharField(widget=forms.TextArea)
     sender = form.EmailField()
     cc_myself = forms.BooleanField(required=False)
```

```python
# 在view中使用form
form django.shortcuts import render
form django.http import HttpResponseRedirect
 
def contact(request):
     if request.method=="POST":
          form = ContactForm(request.POST)
          if form.is_valid(): #所有验证都通过
           #do something处理业务
           return HttpResponseRedirect('/')
          else:
           form = ContactForm()
          return render(request,'contact.html',{'form':form})
```

```html
// 在html中使用form
<form action='/contact/' method='POST'>
 {% for field in form %}
  <div class = 'fieldWrapper'>
   {{field.label_tag}}:{{field}}
   {{field.errors}}
  </div>
 {% endfor %}
 <div class='fieldWrapper'> <p><input type='submit' value='留言'></p></div>
</form>
```

**处理表单数据**

form.is_valid()返回true后，表单数据都被存储在form.cleaned_data对象中（字典类型，意为经过清洗的数据），而且数据会被自动转换为Python对象

```python
if form.is_valid():
 subject = form.cleaned_data['subject']
 message = form.cleaned_data['message']
 sender = form.cleaned_data['sender']
 cc_myself = form.cleaned_data['cc_myself']
 
 recipients = ['info@example.com']
 if cc_myself:
  recipients.append(sender)
 
 from django.core.mail import send_mail
 send_mail(subject, message, sender, recipients)
 return HttpResponseRedirect('/thanks/') # Redirect after POST
```



urls 内容转载自 :https://code.ziqiangxuetang.com/django/django-url-name.html

form表单内容转自:https://www.cnblogs.com/zongfa/p/7709639.html