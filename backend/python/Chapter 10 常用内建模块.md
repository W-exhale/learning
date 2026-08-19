## datetime
### 基础使用
- 处理日期和时间的标准库
- 获取当前日期和时间：
![Pasted image 20250319105700](images/Pasted%20image%2020250319105700.png)

- datetime是一个模块，datetime还包含一个`datetime`类，通过导包`import datetime`导入的才是这个类
- 如果只导入`import datetime`，用的时候就要用`datetime.datetime`
- `datetime.now()`返回当前时间

-  获取指定日期和时间
```plain
>>> from datetime import datetime
>>> dt = datetime(2015, 4, 19, 12, 20) # 用指定日期时间创建datetime
>>> print(dt)
2015-04-19 12:20:00
```

### timestamp
- 1970年1月1日 00:00:00 UTC+00:00时区的时刻称为epoch time，记为`0`，在这之前的时间为负数
```plain
timestamp = 0 = 1970-1-1 00:00:00 UTC+0:00
#对应的北京时间
timestamp = 0 = 1970-1-1 08:00:00 UTC+8:00
```

- 转换为时间戳
```plain
>>> from datetime import datetime
>>> dt = datetime(2015, 4, 19, 12, 20) # 用指定日期时间创建datetime
>>> dt.timestamp() # 把datetime转换为timestamp
1429417200.0
```
python的timestamp是一个浮点数，整数位表示秒
java(或javaScript)的时间戳使用整数表示毫秒数，除以1000就可以和Python的一样

- 时间戳转datetime：使用`fromtimestamp()`
```plain
>>> from datetime import datetime
>>> t = 1429417200.0
>>> print(datetime.fromtimestamp(t))
2015-04-19 12:20:00
```
这个转换是转换的本地时间，UTC+8:00就是北京时间
```plain
2015-04-19 12:20:00 UTC+8:00
```
此刻的格林威治标准时间与北京时间差了8小时，也就是UTC+0:00时区的时间应该是：
```plain
2015-04-19 04:20:00 UTC+0:00
```
```plain
>>> from datetime import datetime
>>> t = 1429417200.0
>>> print(datetime.fromtimestamp(t)) # 本地时间
2015-04-19 12:20:00
>>> print(datetime.utcfromtimestamp(t)) # UTC时间
2015-04-19 04:20:00
```

### 字符串转换
str转为datetime
```plain
>>> from datetime import datetime
>>> cday = datetime.strptime('2015-6-1 18:19:59', '%Y-%m-%d %H:%M:%S')
>>> print(cday)
2015-06-01 18:19:59
```

- datetime转为str
```plain
>>> from datetime import datetime
>>> now = datetime.now()
>>> print(now.strftime('%a, %b %d %H:%M'))
Mon, May 05 16:28
```
### 时间加减
- 直接+或-，但是要导入`timedelta`类

![Pasted image 20250319111823](images/Pasted%20image%2020250319111823.png)

### 时区转换
- `datetime`类型有一个`tzinfo`，默认为`None`，我们可以强行给`datetime`设置一个时区
```plain
>>> from datetime import datetime, timedelta, timezone
>>> tz_utc_8 = timezone(timedelta(hours=8)) # 创建时区UTC+8:00
>>> now = datetime.now()
>>> now
datetime.datetime(2015, 5, 18, 17, 2, 10, 871012)
>>> dt = now.replace(tzinfo=tz_utc_8) # 强制设置为UTC+8:00
>>> dt
datetime.datetime(2015, 5, 18, 17, 2, 10, 871012, tzinfo=datetime.timezone(datetime.timedelta(0, 28800)))
```
如果系统是UTC+8:00，那么上面代码就是正确的

- 我们可以通过`utcnow()`拿到当前UTC时间，再转换成任意时区的时间
```plain
# 拿到UTC时间，并强制设置时区为UTC+0:00:,utcnow()过时？
>>> utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
>>> print(utc_dt)
2015-05-18 09:05:12.377316+00:00
# astimezone()将转换时区为北京时间:
>>> bj_dt = utc_dt.astimezone(timezone(timedelta(hours=8)))
>>> print(bj_dt)
2015-05-18 17:05:12.377316+08:00
# astimezone()将转换时区为东京时间:
>>> tokyo_dt = utc_dt.astimezone(timezone(timedelta(hours=9)))
>>> print(tokyo_dt)
2015-05-18 18:05:12.377316+09:00
# astimezone()将bj_dt转换时区为东京时间:
>>> tokyo_dt2 = bj_dt.astimezone(timezone(timedelta(hours=9)))
>>> print(tokyo_dt2)
2015-05-18 18:05:12.377316+09:00
```
拿到一个`datetime`时，要知道正确的时区作为基准时间，然后强制设置时区。
- 不是必须从UTC+0:00时区转换到其他时区，任何带时区的`datetime`都可以正确转换，例如上述`bj_dt`到`tokyo_dt`的转换

- 存储datetime最好的方式是转换为timestamp再存储（时间戳不受时区影响）

```python
import re

from datetime import datetime, timezone, timedelta

def to_timestamp(dt_str, tz_str):
	# 解析日期和字符串
    dt = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
    match = re.match(r'UTC([\+\-])(\d{1,2}):(\d{2})+', tz_str)
    if not match:
        raise ValueError('Invalic timezone format')
        
    sign = 1 if match.group(1) == '+' else -1
    hours = int(match.group(2))
    minutes = int(match.group(3))
    tz_offset = timedelta(hours=sign * hours, minutes=sign * minutes)
    tz = timezone(tz_offset)
    
    dt = dt.replace(tzinfo=tz)
    print(dt)
    return dt.timestamp()  
    
t1 = to_timestamp('2015-6-1 08:10:30', 'UTC+7:00')
assert t1 == 1433121030.0, t1
t2 = to_timestamp('2015-5-31 16:10:30', 'UTC-09:00')
assert t2 == 1433121030.0, t2
```
![Pasted image 20250319120541](images/Pasted%20image%2020250319120541.png)

如果不往tzinfo中加东西，那么输出的内容就没有+07:00或者-09:00，设置时区后转化的时间戳也是当地的时间戳

**`utcnow()` 并没有被废弃**，但如果你的应用需要处理时区或跨时区操作，建议使用 `datetime.now(timezone.utc)`，因为它更明确且不容易出错。

## collections
- `namedtuple`：一个函数，可以用来创建一个自定义的`tuple`对象，并且规定了`tuple`元素的个数，用`.`来看tuple的某个元素

- 表示坐标：可以用元组，但是光看`(1,2)`看不出是坐标，也不至于定义一个`class`。
![Pasted image 20250319205142](images/Pasted%20image%2020250319205142.png)
上面创建的Point是tuple的一个子类
```plain
>>> isinstance(p, Point)
True
>>> isinstance(p, tuple)
True
```
- 也可以坐标和半径表示一个圆
```python
# namedtuple('名称', [属性list]):
Circle = namedtuple('Circle', ['x', 'y', 'r'])
```

### deque
-  使用list时按索引访问元素很快，但是插入删除很慢
- `deque`是为了高效实现插入和删除操作的双向列表，适用于队列和栈
```plain
>>> from collections import deque
>>> q = deque(['a', 'b', 'c'])
>>> q.append('x')
>>> q.appendleft('y')
>>> q
deque(['y', 'a', 'b', 'c', 'x'])
```
- 除了实现list的`append()`和`pop()`外，还支持`appendleft()`和`popleft()`，这样就可以非常高效地往头部添加或删除元素。

### defaultdict
使用`dict`时，如果key不存在，就会抛出`KeyError`。如果希望key不存在时返回一个默认值，就可以用`defaultdict`：
```plain
>>> from collections import defaultdict
>>> dd = defaultdict(lambda: 'N/A')
>>> dd['key1'] = 'abc'
>>> dd['key1'] # key1存在
'abc'
>>> dd['key2'] # key2不存在，返回默认值
'N/A'
```

- 默认值通过调用函数返回，使用的匿名函数的方式在创建`defaultdict`对象的时候传入的
- 除了在Key不存在时返回默认值，`defaultdict`的其他行为跟`dict`是完全一样的。

### OrderedDict
使用`dict`时，Key是无序的，如果要保持Key的顺序，我们可以用`OrderedDict`：
```plain
>>> from collections import OrderedDict
>>> d = dict([('a', 1), ('b', 2), ('c', 3)])
>>> d # dict的Key是无序的
{'a': 1, 'c': 3, 'b': 2}
>>> od = OrderedDict([('a', 1), ('b', 2), ('c', 3)])
>>> od # OrderedDict的Key是有序的
OrderedDict([('a', 1), ('b', 2), ('c', 3)])
```
`OrderedDict`的Key会按照插入的顺序排列，不是Key本身排序：
```plain
>>> od1 = OrderedDict()
>>> od1['z'] = 1
>>> od1['y'] = 2
>>> od1['x'] = 3
>>> list(od1.keys()) # 按照插入的Key的顺序返回
['z', 'y', 'x']
```

- 也可以实现FIFO的dict，容量超出限制时，先删最早的
```python
from collections import OrderedDict

class LastUpdateOrderedDict(OrderedDict):

    #初始化方法，capacity是一个用户定义的容量限制
    def __init__(self, capacity):
        #调用父类的初始化方法，确保OrderedDict正确初始化
        super(LastUpdateOrderedDict, self).__init__()
        #_capacity存储最大容量
        self._capacity = capacity
    #重写方法，这个方法定义了通过obj[key] = value设置键值对的行为，重写该方法允许我们在添加或更新键值对时实现自定义逻辑

    def __setitem__(self, key, value):
        #检查键是否已存在于字典中。
        containsKey = 1 if key in self else 0
        #len(self) 返回字典中当前的键值对数量。如果超出容量就删除
        if len(self) - containsKey >= self._capacity:
            #调用 popitem(last=False) 移除最早插入的键值对。last=False 表示移除的是最早插入的（FIFO 顺序）。
            last = self.popitem(last=False)
            #打印被移除的键值对
            print('remove:', last)
        #如果键存在
        if containsKey:
            #使用 del self[key] 删除旧的键值对（在 OrderedDict 中重新插入会改变顺序）。
            del self[key]
            print('set:', (key, value))
        else:
            print('add:', (key, value))
            
        #调用父类 OrderedDict 的 __setitem__ 方法将新的键值对插入字典。
        OrderedDict.__setitem__(self, key, value)
```

### ChainMap
- 可以将一组`dict`串起来组成一个逻辑上的`dict`。`ChainMap`也是一个dict，但是查找的时候会按照顺序在内部的dict依次查找

- 应用场景：应用程序往往都要输入参数（通过命令行，环境变量，默认参数），我们可以用`ChainMap`实现参数的优先级查找(先查命令行，如果没有再查环境变量，...)

- 如何查找`user`和`color`？
```python
from collections import ChainMap
import os, argparse

# 构造缺省参数:
defaults = {
    'color': 'red',
    'user': 'guest'
}

# 构造命令行参数:
parser = argparse.ArgumentParser()
parser.add_argument('-u', '--user')
parser.add_argument('-c', '--color')
namespace = parser.parse_args()
command_line_args = { k: v for k, v in vars(namespace).items() if v }

# 组合成ChainMap:
combined = ChainMap(command_line_args, os.environ, defaults)

# 打印参数:
print('color=%s' % combined['color'])
print('user=%s' % combined['user'])
```
- 没有任何参数时，打印出默认参数：
```plain
$ python3 use_chainmap.py 
color=red
user=guest
```
- 当传入命令行参数时，优先使用命令行参数：
```plain
$ python3 use_chainmap.py -u bob
color=red
user=bob
```
- 同时传入命令行参数和环境变量，命令行参数的优先级较高：
```plain
$ user=admin color=green python3 use_chainmap.py -u bob
color=green
user=bob
```

### Counter
- 计数器
- 统计字符出现的个数
```plain
>>> from collections import Counter
>>> c = Counter('programming')
>>> for ch in 'programming':
...     c[ch] = c[ch] + 1
...
>>> c
Counter({'g': 2, 'm': 2, 'r': 2, 'a': 1, 'i': 1, 'o': 1, 'n': 1, 'p': 1})
>>> c.update('hello') # 也可以一次性update
>>> c
Counter({'r': 2, 'o': 2, 'g': 2, 'm': 2, 'l': 2, 'p': 1, 'a': 1, 'i': 1, 'n': 1, 'h': 1, 'e': 1})
```
`Counter`实际上也是`dict`的一个子类，上面的结果可以看出每个字符出现的次数。

## argparse
- 命令行程序经常需要获取命令行参数，Python内置的`sys.argv`保存了完整的参数列表，我们可以从中解析出需要的参数
```python
import sys

print(sys.argv)
source = sys.argv[1]
target = sys.argv[2]
```
![Pasted image 20250321091614](images/Pasted%20image%2020250321091614.png)
上面调用sys的方法只能应付一些简单的参数，如果参数比较复杂，可以用`-d`复制目录，使用`--filename *.py`过滤文件名

- 可以用内置的`argparse`简化参数解析，定义好各个参数后能直接返回有效的参数


假设我们想编写一个备份MySQL数据库的命令行程序，需要输入的参数如下：

- host参数：表示MySQL主机名或IP，不输入则默认为`localhost`；
- port参数：表示MySQL的端口号，int类型，不输入则默认为`3306`；
- user参数：表示登录MySQL的用户名，必须输入；
- password参数：表示登录MySQL的口令，必须输入；
- gz参数：表示是否压缩备份文件，不输入则默认为`False`；
- outfile参数：表示备份文件保存在哪，必须输入。

其中，`outfile`是位置参数，而其他则是类似`--user root`这样的“关键字”参数。

```python
import argparse

def main():
    #定义一个ArgumentParser实例：
    parser = argparse.ArgumentParser(
        prog='backup', # 程序名
        description='Backup MySQL database', #描述
        epilog='Copyright(r), 2023' #说明信息

    )
    # 定义位置参数：表示备份文件在哪，必须输入
    parser.add_argument('outfile')
    
    # 定义关键字参数：
    # 表示主机名或IP，不输入默认为localhost
    parser.add_argument('--host', default='localhost')
    # 此参数必须为int类型，端口号，不输入默认3306
    parser.add_argument('--port', default='3306', type=int)
    # 允许用户输入简写的-u，表示登录MySQL的用户名，必须输入
    parser.add_argument('-u', '--user', required=True)
    parser.add_argument('-p', '--password', required=True)
    parser.add_argument('--database', required=True)
    # gz参数不跟参数值，所以指定action='store_true'，意思是出现-gz表示True，表示是否压缩备份文件，不输入默认False
    parser.add_argument('-gz', '--gzcompress', action='store_true', required=False, help='Compress backup files by gz.')

    # 解析参数，获取的有效代码，不用捕获异常如果参数有问题会自动打印错误信息，结束进程，如果参数是-h,打印帮助信息后结束进程。只有参数全部有效时才会返回一个NameSpace对象，获取对应的参数就把参数名当作属性获取
    args = parser.parse_args()

    # 打印参数
    print('parsed args:')
    print(f'outfile = {args.outfile}')
    print(f'host = {args.host}')
    print(f'port = {args.port}')
    print(f'user = {args.user}')
    print(f'password = {args.password}')
    print(f'database = {args.database}')
    print(f'gzcompress = {args.gzcompress}')

if __name__ == '__main__':
    main()
```
![Pasted image 20250321112829](images/Pasted%20image%2020250321112829.png)

## base64
- base64是一种用64个字符来表示任意二进制数据的方法

用记事本打开`exe`、`jpg`、`pdf`这些文件的时候我们都会看到一堆乱码，因为二进制文件包含很多无法显示和打印的字符，所以如果想让记事本能够处理二进制数据，就需要一个二进制到字符串的转换方法

- Base64标准编码的字符集包括：`A-Z`、`a-z`、`+`、`/`
```python
['A', 'B', 'C', ... 'a', 'b', 'c', ... '0', '1', ... '+', '/']
```
- 对二进制数据进行处理，每3个字节一组，一共`3*8=24`bit，化为4组，每组正好6个bit
![Pasted image 20250321140836](images/Pasted%20image%2020250321140836.png)
这样我们可以得到4个数字作为索引，然后查表获得相应的4个字符，就是编码后的字符串

总的来说，就是Base64编码会把3字节的二进制数据编码为4字节的文本数据，长度增加为33%，好处是编码后的文本数据可以在邮件正文、网页等直接显示

- 如果要编码的二进制数据不是3的倍数，最后剩下1个或2个，Base64会用`\x00`字节在末尾补足后，再在编码的末尾加上1个或2个=号，表示补了多少字节，解码的时候会自动去掉

![Pasted image 20250321142410](images/Pasted%20image%2020250321142410.png)

- 假如要编码字符`+`和`/`，可以用“url safe”的base64编码，将+和/变成-和_

- Base64是一种通过查表来编码的方法，不能用于加密，即使使用自定义的编码表也不行
- Base64适用于小段内容的编码，例如数字证书签名、Cookie、网页中传输少量二进制数据的内容

- =也可能出现在Base64编码中，但是=用在URL、Cookie中会造成歧义，所以很多Base64编码后不会有=，如果不够4的倍数，我们认为加上即可
```plain
# 标准Base64:
'abcd' -> 'YWJjZA=='
# 自动去掉=:（有的会删掉，我们解码的时候人为加上就好）
'abcd' -> 'YWJjZA'
```
```python
import base64

def safe_base64_decode(s):
    #将字符串长度补齐为4的倍数
    padding_needed = 4 - (len(s) % 4)
    if padding_needed != 4: #需要补充'='
        s += '=' * padding_needed
    return base64.b64decode(s)
# 测试:
assert b'abcd' == safe_base64_decode('YWJjZA=='), safe_base64_decode('YWJjZA==')
assert b'abcd' == safe_base64_decode('YWJjZA'), safe_base64_decode('YWJjZA')
print('ok')
```

## struct
- Python没有专门处理字节的数据类型。但是`b'str'`可以表示字节，所以字节数组=二进制`str`。在C语言中，我们可以很方便的用`struct`、`union`来处理字节，以及字节和int，float的转换
- 在Python中将32为无符号整数变成字节（4个长度的bytes）
```plain
>>> n = 10240099
>>> b1 = (n & 0xff000000) >> 24
>>> b2 = (n & 0xff0000) >> 16
>>> b3 = (n & 0xff00) >> 8
>>> b4 = n & 0xff
>>> bs = bytes([b1, b2, b3, b4])
>>> bs
b'\x00\x9c@c'
```
 - 很麻烦，如果是浮点数，这种方法还不行

- `struct`的`pack`函数将任意数据类型变成`bytes`：
```plain
>>> import struct
>>> struct.pack('>I', 10240099)
b'\x00\x9c@c'
```
`pack`的第一个参数是处理指令，`>I`：`>`表示字节顺序是big-endian，即网络序，`I`表示4字节无符号整数
后面参数个数要和处理的指令一致

`unpack`把`bytes`变成相应的数据类型：
```plain
>>> struct.unpack('>IH', b'\xf0\xf0\xf0\xf0\x80\x80')
(4042322160, 32896)
```
根据`>IH`的说明，后面的`bytes`依次变为`I`：4字节无符号整数和`H`：2字节无符号整数。

尽管Python不适合编写底层操作字节流的代码，但在对性能要求不高的地方，利用`struct`就方便多了。

Windows的位图文件（.bmp）是一种非常简单的文件格式，我们来用`struct`分析一下。

首先找一个bmp文件，没有的话用“画图”画一个。

读入前30个字节来分析：

```plain
>>> s = b'\x42\x4d\x38\x8c\x0a\x00\x00\x00\x00\x00\x36\x00\x00\x00\x28\x00\x00\x00\x80\x02\x00\x00\x68\x01\x00\x00\x01\x00\x18\x00'
```

BMP格式采用小端方式存储数据，文件头的结构按顺序如下：

两个字节：`'BM'`表示Windows位图，`'BA'`表示OS/2位图； 一个4字节整数：表示位图大小； 一个4字节整数：保留位，始终为0； 一个4字节整数：实际图像的偏移量； 一个4字节整数：Header的字节数； 一个4字节整数：图像宽度； 一个4字节整数：图像高度； 一个2字节整数：始终为1； 一个2字节整数：颜色数。

所以，组合起来用`unpack`读取：

```plain
>>> struct.unpack('<ccIIIIIIHH', s)
(b'B', b'M', 691256, 0, 54, 40, 640, 360, 1, 24)
```

结果显示，`b'B'`、`b'M'`说明是Windows位图，位图大小为640x360，颜色数为24。

请编写一个`bmpinfo.py`，可以检查任意文件是否是位图文件，如果是，打印出图片大小和颜色数。

```python
import base64, struct
bmp_data = base64.b64decode('Qk1oAgAAAAAAADYAAAAoAAAAHAAAAAoAAAABABAAAAAAADICAAASCwAAEgsAA' +
                   'AAAAAAAAAAA/3//f/9//3//f/9//3//f/9//3//f/9//3//f/9//3//f/9//3//f/9//3/' +
                   '/f/9//3//f/9//3//f/9/AHwAfAB8AHwAfAB8AHwAfP9//3//fwB8AHwAfAB8/3//f/9/A' +
                   'HwAfAB8AHz/f/9//3//f/9//38AfAB8AHwAfAB8AHwAfAB8AHz/f/9//38AfAB8/3//f/9' +
                   '//3//fwB8AHz/f/9//3//f/9//3//f/9/AHwAfP9//3//f/9/AHwAfP9//3//fwB8AHz/f' +
                   '/9//3//f/9/AHwAfP9//3//f/9//3//f/9//38AfAB8AHwAfAB8AHwAfP9//3//f/9/AHw' +
                   'AfP9//3//f/9//38AfAB8/3//f/9//3//f/9//3//fwB8AHwAfAB8AHwAfAB8/3//f/9//' +
                   '38AfAB8/3//f/9//3//fwB8AHz/f/9//3//f/9//3//f/9/AHwAfP9//3//f/9/AHwAfP9' +
                   '//3//fwB8AHz/f/9/AHz/f/9/AHwAfP9//38AfP9//3//f/9/AHwAfAB8AHwAfAB8AHwAf' +
                   'AB8/3//f/9/AHwAfP9//38AfAB8AHwAfAB8AHwAfAB8/3//f/9//38AfAB8AHwAfAB8AHw' +
                   'AfAB8/3//f/9/AHwAfAB8AHz/fwB8AHwAfAB8AHwAfAB8AHz/f/9//3//f/9//3//f/9//' +
                   '3//f/9//3//f/9//3//f/9//3//f/9//3//f/9//3//f/9//3//f/9//38AAA==')

def bmp_info(data):
    return {
        'width': 200,
        'height': 100,
        'color': 24
    }

# 测试
bi = bmp_info(bmp_data)
assert bi['width'] == 28
assert bi['height'] == 10
assert bi['color'] == 16
print('ok')
```

## hashlib
- 提供了常见的哈希算法，如MD5，SHA1等等
- 哈希算法（摘要算法、散列算法）：通过一个函数将任意长度的数据转换为一个长度固定的数据串（通常用16进制的字符串表示）
- 这是一个单向函数，计算`digest=hash(data)`很容易，但是通过`digest`反推`data`十分困难。对原始数据做一个bit的修改都会导致哈希完全不同
- 以哈希算法MD5为例，计算出一个字符串的MD5
```python
import hashlib

md5 = hashlib.md5()
md5.update('how to use md5 in python hashlib?'.encode('utf-8'))
print(md5.hexdigest())
```
```plain
d26a53750bc40b38b65a520292f69306
```

- 也可以分块多次使用update效果和上面是一样的
```python
import hashlib

md5 = hashlib.md5()
md5.update('how to use md5 in '.encode('utf-8'))
md5.update('python hashlib?'.encode('utf-8'))
print(md5.hexdigest())
```
另一种常见的哈希算法是SHA1，调用SHA1和调用MD5完全类似：

```python
import hashlib

sha1 = hashlib.sha1()
sha1.update('how to use sha1 in '.encode('utf-8'))
sha1.update('python hashlib?'.encode('utf-8'))
print(sha1.hexdigest())
```

SHA1的结果是160 bit/20字节，通常用一个40位的16进制字符串表示。

比SHA1更安全的算法是SHA256和SHA512，不过越安全的算法不仅越慢，而且哈希长度更长。

- 应用：在数据库中数据库的密码部分存储密码的哈希，而不是明文（假如是MD5），存储MD5的好处是即使运维人员能访问数据库，也无法获知用户的明文口令。
当用户登录时，首先计算用户输入的明文口令的MD5，然后和数据库存储的MD5对比，如果一致，说明口令输入正确，如果不一致，口令肯定错误。
