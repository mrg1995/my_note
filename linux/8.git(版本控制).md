#  git
## 1.git简介
![image](git.png)
- workspace 工作区
- index 暂存区
- repository 本地版本库
- remote 远程仓库
## 2.常用git命令
   - git --version 查看版本
- git config -l 查看配置信息
- 修改name和email 
    - git config --global user.name 'ddd'
    - git config --global user.email 'ddd@jdjdjd.com'
- 克隆版本库  
    - git clone 版本库地址     将远端服务上的项目克隆到本地
- 创建版本库 
    - git init   初始化一个新的项目 ，必须切换到版本库所在目录 
- 将文件添加到暂存区
    - git add 文件名     将指定文件添加到暂存区
    - git add .          将所有文件添加到暂存区
- 提交代码到版本库
    -  git commit  -m "说明信息"
    -  git commit -a -m    提交所有文件
- 将本地代码推送到远端托管服务器
    - git push [origin master] 默认推送到主分支
    - git push origin 分支名     推送到指定分支
- 从远端服务器拉取内容
    - git pull
- 查看版本库状态
    - git status
- 查看提交记录
    - git log
    - git log --prety=oneline
      -版本回退
    - git reset --hard head~n
        - head~ 上一个版本
        - head~~上两个版本
        - head~n 上n版本
    - git reset --hard 版本号
## 3.git使用流程
- 首先到托管服务器上创建一个空版本库，例如在github、coding、oschina等
- 然后克隆到本地(clone)创建一个新项目
- 或者可以通过初始化项目创建一个新项目 git init
    - git remote add origin 远程仓库地址 
- 添加代码文件（git add)
- 提交代码到本地库 git commit -m
- 将代码推送到远端服务器 git push
- 从远端服务器拉取代码git  pull
## 4 冲突管理
- 如果有多个人同时修改同一个文件的相同行，在推送时会有冲突
- 发生冲突后，首先将服务器端代码拉到本地（pull），手动合并冲突
- 然后添加修改后的代码文件，重新提交
- 将代码推送到服务器
## 5 分支管理
- master 主分支，记录发布版本
- online 线上分支 正在运行的版本
- develop 开发分支 用于测试
- local 本地分支
- 分支管理常用命令
    - git branch 查看分支
    - git branch 新分支 [旧分支]    基于旧分支创建新分支
    - git branch -d 分支名      删除分支
    - git checkout 分支           切换到指定分支
    - git merge 分支名            将指定分支合并到当前分支
## 问题
- 如果克隆的时候出现了： unable to access 'https://git.coding.net/landmark/php1702.git/': error setting certificate 解决方式：
    - Git config --global http.sslVerify false 