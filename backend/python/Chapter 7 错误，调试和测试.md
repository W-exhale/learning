## 错误处理
- 如果发生错误，可以返回一个错误代码，这样就可以快速知道出错的原因。在操作系统提供的调用中，返回错误码十分常见。例如打开文件的函数`open()`成功就返回文件描述符（一个整数），出错时返回`-1`
- 但是使用错误码很不方便，函数本身返回的正常结果会和错误码混在一起
```python
def foo():
    r = some_function()
    if r==(-1):
        return (-1)
    # do something
    return r

def bar():
    r = foo()
    if r==(-1):
        print('Error')
    else:
        pass
```
一旦出错，要一级一级上报，直到给用户输出一个错误信息
### try
```python
try:
    print('try...')
    r = 10 / 0
    print('result:', r)
except ZeroDivisionError as e:
    print('except:', e)
finally:
    print('finally...')
print('END')
```
我们觉得某段代码可能有问题时，就可以使用try来运行这段代码，如果执行出错，后面的代码也不会继续执行，而是直接跳转到错误处理代码即except，执行完except后如果有finally就执行
```plain
try...
except: division by zero
finally...
END
```
- 改成2
```plain
try...
result: 5
finally...
END
```

- 可以用多个except来捕获不同类型的错误
```python
try:
    print('try...')
    r = 10 / int('a')
    print('result:', r)
except ValueError as e:
    print('ValueError:', e)
except ZeroDivisionError as e:
    print('ZeroDivisionError:', e)
finally:
    print('finally...')
print('END')
```
所有的错误类型都继承自`BaseException`
[Built-in Exceptions — Python 3.13.2 documentation](https://docs.python.org/3/library/exceptions.html#exception-hierarchy)

- 使用except时要注意，如果第一个是父类，第二个是子类，第一个捕获了，第二个就不会了
```python
try:
    foo()
except ValueError as e:
    print('ValueError')
except UnicodeError as e:
    print('UnicodeError')
```
第二个`except`永远也捕获不到`UnicodeError`，因为`UnicodeError`是`ValueError`的子类，如果有，也被第一个`except`给捕获了。

- 不用再每个可能出错的地方都捕获错误，只要在合适的层次捕获即可，因为try...except可以跨越多层调用
### 调用栈
如果错误没有被捕获，它就会一直往上抛，最后被Python解释器捕获，打印一个错误信息，然后程序退出。来看看`err.py`：
```python
# err.py:
def foo(s):
    return 10 / int(s)
def bar(s):
    return foo(s) * 2
def main():
    bar('0')
main()
```
```plain
$ python3 err.py
Traceback (most recent call last):
  File "err.py", line 11, in <module>
    main()
  File "err.py", line 9, in main
    bar('0')
  File "err.py", line 6, in bar
    return foo(s) * 2
  File "err.py", line 3, in foo
    return 10 / int(s)
ZeroDivisionError: division by zero
```
根据错误类型`ZeroDivisionError`，我们判断，`int(s)`本身并没有出错，但是`int(s)`返回`0`，在计算`10 / 0`时出错，至此，找到错误源头。
>出错的时候，一定要分析错误的调用栈信息，才能定位错误的位置。

### 记录错误
- 如果不捕获错误，可以让python解释器打印出错误堆栈，但是同时程序也结束了。如果我们捕获错误，可以将错误堆栈打印出来，再分析错误原因，同时让程序继续执行
- Python内置的`logging`模块可以非常容易地记录错误信息：
```python
import logging

def foo(s):
    return 10 / int(s)

def bar(s):
    return foo(s) * 2

def main():
    try:
        bar('0')
    except Exception as e:
        logging.exception(e)

main()
print('END')
```
这样程序打印完错误后会继续执行，并正常退出
```plain
$ python3 err_logging.py
ERROR:root:division by zero
Traceback (most recent call last):
  File "err_logging.py", line 13, in main
    bar('0')
  File "err_logging.py", line 9, in bar
    return foo(s) * 2
  File "err_logging.py", line 6, in foo
    return 10 / int(s)
ZeroDivisionError: division by zero
END
```
可以通过配置使`logging`把错误记录到日志文件里
### 抛出错误
- 异常是一个class，捕获的异常就是捕获到该class的一个实例。所以异常是有意创建并抛出的，我们自己也可以写

- 首先我们需要定义一个错误的class，选择好继承关系，然后用`raise`语句抛出一个错误的实例：
```python
class FooError(ValueError):
    pass
def foo(s):
    n = int(s)
    if n==0:
        raise FooError('invalid value: %s' % s)
    return 10 / n
foo('0')
```
```plain
$ python3 err_raise.py 
Traceback (most recent call last):
  File "err_throw.py", line 11, in <module>
    foo('0')
  File "err_throw.py", line 8, in foo
    raise FooError('invalid value: %s' % s)
__main__.FooError: invalid value: 0
```
- 一般都是使用python内置的异常类型（ValueError、TypeError）
- 使用`raise`抛出
- 下面是另一种异常抛出方式（很常见）
```python
def foo(s):
    n = int(s)
    if n==0:
        raise ValueError('invalid value: %s' % s)
    return 10 / n

def bar():
    try:
        foo('0')
    except ValueError as e:
        print('ValueError!')
        raise

bar()
```
使用except捕获之后又使用了raise将错误抛出了
```python
ValueError!
Traceback (most recent call last):
  File "<filename>", line 13, in <module>
    bar()
  File "<filename>", line 10, in bar
    foo('0')
  File "<filename>", line 4, in foo
    raise ValueError('invalid value: %s' % s)
ValueError: invalid value: 0
```
这种方式就是虽然通过except捕获到了错误也打印出来了，但是在这之后函数就不知道要怎么处理了，最好的方式就是往上抛，抛到了foo，然后碰到了raise将错误抛出

- raise如果不带参数就会将当前错误原样抛出，此外，如果在except中raise一个Error，还可以把一种类型的错误转化为另一种类型
```python
try:
    10 / 0
except ZeroDivisionError:
    raise ValueError('input error!')
```
但是不要将IOError换成毫不相干的ValueError

## 调试
### 使用print打印
把可能有问题的变量打印出来
```python
def foo(s):
    n = int(s)
    print('>>> n = %d' % n)
    return 10 / n

def main():
    foo('0')

main()
```
```plain
$ python err.py
>>> n = 0
Traceback (most recent call last):
  ...
ZeroDivisionError: integer division or modulo by zero
```

### 使用断言
```python
def foo(s):
    n = int(s)
    assert n != 0, 'n is zero!' #表示n如果不符合n!=0这个条件，不然报AssertionError
    return 10 / n

def main():
    foo('0')
```
```plain
$ python err.py
Traceback (most recent call last):
  ...
AssertionError: n is zero!
```
- 但是到处都是assert也比print好不到哪去，但是可以输入-O关掉assert
```plain
$ python -O err.py
Traceback (most recent call last):
  ...
ZeroDivisionError: division by zero
```
>断言的开关“-O”是英文大写字母O，不是数字0。

### logging
将print换成logging，logging不会抛出错误，可以输出到文件
```python
import logging

s = '0'
n = int(s)
logging.info('n = %d' % n)
print(10 / n)
```
- 这样我们发现除了`ZeroDivisionError`没有任何信息
- 可以在`import logging`后添加一行配置
```python
import logging
logging.basicConfig(level=logging.INFO)
```
```plain
$ python err.py
INFO:root:n = 0
Traceback (most recent call last):
  File "err.py", line 8, in <module>
    print(10 / n)
ZeroDivisionError: division by zero
```

- logging允许我们指定记录信息的级别，有debug，info，warning，error等几个级别，当我们指定`level=INFO`时，`logging.debug`就不起作用。这样，我们就可以放心输出不同级别的信息，不用删除，最后统一控制输出哪个级别的信息

- logging可以通过简单配置将一条语句同时输出到不同的地方，例如console、文件

### pdb
还可以启动python的调试器pdb，让程序以单步方式运行，可以随时查看运行状态
```python
# err.py
s = '0'
n = int(s)
print(10 / n)
```
然后启动
```plain
$ python -m pdb err.py
> /Users/michael/Github/learn-python3/samples/debug/err.py(2)<module>()
-> s = '0'
```
使用`-m pdb`启动后，pdb会定位到下一步要执行的代码`-> s = '0'`。可以输入`l`查看代码
```plain
(Pdb) l
  1     # err.py
  2  -> s = '0'
  3     n = int(s)
  4     print(10 / n)
```
用n单步执行代码：
```plain
(Pdb) n
> /Users/michael/Github/learn-python3/samples/debug/err.py(3)<module>()
-> n = int(s)
(Pdb) n
> /Users/michael/Github/learn-python3/samples/debug/err.py(4)<module>()
-> print(10 / n)
```
- 输入`p 变量名`查看变量：
```plain
(Pdb) p s
'0'
(Pdb) p n
0
```
- `q`结束调试，退出程序
![[Pasted image 20250306162319.png]]


### pdb.set_trace()
这个方法也是用的pdb，但是不用单步执行，只需要`import pdb`，然后再可能出错的地方放一个`pdb.set_trace()`，就可以设置一个断点
```python
# err.py
import pdb

s = '0'
n = int(s)
pdb.set_trace() # 运行到这里会自动暂停
print(10 / n)
```
运行代码程序到断点处会自动暂停并进入pdb调试环境，可以用命令`p`查看变量或者用命令`c`继续运行：
```plain
$ python err.py 
> /Users/michael/Github/learn-python3/samples/debug/err.py(7)<module>()
-> print(10 / n)
(Pdb) p n
0
(Pdb) c
Traceback (most recent call last):
  File "err.py", line 7, in <module>
    print(10 / n)
ZeroDivisionError: division by zero
```

### IDE
使用ide！

- 但是logging才是终极

## 单元测试
### 介绍
- 测试驱动开发：TDD：Test-Driven Development
- 单元测试：对一个模块、一个函数或者一个类来进行正确性检验的测试工作
- 例如对于函数`abs()`：
1. 输入正数，比如`1`、`1.2`、`0.99`，期待返回值与输入相同；
2. 输入负数，比如`-1`、`-1.2`、`-0.99`，期待返回值与输入相反；
3. 输入`0`，期待返回`0`；
4. 输入非数值类型，比如`None`、`[]`、`{}`，期待抛出`TypeError`。
将上面的测试用例放到一个测试模块里就是一个完整的单元测试

### 案例展示
编写一个`Dict`类，这个类的行为和`dict`一致，但是可以通过属性来访问：
```plain
>>> d = Dict(a=1, b=2)
>>> d['a']
1
>>> d.a
1
```
- `mydict.py`
```python
class Dict(dict):
    def __init__(self, **kw):
        super().__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value
```

- 使用单元测试需要引入`Python`自带的`unittest`，下面是`mydict_test.py`
```python
import unittest

from mydict import Dict

class TestDict(unittest.TestCase):#从这个类继承，以test开头的方法是测试方法，否则不是，测试的时候不会被执行
    def test_init(self):
        d = Dict(a=1, b='test')
        self.assertEqual(d.a, 1)
        self.assertEqual(d.b, 'test')
        self.assertTrue(isinstance(d, dict))

    def test_key(self):
        d = Dict()
        d['key'] = 'value'
        self.assertEqual(d.key, 'value')

    def test_attr(self):
        d = Dict()
        d.key = 'value'
        self.assertTrue('key' in d)
        self.assertEqual(d['key'], 'value')

    def test_keyerror(self):
        d = Dict()
        with self.assertRaises(KeyError):
            value = d['empty']

    def test_attrerror(self):
        d = Dict()
        with self.assertRaises(AttributeError):
            value = d.empty
```
`unittest.TestCase`提供了很多内置的条件判断，我们调用这些方法就可以断言输入答案是不是我们想要的
- 判断是否是期待的值
```python
self.assertEqual(abs(-1), 1) # 断言函数返回的结果与1相等
```
- 判断是否是期待的Error，例如通过`d['empty']`访问不存在的key时，断言会抛出`KeyError`：
```python
with self.assertRaises(KeyError):
    value = d['empty']
```
在python中，`with`语句用于确保某个操作（如文件操作、网络连接、数据库连接）发生后清理工作被自动执行，通常和上下文管理器(context manager)一起使用，
在上面的例子用它用于捕捉异常，将该断言作为上下文管理器来执行，监控是否出现对应的异常，比try...except更简便
如果使用后者
```python
try:
    value = d['empty']
except KeyError:
    print("KeyError occurred!")
```

### 运行单元测试
1. 在`mydict_test.py`的最后加上
```python
if __name__ == '__main__':
    unittest.main()
```
- 之后在命令行输入下面的内容
```plain
$ python mydict_test.py
```
2. 或者在命令行`-m unittest`直接运行单元测试
```plain
$ python -m unittest mydict_test
.....
----------------------------------------------------------------------
Ran 5 tests in 0.000s

OK
```
这种可以一次批量运行很多单元测试

### setUp与tearDown
- 这两种方法分别在调用一个测试方法的前后分别被执行
- 作用：假如我们的测试需要启动一个数据库，这是就可以在setUp()方法中连接数据库，在`tearDown()`中关闭数据库，这样就不用在每个测试方法中重复相同的代码
```python
class TestDict(unittest.TestCase):
    def setUp(self):
        print('setUp...')

    def tearDown(self):
        print('tearDown...')
```
### 使用
```python
import unittest
class Student(object):
    def __init__(self, name, score):
        self.name = name
        self.score = score
    def get_grade(self):
        if self.score > 100 or self.score < 0:
            raise ValueError('invalid value: %d' % self.score)
        if self.score >= 80:
            return 'A'
        if self.score >= 60:
            return 'B'
        return 'C'
class TestStudent(unittest.TestCase):
    def test_80_to_100(self):
        s1 = Student('Bart', 80)
        s2 = Student('Lisa', 100)
        self.assertEqual(s1.get_grade(), 'A')
        self.assertEqual(s2.get_grade(), 'A')
    def test_60_to_80(self):
        s1 = Student('Bart', 60)
        s2 = Student('Lisa', 79)
        self.assertEqual(s1.get_grade(), 'B')
        self.assertEqual(s2.get_grade(), 'B')
    def test_0_to_60(self):
        s1 = Student('Bart', 0)
        s2 = Student('Lisa', 59)
        self.assertEqual(s1.get_grade(), 'C')
        self.assertEqual(s2.get_grade(), 'C')
    def test_invalid(self):
        s1 = Student('Bart', -1)
        s2 = Student('Lisa', 101)
        with self.assertRaises(ValueError):
            s1.get_grade()
        with self.assertRaises(ValueError):
            s2.get_grade()
if __name__ == '__main__':
    unittest.main()
```
## 文档测试（doctest）
[re模块](https://docs.python.org/3/library/re.html)带了很多示例代码：
```plain
>>> import re
>>> m = re.search('(?<=abc)def', 'abcdef')
>>> m.group(0)
'def'
```
结果与文档中的示例代码显示的一致。
这些代码与其他说明可以写在注释中，然后，由一些工具来自动生成文档。
- 可以自动执行写在注释中的代码
当我们编写注释时，如果写上这样的注释：

```python
def abs(n):
    '''
    Function to get absolute value of number.
    
    Example:
    
    >>> abs(1)
    1
    >>> abs(-1)
    1
    >>> abs(0)
    0
    '''
    return n if n >= 0 else (-n)
```

Python内置的“文档测试”（doctest）模块可以直接提取注释中的代码并执行测试。
doctest严格按照Python交互式命令行的输入和输出来判断测试结果是否正确。只有测试异常的时候，可以用`...`表示中间一大段烦人的输出。

用doctest来测试上次编写的`Dict`类：

```python
# mydict2.py
class Dict(dict):
    '''
    Simple dict but also support access as x.y style.

    >>> d1 = Dict()
    >>> d1['x'] = 100
    >>> d1.x
    100
    >>> d1.y = 200
    >>> d1['y']
    200
    >>> d2 = Dict(a=1, b=2, c='3')
    >>> d2.c
    '3'
    >>> d2['empty']
    Traceback (most recent call last):
        ...
    KeyError: 'empty'
    >>> d2.empty
    Traceback (most recent call last):
        ...
    AttributeError: 'Dict' object has no attribute 'empty'
    '''
    def __init__(self, **kw):
        super(Dict, self).__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

if __name__=='__main__':
    import doctest
    doctest.testmod()
```
什么输出也没有。这说明我们编写的doctest运行都是正确的。如果程序有问题，比如把`__getattr__()`方法注释掉，再运行就会报错：
```plain
$ python mydict2.py
**********************************************************************
File "/Users/michael/Github/learn-python3/samples/debug/mydict2.py", line 10, in __main__.Dict
Failed example:
    d1.x
Exception raised:
    Traceback (most recent call last):
      ...
    AttributeError: 'Dict' object has no attribute 'x'
**********************************************************************
File "/Users/michael/Github/learn-python3/samples/debug/mydict2.py", line 16, in __main__.Dict
Failed example:
    d2.c
Exception raised:
    Traceback (most recent call last):
      ...
    AttributeError: 'Dict' object has no attribute 'c'
**********************************************************************
1 items had failures:
   2 of   9 in __main__.Dict
***Test Failed*** 2 failures.
```
注意到最后3行代码。当模块正常导入时，doctest不会被执行。只有在命令行直接运行时，才执行doctest。所以，不必担心doctest会在非测试环境下执行。