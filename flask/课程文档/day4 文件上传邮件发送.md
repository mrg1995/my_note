# 文件上与邮件发送

## 文件上传

## 一、原生文件上传

#### 模板文件

```python
{% if newName %}
    <img src="{{ url_for('static',filename=newName) }}" alt="">
{% endif %}
<form action="{{ url_for('upload') }}" enctype="multipart/form-data" method="post">
    <input type="file" name="file">
    <p><input type="submit" value="submit"></p>
</form>
```

#### manage.py

```python
from flask import Flask,render_template,request
from flask_script import Manager
from flask_bootstrap import Bootstrap
import os
from PIL import Image
#pip3 install pillow 图片处理库

app = Flask(__name__)
#允许上传的后缀
app.config['ALLOWED_EXTENSIONS'] = ['.jpg','.jpeg','.png','.gif']
#上传的大小
app.config['MAX_CONTENT_LENGTH'] = 1024*1024*64 #64兆
#配置文件上传的路径
app.config['UPLOAD_FOLDER'] = os.getcwd()+'/static'

bootstrap = Bootstrap(app)
manager = Manager(app)

@app.route('/')
def index():
    return render_template('index.html')

#生成随机图片名称的函数
def new_name(shuffix,length=32):
    import string, random
    myStr = string.ascii_letters + '0123456789'
    newName = ''.join(random.choice(myStr) for i in range(length))
    return newName+shuffix

def allowed_file(shuffix):
    return shuffix in app.config['ALLOWED_EXTENSIONS']

# 处理
#1 获取后缀 判断是否所允许
#2 设置上传大小
#3 生成随机的图片名称
@app.route('/upload',methods=['GET','POST'])
def upload():
    img_name = None
    if request.method == 'POST':
        # print(request.files)
        file = request.files.get('file') #拿到文件对象
        filename = file.filename #获取上传的图片名称
        shuffix = os.path.splitext(filename)[-1]
        #获取到名称的后缀
        #为真 则继续处理
        if allowed_file(shuffix):
            #调用生成随机图片名称的函数
            while True:
            	newName = new_name(shuffix)
                newPath = os.path.join(app.config['UPLOAD_FOLDER'],newName)
            	if not os.path.exists(newPath)
            	break
            img_name = newName
            #拼凑完整的图片上传路径
            file.save(newPath) #保存图片

            #处理图片的缩放
            img = Image.open(newPath)
            print(img.size)
            #重新设置大小和尺寸
            img.thumbnail((200,200))
            #自己回去验证  这个位置的缩放 是否为等比缩放 如果不是等比缩放 变成等比缩放
            #400 200
            #200 300
            #200 100
            img.save(newPath)
        # return '上传成功 名称为{}'.format(newName)
    return render_template('upload.html',newName=img_name)
```





## 二、flask-uploads

文件上传的第三方模块

pip3 install flask-uploads

**导入**

```
from flask_uploads import UploadSet,IMAGES,configure_uploads,patch_request_class
```

**完整**

```python
from flask import Flask,render_template,request
from flask_script import Manager
from flask_bootstrap import Bootstrap
import os
from flask_uploads import UploadSet,IMAGES,configure_uploads,patch_request_class
from flask_wtf import FlaskForm
from wtforms import FileField,SubmitField
from flask_wtf.file import FileAllowed,FileRequired

app = Flask(__name__)
#允许上传的后缀
app.config['SECRET_KEY'] = 'image'
app.config['MAX_CONTENT_LENGTH'] = 1024*1024*64 #64兆
#配置文件上传的路径
app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd()+'/static/upload'

file = UploadSet('photos',IMAGES)
configure_uploads(app,file)
patch_request_class(app,size=None)


bootstrap = Bootstrap(app)
manager = Manager(app)

class File(FlaskForm):
    file = FileField('文件上传',validators=[FileRequired(message='您还没有选择文件'),FileAllowed(file,message='只能上擦图片')])
    submit = SubmitField('上传')

#生成随机图片名称的函数
def new_name(shuffix,length=32):
    import string, random
    myStr = string.ascii_letters + '0123456789'
    newName = ''.join(random.choice(myStr) for i in range(length))
    return newName+shuffix

@app.route('/upload',methods=['GET','POST'])
def upload():
    form = File()
    img_url = None
    # if request.method == 'POST' and 'file' in request.files:
    if form.validate_on_submit():
        shuffix = os.path.splitext(form.file.data.filename)[-1]
        newName = new_name(shuffix=shuffix)
        file.save(form.file.data,name=newName)
        img_url = file.url(newName)
    return  render_template('boot_upload.html',newName=img_url,form=form)

if __name__ == '__main__':
    manager.run()
```



## 三、flask-mail 邮件发送

**安装**

pip3 install flask-mail

```python
from flask import Flask,render_template_string
from flask_mail import Mail,Message
import os

app = Flask(__name__)

app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER','smtp.1000phone.com')

app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME','xialigang@1000phone.com')

app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD','123456')
mail = Mail(app)

@app.route('/')
def index():
    msg = Message(subject='邮件激活',recipients=['13484275339@163.com'],sender=app.config['MAIL_USERNAME'])
    msg.html = render_template_string('<h2>大郎啊 我是金莲啊</h2>')
    mail.send(message=msg)
    return '发送邮件'

if __name__ == '__main__':
    app.run(debug=True)
```

**使用线程发送邮件  避免用户在等待（也就是防止当前页面没有很快响应的问题）**

```python
from flask import Flask,render_template_string,render_template
from flask_mail import Mail,Message
import os
from threading import Thread

app = Flask(__name__)

app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER','smtp.1000phone.com')

app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME','xialigang@1000phone.com')

app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD','123456')
mail = Mail(app)

def async_send_mail(app,msg):
    #获取当前程序的上下文
    with app.app_context():
        mail.send(message=msg)


def send_mail(subject,to,tem,**kwargs):
    msg = Message(subject=subject, recipients=[to], sender=app.config['MAIL_USERNAME'])
    msg.html = render_template(tem+'.html',**kwargs)
    send = Thread(target=async_send_mail,args=(app,msg))
    send.start()

@app.route('/')
def index():
    send_mail('邮件激活','13484275339@163.com','mail',username='zhangsan')
    return '发送邮件'

if __name__ == '__main__':
    app.run(debug=True)
```







































