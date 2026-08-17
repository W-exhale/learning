
## 切片（slice）
- 当我们想从一个list里面取一部分数据得到一个新list，一般的方法：
	1. 使用list下标
	2. 使用遍历
- 很麻烦，使用切片就会很方便
- 假设一个list为：`L=list(range(100))`（0-99的list，数据类型转换），0可以省略
	- 前十个数：`L[:10]`
	- 后十个数：`L[-10:]`
	- 前十个数，每两个取一个：`L[0:10:2]`
	- 所有数每五个取一个：L\[::5\]
	- 复制：`L[:]`
- tuple也可以
- 字符串也可以，得出来还是字符串
- 步长默认为1，表示正向遍历，如果为-1，则是反向遍历，常用于字符串反转
## 迭代（Iteration）
- 也就是for...in
- python的迭代可以用在很多可迭代的对象（list，tuple，dict，字符串，...）上，java的foreach只适用于数组

- 使用dict
```python
d = {'a': 1, 'b': 2, 'c': 3}
for key in d:
    print(key)
-键值都要
for key, value in d:
    print(key,value)
```
- 字符串
```python
for ch in 'ABC':
     print(ch)
```

- 判断是否是可迭代对象（即是否是`Iterable`类型）
```python
>>> from collections.abc import Iterable
>>> isinstance('abc', Iterable) # str是否可迭代
True
>>> isinstance([1,2,3], Iterable) # list是否可迭代
True
>>> isinstance(123, Iterable) # 整数是否可迭代
False
```

- 将list的下标和值都输出
```python
>>> for i, value in enumerate(['A', 'B', 'C']):
...     print(i, value)
...
0 A
1 B
2 C
```

- 输出坐标
```python
>>> for x, y in [(1, 1), (2, 4), (3, 9)]:
...     print(x, y)
...
1 1
2 4
3 9
```


## 列表生成式（List Comprehensions）
- 一般来说我们要生成1-15的list可以使用`list(range(1,16))`
- 但是如果我们需要它们平方的列表，可能就需要用到循环
```python
L=list(range(1,16))
 for x in range(1, 16):
	L.append(x * x)
```

- 如果使用列表生成式，就可以很简洁的完成
`[x * x for x in range(1,16)]`
for前面的是列表里的内容

- 也可以筛选后放入列表，仅选出偶数的平方：`[x * x for x in range(1, 16) if x % 2 == 0]`，但是if放在前面必须要加else，放前面表示选择，放后面表示筛选不能加else
```python
>>> [x if x % 2 == 0 else -x for x in range(1, 11)]
[-1, 2, -3, 4, -5, 6, -7, 8, -9, 10]
```
- 或者使用两层循环实现两个list的全组合
```python
>>> [m + n for m in 'ABC' for n in 'XYZ']
['AX', 'AY', 'AZ', 'BX', 'BY', 'BZ', 'CX', 'CY', 'CZ']
```

- 列出当前目录的所有文件和目录名
```python
>>> import os # 导入os模块，模块的概念后面讲到
>>> [d for d in os.listdir('.')] # os.listdir可以列出文件和目录
['.emacs.d', '.ssh', '.Trash', 'Adlm', 'Applications', 'Desktop', 'Documents', 'Downloads', 'Library', 'Movies', 'Music', 'Pictures', 'Public', 'VirtualBox VMs', 'Workspace', 'XCode']
```

- 使用两个变量生成list
```python
>>> d = {'x': 'A', 'y': 'B', 'z': 'C' }
>>> [k + '=' + v for k, v in d.items()]
['y=B', 'x=A', 'z=C']
```

- 将list中所有的字符串变成小写
```python
>>> L = ['Hello', 'World', 'IBM', 'Apple']
>>> [s.lower() for s in L]
['hello', 'world', 'ibm', 'apple']
```

- 二维数组提取
```python
L = [('Bob', 75), ('Adam', 92), ('Bart', 66), ('Lisa', 88)]
names = [item[0] for item in L]
print(names)  # 输出：['Bob', 'Adam', 'Bart', 'Lisa']
```

- 转为字典
```python
L = [('Bob', 75), ('Adam', 92), ('Bart', 66), ('Lisa', 88)]
result_dict = {item[0]: item[1] for item in L}
print(result_dict)  # 输出：{'Bob': 75, 'Adam': 92, 'Bart': 66, 'Lisa': 88}
```
## 生成器（generator）
### 介绍
- 一边循环一边计算的机制，（本质上是一种算法），和列表生成器类似，将`[]`改为`()`即为generator
- 假如说我们要知道前100万个数的平方和，那么如果使用list comprehensions生成完整的含100万个数的list，会十分浪费资源。
- list可以直接打印，但是generator不行
```python
>>> L = [x * x for x in range(10)]
>>> L
[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
>>> g = (x * x for x in range(10))
>>> g
<generator object <genexpr> at 0x1022ef630>
```

- g的打印方式
	1. next()获得g的下一个返回值`next(g)`，直到最后一个元素，没有更多元素时抛出StopIteration（很少用）
	2. 使用for循环，不用关心StopIteration的错误
```python
>>> g = (x * x for x in range(10))
>>> for n in g:
...     print(n)
```

### 定义generator function
- 定义generator的另一种方法（一个函数定义中包含yield关键字），返回一个generator
```python
def fib(max):#这就是一个generator函数
    n, a, b = 0, 0, 1
    while n < max:
        yield b #将这一行换成print(b)就会打印斐波那契
        a, b = b, a + b
        n = n + 1
    return 'done'
```

用for循环获取值：
```plain
>>> for n in fib(6):
...     print(n)
...
1
1
2
3
5
```
用for循环调用generator时，拿不到return语句的返回值。如果要拿到返回值，就需要捕获StopIteration错误，返回值包含在`StopIteration`的value中
```plain
>>> g = fib(6)
>>> while True:
...     try:
...         x = next(g)
...         print('g:', x)
...     except StopIteration as e:
...         print('Generator return value:', e.value)
...         break
...
g: 1
g: 1
g: 2
g: 3
g: 5
g: 8
Generator return value: done #函数走完了用next就会报错
```

- 与普通函数不同，generator调用next()的时候执行，遇到yield语句返回，再次执行从上次返回的yield语句处继续执行，如下依次返回数字1，3，5
```python
def odd():
    print('step 1')
    yield 1
    print('step 2')
    yield(3)
    print('step 3')
    yield(5)
```

- 调用
	1. 生成一个generator对象：`o = odd()`
	2. 使用next()函数获得下一个值：`next(o)`
```plain
>>> o = odd()
>>> next(o)
step 1
1
>>> next(o)
step 2
3
>>> next(o)
step 3
5
>>> next(o)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration
```

- 原理：在for循环的过程中不断计算出下一个元素并在适当条件结束for循环

### 十分巧妙的杨辉三角
- 根据杨辉三角来源，最旁边还有隐形的0，每一行都是由上一行相加得来，第二行的上一行应该会有四个数，第三行上一行六个...分别由前一行前面后面分别加0相加得到
```python
def triangles():
    row=[1]
    while True:
        yield row
        row=[x+y for x,y in zip([0]+row,row+[0])]
```

## 迭代器
- 可以被next()调用并不断返回下一个值的对象就是迭代器：`Iterator`
- 使用`isinstance()`判断是否是`Iterator`对象
```plain
>>> from collections.abc import Iterator
>>> isinstance((x for x in range(10)), Iterator)
True
>>> isinstance([], Iterator)
False
>>> isinstance({}, Iterator)
False
>>> isinstance('abc', Iterator)
False
```

生成器都是`Iterator`对象，但`list`、`dict`、`str`虽然是`Iterable`但不是`Iterator`

- python的`Iterator`对象表示的是一个数据流，`Iterator`对象可以被next()函数调用并不断返回下一个数据直到抛出`StopIteration`错误。我们不知道Iterator的长度，只有使用的时候它才会计算，可以表示一个无限大的数据流（全体自然数）。而list是永远不可能存储全体自然数的。

1. 凡是可作用于`for`循环的对象都是`Iterable`类型；
2. 凡是可作用于`next()`函数的对象都是`Iterator`类型，它们表示一个惰性计算的序列；
3. 集合数据类型如`list`、`dict`、`str`等是`Iterable`但不是`Iterator`，不过可以通过`iter()`函数获得一个`Iterator`对象。
4. Python的`for`循环本质上就是通过不断调用`next()`函数实现的，例如：
```python
for x in [1, 2, 3, 4, 5]:
    pass
```
实际上完全等价于：
```python
# 首先获得Iterator对象:
it = iter([1, 2, 3, 4, 5])
# 循环:
while True:
    try:
        # 获得下一个值:
        x = next(it)
    except StopIteration:
        # 遇到StopIteration就退出循环
        break
```
