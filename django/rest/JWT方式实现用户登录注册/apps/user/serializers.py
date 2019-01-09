import re
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.conf import settings
from .models import VerifyCode

User = get_user_model()


# 如果只是简单对传入的表单数据进行判断,可以继承serializers.Serializer
# 这样可以调用serializers中的一些写好的判断
class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11, required=True, help_text='注册手机号')

    def validate_mobile(self, mobile):
        # 查看user表中是否存在
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("该手机号已被注册")
        # 判断手机号是否正确
        if not re.match(settings.REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码有误")
        one_minute = datetime.now() - timedelta(minutes=1)
        if VerifyCode.objects.filter(add_time__gt=one_minute, mobile=mobile).count():
            raise serializers.ValidationError("距离上次发送未超过60秒")
        return mobile

# 写一个用户序列化类
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'gender', 'email', 'mobile')

# 注册时的序列化类
# 写两个用户的序列化类,方便处理 注册 和 用户信息读取 这两个方面
class UserRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=11, min_length=2, required=True, help_text='手机号')
    # 密码和验证码 都是write_only
    password = serializers.CharField(max_length=12, min_length=2, required=True, write_only=True, help_text='密码')
    code = serializers.CharField(max_length=4, min_length=4, required=True, write_only=True, help_text='验证码')

    # 验证码校验
    # 验证的格式是 validate_(被验证的字段)
    def validate_code(self, code):
        # 取得验证码
        # 传入的数据在 initial_data  对象中
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data['username']).order_by('-add_time')

        if verify_records:
            last_record = verify_records[0]
            five_minutes_ago = datetime.now() - timedelta(minutes=5)
            if five_minutes_ago > last_record.add_time:
                raise serializers.ValidationError("验证码过期")
            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")
        else:
            raise serializers.ValidationError('验证码错误')

    # 当传入的数据仅当做验证,不需要保存数据库,如验证码  可以在通过验证后手动删除
    # 验证码校验后,因为不需要存在user表中, 因此删除code
    def validate(self, attrs):
        attrs['mobile'] = attrs['username']
        del attrs['code']
        return attrs

    # 因为 密码不能明文保存, 因此 重写create 方法  调用了auth自带的create_user方法创建用户
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = ('username', 'code', 'password')
