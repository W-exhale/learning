- OOP：Object Oriented Programming

## 封装
```python
class Student(object): #括号里是继承的类，不能空着
	def __init__(self, name, score):# 类似构造方法，self表示创建的实例本身（指向创建的实例）
		self.name = name
		self.score = score
	def get_grade(self):
		if self.score >= 90:
			return 'A'
		elif self.score >= 60:
			return 'B'
		else:
			return 'C'

lisa = Student('Lisa', 99)
bart = Student('Bart', 59)
print(lisa.name, lisa.get_grade())
print(bart.name, bart.get_grade())
```

- 在属性前面加上两个下划线`__`，表示private，只有内部可以访问，但其实不是绝对的，实际上就是将`__name`变成了`_Student__name`，所以严格意义上来说，也不能说是private，不过不同版本的python的解释器是不一样的。
- 如果仍然使用`bart.__name = 'New Name'`，有效，但是不是我们想要的的name，而是外部代码给bart新增了一个`__name`变量
```python
class Student(object):

    def __init__(self, name, score):
        self.__name = name
        self.__score = score

    def get_name(self):
        return self.__name

    def get_score(self):
        return self.__score

    def set_score(self, score):
        if 0 <= score <= 100:
            self.__score = score
        else:
            raise ValueError('bad score')

    def get_grade(self):
        if self.__score >= 90:
            return 'A'
        elif self.__score >= 60:
            return 'B'
        else:
            return 'C'

bart = Student('Bart Simpson', 59)
print('bart.get_name() =', bart.get_name())
bart.set_score(60)
print('bart.get_score() =', bart.get_score())

print('DO NOT use bart._Student__name:', bart._Student__name)
```

## 继承和多态
继承的：Subclass、
被继承的：基类、父类、超类（Base class、Super class）
- 判断一个变量是否是某个类型可以用`isinstance()`
```plain
>>> isinstance(a, list)
True
>>> isinstance(b, Animal)
True
>>> isinstance(c, Dog)
True
>>> isinstance(c, Animal) #可以看到c也属于Animal，这就是多态
True
```

- 静态语言 VS 动态语言
-Java是静态语言：如果要传入Animal类型，传入的对象必须是Animal或的它的子类
-对于python来说，不一定要传入Animal类型或者它的子类，只需要对象有一个run方法就行

- python不要求严格的继承，一个对象只要看起来像鸭子，走起路来像鸭子，就可以被看作是鸭子

```python
class Animal(object):
    def run(self):
        print('Animal is running...')
class Timer(object):
    def run(self):
        print('Start...')
```

## 获取对象信息
### type()
- 使用`type()`函数判断对象类型
```plain
>>> type(123)
<class 'int'>
>>> type('str')
<class 'str'>
>>> type(None)
<type(None) 'NoneType'>
```
- 如果一个变量指向函数或者类，也可以用`type()`判断
```plain
>>> type(abs)
<class 'builtin_function_or_method'>
>>> type(a)
<class '__main__.Animal'>
```

- `type()`返回对应的class类型
- 判断一个对象是否是函数，type模块里有很多常量，可以进行判断使用
```plain
>>> import types
>>> def fn():
...     pass
...
>>> type(fn)==types.FunctionType
True
>>> type(abs)==types.BuiltinFunctionType
True
>>> type(lambda x: x)==types.LambdaType
True
>>> type((x for x in range(10)))==types.GeneratorType
True
```

### isinstance()
- 对于class的继承关系使用type()不方便，这时就可以使用isinstance()，这个判断一般优先使用
```plain
>>> a = Animal()
>>> d = Dog()
>>> h = Husky()
>>> isinstance(h, Husky)
True
>>> isinstance(h, Dog)
True
>>> isinstance(h, Animal)
True
```
### dir()
- 如果要获得一个对象的所有属性和方法，可以使用`dir()`函数，返回一个包含字符串的list
- 例如获得一个str对象的所有属性和方法
```plain
>>> dir('ABC')
['__add__', '__class__',..., '__subclasshook__', 'capitalize', 'casefold',..., 'zfill']
```
- `__len__`属性返回长度
```plain
>>> len('ABC')
3
>>> 'ABC'.__len__()
3
```
- 我们自己的类也可以自己定义一个`__len__`
- 剩下的都是普通属性或方法，比如`lower()`返回小写的字符串：
```plain
>>> 'ABC'.lower()
'abc'
```
- 仅仅把属性和方法列出来是不够的，配合`getattr()`、`setattr()`以及`hasattr()`，我们可以直接操作一个对象的状态：
```plain
>>> class MyObject(object):
...     def __init__(self):
...         self.x = 9
...     def power(self):
...         return self.x * self.x
...
>>> obj = MyObject()
测试对象的属性：
>>> hasattr(obj, 'x') # 有属性'x'吗？
True
>>> obj.x
9
>>> hasattr(obj, 'y') # 有属性'y'吗？
False
>>> setattr(obj, 'y', 19) # 设置一个属性'y'
>>> hasattr(obj, 'y') # 有属性'y'吗？
True
>>> getattr(obj, 'y') # 获取属性'y'
19
>>> obj.y # 获取属性'y'
19
```

- 如果想要获取不存在的属性，会抛出`AttributeError`的错误
```plain
>>> getattr(obj, 'z') # 获取属性'z'
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'MyObject' object has no attribute 'z'
```

- 也可以传入一个default参数，如果属性不存在就返回默认值
```plain
>>> getattr(obj, 'z', 404) # 获取属性'z'，如果不存在，返回默认值404
404
```

- 获得对象的方法
```plain
>>> hasattr(obj, 'power') # 有属性'power'吗？
True
>>> getattr(obj, 'power') # 获取属性'power'
<bound method MyObject.power of <__main__.MyObject object at 0x10077a6a0>>
>>> fn = getattr(obj, 'power') # 获取属性'power'并赋值到变量fn
>>> fn # fn指向obj.power
<bound method MyObject.power of <__main__.MyObject object at 0x10077a6a0>>
>>> fn() # 调用fn()与调用obj.power()是一样的
81
```
- 常用方式：
```python
def readImage(fp):
    if hasattr(fp, 'read'):
        return readData(fp)
    return None
```

- 假设我们从文件流fp中获取图像，
	1. 判断该fp对象是否存在read方法，如果存在，那对象就是一个流，如果不存在就无法读取。这时候就可以`hasattr()`
	2. 根据鸭子类型，有`read()`方法，不代表该fp对象就是一个文件流，它也可能是网络流，也可能是内存中的一个字节流，但只要`read()`方法返回的是有效的图像数据，就不影响读取图像的功能。

## 实例属性和类属性
- Python是动态语言，根据类创建的实例可以任意绑定属性或者通过`self`变量
```python
class Student(object):
    def __init__(self, name):
        self.name = name

s = Student('Bob')
s.score = 90
```
如果Student类本身需要绑定一个属性，可以直接在class中设定，这种叫类属性
```python
class Student(object):
    name = 'Student'
```
这个属性虽然归类所有，但类的所有实例都可以访问，如果设定了实例属性，会把类属性覆盖

在访问类属性用`Student.name`，而不是`self.name`，这是实例类

