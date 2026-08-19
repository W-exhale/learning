- 我们会将很多函数分组，分别放到不同的文件里，在python中，一个.py文件就称为一个模块（Module）
- 好处：
	1. 提高代码的可维护性
	2. 避免函数名和变量名冲突，但是要注意不要于内置函数名字冲突
- 包：Package
- 每个Package下都会有一个`__init__.py`的文件，这个文件必须存在，否则，Python会把这个目录当成普通目录，而不是一个包
- 模块名：`mycompany.utils`或`mycompany.web.utils`等

>注意：自己创建模块时要注意命名，不能和Python自带的模块名称冲突。例如，系统自带了sys模块，自己的模块就不可命名为`sys.py`，否则将无法导入系统自带的sys模块。

模块名：不要使用中文、特殊字符
命名时要看系统中是否已经存在该模块：在python交互环境中执行`import abc`，如果有就说明系统中有

## 使用模块
### 介绍
- 以python内建的sys模块为例，编写一个hello的模块
```python
#!/usr/bin/env python3 可以让hello.py这个文件直接在Unix/Linux/Mac上运行
# -*- coding: utf-8 -*- 表示.py文件本身使用标准UTF-8编码

' a test module '#模块的文档注释

__author__ = 'Michael Liao' #作者

import sys

def test():
    args = sys.argv #获得命令行参数
    if len(args)==1:
        print('Hello, world!')
    elif len(args)==2:
        print('Hello, %s!' % args[1])
    else:
        print('Too many arguments!')

if __name__=='__main__':
    test()
```
上面是Python模块的标准文件模板

- 导入sys模块后，就有了sys变量指向该模块，通过sys这个变量就可以访问sys模块的所有功能
- sys模块有一个argv变量，使用list存储了命令行所有参数，argv至少有一个元素，这个元素是该.py文件的名称：
1. 运行`python3 hello.py`获得的`sys.argv`就是`['hello.py']`
2. 运行`python3 hello.py Michael`获得的`sys.argv`就是`['hello.py', 'Michael']`

```python
if __name__=='__main__':
    test()
```
- `__name__`：
	- 每个Python模块都有一个特殊的内置变量`__name__`、
	- 当模块被直接运行时，`__name__`的值为`__main__`
	- 当模块作为导入模块使用时，`__name__`的值为模块的名字（不加扩展名的文件名）
- 上面代码的主要作用是区分直接运行还是被导入
- 假如说我们进入交互环境使用`import hello`，就不会输出helloworld！再调用`hello.test()`时，才会输出`Hello,World!`

### 作用域
- public：`abc`、`x123`、`PI`、....
- private：
	- 特殊变量：`__xxx__`、`__author__`、`__name__`、还有像hello模块定义的文档注释也可以用特殊变量`__doc__`访问，我们自己的变量一般不要用这种，这种可以直接访问
	- 普通：`_xxx`、`__xxx`
- private函数和变量“不应该”被直接引用，而不是不能被直接引用，因为Python并没有一种方法可以完全限制访问private函数或变量
```python
def _private_1(name):
    return 'Hello, %s' % name

def _private_2(name):
    return 'Hi, %s' % name

def greeting(name):
    if len(name) > 3:
        return _private_1(name)
    else:
        return _private_2(name)
```
## 安装第三方模块
### 介绍
- python中的第三方模块通过包管理工具pip完成
- 如果是Mac或者Linux，可以跳过安装pip这个步骤
- 如果是windows，在安装python时可以设置安装`pip`、`Add python.exe to Path`，安装好后在cmd里输入pip就可以知道有没有下载了，如果没有，就重新运行python的安装程序添加pip

>注意：Mac或Linux上有可能并存Python 3.x和Python 2.x，因此对应的pip命令是`pip3`。

- 假如说我们需要安装一个第三方库——Python Imaging Library（一个非常强大的处理图像的工具库），不过，PIL目前只支持到Python 2.7，并且有年头没有更新了，因此，基于PIL的Pillow项目开发非常活跃，并且支持最新的Python 3。

- 一般来说，第三方库都会在Python官方的[pypi.python.org](https://pypi.python.org/)网站注册，要安装一个第三方库，必须先知道该库的名称，可以在官网或者pypi上搜，例如Pillow的名称就叫Pillow，所以`pip install Pillow`即可

### 安装常用模块
- Pillow，MySQL驱动程序，Web框架Flask，科学计算Numpy等。
- 用pip一个一个安装十分费时费力，还要考虑兼容性，可以直接使用[Anaconda](https://www.anaconda.com/)，这是一个基于Python的数据处理和科学计算平台，内置了很多有用的第三方库。
- 可以从上面的官网下载GUI安装包，下载后直接安装，Anaconda会把系统Path中的python指向自己自带的Python，并且，Anaconda安装的第三方模块会安装在Anaconda自己的路径下，不影响系统已经安装的Python目录
![Pasted image 20250304205851](images/Pasted%20image%2020250304205851.png)
可以尝试使用`import numpy`等已安装的第三方模块

### 模块搜索路径
当我们试图加载一个模块时，Python会在指定的路径下搜索对应的.py文件，如果找不到，就会报错：

```plain
>>> import mymodule
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ImportError: No module named mymodule
```

- 默认情况下，Python解释器会搜索当前目录、所有已安装的内置模块和第三方模块，搜索路径存放在`sys`模块的`path`变量中：![Pasted image 20250304210248](images/Pasted%20image%2020250304210248.png)
- 如果要添加自己的搜索目录
	1. 修改sys.path：`sys.path.append('/Users/michael/my_py_scripts')`，这种方法在运行时修改，运行结束后失效
	2. 设置环境变量：`PYTHONPATH`，该环境变量的内容会被自动添加到模块搜索路径中。
		- 注意：只需要添加我们自己的搜索路径，Python本身的搜索路径不受影响