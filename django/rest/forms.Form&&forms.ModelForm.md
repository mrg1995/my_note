# forms.Form和forms.ModelForm

一. forms.Form
二. forms.ModelForm
三. ModelForm的clean_字段名的方法

------

#### 一. forms.Form

比如, 验证手机号姓名等

- form.py

```python
from django import forms
from operation.models import UserAsk
class UserAskForm(forms.Form):
    # 姓名
    name = forms.CharField(required=True, min_length=2, max_length=20)
    # 电话11位 不可以为空
    phone = forms.CharField(required=True, min_length=11, max_length=11)
    # 课程名字
    course_name = forms.CharField(required=True, min_length=5, max_length=15)
```

- models.py

```python
class UserAsk(models.Model):
    name = models.CharField(max_length=20, verbose_name=u'姓名')
    mobile = models.CharField(max_length=11, verbose_name=u'手机')
    course_name = models.CharField(max_length=50, verbose_name=u'课程名')
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
```

forms和models中有大量重复, 因此选用 ModelForm

#### 二. forms.ModelForm

- form.py

```python
from django import forms
from operation.models import UserAsk
class UserAskForm(forms.ModelForm):
    # my_field = 也可以选择在原模型的基础上添加其他form验证字段
    class Meta:
        # 使用的模型类
        model = UserAsk
        # 列表里表示需要验证的字段, 直接使用model中的限制, 比如max_length null = True 之类
        fields = ['name', 'mobile', 'course_name']
```

比如此处也可以对手机号做合法性判断, 定义chean_mobile方法

#### 三. clean_字段名

- 比如判断手机号码

```python
import re
class UserAskForm(forms.ModelForm):
    # my_field =
    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    # 会自动调用此方法, 对mobile进行验证. 函数名必须是clean_字段的形式
    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        p = re.compile('^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}')
        if p.match(mobile):
            return mobile
        else:
            # 抛出异常
            raise forms.ValidationError(u'手机号码非法', code='mobile_invalid')
```

同时ModelForm还支持直接将合理数据保存, 例

- views.py

```python
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            # commit为True表示提交数据库, 默认True
            user_ask = userask_form.save(commit=True)
            return HttpResponse('{"status": "succes"}', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail", "msg": "添加出错"}',
                                content_type='application/json')
```

