## 使用__slots__
- 当我们定义了一个class，创建了一个class的实例后，我们可以给该实例绑定任何属性和方法，这就是动态语言的灵活性。
```python
class Student(object):
    pass
>>> s = Student()
>>> s.name = 'Michael' # 动态给实例绑定一个属性
>>> print(s.name)
Michael
>>> def set_age(self, age): # 定义一个函数作为实例方法
...     self.age = age
...
>>> from types import MethodType
>>> s.set_age = MethodType(set_age, s) # 给实例绑定一个方法
>>> s.set_age(25) # 调用实例方法
>>> s.age
```

- 给一个实例特别绑定的方法对另一个实例不起作用
```plain
>>> s2 = Student() # 创建新的实例
>>> s2.set_age(25) # 尝试调用方法
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'Student' object has no attribute 'set_age'
```

- 如果要实现给一个实例绑定的方法应用到其他实例，可以给class绑定方法，即将类的方法指向实例的方法
```plain
>>> def set_score(self, score):
...     self.score = score
...
>>> Student.set_score = set_score
```

- 如果我们要限制实例属性，例如只允许对Student实例添加`name`和`age`属性，在类中可以定义一个特殊的`__slots__`变量，来限制该`class`实例能添加的属性
```python
class Student(object):
    __slots__ = ('name', 'age') # 用tuple定义允许绑定的属性名称
```
```plain
>>> s = Student() # 创建新的实例
>>> s.name = 'Michael' # 绑定属性'name'
>>> s.age = 25 # 绑定属性'age'
>>> s.score = 99 # 绑定属性'score'
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'Student' object has no attribute 'score'
```
Student中没有给score权限，所以不能进行设定，否则会报错，只能设定name和age，其他都不行

- 注意：`__slots__`定义的属性仅对当前类的实例起作用，对继承的子类是没用的，除非在子类中也定义`__slots__`，这样子类能用的就是父类的`__slots__`加上子类的`__slots__`

## 使用@property
- 如果直接暴露属性，写起来简单，但是没办法检查参数，这时候就可以设定set方法来自定义，再通过get方法获得
```python
class Student(object):
    def get_score(self):
         return self._score

    def set_score(self, value):
        if not isinstance(value, int):
            raise ValueError('score must be an integer!')
        if value < 0 or value > 100:
            raise ValueError('score must between 0 ~ 100!')
        self._score = value
```

- 但是getset的方法很复杂，装饰器（decorator）中就有这么个功能，既能检查参数，又能设定属性
- 使用python内置的`@property`装饰器把一个方法变成属性调用
```python
class Student(object):
    @property
    def score(self):
        return self._score
    @score.setter
    def score(self, value):
        if not isinstance(value, int):
            raise ValueError('score must be an integer!')
        if value < 0 or value > 100:
            raise ValueError('score must between 0 ~ 100!')
        self._score = value
```
- 如上，在方法前加上`@property`相当于将get方法变成了属性，然后在set方法加上@setter就可以将set方法变成属性赋值，对属性进行限制
```plain
>>> s = Student()
>>> s.score = 60 # OK，实际转化为s.score(60)
>>> s.score # OK，实际转化为s.score()
60
>>> s.score = 9999
Traceback (most recent call last):
  ...
ValueError: score must between 0 ~ 100!
```

- 还可以定义只读属性，只加@property的get方法，不设定@setter就行

- 注意：属性的方法名不要和实例变量重名，像下面的代码就是错误的
```python
class Student(object):
    # 方法名称和实例变量均为birth:
    @property
    def birth(self):
```
调用s.birth时，首先转化为方法调用，在执行`return self.birth`时，又访问self的birth属性，之后又转为方法，无限递归，最后就会导致栈溢出报错`RecursionError`

### 练习
请利用`@property`给一个`Screen`对象加上`width`和`height`属性，以及一个只读属性`resolution`：

```python
class Screen(object):
    pass

# 测试:
s = Screen()
s.width = 1024
s.height = 768
print('resolution =', s.resolution)
if s.resolution == 786432:
    print('测试通过!')
else:
    print('测试失败!')
```

- 实现
```python
class Screen(object):
    @property
    def width(self):
        return self._width
    @width.setter
    def width(self, value):
        if not isinstance(value, int):
            raise ValueError('width must be an integer!')
        self._width = value
    @property
    def height(self):
        return self._height
    @height.setter
    def height(self, value):
        if not isinstance(value, int):
            raise ValueError('score must be an integer!')
        self._height = value
    @property
    def resolution(self):
        self._resolution = 786432
        return self._resolution # 注意这里不能直接用resolution，不然会栈溢出
# 测试:
s = Screen()
s.width = 1024
s.height = 768
print('resolution =', s.resolution)
if s.resolution == 786432:
    print('测试通过!')
else:
    print('测试失败!')
```

## 多重继承
![[Pasted image 20250305163418.png]]

用创建子类父类的方式就要创建非常多的类，十分的麻烦，这时候就可以采用多重继承
```python
class Animal(object):
    pass

# 大类:
class Mammal(Animal): #哺乳类
    pass

class Bird(Animal):
    pass

# 各种动物:
class Dog(Mammal):
    pass

class Bat(Mammal):
    pass

class Parrot(Bird):
    pass

class Ostrich(Bird):
    pass
```

- 假如我们要给动物加上`Runnable`和`Flyable`的功能，只需要先定义好`Runnable`和`Flyable`
```python
class Runnable(object):
    def run(self):
        print('Running...')

class Flyable(object):
    def fly(self):
        print('Flying...')
```
对于需要`Flyable`功能的动物，多继承一个`Flyable`即可
```python
class Dog(Mammal, Runnable):
    pass
class Bat(Mammal, Flyable):
    pass
```

### MixIn
- 在设计类的继承关系时，主线一般都是单一继承的，如果要加其他功能，就需要通过多重继承。这种设计通常称为MixIn
- 为了能更好的看出继承关系，通常把`Runnable`和`Flyable`改为`RunnableMixIn`和`FlyableMixIn`
```python
class Dog(Mammal, RunnableMixIn, CarnivorousMixIn):
    pass
```

所以在设计类的时候，通常优先考虑通过多重继承来组合多个MixIn的功能而不是复杂的继承关系

- Python自带的很多库页使用了MixIn，例如Python自带了`TCPServer`和`UDPServer`这两类网络服务，而要同时服务多个用户就必须使用多进程或多线程模型，这两种模型由`ForkingMixIn`和`ThreadingMixIn`提供。通过组合，我们就可以创造出合适的服务来。

- 比如，编写一个多进程模式的TCP服务，定义如下：
```python
class MyTCPServer(TCPServer, ForkingMixIn):
    pass
```
- 编写一个多线程模式的UDP服务，定义如下：
```python
class MyUDPServer(UDPServer, ThreadingMixIn):
    pass
```
- 如果你打算搞一个更先进的协程模型，可以编写一个`CoroutineMixIn`：
```python
class MyTCPServer(TCPServer, CoroutineMixIn):
    pass
```
## 定制类
- 在python中，类似`__xxx__`的变量或者函数名是有特殊用途的，`__len__()`方法的作用就是能让class作用于`len()`函数（计算类的“大小”，当类是一个可计算的对象是）
### \_\_str\_\_
- 打印实例
```plain
>>> class Student(object):
...     def __init__(self, name):
...         self.name = name
...
>>> print(Student('Michael'))
<__main__.Student object at 0x109afb190>
```
可以看到打印出来的很不好看，类似java中的toString，我们可以进行修改
```plain
>>> class Student(object):
...     def __init__(self, name):
...         self.name = name
...     def __str__(self):
...         return 'Student object (name: %s)' % self.name
...
>>> print(Student('Michael'))
Student object (name: Michael)
```

- 但是即使用了上面的方式直接输实例，还是不好看
```plain
>>> s = Student('Michael')
>>> s
<__main__.Student object at 0x109afb310>
```

python中显示变量调用的是`__repr__()`而不是`__str__()`，两个的区别：前者返回程序开发者看到的字符串，后者返回用户看到的字符串。即，`__repr__()`是为了调试服务的，解决方案通常是直接在下面加`__repr__=__str__`
```python
class Student(object):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return 'Student object (name=%s)' % self.name
    __repr__ = __str__
```

### \_\_iter\_\_
- 如果一个类想被用于`for...in`循环，类似list或tuple那样，就必须实现\_\_iter\_\_()方法，该方法返回一个迭代对象，然后Python的for循环就会不断调用该迭代对象的`__next__()`方法拿到循环的下一个值，直到遇到`StopIteration`错误退出循环
- 以斐波那契数列为例，写一个Fib类，可以作用于for循环：
```python
class Fib(object):
	def __init__(self):
		self.a,self.b = 0, 1 #初始化两个计数器a，b
	def __iter__(self):
		return self #实例1本身就是迭代对象，返回自己
	def __next__(self):
		self.a, self.b = self.b, self.a + self.b #计算下一个值
		if self.a > 100000: #退出循环的条件
			raise StopIteration()
		return self.a #返回下一个值
```
```plain
>>> for n in Fib():
...     print(n)
...
1
1
2
3
5
...
46368
75025
```

## \_\_getitem\_\_
- Fib实例虽然能用于for循环但还是不能和list一样通过下标获得数据
```plain
>>> Fib()[5]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'Fib' object does not support indexing
```

- 实现\_\_getitem\_\_方法就可以通过下标来访问对象
```python
class Fib(object):
    def __getitem__(self, n):
        a, b = 1, 1
        for x in range(n):
            a, b = b, a + b
        return a
```
```plain
>>> f = Fib()
>>> f[0]
1
>>> f[1]
1
```
- 但是如果想要使用list的切片功能还要进行判断，因为\_\_getitem\_\_传入的参数可能是一个int，也可能是一个切片对象slice
```python
class Fib(object):
    def __getitem__(self, n):
        if isinstance(n, int): # n是索引
            a, b = 1, 1
            for x in range(n):
                a, b = b, a + b
            return a
        if isinstance(n, slice): # n是切片
            start = n.start
            stop = n.stop
            if start is None:
                start = 0
            a, b = 1, 1
            L = []
            for x in range(stop):
                if x >= start:
                    L.append(a)
                a, b = b, a + b
            return L
```
```plain
>>> f = Fib()
>>> f[0:5]
[1, 1, 2, 3, 5]
>>> f[:10]
[1, 1, 2, 3, 5, 8, 13, 21, 34, 55]

```
但是没有对step参数（第三个参数）进行处理，也没有第一个负数作处理。如果将对象看成dict，`__getitem__()`的参数也可能是一个可以作key的object，例如str

- 和`__getitem__()`对应的还有`__setitem__()`方法，把对象视作list或dict来对集合赋值。还有一个`__delitem__()`方法，用于删除某个元素
- 可以和上面那样用主要是因为动态语言的“鸭子类型”，不需要强制继承某个接口

## \_\_getattr\_\_
- 当调用不存在的属性（`score`）时，系统会报错，解决这个问题一种是设置一个score属性，还有一种就是使用`__getattr__()`动态返回一个属性
```python
class Student(object):
    def __init__(self):
        self.name = 'Michael'
    def __getattr__(self, attr):#attr表示属性名
        if attr=='score':
            return 99
>>> s = Student()
>>> s.name
'Michael'
>>> s.score
99
```
- 也可以动态设置一个函数，返回函数即可
```python
class Student(object):
    def __getattr__(self, attr):#attr表示函数名
        if attr=='age':
            return lambda: 25
>>> s.age()
25
```
- 只有在没有找到属性的时候才会去`__getattr__`中寻找，如果里面没有，就会返回None（默认返回None）
- 要让class只响应特定的几个属性，我们就要按照约定，抛出`AttributeError`的错误：
```python
class Student(object):
    def __getattr__(self, attr):
        if attr=='age':
            return lambda: 25
        raise AttributeError('\'Student\' object has no attribute \'%s\'' % attr)
```

- 应用案例：（忽略）
现在很多网站都搞REST API，比如新浪微博、豆瓣啥的，调用API的URL类似：
- http://api.server/user/friends
- http://api.server/user/timeline/list
如果要写SDK，给每个URL对应的API都写一个方法，那得累死，而且，API一旦改动，SDK也要改。
利用完全动态的`__getattr__`，我们可以写出一个链式调用：
```python
class Chain(object):
    def __init__(self, path=''):
        self._path = path

    def __getattr__(self, path):
        return Chain('%s/%s' % (self._path, path))

    def __str__(self):
        return self._path
    __repr__ = __str__
```
```plain
>>> Chain().status.user.timeline.list
'/status/user/timeline/list'
```
无论API怎么变，SDK都可以根据URL实现完全动态的调用，而且，不随API的增加而改变！

还有些REST API会把参数放到URL中，比如GitHub的API：
```plain
GET /users/:user/repos
```
调用时，需要把`:user`替换为实际用户名。如果我们能写出这样的链式调用：
```plain
Chain().users('michael').repos
```

### \_\_call\_\_
- 一个对象实例调用方法一般是`instancemethod()`，如果我们想要输入实例的时候也有程序运行，就会用到\_\_call\_\_
```python
class Student(object):
    def __init__(self, name):
        self.name = name

    def __call__(self):
        print('My name is %s.' % self.name)
>>> s = Student('Michael')
>>> s() # self参数不要传入
My name is Michael.
```

- \_\_call\_\_也可以定义参数，这样对实例进行调用就和函数类似，对象可以看成函数，函数也可以看成对象

- 函数本身其实也可以在运行期动态创建出来，因为类的实例都是运行期创建出来的，这么一来，我们就模糊了对象和函数的界限。

- 如何判断一个变量是对象还是函数？通过判断一个对象是否能被调用，能被调用的对象就是一个`Callable`对象。
```plain
>>> callable(Student())
True
>>> callable(max)
True
>>> callable([1, 2, 3])
False
>>> callable(None)
False
>>> callable('str')
False
```

## 使用枚举类
- 定义常量通常使用大写变量来定义，例如月份，一个一个定义太麻烦，我们可以使用枚举类来进行定义
```python
from enum import Enum

Month = Enum('Month', ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))
```
我们可以通过`Month.Jan`来访问，或者枚举它的所有成员
```python
for name, member in Month.__members__.items():
    print(name, '=>', member, ',', member.value)
```
value属性自动给成员赋int常量，默认从1开始计数，如果要精确地控制枚举类型，可以从`Enum`派生出自定义类
```python
from enum import Enum, unique
@unique
class Weekday(Enum):
    Sun = 0 # Sun的value被设定为0
    Mon = 1
    Tue = 2
    Wed = 3
    Thu = 4
    Fri = 5
    Sat = 6
```
`@unique`装饰器可以帮助我们检查保证没有重复值。
- 访问枚举类型
```plain
>>> day1 = Weekday.Mon
>>> print(day1)
Weekday.Mon
>>> print(Weekday['Tue'])
Weekday.Tue
>>> print(Weekday.Tue.value)
2
>>> print(day1 == Weekday.Mon)
True
>>> print(Weekday(1))
Weekday.Mon
>>> print(day1 == Weekday(1))
True
>>> Weekday(7)
Traceback (most recent call last):
  ...
ValueError: 7 is not a valid Weekday
>>> for name, member in Weekday.__members__.items():
...     print(name, '=>', member)
...
Sun => Weekday.Sun
Mon => Weekday.Mon
Tue => Weekday.Tue
Wed => Weekday.Wed
Thu => Weekday.Thu
Fri => Weekday.Fri
Sat => Weekday.Sat
```
也就是可以通过成员名称引用枚举常量，又可以根据value的值获得枚举常量

## 使用元类
### type()
- 动态语言和静态语言最大的不同就是函数和类的定义，不是编译时定义的而是运行时动态创建的
```python
class Hello(object):
    def hello(self, name='world'):
        print('Hello, %s.' % name)
```
当python解释器载入上面hello模块时，就会依次执行该模块的所有语句，执行结果就是动态创建出一个Hello的class对象
```plain
>>> from hello import Hello
>>> h = Hello()
>>> h.hello()
Hello, world.
>>> print(type(Hello))
<class 'type'>
>>> print(type(h))
<class 'hello.Hello'>
```
`type()`函数可以查看一个类型或者变量的类型，Hello是一个class，类型是type()，h是一个实例，类型是它的class，Hello

- class是运行时动态创建的，创建class的方法就是使用`type()`函数；`type()`函数既可以返回一个对象的类型，又可以创建出新的类型，我们可以更改上面代码，通过type()函数创建出Hello类
```plain
>>> def fn(self, name='world'): # 先定义函数
...     print('Hello, %s.' % name)
...
>>> Hello = type('Hello', (object,), dict(hello=fn)) # 创建Hello class
>>> h = Hello()
>>> h.hello()
Hello, world.
>>> print(type(Hello))
<class 'type'>
>>> print(type(h))
<class '__main__.Hello'>
```
- type()中要传入3个参数：
	1. class的名称
	2. 继承的父类，使用tuple
	3. class的方法名称与函数绑定，上面是将fn绑定到方法名hello上
- 通过type()创建和直接写是一样的，因为Python解释器遇到class定义时，只是扫描一下class定义的语法，然后调用`type()`函数创建出class
- 正常情况下，我们是用`class XxX ...`来定义类，用type()的方法属于动态创建类，如果在静态语言运行期间创建类，需要构造源代码字符串，再调用编译器，或者借助工具生成字节码实现，也是动态编译，但是很复杂

### metaclass（元类）
- type()主要是动态创建类，而使用metaclass可以控制类的创建行为（即是否创建？是否修改）
- 可以将类看成是metclass创建出来的实例
- （大多数情况基本不用）
- 先定义metaclass，创建类，创建实例

1. 定义`ListMetaclass`，按照默认习惯，metaclass的类名总是以Metaclass结尾，以便清楚地表示这是一个metaclass：
```python
# metaclass是类的模板，所以必须从`type`类型派生：
class ListMetaclass(type):
    def __new__(cls, name, bases, attrs):
        attrs['add'] = lambda self, value: self.append(value)
        return type.__new__(cls, name, bases, attrs)
```
`__new__()`方法接收到的参数依次是：
	1. 当前准备创建的类的对象
	2. 类的名字
	3. 类继承的父类集合
	4. 类的方法集合

2. 定义类的时候要指示使用`ListMetaclass`来定制类，传入关键字参数`metaclass`
```python
class MyList(list, metaclass=ListMetaclass):
    pass
```
传入关键字参数metaclass，指示python解释器在创建`MyList`时，要通过`ListMetclass.__new__()`来创建，我们可以在这里修改类的定义，例如加上新的方法，然后返回修改后的定义。
```plain
>>> L = MyList()
>>> L.add(1)
>> L
[1]
-普通的list就没有add
>>> L2 = list()
>>> L2.add(1)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'list' object has no attribute 'add'
```
虽然这样写很麻烦，这个案例的解决方案也不会是这个，应该直接在类里加add方法，但是总有用到metaclass的时候

- ORM就是一个典型的例子
要编写一个ORM框架，所有的类都只能动态定义，因为只有使用者才能根据表的结构定义出对应的类来。

### 尝试编写ORM框架
1. 写出调用接口：例如如果我们要使用ORM框架，需要定义一个`User`类来操作对应的数据库表`User`，我们可以这样写：
```python
class User(Model):
    # 定义类的属性到列的映射：
    id = IntegerField('id')
    name = StringField('username')
    email = StringField('email')
    password = StringField('password')

# 创建一个实例：
u = User(id=12345, name='Michael', email='test@orm.org', password='my-pwd')
# 保存到数据库：
u.save()
```
其中，父类`Model`和属性类型`StringField`、`IntegerField`由ORM框架提供，`save()`由父类`Model`自动完成。虽然metaclass的编写比较复杂，但是ORM用起来却很简单

2. 定义`Field`类，负责保存数据库表的字段名和字段类型：（按上面的接口来实现ORM）
```python
class Field(object):

    def __init__(self, name, column_type):
        self.name = name
        self.column_type = column_type

    def __str__(self):
        return '<%s:%s>' % (self.__class__.__name__, self.name)
```
3. 在`Field`的基础上，进一步定义各种类型的`Field`
```python
class StringField(Field):
    def __init__(self, name):
        super(StringField, self).__init__(name, 'varchar(100)')

class IntegerField(Field):
    def __init__(self, name):
        super(IntegerField, self).__init__(name, 'bigint')
```
4. 编写最复杂的`ModelMetaclass`
```python
class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        if name=='Model':
            return type.__new__(cls, name, bases, attrs)
        print('Found model: %s' % name)
        mappings = dict()
        for k, v in attrs.items():
            if isinstance(v, Field):
                print('Found mapping: %s ==> %s' % (k, v))
                mappings[k] = v
        for k in mappings.keys():
            attrs.pop(k)
        attrs['__mappings__'] = mappings # 保存属性和列的映射关系
        attrs['__table__'] = name # 假设表名和类名一致
        return type.__new__(cls, name, bases, attrs)
```
- 基类：`Model`
```python
class Model(dict, metaclass=ModelMetaclass):
    def __init__(self, **kw):
        super(Model, self).__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

    def save(self):
        fields = []
        params = []
        args = []
        for k, v in self.__mappings__.items():
            fields.append(v.name)
            params.append('?')
            args.append(getattr(self, k, None))
        sql = 'insert into %s (%s) values (%s)' % (self.__table__, ','.join(fields), ','.join(params))
        print('SQL: %s' % sql)
        print('ARGS: %s' % str(args))
```
当用户定义一个User(Model)时，Python解释器先在当前类`User`的定义中查找`metaclass`，如果没找到，就在父类`Model`中查找`metaclass`，如果Model里面有，就使用`Model`中定义的`metaclass`的`ModelMetaclass`来创建`User`类，也就是metaclass可以隐式地继承到子类，但子类自己感觉不到

- 解析`ModelMetaclass`
	1. 排除对`Model`类的修改
	2. 在当前类（`User`）中查找定义的类的所有属性，如果找到了一个`Field`属性，就把它保存到一个`__mappings__`的dict中
	3. 将表名保存到`__table__`中，这里的表明默认为类名

在`Model`类中，可以定义各种操作数据库的方法，`sava()`、`delete()`、`find()`、`update()`等

- 使用
```python
u = User(id=12345, name='Michael', email='test@orm.org', password='my-pwd')
u.save()
```
```plain
Found model: User
Found mapping: email ==> <StringField:email>
Found mapping: password ==> <StringField:password>
Found mapping: id ==> <IntegerField:uid>
Found mapping: name ==> <StringField:username>
SQL: insert into User (password,email,username,id) values (?,?,?,?)
ARGS: ['my-pwd', 'test@orm.org', 'Michael', 12345]
```
可以看到，`save()`方法已经打印出了可执行的SQL语句，以及参数列表，只需要真正连接到数据库，执行该SQL语句，就可以完成真正的功能。

