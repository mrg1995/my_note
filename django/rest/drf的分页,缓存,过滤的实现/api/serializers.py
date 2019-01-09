from rest_framework import serializers
from api.models import User_info, Bt_test
from django.contrib.auth.models import User


class User_infoSerializer(serializers.ModelSerializer):

    class Meta:
        model = User_info
        fields = ('id', 'age', 'gender', 'phone')


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class Bt_testSerializer(serializers.ModelSerializer):
    # 我需要序列化输出单个bt种子的网页地址
    # 具体可以看 https://www.jianshu.com/p/89e9031b7fae
    # 里面有 ModelSerializer 的两种情景 第二种符合当前情景
    url = serializers.SerializerMethodField()

    # 生成 自定义的url 用来返回
    def get_url(self,obj):
        return 'http://127.0.0.1:8000/search/bts/{}/'.format(obj.id)

    class Meta:
        model = Bt_test
        fields = ('url', 'av_name', 'magent', 'hash_info', 'time_info', 'size_info')

    # @classmethod
    # def setup_eager_loading(cls, queryset):
    #     queryset = queryset.prefetch_related()
