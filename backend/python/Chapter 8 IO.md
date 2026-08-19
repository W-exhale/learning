## 文件读写
- 用法和C兼容的
- 磁盘上读写文件的功能由操作系统提供，现代操作系统不允许普通的程序直接操作磁盘。
- 读写文件其实就是请求操作系统打开一个文件对象（文件描述符），然后通过操作系统提供的接口从这个文件对象读取（写入）数据（读写文件），

### 读文件
- 传入文件名和标识符：`f = open('/Users/michael/test.txt', 'r')`（返回一个对象）
- windows中的文件路径是\如果和t等转义字符放一起就会编译失败
`C:\Users\W_exhale\Desktop\test.txt`
- 我们可以有三种方式进行修改：（命令行）
	- 格式化：`f = open(r'C:\Users\W_exhale\Desktop\test.txt', 'r')`
	- 双反斜杠：`f = open('C:\\Users\\W_exhale\\Desktop\\test.txt', 'r')`
	- 使用正斜杠：`f = open('C:/Users/W_exhale/Desktop/test.txt', 'r')`
- 如果文件不存在，`open()`函数会抛出一个`IOError`的错误，并且给出错误码和详细的信息告诉你文件不存在：
```plain
>>> f=open('/Users/michael/notfound.txt', 'r')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
FileNotFoundError: [Errno 2] No such file or directory: '/Users/michael/notfound.txt'
```

- 如果文件打开成功，调用`read()`方法可以一次读取文件的全部内容，Python把内容读到内存，用`str`对象表示：（命令行）
```plain
>>> f.read()
'Hello, world!'
>>> f.close()
```

文件的打开和关闭经常出错（IOError），我们可以用try来保证无论是否出错都会关闭文件
```python
try:
    f = open(r'C:\Users\W_exhale\Desktop\test.txt', 'r')
    print(f.read())
finally:
    if f:
        f.close()
```

- 简化，使代码更简洁，而且自动调用`f.close()`方法
```python
with open(r'C:\Users\W_exhale\Desktop\test.txt', 'r') as f:
    print(f.read())
```

- 调用`read()`会一次性读取文件的全部内容，而且是通过内存调用，如果有10G内存会炸，保险起见我们最好使用`read(size)`方法，每次最多读取size个字节的内容。调用`readline()`可以每次读一行的内容，调用`readlines()`一次读取所有内容并按行返回list
- 文件小使用`read()`；不确定文件大小，反复调用`read(size)`；配置文件，调用`readlines()`
```python
for line in f.readlines():
    print(line.strip()) # 把末尾的'\n'删掉
```


- file-like Object：类似open()函数返回的这种有个`read()`（或者说`write()`、`close()`）方法的对象（除了file外，还可以是内存的自己流，网络流，自定义流）。file-like Object不要求从特定类继承，写一个`read()`方法就行
- `StringIO`就是在内存中创建的file-like Object，常用作临时缓冲，在内存中操作字符串流
```python
import io

# StringIO 示例
string_io = io.StringIO("Hello, world!")
print(string_io.read())  # 输出: Hello, world!

# BytesIO 示例
bytes_io = io.BytesIO(b"Binary data")
print(bytes_io.read())  # 输出: b'Binary data'

```

### 二进制文件
- 上面都是默认读取文本文件，并且是UTF-8编码的文本文件。
- 如果要读取二进制文件，比如说图片、视频等等，用`rb`模式打开即可
```plain
>>> f = open('/Users/michael/test.jpg', 'rb')
>>> f.read()
b'\xff\xd8\xff\xe1\x00\x18Exif\x00\x00...' # 十六进制表示的字节
```

### 字符编码
要读取非UTF-8编码的文本文件，需要给`open()`函数传入`encoding`参数，例如，我们如果要读取GBK编码文件：
```plain
>>> f = open('/Users/michael/gbk.txt', 'r', encoding='gbk')
>>> f.read()
'测试'
```
- 如果我们遇到`UnicodeDecodeError`，可能是在文本文件中夹杂了一些非法编码的字符。此时，open函数可以接收一个errors参数，表示如果遇到编码错误后如何处理
```plain
>>> f = open('/Users/michael/gbk.txt', 'r', encoding='gbk', errors='ignore')
```

### 写文件
- open()函数传入`w`或`wb`
```plain
>>> f = open('/Users/michael/test.txt', 'w')
>>> f.write('Hello, world!')
>>> f.close()
```

- 我们可以反复调用`write()`来写入文件，但是务必要调用`f.close()`来关闭文件
- 写入文件时，数据不是立刻写入磁盘，而是放到内存缓存，空闲的时候再慢慢写入
- 只有调用`close()`方法时，操作系统才能保证把没有写入的数据全部写入磁盘，不使用close会发生数据丢失的情况
- 综上，最好使用with
```python
with open('/Users/michael/test.txt', 'w') as f:
    f.write('Hello, world!')
```

- 注意：使用w时，如果文件已经存在会直接覆盖（相当于删掉后重新写入一个文件），如果我们要接着写应该使用追加模式`'a'`

## StringIO和BytesIO
### StringIO
很多时候，数据读写不一定是文件，也可以是内存
- StringIO就是在内存中读写`str`
- 要将str写入`StringIO`，我们需要先创建一个`StringIO`，然后像文件一样写入即可

![Pasted image 20250312092613](images/Pasted%20image%2020250312092613.png)

- `getvalue()`用来获得写入后的`str`
- 要读取`StringIO`，可以用一个`str`初始化`StringIO`，然后像文件一样读取：
```plain
>>> from io import StringIO
>>> f = StringIO('Hello!\nHi!\nGoodbye!')
>>> while True:
...     s = f.readline()
...     if s == '':
...         break
...     print(s.strip())
...
Hello!
Hi!
Goodbye!
```

### BytesIO
- 操作二进制数据，在内存中读写`bytes`
```plain
>>> from io import BytesIO
>>> f = BytesIO()
>>> f.write('中文'.encode('utf-8'))
6
>>> print(f.getvalue())
b'\xe4\xb8\xad\xe6\x96\x87'
```

- 注意：写入的不是`str`，而是经过UTF-8编码的`bytes`。
- 也可以初始化后然后进行读写
```plain
>>> from io import BytesIO
>>> f = BytesIO(b'\xe4\xb8\xad\xe6\x96\x87')
>>> f.read()
b'\xe4\xb8\xad\xe6\x96\x87'
```

## 操作文件和目录
### 查看系统
- 命令行可以使用cmd命令，python程序中如果要执行这些目录和文件操作，可以使用python内置的os模块来直接调用操作系统提供的接口函数
```plain
>>> import os
>>> os.name # 操作系统类型
'posix'
```
- 如果是posix，说明系统是linux、unix或macOS，如果是nt，就是windows系统
- 使用`uname()`函数获取详细的系统信息（Windows中没有）：
```plain
>>> os.uname()
posix.uname_result(sysname='Darwin', nodename='MichaelMacPro.local', release='14.3.0', version='Darwin Kernel Version 14.3.0: Mon Mar 23 11:59:05 PDT 2015; root:xnu-2782.20.48~5/RELEASE_X86_64', machine='x86_64')
```
所以os的某些函数跟操作系统有关
![Pasted image 20250312101822](images/Pasted%20image%2020250312101822.png)

### 环境变量
- 操作系统中定义的环境变量，全部保存在`os.environ`这个变量中，可以直接查看
![Pasted image 20250312102131](images/Pasted%20image%2020250312102131.png)

- 使用`os.environ.get('key')`获取某个环境变量的值
![Pasted image 20250312102346](images/Pasted%20image%2020250312102346.png)

### 操作文件和目录
- 一部分放在os中，一部分放在`os.path`中
```python
# 查看当前目录的绝对路径
>>> os.path.abspath('.')
'/Users/michael'
# 在某个目录下创建一个新目录，先要写出新目录的完成路径
>>> os.path.join('/Users/michael', 'testdir')
'/Users/michael/testdir'
# 创建一个目录：
>>>os.mkdir('/Users/michael/testdir')
# 删掉一个目录
>>> os.rmdir('/Users/michael/testdir')
```

- 将两个路径合成一个时，不能直接拼接字符串，而要通过`os.path.join()`，可以正确处理不同操作系统的路径分隔符
- Linux/Unix/Mac
```plain
part-1/part-2
```
- Windows
```plain
part-1\part-2
```

- 拆分路径时，也是如此，需要通过`os.path.split()`函数，后一部分总是最后级别的目录或文件名
```plain
>>> os.path.split('/Users/michael/testdir/file.txt')
('/Users/michael/testdir', 'file.txt')
```

- 通过`os.path.splitext()`，我们可以得到文件扩展名：
```plain
>>> os.path.splitext('/path/to/file.txt')
('/path/to/file', '.txt')
```

- 注意：合并拆分的函数不要求目录和文件真实存在，只是对字符串进行操作。

- 假设当前目录下有一个`test.txt`文件
```python
# 对文件重命名
>>> os.rename('test.txt', 'test.py')
# 删掉文件：
>>> os.remove('test.py')
```

- 注意：复制文件的函数在os模块中不存在，因为复制文件并非由操作系统提供的系统调用，理论上说，我们通过上一节的读写文件可以完成文件复制，但是很复杂

- `shutil`模块提供了`copyfile()`的函数，还有很多其他的可以当作os的补充函数

### 过滤文件
- 列出当前目录下的所有目录
```
>>> [x for x in os.listdir('.') if os.path.isdir(x)]
['.lein', '.local', '.m2', '.npm', '.ssh', '.Trash', '.vim', 'Applications', 'Desktop', ...]
```

- 选出所有.py文件
```plain
>>> [x for x in os.listdir('.') if os.path.isfile(x) and os.path.splitext(x)[1]=='.py']
['apis.py', 'config.py', 'models.py', 'pymonitor.py', 'test_db.py', 'urls.py', 'wsgiapp.py']
```

## 序列化
### 介绍
- 在程序运行的过程中，所有的变量都存在内存中，例如定义一个dict：
```python
d = dict(name='Bob', age=20, score=88)
```
- 假如把name换成Bill，一旦程序结束，变量所占用的内存就会被操作系统全部回收。如果没有把修改后的`Bill`存储到磁盘上，重新下载运行程序，变量又被初始化为`Bob`

- 序列化：变量从内存中变成可存储或传输的过程，在python中叫picking，在其他语言可能叫serialization，marshalling，flattening等等

- 序列化之后可以将序列化后的内容写入磁盘或者通过网络传输到别的机器上
- 将变量从序列化对象重新读到内存里叫做反序列化，即unpicking，python提供`pickle`实现序列化

- 将一个对象序列化并写入文件
![Pasted image 20250312110958](images/Pasted%20image%2020250312110958.png)

`pickle.dumps()`方法将任意对象序列化成一个`bytes`，然后可以将`bytes`写入文件，或者用`pickle.dump()`直接把对象序列化后写入一个file-立刻 Object：
```plain
>>> f = open('dump.txt', 'wb')
>>> pickle.dump(d, f)
>>> f.close()
```
- 但是`dump.txt`文件里面是一堆乱七八糟的内容，是python保存的对象内部信息

- 我们如果要把对象从磁盘读到内存，可以先将内容读到`bytes`，然后用pickle.loads()方法反序列化出对象，也可以用`pickle.load()`方法从一个`file-like Object`中直接反序列化出对象。
```plain
>>> f = open('dump.txt', 'rb')
>>> d = pickle.load(f)
>>> f.close()
>>> d
{'age': 20, 'score': 88, 'name': 'Bob'}
```
可以看到和原来变量一样的内容，但是要注意这个变量和原来的变量是毫不相关的，只是内容相同

- 缺点：只能用于python，不同版本python可能还不兼容，所以只能用序列化保存不重要的数据

- pickle是Python的序列化工具，有一定的限制
	- 可序列化：基本数据类型，实现了`__reduce__`、`__getstate__`方法的自定义对象
	- 不能序列化：打开的文件句柄、线程、进程、匿名函数(`lambda`)、非全局定义的函数
### JSON
- 如果我们要在不同的编程语言之间传递对象，就必须把对象序列化为标准格式
- 例如XML，但是更好的方法是序列化为JSON，因为json表示出来就是一个字符串，可以被所有语言读取，也可以更方便地存储到磁盘或者通过网络传输。
- json不仅是标准格式，而且比XML更快，也可以直接在Web页面中读取

- json表示的对象就是标准的JavaScript语言对象，json和python内置的数据类型对应
![Pasted image 20250312112447](images/Pasted%20image%2020250312112447.png)

- python内置的json提供了python对象到json格式的转换
```plain
>>> import json
>>> d = dict(name='Bob', age=20, score=88)
>>> json.dumps(d)
'{"age": 20, "score": 88, "name": "Bob"}'
```

- `dumps()`方法返回一个`str`，内容是标准的json。`dump()`可以直接把json写入`file-like Object`

- 要把json反序列化为python对象，用`loads()`或者`load()`方法，前者将json的字符串反序列化，后者从`file-like Object`中读取字符串并反序列化：
```plain
>>> json_str = '{"age": 20, "score": 88, "name": "Bob"}'
>>> json.loads(json_str)
{'age': 20, 'score': 88, 'name': 'Bob'} #转回python
```

- json标准规定json编码是utf-8，所以python的str和json字符串之间可以很好的转换

### json进阶
python的`dict`对象可以直接序列化为json的`{}`，我们大部分时候都更喜欢用class表示对象，定义`Student`类然后序列化
```python
import json

class Student(object):
    def __init__(self, name, age, score):
        self.name = name
        self.age = age
        self.score = score

s = Student('Bob', 20, 88)
print(json.dumps(s))
```

运行后报错了，原因是`Student`对象不是一个可序列化为json的对象![Pasted image 20250312113852](images/Pasted%20image%2020250312113852.png)
- 我们可以发现dumps除了obj参数外还提供了很多可选参数![Pasted image 20250312114134](images/Pasted%20image%2020250312114134.png)
- 我们可以通过这些可选参数来定制json序列化，上面的代码会报错是因为默认情况下dumps方法不知道怎么将`Student`实例变成一个json的`{}`对象
- 可选参数`default`将任意一个对象变成一个可序列为json的对象，我们只用为`Student`专门写一个转换函数，再把函数传进去就行
```python
def student2dict(student):
    return {
        'name': student.name,
        'age': student.age,
        'score': student.score
    }
```
- 这样Student实例首先被`student2dict()`函数转换为`dict`，然后再被顺利序列化为json
```plain
>>> print(json.dumps(s, default=student2dict))
{"age": 20, "name": "Bob", "score": 88}
```

- 如果遇到一个`Teacher`类的实例，还是不能序列化json
```python
print(json.dumps(s, default=lambda obj: obj.__dict__))
```

因为通常`class`的实例都有一个`__dict__`属性，它就是一个`dict`，用来存储实例变量。也有少数例外，比如定义了`__slots__`的class。

- 如果我们要把json反序列化为一个`Student`对象实例，`loads()`方法首先转换出一个`dict`对象，然后将传入的`object_hook`函数转换成`Student`实例

```python
def dict2student(d):
    return Student(d['name'], d['age'], d['score'])
```
```plain
>>> json_str = '{"age": 20, "score": 88, "name": "Bob"}'
>>> print(json.loads(json_str, object_hook=dict2student))
<__main__.Student object at 0x10cd3c190>
```
打印出来的就是反序列化的`Student`实例对象

对中文进行JSON序列化时，`json.dumps()`提供了一个`ensure_ascii`参数，观察该参数对结果的影响：

```python
import json

obj = dict(name='小明', age=20)
s = json.dumps(obj, ensure_ascii=True)
print(s)
```

最后打印出来的小明是十六进制表示的，`\u`表示unicode码点![Pasted image 20250312124215](images/Pasted%20image%2020250312124215.png)
`\u` 是 JSON 用来表示 Unicode 字符的转义形式，常用于表示非 ASCII 字符，比如中文、日文、韩文等。通过解析工具或代码可以轻松还原为可读文本。
在 JSON 传输中，有些环境可能对非 ASCII 字符（如中文）支持不好，因此使用 Unicode 转义序列可以确保兼容性。