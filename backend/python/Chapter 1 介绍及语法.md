## 对比C语言
- 运行
	- C语言：可执行文件是已经编译好的机器语言，也就是可以直接点击exe文件运行，很快![Pasted image 20250220232725](images/Pasted%20image%2020250220232725.png)
	- python：不会生成可执行文件，每次运行都要翻译一遍源码。通过解释器翻译成字节码文件，然后再由PVM将字节码进行翻译并执行，比较慢![Pasted image 20250220233247](images/Pasted%20image%2020250220233247.png)
- 代码不能加密，要给别人用只能发源码
- 应用
	1. 可以做日常任务，比如自动备份你的MP3；
	2. 可以做网站，很多著名的网站包括YouTube就是Python写的；
	3. 可以做网络游戏的后台，很多在线游戏的后台都是Python开发的。
- Python当然也有不能干的事情，
	- 比如写操作系统，这个只能用C语言写；
	- 写手机应用，只能用Swift/Objective-C（针对iPhone）和Java（针对Android）；
	- 写3D游戏，最好用C或C++。

## python 解释器
- 在官网下完python3.x就自带官方版本的解释器：CPython，在cmd里运行python就是启动CPython
- 其他不常用

## python 交互模式

命令行输入`python`进入到Python交互模式，它的提示符是`>>>`。
- `exit()`退出

Python交互模式的代码是输入一行，执行一行，Python交互模式主要是为了调试Python代码用的

![Pasted image 20241110183324](images/Pasted%20image%2020241110183324.png)

- 命令行运行.py文件
![Pasted image 20241110184229](images/Pasted%20image%2020241110184229.png)


## 输出

- `print()`函数也可以接受多个字符串，用逗号“,”隔开，就可以连成一串输出：

```python
>>> print('The quick brown fox', 'jumps over', 'the lazy dog')
- 输出：
- The quick brown fox jumps over the lazy dog
```

`print()`会依次打印每个字符串，遇到逗号“,”会输出一个空格，因此，输出的字符串是这样拼起来的：

`print()`也可以打印整数，或者计算结果：

```python
>>> print(300)
300
>>> print(100 + 200)
300
```

## 输入

![Pasted image 20241110185212](images/Pasted%20image%2020241110185212.png)


- *input返回是string*，所以在用数字的时候，需要使用数字类型转换
```python
s = input('birth: ')
birth = int(s)
if birth < 2000:
    print('00前')
else:
    print('00后')
```
## 各种语句
### 判断
- 语句的最后要加冒号
```python
# print absolute value of an integer:
a = 100
if a >= 0:#注意这里有一个冒号
    print(a)#if下面缩进的全部都执行（连续的）
else:#注意这里有一个冒号
    print(-a)
```

- 大小写敏感
可以用elif，（就是 else if，不用冒号）

```python
age = 20
if age >= 6:
    print('teenager')
elif age >= 18:
    print('adult')
else:
    print('kid')
```

`if`判断条件还可以简写，比如写：

```python
if x:
    print('True')
```

只要`x`是非零数值、非空字符串、非空list等，就判断为`True`，否则为`False`。

-match语句（类似switch）
```python
score = 'B'
match score:
    case 'A':
        print('score is A.')
    case 'B':
        print('score is B.')
    case 'C':
        print('score is C.')
    case _: # _表示匹配到其他任何情况
        print('score is ???.')
```

`match`语句除了可以匹配简单的单个值外，还可以匹配多个值、匹配一定范围，并且把匹配后的值绑定到变量：

```python
age = 15

match age:
    case x if x < 10:
        print(f'< 10 years old: {x}')
    case 10:
        print('10 years old.')
    case 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18:
        print('11~18 years old.')
    case 19:
        print('19 years old.')
    case _:
        print('not sure.')
```

第一个`case x if x < 10`表示当`age < 10`成立时匹配，且赋值给变量`x`，
第二个`case 10`仅匹配单个值，
第三个`case 11|12|...|18`能匹配多个值，用`|`分隔。（单个`|`，java是`||`）
第四个表示其他

- 匹配列表
- 还可以匹配多个值、匹配一定范围，全部匹配成功则选择，并且能够把匹配后的值赋给变量，变量不用进行匹配，直接赋值
```python
args = ['gcc', 'hello.c', 'world.c']
# args = ['clean']
# args = ['gcc']

match args:
    # 如果仅出现gcc，报错:
    case ['gcc']:
        print('gcc: missing source file(s).')
    # 出现gcc，且至少指定了一个文件:
    case ['gcc', file1, *files]:
        print('gcc compile: ' + file1 + ', ' + ', '.join(files))
        #', '.join(files)表示将后面的合成一个字符串输出，用，隔开
    # 仅出现clean:
    case ['clean']:
        print('clean':
        print('invalid command.'kk)
    case _:
        print('invalid command.')
```

第一个`case ['gcc']`表示列表仅有`'gcc'`一个字符串，没有变量名，不符；

第二个`case ['gcc', file1, *files]`表示列表第一个字符串是`'gcc'`，第二个字符串绑定到变量`file1`，剩下的赋给`*files`（符号`*`的作用将在[函数的参数](https://liaoxuefeng.com/books/python/function/parameter/index.html)中讲解），它实际上表示至少指定一个文件；

### 循环
Python的循环有两种，一种是for...in循环，依次把list或tuple中的每个元素迭代出来，类似java中的foreach：

```python
names = ['Michael', 'Bob', 'Tracy']
for name in names:
    print(name)
```

执行这段代码，会依次打印`names`的每一个元素：

```plain
Michael
Bob
Tracy
```

比如我们想计算1-10的整数之和，可以用一个`sum`变量做累加：

```python
sum = 0
for x in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
    sum = sum + x
print(sum)
```

如果要计算1-100的整数之和，从1写到100有点困难，幸好Python提供一个`range()`函数，可以生成一个整数序列，再通过`list()`函数可以转换为list。比如`range(5)`生成的序列是从0开始小于5的整数：

```plain
>>> list(range(5))
[0, 1, 2, 3, 4]
```

`range(101)`就可以生成0-100的整数序列，计算如下：

```python
sum = 0
for x in range(101):
    sum = sum + x
print(sum)
```

- while
while循环，只要条件满足，就不断循环，条件不满足时退出循环。比如我们要计算100以内所有奇数之和，可以用while循环实现：

```python
sum = 0
n = 99
while n > 0:
    sum = sum + n
    n = n - 2
print(sum)
```

break；
continue；
同其他语言
## 数据类型

- 允许数字中间_分隔
写成`10_000_000_000`和`10000000000`是完全一样的。十六进制数也可以写成`0xa1b2_c3d4`。


- 字符串
使用`''`或者`""`
如果`''`也是字符就可以用`""`括起来

既包含`''`又包含`""`可以用转义字符

如果字符串内部有很多换行，用`\n`写在一行里不好阅读，为了简化，Python允许用`'''...'''`的格式表示多行内容，可以自己试试（在命令行中会自己出现...，在文本编辑器中不需要）：

```python
>>> print('''line1
... line2
... line3''')

line1
line2
line3
```
`...`是提示符，不是代码的一部分

如果写成程序并存为`.py`文件，就是：

```python
print('''line1
line2
line3''')
```

多行字符串`'''...'''`还可以在前面加上`r`使用，这样`\n`就会失去作用：
```python
print(r'''hello,\n
world''')
```

- 布尔值：True 和 False

and，or，not  运算

空值：None



动态语言：
`a = 123`
静态语言：
`int a = 123;`

- 常量
`PI`

python中有两种除法
1. /除法结果是浮点数
2. //除法的结果是整数


```python
n = 123
f = 456.789
s1 = 'Hello, world'
s2 = 'Hello, \'Adam\''
s3 = r'Hello, "Bart"' #格式化就不用转义字符了
s4 = r'''Hello,
Bob!'''

-输出
123
456.789
Hello, world
Hello, 'Adam'
Hello, "Bart"
Hello,
Bob!
```

- Python的*整数没有大小限制*，而某些语言的整数根据其存储长度是有大小限制的，例如Java对32位整数的范围限制在`-2147483648`-`2147483647`。
- Python的*浮点数*也*没有大小限制*，但是超出一定范围就直接表示为`inf`（无限大）。
## 字符串和编码

Unicode标准最常用的是UCS-16编码，用两个字节表示一个字符（如果要用到非常偏僻的字符，就需要4个字节）。现代操作系统和大多数编程语言都直接支持Unicode。

字母`A`用ASCII编码是十进制的`65`，二进制的`01000001`；

字符`0`用ASCII编码是十进制的`48`，二进制的`00110000`；

汉字`中`已经超出了ASCII编码的范围，用Unicode编码是十进制的`20013`，二进制的`01001110 00101101`。

如果把ASCII编码的`A`用Unicode编码，只需要在前面补0就可以，因此，`A`的Unicode编码是`00000000 01000001`。

- UTF-8
如果统一成Unicode编码，乱码问题从此消失了。但是，如果你写的文本基本上全部是英文的话，用Unicode编码比ASCII编码需要多一倍的存储空间，在存储和传输上就十分不划算。

所以为了节约又出现了把Unicode编码转化为“可变长编码”的`UTF-8`编码。UTF-8编码把一个Unicode字符根据不同的数字大小编码成1-6个字节，常用的英文字母被编码成1个字节，汉字通常是3个字节，只有很生僻的字符才会被编码成4-6个字节。UTF-8包括ASCII，所以可以兼容ASCII的程序：

|字符|ASCII |UTF-8|Unicode|
|------|--------|---------|----|
|A|01000001  |01000001    |00000000 01000001|
|中|  |11100100 10111000 10101101    |01001110 00101101|

在计算机内存中，统一使用Unicode编码，当需要保存到硬盘或者需要传输的时候，就转换为UTF-8编码。

用记事本编辑的时候，从文件读取的UTF-8字符被转换为Unicode字符到内存里，编辑完成后，保存的时候再把Unicode转换为UTF-8保存到文件：
![Pasted image 20241110192432](images/Pasted%20image%2020241110192432.png)

在最新的Python 3版本中，字符串是以Unicode编码的，也就是说，Python的字符串支持多语言

对于单个字符的编码，Python提供了`ord()`函数获取字符的整数表示，`chr()`函数把编码转换为对应的字符：

```python
>>> ord('A')
65
>>> ord('中')
20013
>>> chr(66)
'B'
>>> chr(25991)
'文'
```

如果知道字符的整数编码，可以用十六进制这么写：

```python
>>> '\u4e2d\u6587'
'中文'
```

由于Python的字符串类型在内存中以Unicode表示，一个字符对应若干个字节。如果要在网络上传输，或者保存到磁盘上，就需要转换为以字节为单位的`bytes`。

Python对`bytes`类型的数据用带`b`前缀的单引号或双引号表示：

```python
x = b'ABC'
```

以Unicode表示的`str`通过`encode()`方法可以编码为指定的`bytes`，例如：

```python
>>> 'ABC'.encode('ascii')
b'ABC'
>>> '中文'.encode('utf-8')
b'\xe4\xb8\xad\xe6\x96\x87'
>>> '中文'.encode('ascii')

Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
UnicodeEncodeError: 'ascii' codec can't encode characters in position 0-1: ordinal not in range(128)
```

纯英文的`str`可以用`ASCII`编码为`bytes`，内容是一样的，含有中文的`str`可以用`UTF-8`编码为`bytes`。中文编码的范围超过了`ASCII`编码的范围，Python会报错。

如果我们从网络或磁盘上读取了字节流，那么读到的数据就是`bytes`。要把`bytes`变为`str`，就需要用`decode()`方法：

```python
>>> b'ABC'.decode('ascii')
'ABC'
>>> b'\xe4\xb8\xad\xe6\x96\x87'.decode('utf-8')
'中文'
```

- 如果`bytes`中只有一小部分无效的字节，可以传入`errors='ignore'`忽略错误的字节：

```plain
>>> b'\xe4\xb8\xad\xff'.decode('utf-8', errors='ignore')
'中'
```


要计算`str`包含多少个字符，可以用`len()`函数：

```python
>>> len('ABC')
3
>>> len('中文')
2
```

`len()`函数计算的是`str`的字符数，如果换成`bytes`，`len()`函数就计算字节数：

```python
>>> len(b'ABC')
3
>>> len(b'\xe4\xb8\xad\xe6\x96\x87')
6
>>> len('中文'.encode('utf-8'))
6
```

1个中文字符经过UTF-8编码后通常会占用3个字节，而1个英文字符只占用1个字节。

由于Python源代码也是一个文本文件，所以，当源代码中包含中文的时候，在保存源代码时，就需要指定保存为UTF-8编码。
当Python解释器读取源代码时，为了让它按UTF-8编码读取，我们通常在文件开头写上这两行：

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
```

第一行注释是为了告诉Linux/OS X系统，这是一个Python可执行程序，Windows系统会忽略这个注释；

第二行注释是为了告诉Python解释器，按照UTF-8编码读取源代码，否则，你在源代码中写的中文输出可能会有乱码。

如果`.py`文件本身使用UTF-8编码，并且也申明了`# -*- coding: utf-8 -*-`，打开命令提示符测试就可以正常显示中文

## 格式化
在Python中，格式化用`%`实现，%就表示要格式化
```python
>>> 'Hello, %s' % 'world'
'Hello, world'
>>> 'Hi, %s, you have $%d.' % ('Michael', 1000000)
'Hi, Michael, you have $1000000.'
```

![Pasted image 20241110193943](images/Pasted%20image%2020241110193943.png)

用%时，可以用`%%` 来表示一个%

- format()，用数字编号，冒号后面是精度条件等等，用中括号括起来
![Pasted image 20241110194315](images/Pasted%20image%2020241110194315.png)

将前面的字符串当成一个整体，直接.加函数

最后一种格式化字符串的方法是使用以`f`开头的字符串，称之为`f-string`，它和普通字符串不同之处在于，字符串如果包含`{xxx}`，就会以对应的变量替换，自己检测，不用注明：

```python
>>> r = 2.5
>>> s = 3.14 * r ** #19.62
>>> print(f'The area of a circle with radius {r} is {s:.2f}')
The area of a circle with radius 2.5 is 19.62
```

用花括号来表示格式化

## List
- 比较像数组
可以用`len`来获取list元素的个数

![屏幕截图 2024-11-10 195219](images/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE%202024-11-10%20195219.png)

用负数也可以表示，但是不能到-4，不然也会越界

- 函数
- `append()`，`insert()`，`pop()`，删除
![Pasted image 20241110195453](images/Pasted%20image%2020241110195453.png)

list里面的数据类型可以不同

```python
>>> p = ['asp', 'php']
>>> s = ['python', 'java', p, 'scheme']
```

要拿到`'php'`可以写`p[1]`或者`s[2][1]`，因此`s`可以看成是一个二维数组，类似的还有三维、四维……数组，不过很少用到。

如果一个list中一个元素也没有，就是一个空的list，它的长度为0：

```python
>>> L = []
>>> len(L)
0
```

## tuple
- 元组
一旦初始化就不能更改

如果要定义一个空的tuple，可以写成`()`：
```plain
>>> t = ()
>>> t
()
```

但是，要定义一个只有1个元素的tuple，如果你这么定义：

```plain
>>> t = (1)
>>> t
1
```
相当于是 t = 1（括号表示小括号）

所以，只有1个元素的tuple定义时必须加一个逗号`,`，来消除歧义：

```plain
>>> t = (1,)
>>> t
(1,)
```

Python在显示只有1个元素的tuple时，也会加一个逗号`,`，以免你误解成数学计算意义上的括号。


- “可变”的tuple
tuple所谓的“不变”是说，tuple的每个元素，指向永远不变。即指向`'a'`，就不能改成指向`'b'`，指向一个list，就不能改成指向其他对象，但是list可以变
```python
>>> t = ('a', 'b', ['A', 'B'])
>>> t[2][0] = 'X'
>>> t[2][1] = 'Y'
>>> t
('a', 'b', ['X', 'Y'])
```

## 使用dict和set
Python内置了字典：dict的支持，dict全称dictionary，类似其他语言中的map，使用键-值（key-value）存储，具有极快的查找速度。

假设要根据同学的名字查找对应的成绩，如果用list实现，需要两个list：

```python
names = ['Michael', 'Bob', 'Tracy']
scores = [95, 75, 85]
```

给定一个名字，要查找对应的成绩，就先要在names中找到对应的位置，再从scores取出对应的成绩，list越长，耗时越长。

如果用dict实现，只需要一个“名字”-“成绩”的对照表，直接根据名字查找成绩，无论这个表有多大，查找速度都不会变慢。名字就是“键”，成绩就是“值”

```plain
>>> d = {'Michael': 95, 'Bob': 75, 'Tracy': 85}
>>> d['Michael']
95
```

list的查询方式：把字典从第一页往后翻，直到找到我们想要的字为止
- 变量d就类似于一个数据字典
dict的查询方式：先在字典的索引表里（比如部首表）查这个字对应的页码，然后直接翻到该页，找到这个字。无论找哪个字，这种查找速度都非常快，不会随着字典大小的增加而变慢。

把数据放入dict的方法，除了初始化时指定外，还可以通过key放入：

```plain
>>> d['Adam'] = 67
>>> d['Adam']
67
```

由于一个key只能对应一个value，新值会覆盖旧值：

```plain
>>> d['Jack'] = 90
>>> d['Jack']
90
>>> d['Jack'] = 88
>>> d['Jack']
88
```

如果key不存在，dict就会报错：

```plain
>>> d['Thomas']
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
KeyError: 'Thomas'
```

- 判断key是否存在
1. 通过`in`判断key是否存在：
```plain
>>> 'Thomas' in d
False
```

1. 通过dict提供的`get()`方法，如果key不存在，返回`None`，或者自己指定的value（比如说下面的-1）：
```plain
>>> d.get('Thomas')
>>> d.get('Thomas', -1)
-1
```
注意：返回`None`的时候Python的交互环境不显示结果。

- 删除一个键值：`pop(key)`：

```plain
>>> d.pop('Bob')
75
>>> d
{'Michael': 95, 'Tracy': 85}
```

- 注意，dict内部存放的顺序和key放入的顺序是没有关系的。

- 与list相比：
1. 查找和插入的速度极快，不会随着key的增加而变慢；
2. 需要占用大量的内存，内存浪费多。

- dict是用空间换时间
- dict通过key计算位置，这种算法是哈希算法（Hash）
- 在Python中，字符串、整数等都是唯一的值，作为key。而list不唯一，就不能作为key

- set类似没有value的key组合，特点是集合中没有重复的值，也是没有顺序
- 创建set：
1. 用`{x,y,z,...}`列出每个元素：
```plain
>>> s = {1, 2, 3}#这种方法就不能传list
>>> s
{1, 2, 3}
```
2. 使用set可以用一个list，作为输入，但是不能两个，因为key是唯一的：
```plain
>>> s = set([1, 2, 3])
>>> s
{1, 2, 3}
```
- 注意，传入的参数`[1, 2, 3]`是一个list，而显示的`{1, 2, 3}`只是告诉你这个set内部有1，2，3这3个元素，也是没有顺序
- 重复元素在set中自动被过滤：
```plain
>>> s = {1, 1, 2, 2, 3, 3}
>>> s
{1, 2, 3}
```
- set的方法使用
1. 通过`add(key)`方法可以添加元素到set中，可以重复添加，但不会有效果：
```plain
>>> s.add(4)
>>> s
{1, 2, 3, 4}
>>> s.add(4)
>>> s
{1, 2, 3, 4}
```
2. 通过`remove(key)`方法可以删除元素：
```plain
>>> s.remove(4)
>>> s
{1, 2, 3}
```
3. set可以看成数学意义上的无序和无重复元素的集合，因此，两个set可以做数学意义上的交集、并集等操作：
```plain
>>> s1 = {1, 2, 3}
>>> s2 = {2, 3, 4}
>>> s1 & s2
{2, 3}
>>> s1 | s2
{1, 2, 3, 4}
```
## 函数
### 定义函数
- 定义函数
```python
def my_abs(x):
#使用def语句创建函数，my_abs是函数名，后面是参数，要记得加:
    if x >= 0:
        return x#要注意缩进，用return返回
    else:
        return -x

print(my_abs(-99))
```
- 如果没有`return`语句，函数执行完毕后也会返回结果，只是结果为`None`。`return None`可以简写为`return`。

- 在Python交互环境中定义函数时，注意Python会出现`...`的提示。函数定义结束后需要按两次回车重新回到`>>>`提示符下：
![Pasted image 20241110204344](images/Pasted%20image%2020241110204344.png)

- 如果`my_abs()`的函数定义在`abstest.py`文件中，在交互模式中需要使用`from abstest import my_abs`来导入`my_abs()`函数，注意`abstest`是文件名（不含`.py`扩展名）：
```
>>>from abstest import my_abs                     
>>>my_abs(-9)                                     
9         
```
- 返回多个值
比如在游戏中经常需要从一个点移动到另一个点，给出坐标、位移和角度，就可以计算出新的坐标：
```python
import math #导包，使用数学函数
def move(x, y, step, angle=0):
    nx = x + step * math.cos(angle)
    ny = y - step * math.sin(angle)
    return nx, ny
```
```plain
>>> x, y = move(100, 100, 60, math.pi / 6)
>>> print(x, y)
151.96152422706632 70.0
```
但实际上Python函数返回的单一值：
```plain
>>> r = move(100, 100, 60, math.pi / 6)
>>> print(r)
(151.96152422706632, 70.0)
```
- 实际上Python的函数返回多值其实就是返回一个tuple。在语法上，返回一个tuple可以省略括号，而多个变量可以同时接收一个tuple，按位置赋给对应的值。


- 更改函数名字
```python
from operator import add,sub
def a_plus_abs_b(a,b):
    """Return a+abs(b),but without calling abs."""
    if b < 0:
        f = sub#加
    else:
        f = add#减
        return f(a,b)#f就表示上面的函数
a = 1
b = 2
print(f'a + b = {a_plus_abs_b(a,b)}')
```
### pass
- 如果想定义一个什么事也不做的空函数，可以用`pass`语句：
```python
def nop():
    pass
```
- `pass`可以用来作为占位符，比如现在还没想好怎么写函数的代码，就可以先放一个`pass`，让代码能运行起来。（有点像写个`//to do...`的注释）
- `pass`还可以用在其他语句里，比如：
```python
if age >= 18:
    pass
```
缺少了`pass`，代码运行就会有语法错误。

让我们修改一下`my_abs`的定义，对参数类型做检查，只允许整数和浮点数类型的参数。数据类型检查用内置函数`isinstance()`实现：
```python
def my_abs(x):
    if not isinstance(x, (int, float)):#只能是int或float，好像泛型，专门用来检查
        raise TypeError('bad operand type')
    if x >= 0:
        return x
    else:
        return -x
```
- 如果传入错误的参数类型，函数就可以抛出一个错误：
```plain
>>> my_abs('A')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 3, in my_abs
TypeError: bad operand type
```
- 函数名其实就是指向一个函数对象的引用，可以把函数名赋给一个变量，相当于给这个函数起了一个“别名”：
```plain
>>> a = abs # 变量a指向abs函数
>>> a(-1) # 所以也可以通过a调用abs函数
1
```
### 常用函数
- 绝对值`abs()`，只有一个参数。可以直接从Python的官方网站查看[文档](http://docs.python.org/3/library/functions.html#abs)，也可以在交互式命令行通过`help(abs)`查看`abs`函数的帮助信息。
```plain
>>> abs(100)
100
>>> abs(-20)
20
>>> abs(12.34)
12.34
```
- 最大值：`max(1, 2)`
- 数据类型转换：`int()`函数可以把其他数据类型转换为整数：
```plain
>>> int('123')
123
>>> int(12.34)
12
>>> float('12.34')
12.34
>>> str(1.23)
'1.23'
>>> str(100)
'100'
>>> bool(1)
True
>>> bool('')
False
```

## 参数
`*args`是可变参数，args接收的是一个tuple；
`**kw`是关键字参数，kw接收的是一个dict。
可变参数既可以直接传入：`func(1, 2, 3)`，可以直接传list或tuple
关键字参数既可以直接传入：`func(a=1, b=2)`，也可以直接传dict
### 默认参数
计算高次方可以用到默认参数（不变的参数），如下，将n设置为2：

```python
def power(x, n=2):
    s = 1
    while n > 0:
        n = n - 1
        s = s * x
    return s
```
这样，当我们调用`power(5)`时，相当于调用`power(5, 2)`，但是调用非2的数时就要用两个：
```plain
>>> power(5)
25
>>> power(5, 2)
25
```
- 注意：
1. 必选参数在前，默认参数在后，否则Python的解释器会报错
2. 多个参数时，把变化大的参数放前面，变化小的参数放后面。变化小的参数就可以作为默认参数。
3. 默认参数必须指向不变对象
```python
def enroll(name, gender, age=6, city='Beijing'):
    print('name:', name)
    print('gender:', gender)
    print('age:', age)
    print('city:', city)
```
这样，大多数学生注册时只提供必须的两个参数：
```plain
>>> enroll('Sarah', 'F')
name: Sarah
gender: F
age: 6
city: Beijing
```
- 只有与默认参数不符的学生才需要提供额外的信息：
```python
enroll('Bob', 'M', 7)
enroll('Adam', 'M', city='Tianjin')
```

- 定义一个函数，传入一个list，添加一个`END`再返回：
```python
def add_end(L=[]):
    L.append('END')
    return L
```
当你正常调用时，结果似乎正常：
```plain
>>> add_end([1, 2, 3])
[1, 2, 3, 'END']
>>> add_end(['x', 'y', 'z'])
['x', 'y', 'z', 'END']
```
- 使用默认参数调用两次`add_end()`，：
```plain
>>> add_end()
['END', 'END']   //这里没有传参数，直接用的原来的，所以会递增end
>>> add_end()   //相当于用了两次append
['END', 'END', 'END']
```

- 修改方案：我们可以用`None`这个不变对象来实现：
```python
def add_end(L=None):
    if L is None:
        L = []
    L.append('END')
    return L
```
```plain
>>> add_end()
['END']
>>> add_end()
['END']
```
所以，我们在编写程序时，*尽量设计成不变对象*，不要使用上面那种可变的List。
### 可变参
- 使用list或tuple
由于参数个数不确定，我们首先想到可以把a，b，c……作为一个list或tuple传进来，但是不能传0个参数，类似：`calc()`：
```python
def calc(numbers):
    sum = 0
    for n in numbers:
        sum = sum + n * n
    return sum
```
```plain
>>> calc([1, 2, 3]) //list
14
>>> calc((1, 3, 5, 7))  //tuple
84
```
- 使用可变参
加上\*变成可变参数：
```python
def calc(*numbers):
    sum = 0
    for n in numbers:
        sum = sum + n * n
    return sum
```
在函数内部，参数`numbers`接收到的是一个tuple。调用该函数时，可以传入任意个参数，会自动变成tuple，严格以上来说还是一个参数，可以传0个参数：
```plain
>>> calc(1, 2)
5
>>> calc()
0
```
- Python允许你在list或tuple前面加一个`*`号，把list或tuple的元素变成可变参数传进去：
```plain
>>> nums = [1, 2, 3] //传list要加星号
>>> calc(*nums)
14
```
`*nums`表示把`nums`这个list的所有元素作为可变参数传进去。
### 关键字参数
- 普通
关键字参数允许传入0个或任意个含参数名的参数，这些关键字参数在函数内部自动组装为一个dict，一个星号是tuple。两个是dict：
```python
def person(name, age, **kw): //传dict
    print('name:', name, 'age:', age, 'other:', kw)
```
函数`person`除了必选参数`name`和`age`外，还接受关键字参数`kw`。在调用该函数时，可以传大于等于两个参数：
```plain
>>> person('Michael', 30)
name: Michael age: 30 other: {}
```
```plain
>>> person('Bob', 35, city='Beijing')
name: Bob age: 35 other: {'city': 'Beijing'}
>>> person('Adam', 45, gender='M', job='Engineer')
name: Adam age: 45 other: {'gender': 'M', 'job': 'Engineer'}
```

- 命名关键字参数，如下，只接收`city`和`job`作为关键字参数，也就是dict里只有city和job，也必须给值：
```python
def person(name, age, *, city, job): # *（分隔符）后面的参数被视为命名关键字参数。
    print(name, age, city, job)
```
```plain
>>> person('Jack', 24, city='Beijing', job='Engineer')
Jack 24 Beijing Engineer
```
- 注意：
	- 命名关键字必须使用`city='Beijing'`的方式进行调用，
	- 同时也必须输入，不能省略
	- 如果命名关键字参数有默认值，那么调用的时候可以省略

- 可变参数后面跟着的都是命名关键字参数，不用额外的星号
```python
def person(name, age, *args, city, job):
    print(name, age, args, city, job)
```
必选参数、默认参数、可变参数，关键字参数，命名关键字参数
```python
ef f1(a, b, c=0, *args, **kw):
    print('a =', a, 'b =', b, 'c =', c, 'args =', args, 'kw =', kw)

def f2(a, b, c=0, *, d, **kw):
    print('a =', a, 'b =', b, 'c =', c, 'd =', d, 'kw =', kw)

```python
>>> f1(1, 2)
a = 1 b = 2 c = 0 args = () kw = {}
>>> f1(1, 2, c=3)
a = 1 b = 2 c = 3 args = () kw = {}
>>> f1(1, 2, 3, 'a', 'b')
a = 1 b = 2 c = 3 args = ('a', 'b') kw = {}
>>> f1(1, 2, 3, 'a', 'b', x=99)
a = 1 b = 2 c = 3 args = ('a', 'b') kw = {'x': 99}
>>> f2(1, 2, d=99, ext=None)
a = 1 b = 2 c = 0 d = 99 kw = {'ext': None}
```
## 递归函数
- 理论上，所有的递归函数都可以写成循环的方式，但循环的逻辑不如递归清晰。
- 注意
	1. 防止栈溢出：计算机中，函数调用通过栈（stack）实现，每当进入一个函数调用，栈就会加一层栈帧，每当函数返回，栈就会减一层栈帧。由于栈的大小不是无限的，所以，递归调用的次数过多，会导致栈溢出。
	2. 尽量使用尾递归：事实上尾递归和循环的效果是一样的，所以，把循环看成是一种特殊的尾递归函数也是可以的，尾递归就是return本函数，并且return语句不能包含表达式。

编译器或者解释器如果有对尾递归做优化的功能，那么递归本身无论调用多少次，都只占用一个栈帧，不会出现栈溢出的情况。
遗憾的是，大多数编程语言没有针对尾递归做优化，Python解释器也没有做优化，所以改成尾递归方式，也会导致栈溢出。
## 注释
```python
-单行注释
#单行注释
-多行注释
"""
多行
注释
"""
```

