## 介绍
- 作用：
1. 版本控制（保留了一切历史版本，可以让代码恢复到你想指定的位置）
2. 协作开发

linux内核创始人：林纳斯（linus）

- 集中式版本控制系统：svn
- 分布式版本控制系统：git

- 与github的关系：在自己的电脑上使用git，只有版本控制功能，与github连用可以使用协作开发功能


## 极速创建
- `git config` 配置
- `git init`：初始化
- `git add`：添加文件或文件夹（存入暂存区）
- `git commit -m "first commit"`：提交
	- `git status`：状态
	- `git log`：历史记录
	- `git reset -hard 7483927`：版本回退
- `git remote add origin https://github.com/W-exhale/learning.git`：连接到远程
- `git push -u origin main`：推送到远程
## 安装
### windows
1. 直接在官网下
2. 通过Scoop（包管理器）下：`scoop install git`
	升级非常方便：`scoop update git`
### linux
1. `sudo apt install git`

### 配置
```plain
$ git config --global user.name "Your Name"
$ git config --global user.email "email@example.com"
```
- 注意
	- `git config`命令的`--global`参数，用了这个参数，表示你这台机器上所有的Git仓库都会使用这个配置，当然也可以对某个仓库指定不同的用户名和Email地址。
	- ![[Pasted image 20250321172404.png]]
- 后续可以通过`git config --list`来查看当前目录的用户名和邮箱

### 创建版本库
- 即创建一个目录（也可以在一个有东西的目录），这个目录里的所有文件都可以被Git管理起来，每个文件的修改、删除Git都可以跟踪
1. 先找一个没有中文的目录创建一个文件夹
2. 在那个文件夹git bash，然后输入`git init`（如下图就是创建好了，还告诉你是一个空的仓库）![[Pasted image 20250321164739.png|500]]![[Pasted image 20250321170627.png]]
3. 创建一个文件：`README.txt`，使用`git add README.txt`添加到仓库
	1. 可以同时添加很多文件：`git add file2.txt file3.txt`
4. 提交：`git commit -m "wrote a readme file"`![[Pasted image 20250321173548.png]]
	1. `-m`后面输入的是本次提交的说明

- 注意
1. 所有的版本控制系统只能跟踪文本文件的改动(txt文件，网页，程序代码等)，
	1. git可以告诉你在第5行加了一个单词“Linux”，在第8行删了一个单词“Windows”等，
	2. 但是图片、视频这些二进制文件，虽然也能由版本控制系统管理，但没法跟踪文件的变化，只能把二进制文件每次改动串起来，也就是只知道图片从100KB改成了120KB，但到底改了啥是无法知道的。
	3. Microsoft的Word格式是二进制格式，因此，版本控制系统是没法跟踪Word文件的改动的
2. 如果没有历史遗留问题，强烈建议使用标准的UTF-8编码，所有语言使用同一种编码，既没有冲突，又被所有平台所支持。
3. 不要使用Windows自带的**记事本**编辑任何文本文件。
	1. Microsoft开发记事本的团队使用了一个非常弱智的行为来保存UTF-8编码的文件，他们在每个文件开头添加了0xefbbbf（十六进制）的字符，
	2. 你会遇到的问题，比如，网页第一行可能会显示一个“?”，明明正确的程序一编译就报语法错误，等等
4. git命令只能在git仓库内使用





## 提交
### 基础提交
- 查看仓库当前状态：`git status`，下面的modified表示已修改，红色表示还没提交![[Pasted image 20250322133627.png]]
- 查看更改(不同)：`git diff`，减号表示删减，加号表示添加的内容（abc）![[Pasted image 20250322133909.png]]
- 提交到仓库前可以通过上面的方式检查，提交修改和提交新文件也是先`git add README.txt`，然后`git commit -m "add abc"`
- ![[Pasted image 20250322134513.png]]
### 版本回退
- 存快照，快照叫`commit`
- 用`git log`查看历史记录，也可以加上`--pretty=oneline`参数，更简约

![[Pasted image 20250322205651.png]]![[Pasted image 20250322210225.png]]
一串乱码样的是`commit id`（版本号），和SVN不一样，Git的版本号不是1，2，3....，这是由SHA1计算出来的一个非常大的数字，用16进制表示，因为Git是分布式版本控制系统，会有很多人协同开发，如果都用1，2，3....，一定会冲突


- `HEAD`表示当前版本，`HEAD^`表示上一个版本，上上个`HEAD^^`，如果上100个`HEAD~100`。
- 回退到上一个版本：`git reset --hard HEAD^`，`--hard`表示回退到上一个版本的已提交状态，`--soft`回到未提交状态，`--mixed`回退到已添加但未提交状态![[Pasted image 20250322213039.png]]
- 如果想回到未来，可以向上翻，找到未来的版本号，输入前几个就可以，Git会自动找
- Git的版本回退速度非常快，因为Git在内部有个指向当前版本的`HEAD`指针，当你回退版本的时候，Git仅仅是把HEAD指向之前的版本![[Pasted image 20250322214501.png]]
- 如果关了电脑就没办法往上翻找版本号了，git提供了一个命令`git reflog`来记录每一次命令：![[Pasted image 20250322214725.png]]
## 工作区和暂存区
- Git和SVN等其他版本控制系统有个不同的地方就是有个暂存区
### 工作区(Working Directory)
- 即在电脑中能看到的目录，gitRepository就算一个

### 版本库(Reposity)
- 工作区中的隐藏目录：`.git`，这个不算工作区，属于Git的版本库
- 版本库中有一个叫stage(index)的暂存区，还有Git为我们自动创建的第一个分支master，以及指向`master`的一个指针`HEAD`。
- 将文件加入Git版本库有两步：
	1. `git add`：将文件加进去，实际上就是将文件修改加到暂存区
	2. `git commit`：提交修改，实际上就是将暂存区的所有内容提交到当前分支（创建Git版本库的时候，Git自动为我们创建了唯一一个`master`分支，这里分支就是这个master）
## 修改
### 管理修改
- git和其他版本控制系统相比更优秀，原因就是Git跟踪并管理的修改，而不是文件
- 修改：比如你新增了一行，这就是一个修改，删除了一行，也是一个修改，更改了某些字符，也是一个修改，删了一些又加了一些，也是一个修改，甚至创建一个新文件，也算一个修改。
- 一定要将确定的修改放到暂存区再提交，提交是提交的暂存区的内容

### 撤销修改
2.23及以后的版本用`git restore`命令
1. 修改后还没有`git add`，老版本用`git checkout -- example.txt`，新版本用`git restore example.txt`
2. 已经`git add`，使用`git reset HEAD example.txt`取消暂存，然后使用方法1撤销工作区的修改
3. 已经`git commit`但还没有提交远程仓库，
	1. `git reset --soft HEAD~1`：保留修改到工作区
	2. `git reset --hard HEAD~1`：完全撤销
4. 强制覆盖远程：（最好不要用）
	1. `git reset --hard <目标提交>`
	2. `git push --force`

### 删除文件
- 一般是直接在文件管理器中将文件删了，或者用`rm`命令删除
- 这时git知道我们删除了文件，所以工作区和版本库不一致，可以用`git status`看哪些文件被删除了
![[Pasted image 20250323192017.png]]

1. 如果确实要从版本库中删除该文件，`git rm`，然后`git commit`![[Pasted image 20250323192224.png]]
2. 使用`git checkout -- test.txt`：其实就是用版本库替换工作区的版本，无论工作区是修改还是删除都可以一键还原（或者用`git restore test.txt`）
3. 没有加到版本库中的文件无法恢复的（暂存区的可以恢复）
## 远程仓库
- 如果只是在一个仓库里管理文件，那么Git和SVN确实没有区别，但是Git的牛逼功能之一：远程仓库
- 同一个Git仓库可以分布到不同的机器上，最早是一台机器一个原始版本库，之后其他的机器可以“克隆”这个原始版本库，同时，每台机器的版本库都是一样的，没有主次之分

- 一台电脑上也可以克隆多个版本库，只要不在同一个目录下，但是一般不这样，因为如果硬盘没了，这个库还是全都没了

- 一般是找一台电脑充当服务器的角色，每天24小时开机，其他的人都从这个服务器仓库上克隆一份到自己电脑上，并且各自把各自的提交推送到服务器仓库里，也可以从服务器仓库中拉取别人的提交
- 可以搭建一台运行Git的服务器，但是有点小题大做了。幸好有GitHub，这是一个提供Git仓库托管服务的，所以只要注册一个GitHub账号，就可以免费获得Git远程仓库

- 我们本地Git仓库和GitHub仓库之间的传输是通过SSH加密的，所以我们需要进行设置：
	1. 创建SSH Key。在用户主目录下，看看有没有.ssh目录，如果有，可以看看这个目录下有无`id_rsa`和`id_rsa.pub`这两个文件，如果已经有了，可以直接下一步，没有就打开Shell(windows打开Git Bash)创建SSH Key（将邮件地址换成我们自己的一路回车，使用默认值就行，这个key不是很重要可以不设置）：`ssh-keygen -t rsa -C "youremail@example.com"`
		1. 如果创建好了，就可以看到.ssh下面有上面两个文件![[Pasted image 20250323224520.png]]
		2. `id_rsa`是私钥，不能泄露，`id_rsa.pub`是公钥可以告诉别人![[Pasted image 20250323224340.png]]
	2. 登录GitHub，打开“Account settings”，"SSH Keys"页面：点击“Add SSH Key”，填上任意Title，在“Key”文本框粘贴`id_rsa.pub`里面的内容![[Pasted image 20250323224944.png]]
- 为什么需要Key，因为要确定这台电脑提交的是我们自己，假如我们有多台电脑，可以将这几台电脑的ssh都加上，这样每台电脑上的都可以推送了
- GitHub上免费托管的Git仓库，任何人都可以看到，只是只有自己才能改
	- 可以将公开的仓库设置为私有的，这样别人就看不见
	- 自己动手搭建一个Git服务器，因为是自己的服务器，所以别人看不见。
### 添加到远程仓库
- 和本地关联：`git remote add origin git@github.com:W-exhale/gitRepository.git`（添加后，远程库的名字就是`origin`，这是Git默认的叫法，也可以改成别的，但是`origin`这个名字一看就知道是远程库。）![[Pasted image 20250323230512.png]]
- 将本地库内容推送到远程，用`git push`命令，实际上是将当前分支`master`推送到远程
- 由于远程库是空的，我们第一次推送`master`分支时，加上了`-u`参数，Git不但会把本地的`master`分支内容推送的远程新的`master`分支，还会把本地的`master`分支和远程的`master`分支关联起来，在以后的推送或者拉取时就可以简化命令（`git push origin master`）。


>当你第一次使用Git的`clone`或者`push`命令连接GitHub时，会得到一个警告：

```plain
The authenticity of host 'github.com (xx.xx.xx.xx)' can't be established.
RSA key fingerprint is xx.xx.xx.xx.xx.
Are you sure you want to continue connecting (yes/no)?
```
>这是因为Git使用SSH连接，而SSH连接在第一次验证GitHub服务器的Key时，需要你确认GitHub的Key的指纹信息是否真的来自GitHub的服务器，输入`yes`回车即可。
Git会输出一个警告，告诉你已经把GitHub的Key添加到本机的一个信任列表里了：
```plain
Warning: Permanently added 'github.com' (RSA) to the list of known hosts.
```
>这个警告只会出现一次，后面的操作就不会有任何警告了。
如果你实在担心有人冒充GitHub服务器，输入`yes`前可以对照[GitHub的RSA Key的指纹信息](https://help.github.com/articles/what-are-github-s-ssh-key-fingerprints/)是否与SSH连接给出的一致。

### 删除远程库和本地的绑定关系
- `git remote rm <name>`
- 最好先用`git remote -v`查看远程库信息
![[Pasted image 20250324124211.png]]

分布式版本系统的最大好处之一是在本地工作完全不需要考虑远程库的存在，也就是有没有联网都可以正常工作，而SVN在没有联网的时候是拒绝干活的！

### 从远程库clone
- `git clone git@github.com:michaelliao/gitskills.git`

- 如果有多个人协作开发，那么每个人各自从远程克隆一份就可以了。

- 你也许还注意到，GitHub给出的地址不止一个，还可以用`https://github.com/michaelliao/gitskills.git`这样的地址。实际上，Git支持多种协议，默认的`git://`使用`ssh`，但也可以使用`https`等其他协议。

- 使用`https`除了速度慢以外，还有个最大的麻烦是每次推送都必须输入口令，但是在某些只开放`http`端口的公司内部就无法使用`ssh`协议而只能用`https`。

- 更新最新的代码，`git pull`（假如是在gitee上上传文件更改，在vs code端使用这个命令更新）

## 分支管理
分支类似平行宇宙，当你正在电脑前努力学习Git的时候，另一个你正在另一个平行宇宙里努力学习SVN。两个平行宇宙互不干扰，不过，在某个时间点，两个平行宇宙合并了，结果，你既学会了Git又学会了SVN！

其他版本控制系统如SVN等都有分支管理，但是创建和切换分支比蜗牛还慢，但Git的分支是与众不同的，无论创建、切换和删除分支，Git在1秒钟之内就能完成！无论你的版本库是1个文件还是1万个文件
### 创建与合并分支
#### 思想
- 主分支是`master`
- 一开始的时候，`master`分支是一条线，Git用`master`指向最新的提交，再用`HEAD`指向`master`，就能确定当前分支，以及当前分支的提交点
![[Pasted image 20250324131723.png|400]]
每次提交，`master`分支都会向前移动一步，这样，随着你不断提交，`master`分支的线也越来越长。

- 假如我们创建了一个新的分支`dev`，指向`master`相同的提交，再将`HEAD`指向`dev`，就表示当前分支在`dev`上![[Pasted image 20250324131917.png|400]]
- 更改HEAD之后，对工作区的修改就是针对`dev`分支的，新提交一次后，`dev`指针往前，而`master`指针不变![[Pasted image 20250324132311.png|300]]
- 假如我们在`dev`上的工作完成了，就可以把`dev`合并到`master`上。直接把`master`指向`dev`的当前提交，就完成了合并![[Pasted image 20250324132512.png|400]]
- 合并完分支后，甚至可以删除`dev`分支。删除`dev`分支就是把`dev`指针给删掉，删掉后，我们就剩下了一条`master`分支：![[Pasted image 20250324132539.png|300]]
#### 步骤
- 查看当前分支：`git branch`，当前分支会有一个`*`，
- 创建新分支：`git branch <branch-name>`
- 2.23起使用：`git switch -c <branch-name>`创建并切换到新分支，或者`git checkout -b <branch-name>`（`-b`表示创建并切换）
- 切换到新分支：`git checkout <branch-name>`或`git switch master`
- 删除：`git branch -d <name>`

1. 创建dev分支并跳转`git switch -c dev`
2. 修改：`vim README.txt`
3. `git add`，`git commit`
4. 切换回去：`git checkout master`，（此时看README.txt是没有刚刚添加的内容的）
5. 将dev的分支合并到`master`分支上：`git merge dev`![[Pasted image 20250324134359.png]]
	- 有很多种合并方式
6. 合并成功后就可以删除`dev`分支了：`git branch -d dev`
### 解决冲突
- 在一个分支上修改提交，没有合并，在另一个分支上修改提交，就会引发冲突![[Pasted image 20250324141700.png|300]]
- 这时候如果用merge进行合并就会发生冲突，必须手动解决冲突后再进行提交，也可以用`git status`看冲突的文件![[Pasted image 20250324142533.png]]
- 合并失败之后，文件就会变成![[Pasted image 20250324142626.png]]
- 修改后再提交![[Pasted image 20250324142918.png|300]]
- 可以用`git log`查看合并情况![[Pasted image 20250324143139.png]]
- 删除`dev`分支
- 用`git log --graph`命令可以看到分支合并图。
- 使用`git log`会进入分页器，
	- **向下滚动**：
	    - 按下 `Space` 或 `Enter` 键。
	        - `Space`：滚动一页。
	        - `Enter`：滚动一行。
	- **向上滚动**：
	    - 按 `b` 键滚动一页向上。
	- **查找关键字**：
	    - 输入 `/关键字`，然后按 `Enter`，可以搜索日志中的内容。
	- **退出搜索模式**：
	    - 按 `n`：查找下一个匹配项。
	    - 按 `q`：退出搜索并返回到日志。
- 如果不想进入分页器，加上`--oneline`参数，也可以通过`git --no-pager log`禁用分页器
### 分支管理策略
- 一般合并分支时用的都是`Fast forward`模式，但是这种模式下删除分支后会丢掉分支信息
- 如果强制禁用`Fast forward`模式，Git就会在merge时生成一个新的commit，这样从分支历史上就可以看出分支信息

1. 切换到dev，进行修改提交，切换回master，进行合并
2. `git merge --no-ff -m "merge with no-ff" dev`：`--no-ff`参数表示禁用`Fast forward`，禁用后用git log可以看出合并`git log --graph --pretty=oneline --abbrev-commit`![[Pasted image 20250324152413.png]]
3. 合并分支时，加上`--no-ff`参数就可以用普通模式合并，合并后的历史有分支，能看出来曾经做过合并，而`fast forward`合并就看不出来曾经做过合并。

- 原则：
	- `master`分支应该是非常稳定的，仅用来发布最新版本，平时不能在上面干活
	- 干活在dev，所以这个分支不稳定，到1.0发布时再将dev分支合并到master上，在master分支发布1.0版本
- 团队合作的合并就会像这样![[Pasted image 20250324152803.png]]
### Bug分支
- 每个bug都可以通过一个新的临时分支来修复，修复后合并分支，再将临时分支删除
- 假如现在需要创建一个新的分支来修复一个bug，但是在当前的工作还没有完成，新任务又很急，可以使用`git stash`，将当前工作现场“存储起来”，恢复后继续工作

1. 在dev分支中工作，还未加入暂存区，使用`git stash`保存状态，用`git status`，可以看到没有未提交![[Pasted image 20250324154209.png]]
2. 假如我们要在`master`分支上修bug，就从`master`分支上创建分支`bug`，修改提交后回到`master`合并。
3. 回到dev分支，使用`git stash list`命令查看刚刚的工作现场，工作现场还在，只是需要恢复一下![[Pasted image 20250324185547.png]]
4. 恢复：`stash`的内容就就是存储区，
	1. 使用`git stash apply`，但是恢复后，`stash`的内容不删除，需要使用`git stash drop`来删除
	2. `git stash pop`：恢复的同时会把`stash`的内容也删掉（比较方便的感觉），使用`git stash list`就看不到刚刚的记录了
- 但是如果dev是从master分出来的，说明bug在dev也有，在dev要修复同样的bug，不用重复操作一次，有更简单的方法，只要找到bug的版本号，将这个提交所作的修改“复制”到`dev`分支即可![[Pasted image 20250324191010.png]]
- git的`cherry-pick`命令，让我们可以复制一个特定的提交到当前分支![[Pasted image 20250324191350.png]]
- git自动给`dev`分支做了一次提交，可以看到这次的提交和之前的版本号不一样

### Feature分支
- 添加一个新功能时，我们肯定不期望实验性质的代码将主分支弄乱，所以每次添加一个新功能，我们最好新建一个`feature`分支，在上面开发，完成...最后删除
- 假如我们接到一个新任务：开发代号为Vulcan的新功能
1. `git switch -c feature-vulcan`，然后提交
2. 切回`dev`，但是这时候上级说新功能取消，`git branch -d feature-vulcan`，销毁失败，提示如果删除将丢失修改，如果要强行删除需要使用大写的`-D`，即`git branch -D feature-vulcan`

### 多人协作
- 当我们从远程仓库克隆时，实际上Git自动把本地的`master`分支和远程的`master`分支对应起来
- 查看远程库的信息：`git remote`，或者`git remote -v`更详细（显示了可以抓取和推送的`origin`地址）
```plain
$ git remote -v
origin  git@github.com:michaelliao/learngit.git (fetch)
origin  git@github.com:michaelliao/learngit.git (push)
```
- 推送分支：`git push origin master`
	- `master`分支是主分支，需要时刻同步
	- `dev`分支是开发分支，团队所有分支都需要在上面工作，所以也需要与远程同步
	- bug分支只用于本地修复bug，不用推送
	- feature分支取决于是否合作在上面开发

- 抓取分支：多人协作时，会往`master`和`dev`分支上推送各自的修改
	- 假设另一台电脑连接克隆我们的项目，只能看到本地的master分支
	- 如果要在dev分支上开发，就必须创建远程`origin`的`dev`分支到本地：`git checkout -b dev origin/dev`
	- 现在，就可以在`dev`上继续修改，修改好提交后推送
	- 假如我们也修改了，试图推送，但是推送失败，这时候我们需要先用`git pull`将最新的提交拉取过来，然后在本地合并，解决冲突，再进行推送
```plain
$ git pull
There is no tracking information for the current branch.
Please specify which branch you want to merge with.
See git-pull(1) for details.

    git pull <remote> <branch>

If you wish to set tracking information for this branch you can do so with:

    git branch --set-upstream-to=origin/<branch> dev
```
`git pull`也失败了，原因是没有指定本地`dev`分支与远程`origin/dev`分支的链接，根据提示，设置`dev`和`origin/dev`的链接：
```plain
$ git branch --set-upstream-to=origin/dev dev
Branch 'dev' set up to track remote branch 'dev' from 'origin'.
```

- 多人协作工作模式：
	1. 尝试用`git push origin <branch-name>`推送自己的修改
	2. 如果推送失败，使用`git pull`更新
	3. 如果有冲突，在本地解决后提交
	4. 如果都解决了，使用`git push origin <branck-name>`
如果`git pull`提示`no tracking information`，则说明本地分支和远程分支的链接关系没有创建，用命令`git branch --set-upstream-to <branch-name> origin/<branch-name>`。

### Rebase
- 多人协作时很容易出现冲突，后push的人必须先pull，在本地合并后才能push，git的log历史也很不美观![[Pasted image 20250324201517.png]]
- 变基：`rebase`，也就是将基于上一次的修改变了

在和远程分支同步后，我们对`hello.py`这个文件做了两次提交。用`git log`命令看看：
```bash
$ git log --graph --pretty=oneline --abbrev-commit
* 582d922 (HEAD -> master) add author
* 8875536 add comment
* d1be385 (origin/master) init hello
*   e5e69f1 Merge branch 'dev'
|\  
| *   57c53ab (origin/dev, dev) fix env conflict
| |\  
| | * 7a5e5dd add env
| * | 7bd91f1 add new env
...
```
注意到Git用`(HEAD -> master)`和`(origin/master)`标识出当前分支的HEAD和远程origin的位置分别是`582d922 add author`和`d1be385 init hello`，本地分支比远程分支快两个提交。
- push发现推送失败，因为冲突了，于是pull，然后看看状态
```plain
$ git status
On branch master
Your branch is ahead of 'origin/master' by 3 commits.
  (use "git push" to publish your local commits)

nothing to commit, working tree clean
```
```plain
$ git log --graph --pretty=oneline --abbrev-commit
*   e0ea545 (HEAD -> master) Merge branch 'master' of github.com:michaelliao/learngit
|\  
| * f005ed4 (origin/master) set exit=1
* | 582d922 add author
* | 8875536 add comment
|/  
* d1be385 init hello
...
```
- 如果现在将本地push，会很不好看，于是可以使用`git rebase`
```plain
$ git rebase
First, rewinding head to replay your work on top of it...
Applying: add comment
Using index info to reconstruct a base tree...
M	hello.py
Falling back to patching base and 3-way merge...
Auto-merging hello.py
Applying: add author
Using index info to reconstruct a base tree...
M	hello.py
Falling back to patching base and 3-way merge...
Auto-merging hello.py
```
输出了一大堆操作，`git log`看看：
```plain
$ git log --graph --pretty=oneline --abbrev-commit
* 7e61ed4 (HEAD -> master) add author
* 3611cfe add comment
* f005ed4 (origin/master) set exit=1
* d1be385 init hello
...
```
- 发现变成直线了，原理：可以发现我们本地的提交“挪动”了位置，放到了`f005ed4 (origin/master) set exit=1`，之后，这样历史就变成了直线，也就是rebase操作前后最终提交的内容是一致的，只是我们本地的commit修改内容已经从基于`d1be385 init hello`变成了基于`f005ed4 (origin/master) set exit=1`
- 最后，再push本地分支到远程，再用`git log`看看效果：
```plain
$ git log --graph --pretty=oneline --abbrev-commit
* 7e61ed4 (HEAD -> master, origin/master) add author
* 3611cfe add comment
* f005ed4 set exit=1
* d1be385 init hello
...
```

## 标签管理
- 发布一个版本的时候，我们通常会在版本库中打一个tag，将来取某一个标签的版本，就是把那个打tag的历史版本取出来，类似版本库的一个快照
- 虽然说是版本库的一个快照，但其实它就是指向某个commit的指针，和分支有点类似，但是tag不能移动，所以创建和删除tag都是瞬间完成的
- 虽然说也可以通过commit，但是版本号很难记

### 创建标签
1. 切换到需要打标签的分支上，使用`git tag v1.0`打标签，用`git tag`查看所有标签
2. 默认标签是打在commit上的，假如忘记打了，可以找到历史提交的commit id，`git log --pretty=oneline --abbrev-commit`，假如要打给`f52c633`commit，我们可以`git tag v0.9 f52c633`，可以用`git tag`查看
3. 标签不是按时间顺序列出的，而是按字母顺序排序的，可以用`git show <tagname>`查看标签信息
```plain
$ git show v0.9
commit f52c63349bc3c1593499807e5c8e972b82c8f286 (tag: v0.9)
Author: Michael Liao <askxuefeng@gmail.com>
Date:   Fri May 18 21:56:54 2018 +0800

    add merge

diff --git a/readme.txt b/readme.txt
...
```

- 可以创建带有说明的标签：`-a`指定标签名，`-m`指定说明文字`git tag -a v0.1 -m "version 0.1 released" 1094adb`

>标签总是和某个commit挂钩。如果这个commit既出现在master分支，又出现在dev分支，那么在这两个分支上都可以看到这个标签。

### 操作标签
- 删除标签：`git tag -d v0.1`
- 推送标签到远程：`git push origin <tagname>`
- 一次性推送全部尚未推送到远程的本地标签：`git push origin --tags`
- 如果已经推送到远程，要先从本地删除`git tag -d v0.9`，再从远程删除`git push origin :refs/tags/v0.9`
- 可以在hub看是否删除

## 使用GitHub和Gitee
### GitHub
- 点击Fork可以在自己的账号下克隆一个bootstrap仓库，然后从自己的账号下clone，要从自己的账号clone仓库，才能推送修改，一定要从自己的账号下clone仓库。

如果你想修复bootstrap的一个bug，或者新增一个功能，立刻就可以开始干活，干完后，往自己的仓库推送。

如果你希望bootstrap的官方库能接受你的修改，你就可以在GitHub上发起一个pull request。当然，对方是否接受你的pull request就不一定了。

### Gitee
Gitee也提供免费的Git仓库。此外，还集成了代码质量检测、项目演示等功能。对于团队协作开发，Gitee还提供了项目管理、代码托管、文档管理的服务，5人以下小团队免费。
>Gitee的免费版本也提供私有库功能，只是有5人的成员上限。

- 既关联GitHub和Gitee，git给远程库的默认名称是`origin`，如果有多个远程库，我们需要用不同的名称来标识不同的远程库。
- 以`learngit`本地库为例，先删除已关联的`origin`的远程库：`git remote rm origin`
- 关联GitHub`git remote add github git@github.com:michaelliao/learngit.git`，这里的仓库叫`github`而不是`origin`
- 再关联Gitee：`git remote add gitee git@gitee.com:liaoxuefeng/learngit.git`
- `git remote -v`：查看信息
- `git push github master`、`git push gitee master`

## 自定义Git
- `git config`用来配置的
- 之前有username、email
- 设置颜色：`git config --global color.ui true`

### 忽略特殊文件
- 有时候我们必须要将某些文件放到Git工作目录中，但是不能提交它们，比如保存了数据库密码的配置文件，每次`git status`都会显示`Untracked files ...`
- 可以在Git工作区的根目录创建一个特殊的`.gitignore`文件，然后将要忽略的文件名填进去，Git会自动忽略
>`.gitignore`文件本身应该提交给Git管理，这样可以确保所有人在同一项目下都使用相同的`.gitignore`文件。

- 不用从头写`.gitignore`文件，GitHub已经为我们准备了各种配置文件，只用组合一下就行：[配置文件设置](https://github.com/github/gitignore)
- 忽略文件原则：
	1. 忽略操作系统自动生成的文件，比如缩略图等
	2. 忽略编译生成的中间文件、可执行文件等（就是一个文件是通过另一个文件自动生成的，例如java编译产生的`.class`文件）
	3. 忽略自己带有敏感信息的配置文件，例如存放口令的配置文件

- 假设在Windows下进行Python开发，Windows会自动在有图片的目录下生成隐藏的缩略图文件，如果有自定义目录，目录下就会有`Desktop.ini`文件，因此需要忽略Windows自动生成的垃圾文件：
```plain
# Windows:
Thumbs.db
ehthumbs.db
Desktop.ini
```
- 然后，继续忽略Python编译产生的`.pyc`、`.pyo`、`dist`等文件或目录：
```plain
# Python:
*.py[cod]
*.so
*.egg
*.egg-info
dist
build
```

- 加上你自己定义的文件，最终得到一个完整的`.gitignore`文件，内容如下：
```plain
# Windows:
Thumbs.db
ehthumbs.db
Desktop.ini

# Python:
*.py[cod]
*.so
*.egg
*.egg-info
dist
build

# My configurations:
db.ini
deploy_key_rsa
```
- 最后将`.gitignore`提交到Git就可以了，当然检验`.gitignore`的标准是`git status`命令是不是说`working directory clean`。
- 使用windows在资源管理器里创建`.gitignore`文件可能会提示必须输入文件名，如果在文本编辑器里“保存”或者"另存为"就可以了
- 如果我们想添加一个文件到Git，但是添加不了，原因是被`.gitignore`忽略了。
```plain
$ git add App.class
The following paths are ignored by one of your .gitignore files:
App.class
Use -f if you really want to add them.
```

- 如果我们确实想添加该文件，可以用`-f`强制添加到Git：`git add -f App.class`
- 或者可以看看`.gitignore`哪里写的有问题，需要找出哪个规则写错了，可以用`git check-ignore`命令检查
```plain
$ git check-ignore -v App.class
.gitignore:3:*.class	App.class
```
找到位置后，我们就可以通过修改这条配置来解决问题
```plain
# 排除所有.开头的隐藏文件:
.*
# 排除所有.class文件:
*.class
```
但是我们发现`.*`这个规则把`.gitignore`也排除了，并且`App.class`需要被添加到版本库，但是被`*.class`规则排除了。
```plain
# 排除所有.开头的隐藏文件:
.*
# 排除所有.class文件:
*.class

# 不排除.gitignore和App.class:
!.gitignore
!App.class
```

可以通过[GitIgnore Online Generator](https://michaelliao.github.io/gitignore-online-generator/)在线生成`.gitignore`文件并直接下载。
一个Git仓库也可以有多个`.gitignore`文件，`.gitignore`文件放在哪个目录下，就对哪个目录（包括子目录）起作用。
![[Pasted image 20250325090959.png|500]]

### 配置别名
- 比如将`git status`换成`git st`：`git config --global alias.st status`
```plain
$ git config --global alias.co checkout
$ git config --global alias.ci commit
$ git config --global alias.br branch
```

- 将`git reset HEAD file.txt`换成`git unstage file.txt`：`git config --global alias.unstage 'reset HEAD'`

- 配置一个`git last`，让其显示最后一次提交信息：`$ git config --global alias.last 'log -1'`

- 配置文件时，加上`--global`是针对当前用户起作用的，如果不加，只针对当前仓库起作用
- 配置文件都放在`.git/config`文件中
```plain
$ cat .git/config 
[core]
    repositoryformatversion = 0
    filemode = true
    bare = false
    logallrefupdates = true
    ignorecase = true
    precomposeunicode = true
[remote "origin"]
    url = git@github.com:michaelliao/learngit.git
    fetch = +refs/heads/*:refs/remotes/origin/*
[branch "master"]
    remote = origin
    merge = refs/heads/master
[alias]
    last = log -1
```

- 当前用户的Git配置文件放在用户主目录下的一个隐藏文件`.gitconfig`中：
```plain
$ cat .gitconfig
[alias]
    co = checkout
    ci = commit
    br = branch
    st = status
[user]
    name = Your Name
    email = your@email.com
```
配置别名也可以直接修改这个文件，如果改错了，可以删掉文件重新通过命令配置，或者直接删掉配置文件错误的那一行。

### 搭建Git服务器
- 需要准备一台运行Linux的机器，建议使用Ubuntu或Debian
1. 安装`git`：`sudo apt install git`
2. 创建一个`git`用户，用来运行`git`服务：`sudo adduser git`
3. 创建证书登录：收集所有需要登录的用户的公钥，将所有公钥导入`/home/git/.ssh/authorized_keys`文件里一行一个
4. 初始化Git仓库：选定一个目录作为Git仓库，假定是`/srv/sample.git`，在`/srv`目录下输入命令：`sudo git init --bare sample.git`（这样会创建一个裸仓库，没有工作区，因为服务器上的Git仓库纯粹是为了共享，所以不让用户直接登录到服务器上改工作区，并且服务器上的Git仓库通常都以`.git`结尾）
5. 然后将owner改为`git`：`sudo chown -R git:git sample.git`
6. 禁用shell登录：出于安全，第二步创建的git用户不允许登录shell，这个可以通过编辑`/etc/passwd`文件完成。找到`git:x:1001:1001:,,,:/home/git:/bin/bash`，改为`git:x:1001:1001:,,,:/home/git:/usr/bin/git-shell`，这样，`git`用户可以正常通过ssh使用ssh，但是无法登录shell，因为我们为`git`用户指定的`git-shell`，每次一登陆就会自动退出
7. 克隆远程仓库：
```plain
$ git clone git@server:/srv/sample.git
Cloning into 'sample'...
warning: You appear to have cloned an empty repository.
```

- 管理公钥：如果团队很小，将每个人的公钥收集起来放在服务器的`/home/git/.ssh/authorized_keys`文件里就可以，如果有几百号人，可以用[Gitosis](https://github.com/res0nat0r/gitosis)来管理公钥

- 管理权限：git不支持权限控制（linux是开源的），但是Git支持钩子(hook)，可以在服务器端编写一系列脚本来控制提交等操作，达到权限控制的目的，[Gitolite](https://github.com/sitaramc/gitolite)就是这个工具。


## 使用SourceTree
### 下载
当我们已经可以熟练使用Git后，再使用GUI工具就可以提升效率，SourceTree是其中一个GUI，由[Atlassian](https://www.atlassian.com/)开发的免费Git图形界面工具，可以操作任何Git库。

- 官网下载运行
- 第一次运行时，不知道我们的Git库在哪，如果本地有，可以直接从资源管理器把文件夹拖拽到SourceTree上，就添加了一个本地Git库
- 也可以选择“New”-->“Clone from URL”从远程克隆到本地

### 提交
我们双击`learngit`这个本地库，SourceTree会打开另一个窗口，展示这个Git库的当前所有分支以及文件状态。选择左侧面板的“WORKSPACE”-“File status”，右侧会列出当前已修改的文件（Unstaged files）：![[Pasted image 20250325101943.png]]选中某个文件，该文件就自动添加到“Staged files”，实际上是执行了`git add README.md`命令：![[Pasted image 20250325102004.png]]然后，我们在下方输入Commit描述，点击“Commit”，就完成了一个本地提交：
实际上是执行了`git commit -m "update README.md"`命令。
![[Pasted image 20250325102038.png]]

### 分支
在左侧面板的“BRANCHES”下，列出了当前本地库的所有分支。当前分支会加粗并用○标记。要切换分支，我们只需要选择该分支，例如`master`，然后点击右键，在弹出菜单中选择“Checkout master”，实际上是执行命令`git checkout master`：![[Pasted image 20250325102257.png]]要合并分支，同样选择待合并分支，例如`dev`，然后点击右键，在弹出菜单中选择“Merge dev into master”，实际上是执行命令`git merge dev`：![[Pasted image 20250325102317.png]]
### 推送
在SourceTree的工具栏上，分别有`Pull`和`Push`，分别对应命令`git pull`和`git push`，只需注意本地和远程分支的名称要对应起来。其实就是将敲命令转化为了点击，如果操作失误还是会报错![[Pasted image 20250325102444.png]]
- 常用命令
[git-cheat-sheet](https://liaoxuefeng.com/books/git/conclusion/git-cheat-sheet.pdf)
- 官网
[Git - Reference](https://git-scm.com/docs)




pm2的使用
