- 函数式编程：Functional Programming
- 一种抽象程度很高的编程范式，纯粹的函数式编程语言编写的函数没有变量，也就是输入是确定的，输出就是确定的（没有副作用）。而允许使用变量的程序设计语言，输出是不固定的（有副作用）。
- 函数式编程特点：允许把函数本身作为参数传入另一个函数，还允许返回一个函数。
- python允许使用变量，不是纯函数式编程语言

## 高阶函数（Higher-order function）
### 介绍
- 变量可以指向函数
```plain
>>> abs
<built-in function abs>
>>> f = abs
>>> f
<built-in function abs>
>>> f(-10)
10
```

- 函数名就是指向函数的变量，abs就是指向一个可以计算绝对值的函数，如果我们将abs指向其他对象，abs就不能使用绝对值功能了
```plain
>>> abs = 10
>>> abs(-10)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'int' object is not callable
```
不过上面的修改是局部的，如果想要全局修改，就要在abs函数的定义模块（`import builtins`）修改，`import builtins;builtins.abs=10`

- 传入函数
- 一个函数可以接收另一个函数作为参数，这种函数就是高阶函数
```python
def add(x, y, f):
    return f(x) + f(y)

print(add(-5, 6, abs))
```
答案为11

### map/reduce
- map和reduce都是python内建的函数
- map()：接收两个参数，一个函数，一个Iterable，map将传入的函数作用于序列的每个元素，最后将结果作为新的Iterator返回
- 举例：假如我们要得到一个列表的平方和
![[Pasted image 20250303112954.png|400]]

```plain
>>> def f(x):
...     return x * x
...
>>> r = map(f, [1, 2, 3, 4, 5, 6, 7, 8, 9])
>>> list(r)
[1, 4, 9, 16, 25, 36, 49, 64, 81]
```

- reduce：将一个函数作用在一个序列（`[x1,x2,x3,..]`）上，这个函数必须接收两个参数，reduce将结果继续和序列的下一个元素做累积运算
```python
reduce(f, [x1, x2, x3, x4]) = f(f(f(x1, x2), x3), x4)
```
- 实现对数列求和（假设没有sum）
```plain
>>> from functools import reduce
>>> def add(x, y):
...     return x + y
...
>>> reduce(add, [1, 3, 5, 7, 9])
25
```

- 实现将str转换为int
```plain
>>> from functools import reduce
>>> def fn(x, y):
...     return x * 10 + y
...
>>> def char2num(s):
...     digits = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}
...     return digits[s]
...
>>> reduce(fn, map(char2num, '13579'))
13579
```

- 整理
```python
from functools import reduce

DIGITS = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}

def str2int(s):
    def fn(x, y):
        return x * 10 + y
    def char2num(s):
        return DIGITS[s]
    return reduce(fn, map(char2num, s))
```

- 使用lambda函数
```python
from functools import reduce

DIGITS = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}

def char2num(s):
    return DIGITS[s]

def str2int(s):
    return reduce(lambda x, y: x * 10 + y, map(char2num, s))
```

```python
def normalize(name):
    single_list = [s.lower() for s in list(name)]
    if single_list[0].islower():
        single_list[0] = single_list[0].upper()
    return ''.join(single_list)
# 测试:
L1 = ['adam', 'LISA', 'barT']
L2 = list(map(normalize, L1))
print(L2)
```

```python
def prod(L):
	def f(x)
		return x * y
	return reduce(f, L)

```

### filter
- python内建的filter函数用于过滤序列
- 接收一个函数和一个序列，和map类似，filter()把传入的函数依次作用于每个元素，但是`filter()`会根据返回值是true还是false决定保留还是丢弃
- 例如，需要删掉一个list中的偶数，保留奇数
```python
def is_odd(n):
    return n % 2 == 1

list(filter(is_odd, [1, 2, 4, 5, 6, 9, 10, 15]))
# 结果: [1, 5, 9, 15]
```
- 删掉一个序列中的空字符串
```python
def not_empty(s):
    return s and s.strip()
#s用于检查当前元素是否为一个非空值（即不是''、None或其他假值），如果是假值，直接返回False，不用调用strip()
#s.strip()会去掉字符串两端的空格。如果去掉之后还有内容就返回该内容，如果全是空格就返回空字符串''(假值，即0)
list(filter(not_empty, ['A', '', 'B', None, 'C', '  ']))
# 结果: ['A', 'B', 'C']
```
- `filter()`函数返回一个`Iterator`，即一个惰性序列，需要使用list函数获得所有结果并返回list
- 计算素数：使用埃氏筛法，
	1. 先列出从2开始的所有自然数，
	2. 取2，它一定是素数，再去掉2的倍数
	3. 取3，去掉3的倍数
	4. ...
	- 筛完后就可以得到所有的素数

1. 构造一个从3开始的奇数序列（这是一个generator，是无限序列）：
```python
def _odd_iter():#初始序列
    n = 1
    while True:
        n = n + 2
        yield n
```
2. 定义一个筛选函数：返回一个匿名函数，
```python
def _not_divisible(n):
    return lambda x: x % n > 0
    #当x % n > 0 时，返回true；<0时返回false
```
3. 定义一个生成器，不断返回下一个素数：
```python
def primes():
	yield 2
	it = _odd_iter() #初始序列，除去偶数，偶数不是素数
	while True:
		n = next(it) #返回序列的第一个数
		yield n
		it = filter(_not_divisible(n), it)#利用filter()不断产生筛选后的新序列
#打印1000以内的素数，我们构造的是无限序列，调用时需要设置退出循环的条件
for n in primes():
	if n < 100:
		print(n)
	else:
		break
```
依次将奇数序列代入`_not_divisible(n)`，过滤掉所有能被n整除的数。
### sorted
- 排序，从小到大
- 对list进行排序
```plain
>>> sorted([36, 5, -12, 9, -21])
[-21, -12, 5, 9, 36]
```
- 也可以接收一个key函数实现自定义排序
```plain
>>> sorted([36, 5, -12, 9, -21], key=abs)
[5, 9, -12, -21, 36]
```
key指定的函数将作用于list的每一个元素上，并根据key函数返回的结果进行排序

- 字符串排序，按照ASCII大小排序
```plain
>>> sorted(['bob', 'about', 'Zoo', 'Credit'])
['Credit', 'Zoo', 'about', 'bob']
```
- 忽略大小写
```plain
>>> sorted(['bob', 'about', 'Zoo', 'Credit'], key=str.lower)
['about', 'bob', 'Credit', 'Zoo']
```
- 反向排序：`reverse=True`
```plain
>>> sorted(['bob', 'about', 'Zoo', 'Credit'], key=str.lower, reverse=True)
['Zoo', 'Credit', 'bob', 'about']
```

- 数组可以根据`List[0]`排序

## 返回函数
### 介绍
- python不仅可以接受函数作为参数，还可以把函数作为结果值返回
- 一般可变参求和
```python
def calc_sum(*args):
    ax = 0
    for n in args:
        ax = ax + n
    return ax
```

- 假如说我们不需要立即直到这个可变参的值，而是之后再用，那么我们就可以返回一个求和函数
```python
def lazy_sum(*args):
    def sum():
        ax = 0
        for n in args:
            ax = ax + n
        return ax
    return sum
>>> f = lazy_sum(1, 3, 5, 7, 9)
>>> f
<function lazy_sum.<locals>.sum at 0x101c6ed90>
```
内部函数sum()可以引用外部函数lazy_sum()的参数和局部变量，当lazy_sum返回sum时，相关参数和变量都保存再返回的函数中，这种方式就叫“闭包（Closure）”

- 调用lazy_sum()时，每次调用都会返回一个新的函数，即使传入相同的参数，如下，f1和f2的调用结果不影响
```plain
>>> f1 = lazy_sum(1, 3, 5, 7, 9)
>>> f2 = lazy_sum(1, 3, 5, 7, 9)
>>> f1==f2
False
```

### 闭包
- 可以看到上面在内部函数使用了args，当一个函数（lazy）返回一个函数（sum）后，lazy的变量还会被新函数引用。
- 注意：返回的函数并没有立刻执行，直到调用`f()`才执行
```python
def count():
    fs = []
    for i in range(1, 4):
        def f():
             return i*i
        fs.append(f)
    return fs

f1, f2, f3 = count()
```
上面每次循环都创建了一个新的f()，最后将创建的三个函数都返回了，但需要注意的是，最后返回的都是9，因为不是立刻执行，而是等3个函数都返回时执行，此时引用的变量i已经变成了3，所以最终结果都是9

>所以，返回闭包时，要注意返回函数中不要引用任何循环变量，或者后续会发生变化的变量

- 如果一定要引用循环变量，需要再创建一个函数，用该函数绑定循环变量当前的值，即使循环变量更改，已经绑定的值不会变
```python
def count():
    def f(j):
        def g():
            return j*j
        return g
    fs = []
    for i in range(1, 4):
        fs.append(f(i)) # f(i)立刻被执行，因此i的当前值被传入f()
    return fs
```
`f(i)`是确定的，可以被计算，类似于用f函数记录了i的值

- 可以使用lambda函数缩短代码
### nonlocal
- 使用闭包，内部函数可以使用外部函数的局部变量，如果只是读取而不进行修改没问题的，但是如果在内部函数对外部函数进行修改，就会出现报错
```python
def inc():
    x = 0
    def fn():
        # 仅读取x的值:
        return x + 1
    return fn

f = inc()
print(f()) # 1
print(f()) # 1
```
```python
def inc():
    x = 0
    def fn():
        # nonlocal x 类似于在内部函数激活x
        x = x + 1
        return x
    return fn
f = inc()
print(f()) # 1
print(f()) # 2
```
如上，报错原因：x作为局部变量没有初始化，所以直接计算x+1不行，如果我们需要对x进行修改，就需要在`fn()`函数内部加一个nonlocal x的声明。加上这个声明后，解释器会把`fn()`的x看作外层函数的局部变量

>使用闭包时，对外层变量赋值前，需要先使用nonlocal声明该变量是不是当前函数的局部变量

## 匿名函数
- 我们传入函数时，有时不需要显式定义函数，直接传入匿名函数会更方便
- 以`map()`函数为例，计算$f(x)=x^2$时，除了定义一个对数进行处理的函数f(x)外还可以直接传入匿名函数
```plain
>>> list(map(lambda x: x * x, [1, 2, 3, 4, 5, 6, 7, 8, 9]))
[1, 4, 9, 16, 25, 36, 49, 64, 81]
```
上面的`lambda x:x * x`实际上就是
```python
def f(x):
    return x * x
```

- 关键字lambda表示匿名函数，冒号前面的x表示函数参数

- 注意：匿名函数只能有一个表达式，不用写return，返回值就是该表达式的结果

- 可以把匿名函数赋值给一个变量，再利用变量来调用该函数：
```plain
>>> f = lambda x: x * x
>>> f
<function <lambda> at 0x101c6ef28>
>>> f(5)
25
```

- 也可以作为返回值返回
```python
def build(x, y):
    return lambda: x * x + y * y
```

- 修改
```python
def is_odd(n):
    return n % 2 == 1
L = list(filter(is_odd, range(1, 20)))
print(L)
```
```python
L = list(filter(lambda n: n % 2 == 1, range(1,20)))
print(L)
```

## 装饰器（Decorator）
### 介绍
- 每个函数对象有一个`__name__`属性，可以拿到函数的名字：
```plain
>>> def now():
...     print('2024-6-1')
...
>>> f = now
>>> f()
2024-6-1
>>> now.__name__
'now'
>>> f.__name__
'now'
```
- 假如我们要增强`now()`函数的功能，比如，在函数调用前后自动打印日志但是不修改`now()`函数的定义，这种在代码运行期间动态增加功能的方式就是“装饰器”

- 本质上decorator是一个返回函数的高阶函数，所以，我们要定义一个能打印日志的decorator
```python
def log(func):
    def wrapper(*args, **kw):
        print('call %s():' % func.__name__)
        return func(*args, **kw)
    return wrapper
```
这是一个decorator，接受一个函数作为参数并返回一个函数。我们要借助Python的@语法，将decorator置于函数的定义处：
```python
@log
def now():
    print('2024-6-1')
```
这样，我们调用now()函数时，不仅会运行`now()`函数本身，还会在运行`now()`函数前打印一行日志
```plain
>>> now()
call now(): #日志
2024-6-1
```
- 将@log放在`now()`函数的定义处，相当于执行了语句`now=log(now)`
- `log()`是一个decorator，返回一个函数，所以原来的`now()`函数仍然存在，只是now指向了一个新的函数log(now)，返回wrapper()函数。
- `wrapper()`函数的参数定义是`(*args, **kw)`，因此，`wrapper()`函数可以接受任意参数的调用，在`wrapper()`函数内，首先打印日志，再紧接着调用原始函数

- 假如decorator本身需要传入参数，那就需要编写一个返回decorator的高阶函数，写出来会更复杂。比如说我们要自定义log的文本
```python
def log(text):
    def decorator(func):
        def wrapper(*args, **kw):
            print('%s %s():' % (text, func.__name__))
            return func(*args, **kw)
        return wrapper
    return decorator
-使用
@log('execute')
def now():
    print('2024-6-1')
-结果
>>> now()
execute now():
2024-6-1
```
- 相当于`now = log('execute')(now)`
- 顺序：首先执行`log(execute)`，返回的是`decorator`函数，再调用`wrapper()`函数，参数是now()

>函数也是对象，有`__name__`等属性，但是经过decorator修饰之后的函数，它们的`__name__`已经变成了`wrapper`
```plain
>>> now.__name__
'wrapper'
```
- 所以为了保持原来的名字不变，需要把原始函数now的`__name__`等属性复制到`wrapper()`函数中，否则依赖函数签名（就是def那一行）的代码执行就会出错

- 不用我们自定义，可以借助python内置的functools.wraps
```python
import functools

def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        print('call %s():' % func.__name__)
        return func(*args, **kw)
    return wrapper
```
- 三层
```python
import functools

def log(text):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            print('%s %s():' % (text, func.__name__))
            return func(*args, **kw)
        return wrapper
    return decorator
```

### 练习
1. 请设计一个decorator，它可作用于任何函数上，并打印该函数的执行时间：
```python
import time, functools

def metric(fn):
    print('%s executed in %s ms' % (fn.__name__, 10.24))
    return fn

# 测试
@metric
def fast(x, y):
    time.sleep(0.0012)
    return x + y;

@metric
def slow(x, y, z):
    time.sleep(0.1234)
    return x * y * z;

f = fast(11, 22)
s = slow(11, 22, 33)
if f != 33:
    print('测试失败!')
elif s != 7986:
    print('测试失败!')
```
- 实现
```python
import time, functools
def metric(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        start_time = time.time() # 记录开始的时间
        result = fn(*args, **kwargs) #执行被装饰的函数
        end_time = time.time() # 记录结束时间
        elapsed_time = (end_time - start_time) * 1000 # 计算执行时间（毫秒）
        print('%s excuted in %.2f ms' % (fn.__name__, elapsed_time))
        return result # 返回函数执行结果
    return wrapper
# 测试
@metric
def fast(x, y):
    time.sleep(0.0012)
    return x + y
@metric
def slow(x, y, z):
    time.sleep(0.1234)
    return x * y * z
f = fast(11, 22)
s = slow(11, 22, 33)
if f != 33:
    print('测试失败!')
elif s != 7986:
    print('测试失败!')
```
2. 请编写一个decorator，能在函数调用的前后打印出`'begin call'`和`'end call'`的日志。再思考一下能否写出一个`@log`的decorator，使它既支持：
```python
@log
def f():
    pass
```
又支持：
```python
@log('execute')
def f():
    pass
```
- 实现：
```python
import functools
def log(arg = None):#1.允许调用者省略该参数 2.作为占位符，就是有参数就用，没有就不用的意思
    #如果直接传入参数
    if callable(arg):
        @functools.wraps(arg)
        def wrapper(*args, **kw):
            print('bengin call:%s' % arg.__name__)
            result = arg(*args, **kw)
            print('end call:...')
            return result
        return wrapper
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args,**kwargs):
            print(f'begin call: {arg}') # 打印参数
            result = func(*args, **kwargs)
            print(f'end call: {arg}')
            return result
        return wrapper
    return decorator
@log
def f1():
    print('f1ing')
@log('execute')
def f2():
    print('f2ing')
f1()
f2()
```
None作值占位符类似pass作语句占位符，在逻辑中经常用（`if arg is None`）来判断是否提供了参数

- 在OOP的设计模式中，decorator被称为装饰模式，OOP的装饰模式需要通过继承和组合来实现，而Python除了能支持OOP的decorator外，直接从语法层次支持decorator。Python的decorator可以用函数实现，也可以用类实现。

## 偏函数（Partial function）
- 由`functools`模块提供，和数学意义上的偏函数不一样
- 我们知道，通过设定参数的默认值，可以降低函数调用的难度。偏函数也可以这样
- `int()`函数可以把字符串转换为整数，仅传入字符串时，int()函数默认按十进制转换
- `int()`还提供base参数设定基数
```plain
>>> int('12345', base=8)
5349
>>> int('12345', 16)
74565
```

- 假设要转换大量的二进制字符串，我们可以设定一个专门的函数，使base=2变成默认参数
```python
def int2(x, base=2):
    return int(x, base)
```

- `functools.partial`可以帮我们创建一个偏函数，不需要我们自己定义`int2()`，可以直接使用下面的代码创建创建一个新的新的函数`int2`
```plain
>>> import functools
>>> int2 = functools.partial(int, base=2)
>>> int2('1000000')
64
>>> int2('1010101')
85
```

- `functools.partisl`的作用就是，将一个函数的某些参数给固定住（设置默认值），返回一个新的函数
- 即使使用了上面的方式，但是如果我们需要使用其他基数，也可以在使用时再进行重新设定
```plain
>>> int2('1000000', base=10)
1000000
```
- 创建偏函数时，实际上可以接受函数对象、`*args`和`**kw`这三个参数，像上面`int2 = functools.partial(int, base=2)`，就相当于
```python
kw = { 'base': 2 }
int('10010', **kw)
```

- 举例：
当传入：
```python
max2 = functools.partial(max, 10)
```
实际上会把`10`作为`*args`的一部分自动加到左边，也就是：
```python
max2(5, 6, 7)
```
相当于：
```python
args = (10, 5, 6, 7)
max(*args)
-结果为10。
```

