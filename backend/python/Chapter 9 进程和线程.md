## 多进程
### 介绍
```python
import os
print('Process(%s) start...' % os.getpid())
# Only works on Unix/Linux/MacOS
pid = os.fork()
if pid == 0:
	print('I am child process (%s) and my parent is %s.' % (os.getpid(), os.getppid()))
else:
	print('I (%s) just created a child process (%s).' % (os.getpid(),pid))
```

![[Pasted image 20250314082525.png]]

- `os.fork()`：在Unix系统中用于创建子进程的系统调用
	- 调用这个方法后，当前进程会被复制成两个独立的进程：一个父进程一个子进程
	- 会返回两次，所以这句代码后的内容会执行两次，在父进程返回子进程ID，在子进程返回0
- `getpid()`：拿到父进程id
- `getppid()`：拿到子进程id
- 先在父进程返回子进程id进入else，此时的pid是子进程id
- 然后子进程pid为0进入if
- 有`fork`之后，一个进程接到新任务时就可以复制出一个子进程来处理新任务（常见的Apache服务器就是由父进程监听端口，每当有新的http请求时，就`fork`出子进程来处理新的http请求）
### multiprocessing
windows上没有fork调用，python提供跨平台支持，`multiprocessing`模块就是跨平台版本的多进程模块

- `multiprocessing`提供了一个`Process`类来代表一个进程对象
```python
from multiprocessing import Process
import os

# 子进程要执行的代码
def run_proc(name):
    print('Run child process %s (%s)...' % (name, os.getpid()))
    
if __name__=='__main__':
    print('Parent process %s.' % os.getpid())#当前进程id
    p = Process(target=run_proc, args=('test',))
    print('Child process will start.')
    p.start() #开始子进程
    p.join() #等待子进程结束后再继续往下运行，通常用于进程间的同步
    print('Child process end.')
```

### Pool
- 如果要启动大量的子进程，可以用进程池的方式批量创建子进程
```python
from multiprocessing import Pool
import os, time, random

def long_time_task(name): # 模拟长时间运行的任务
    print('Run task %s (%s)...' % (name, os.getpid()))
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print('Task %s runs %0.2f seconds.' % (name, (end - start)))

if __name__ == '__main__':
    print('Parent process %s.' % os.getpid())
    p = Pool(4)
    for i in range(5):
        p.apply_async(long_time_task, args=(i,)) #异步提交任务long_time_task到进程池，并传入参数i（任务名称）
    print('Waiting for all subprocess done...')
    p.close() #关闭进程池，禁止添加新任务
    p.join() #等待所有任务完成，阻塞主进程，直到进程池中所有任务完成
    print('All subprocesses done.')
```
![[Pasted image 20250314110927.png]]

- 对Pool对象调用`join()`方法会等待所有子进程执行完毕，调用`join()`之前先调用`close()`，调用完`close()`之后就不能加新的Process了
- 可以看到上面0123是立刻执行的，因为我们设定的是四个进程，task4要等前面某个task执行完后才能执行
- Pool的默认大小是CPU的核数

### 子进程
- 很多时候，子进程不是自身，而是一个外部进程。创建子进程后，还要控制子进程的输入和输出。
- 通过`subprocess`模块，我们可以非常方便地启动一个子进程，然后控制其输入输出。

```python
import subprocess

print('$ nslookup www.python.org') #打印提示信息，表明接下来执行的命令
r = subprocess.call(['nslookup', 'www.python.org']) #调用nslookup命令，参数是一个列表，此方法会阻塞程序执行，直到命令完成为止
print('Exit code:', r) #打印退出状态码，0表示成功，其他值表示执行过程中可能有错误
```

- 用`subprocess`模块调用系统命令`nslookup`来查询`www.python.org`的DNS信息
- 用`nslookup www.python.org`来查询`www.python.org`的IP地址或DNS信息，

![[Pasted image 20250314113532.png]]

- 如果子进程还需要输入，可以通过`communicate()`方法输入：
```python
import subprocess

print('$ nslookup')

#启动一个子进程，用来运行nslookup命令
p = subprocess.Popen(['nslookup'], stdin = subprocess.PIPE, stdout=subprocess.PIPE)
#stdin=subprocess.PIPE:打开子进程的标准输入管道，用于向子进程发送数据
#stdout=subprocess.PIPE:打开子进程的标准输出管道，用于读取子进程的输出

output, err = p.communicate(b'set q = mx\npython.org\nexit\n')
#p.communicate()：通过标准输入向nslookup进程发送指令
#set q = mx：告诉nslookup查询邮件交换记录（MX记录）
#python.org:要查询的域名
#exit：退出nslookup
#传入的数据必须是字节串（bytes），所以用b''
#返回值output：子进程的标准输出
#err：子进程的错误输出

print(output.decode('gbk'))
#将子进程返回的字节串输出output解码为字符串

print('Exit code:', p.returncode)
#p.returncode：获取子进程的退出状态码，正常完成返回0，非0表示发生错误
```

![[Pasted image 20250314130910.png]]

### 进程间通信
`Process`之间肯定需要进行通信。python的`multiprocessing`模块包装了底层的机制，提供了`Queue`、`Pipes`等多种方式来交换数据

以`Queue`为例，在父进程中创建两个子进程，一个往`Queue`里写数据，一个从`Queue`里读数据：
```python
from multiprocessing import Process, Queue
import os, time, random

# 写数据进程执行的代码：
def write(q):#q是共享的Queue
    print('Process to write: %s' % os.getpid())
    for value in ['A', 'B', 'C']:
        print('Put %s to queue...' % value)
        q.put(value) #将数据(A,B,C)放入队列
        time.sleep(random.random()) #模拟随机的耗时操作
# 读数据进程执行的代码：
def read(q):
    print('Process to read: %s' % os.getpid())
    while True:
        value = q.get(True) #从队列中获取数据，直到没有数据（阻塞模式）
        print('Get %s from queue.' % value) #打印读到的数据

if __name__ == '__main__':
    q = Queue() #创建一个进程间通信的队列
    pw = Process(target=write, args=(q,)) #创建写数据的子进程

    pr = Process(target=read, args=(q,)) #创建读数据的子进程
    #启动子进程pw，写入：
    pw.start()
    #启动子进程pr,读取：
    pr.start()
    #等待pw结束
    pw.join()
    #pr进程是死循环，无法等待其结束，只能强行终止：
    pr.terminate()
```
![[Pasted image 20250314141933.png]]

- 在Unix/Linux下，`multiprocessing`模块封装了`fork()`调用，我们不用关注`fork()`的细节。而Windows没有`fork`调用，因此，`multiprocessing`需要模拟出`fork`的效果，父进程所有Python对象都必须通过pickle序列化在传到子进程中序，所以如果`multiprocessing`在Windows下调用失败了，要先考虑是不是pickle失败了

- `fork`创建的子进程会继承父进程的所有资源，包括变量，内存等。这使得父子进程之间的状态是自然共享的，不需要额外的序列化或传递

- Windows中没有fork系统调用，`multiprocessing`必须通过`spawn`机制模拟出类似效果：
	- 在Windows上创建子进程是，`multiprocessing`会启动一个全新的Python解释器，并运行主模块的代码
	- 所以，父进程的所有资源（变量，函数等）必须显式传递到子进程，而不能像`fork`那样自然继承
	- 传递方式：通过`pickle`（一种序列化协议）将父进程中的对象序列化，再通过进程间的通信机制传递到子进程

- pickle是Python的序列化工具，有一定的限制
	- 可序列化：基本数据类型，实现了`__reduce__`、`__getstate__`方法的自定义对象
	- 不能序列化：打开的文件句柄、线程、进程、匿名函数(`lambda`)、非全局定义的函数
	- 如果 `multiprocessing` 在 Windows 上失败，通常是因为某些对象不能被 `pickle`，从而导致子进程无法正常接收这些对象。
- `Queue`的工作原理
	- `Queue` 是 `multiprocessing` 提供的进程间通信工具，它通过底层的管道（`Pipe`）实现。
	- 当父进程或子进程向队列中 `put` 一个对象时：
		- 该对象会被 `pickle` 序列化成字节流。
		- 然后通过底层的管道传递给另一端（另一个进程）。
		- 接收端通过 `pickle` 反序列化还原出原始对象。


- 在Unix/Linux下，可以使用`fork()`调用实现多进程
- 要实现跨平台的多进程，可以使用`multiprocessing`模块
- 进程间通信通过`Queue`、`Pipes`等实现

## 多线程
### 介绍
```python
import time, threading

#新线程执行的代码：
def loop():
    print('thread %s is running...' % threading.current_thread().name)
    n = 0
    while n < 5:
        n = n + 1
        print('thread %s >>> %s' % (threading.current_thread().name, n))
        time.sleep(1)
    print('thread %s ended.' % threading.current_thread().name)

print('thread %s is running...' % threading.current_thread().name)
t = threading.Thread(target=loop, name='LoopThread')
t.start()
t.join()
print('thread %s ended.' % threading.current_thread().name)
```
![[Pasted image 20250314162928.png|600]]

如果没有取LoopThread的名字，就是默认的Thread-1，如果还有其他线程就是Thread-2....

### Lock
- 多进程中，同一个变量，各自有一份拷贝存在于每个进程中，互不影响；
- 多线程中，所有变量都由所有线程共享，所以，任何一个变量都可以被任何一个线程修改，因此，线程之间共享数据最大的危险就是多个线程同时改一个变量，把内容改乱了
```python
# multithread
import time, threading

# 假定这是你的银行存款:
balance = 0

def change_it(n):
    # 先存后取，结果应该为0:
    global balance
    balance = balance + n
    balance = balance - n

def run_thread(n):
    for i in range(10000000):
        change_it(n)

t1 = threading.Thread(target=run_thread, args=(5,))
t2 = threading.Thread(target=run_thread, args=(8,))
t1.start()
t2.start()
t1.join()
t2.join()
print(balance)
```
- 理论上是0，但是线程的调度是操作系统决定的，当t1,t2交替执行时，只要循环的次数够多，balance的结果就不一定是0了
- 两个线程同时执行这个程序，同时一存一取容易出问题，所以我们需要确保一个线程在修改`balance`的时候，别的线程一定不能改

- 为了确保balance计算正确，就需要给`change_it()`上锁，使其不能和其他线程同时执行，只能等锁被释放之后获得锁以后才能改，只有一个锁，最多只有一个线程拿到锁。
- 通过`threading.Lock()`来创建锁
```python
# multithread
import time, threading

# 假定这是你的银行存款:
balance = 0
lock = threading.Lock() #锁变量

def change_it(n):
    # 先存后取，结果应该为0:
    global balance
    balance = balance + n
    balance = balance - n

def run_thread(n):
    for i in range(10000000):
        #先获取锁
        lock.acquire()
        try:
            change_it(n)
        finally:
            #改完了要记得释放锁：
            lock.release()

t1 = threading.Thread(target=run_thread, args=(5,))
t2 = threading.Thread(target=run_thread, args=(8,))
t1.start()
t2.start()
t1.join()
t2.join()
print(balance)
```

- 注意：获取锁之后一定要释放锁，否则后面的线程会一直等这个锁，成为死线程，所以使用锁的时候最好使用`try...finally`确保锁一定会被释放
- 锁的好处时确保某段代码只能由一个线程从头到尾完整执行（单线程），但是效率下降。
- 可以同时存在多个锁，不同的线程有不同的锁，并试图获取对方持有的锁时，可能会造成死锁，导致多个线程全部挂起。既不能执行，也无法结束，只能靠操作系统强制终止

### 多核CPU
- 如果写一个死循环，可以从任务管理器看到，一个死循环线程会100%占用一个CPU。
- 如果有两个死循环线程，在多核CPU中，会占用200%的CPU，
- 用python写一个死循环
```python
import threading, multiprocessing

def loop():
    x = 0
    while True:
        x = x ^ 1

for i in range(multiprocessing.cpu_count()):
    t = threading.Thread(target=loop)
    t.start()
```

启动与cpu核心相同的N个线程，在4核CPU上可以监控到CPU占用率仅有102%，也就是仅使用了一核。（但是如果用C、C++、Java来写相同的死循环，直接可以把全部核心跑满，4核就会跑到400%...）

- 原因是Python的线程虽然是真正的线程，但是解释器执行代码时，有一个GIL锁：Global Interpreter Lock，任何Python线程执行前，必须获得GIL锁，让别的线程有机会执行。这个GIL全局锁实际上把所有线程的执行代码都上了锁，所以多线程在Python中只能交替执行，即使100个线程跑在100核CPU上，也只用到一个核

- GIL是Python解释器设计的历史遗留问题，通常我们用的解释器是官方实现的CPython，要真正利用多核，除非重写一个不带GIL的解释器。

- 所以，在Python中，可以使用多线程，但不要指望能有效利用多核。如果一定要通过多线程利用多核，那只能通过C扩展来实现，不过这样就失去了Python简单易用的特点。

- 不过，Python虽然不能利用多线程实现多核任务，但可以通过多进程实现多核任务。多个Python进程有各自独立的GIL锁，互不影响。

## ThreadLocal
- 在多线程环境下，每个线程有自己的数据。一个线程使用自己的局部变量好于使用全局变量，因为局部变量只有线程自己能看见，不会影响其他线程，而全局变量的修改必须加锁
- 但是局部变量在函数调用的时候传递起来很麻烦

```python
def process_student(name):
    std = Student(name)
    # std是局部变量，但是每个函数都要用它，因此必须传进去：
    do_task_1(std)
    do_task_2(std)

def do_task_1(std):
    do_subtask_1(std)
    do_subtask_2(std)

def do_task_2(std):
    do_subtask_2(std)
    do_subtask_2(std)
```

- 如果每个函数一层一层调用都这么传参很麻烦，用全局变量也不行，因为每个线程处理不同的`Student`对象，不能共享

- 如果用一个全局`dict`存放所有的`Student`对象，然后以`thread`自身作为`key`获得线程对应的`Student`对象
```python
global_dict = {}

def std_thread(name):
    std = Student(name)
    # 把std放到全局变量global_dict中：
    global_dict[threading.current_thread()] = std
    do_task_1()
    do_task_2()

def do_task_1():
    # 不传入std，而是根据当前线程查找：
    std = global_dict[threading.current_thread()]
    ...

def do_task_2():
    # 任何函数都可以查找出当前线程的std变量：
    std = global_dict[threading.current_thread()]
    ...
```
- 这种方式理论上是可行的，最大的优点是消除了`std`对象在每层函数中的传递问题，但是，每个函数获取`std`的代码有点丑

- 有一个更简单的方式，使用`ThreadLocal`，不用查找dict，`ThreadLocal`会自动帮我们处理
```python
import threading
    
# 创建全局ThreadLocal对象:
local_school = threading.local()

def process_student():
    # 获取当前线程关联的student:
    std = local_school.student
    print('Hello, %s (in %s)' % (std, threading.current_thread().name))

def process_thread(name):
    # 绑定ThreadLocal的student:
    local_school.student = name
    process_student()

t1 = threading.Thread(target= process_thread, args=('Alice',), name='Thread-A')
t2 = threading.Thread(target= process_thread, args=('Bob',), name='Thread-B')
t1.start()
t2.start()
t1.join()
t2.join()
```
```plain
Hello, Alice (in Thread-A)
Hello, Bob (in Thread-B)
```

- 全局`local_school`就是一个`ThreadLocal`对象，每个`Thread`对它都可以读写`student`属性，但互不影响。
- 可以将`local_school`看成全局变量，但每个属性如`local_school.student`都是线程的局部变量，可以任意读写而互不干扰，也不用管理锁的问题，`ThreadLocal`内部会处理

- 可以将全局变量`local_school`是一个`dict`，不仅可以用`local_school.student`，还可以绑定其他变量，如`local_school.teacher`等等
- 常用：为每一个线程绑定一个数据库连接，HTTP请求，用户身份信息等，这样一个线程的所有调用到的处理函数都可以非常方便地访问这些资源

## 进程 vs 线程
### 比较
- 多进程：
	- 稳定性高，一个进程崩溃了不会影响到其他进程（如果主进程没了也还是都没了的，但是主进程只负责分配任务，出问题的可能性比较小），Apache最早就是采用多进程模式
	- 创建进程的代价大，Unix等用fork调用还好，如果是Windows下开销巨大，而且操作系统能同时运行的进程数也是有限的，在内存和CPU的限制下，如果有几千个进程同时运行，操作系统调度都会出问题
- 多线程：
	- 比多进程快一点，但是快不到哪去
	- 一个线程没了，整个进程就没了（Windows上“该程序执行了非法操作，即将关闭”一般是某个线程出了问题）
	- 在Windows下，多线程的效率比多进程高，所以微软的IIS服务器默认采用多线程模式，但稳定性不如Apache

### 线程切换
- 无论多进程还是多线程，只要数量一多，效率还是上不去

- 单任务模型（批处理任务模型）：做完一个再进行下一个
- 多任务模型：切换任务也有代价
	- 保存当前执行的现场环境(CPU寄存器状态、内存页等)-->准备新任务的执行环境(恢复上次的寄存器状态，切换内存页)-->开始执行
	- 这个切换的过程虽然很快，但是也耗费时间。如果有几千个任务同时进行，操作系统可能光忙着切换任务而没有时间去执行任务
	- 一般是硬盘狂响，点窗口无反应，系统处于假死状态
- 所以，多任务一旦多到一个限度，就会消耗掉系统所有的资源，效率急剧下降

### 计算密集型 vs IO密集型
- 是否采用多任务的第二个考虑是任务的类型，可以将任务分为计算密集型

- 计算密集型：
	- 要进行大量的计算，消耗CPU资源（计算圆洲路，对视频进行高清解码，靠CPU的运算能力）
	- 可以用多任务完成，但是任务越多花在切换任务的时间越多，效率越低，所以计算密集型任务同时进行的数量应当等于CPU的核心数
	- 主要消耗CPU资源，所以代码运行效率很重要。Python这样的脚本语言运行效率低，不适合计算密集型任务，对于计算密集型任务最好使用C语言
- IO密集型：
	- 涉及到网络、磁盘IO的任务，常见的大部分任务都是IO密集型任务，比如Web应用
	- CPU消耗少，任务的大部分时间都在等待IO操作完成（因为IO的速度远远低于CPU和内存的速度）
	- 任务越多，CPU效率越高（有限度）。
	- 这种任务执行时，99%时间都花在IO上，花在CPU上的时间很少，所以用C语言无法提升效率，这种类型最好使用开发效率高（代码量最少）的语言，脚本语言是首选，C语言开发效率差

### 异步IO
- 现代操作系统对IO操作已经做了巨大的改进，最大的特点就是支持异步IO。
- 如果充分利用操作系统提供的异步IO支持，就可以用单进程单线程模型来执行多任务，这种模型也叫事件驱动模型
- Nginx就是支持异步IO的Web服务器，它在单核CPU上采用单进程模型就可以高效地支持多任务。
- 在多核CPU上，可以运行多个进程（数量与CPU核心数相同），充分利用多核CPU。
- 用异步IO编程模型来实现多任务是一个主要趋势（进程有限，要求操作系统的调度非常高效）

- 对应到Python语言，单线程的异步编程模型称为协程，有了协程的支持，就可以基于事件驱动编写高效的多任务程序

## 分布式进程（之后看）
- 在Thread和Process中，应当优先Process（更稳定），而且，Process可以分布到多台机器上，而Thread最多只能分布到一台机器的多个CPU上。

- Python的`multiprocessing`模块不但支持多进程，其中`managers`子模块还支持把多进程分布到多台机器上。
- 一个服务进程可以作为调度者，将任务分布到其他多个进程中，依靠网络通信。由于`managers`模块封装很好，不用了解网络通信的细节，就可以很容易的编写分布式多进程程序。

- 例子：假如我们已经有一个通过`Queue`通信的多进程程序在同一台机器上运行，现在由于处理任务的进程任务繁重，希望把发送任务的进程和处理任务的进程分布到两台机器上，如何进行分布式进程实现？

- 原来的`Queue`可以继续用，但是通过`managers`模块把`Queue`通过网络暴露出去，就可以让其他机器的进程访问`Queue`了

```python
# task_master.py
#在win上会出错
import random, time, queue
from multiprocessing.managers import BaseManager

# 发送任务的队列:
task_queue = queue.Queue()
# 接收结果的队列:
result_queue = queue.Queue()

# 从BaseManager继承的QueueManager:
class QueueManager(BaseManager):
    pass

# 把两个Queue都注册到网络上, callable参数关联了Queue对象:
QueueManager.register('get_task_queue', callable=lambda: task_queue)
QueueManager.register('get_result_queue', callable=lambda: result_queue)
# 绑定端口5000, 设置验证码'abc':
manager = QueueManager(address=('', 5000), authkey=b'abc')
# 启动Queue:
manager.start()
# 获得通过网络访问的Queue对象:
task = manager.get_task_queue()
result = manager.get_result_queue()
# 放几个任务进去:
for i in range(10):
    n = random.randint(0, 10000)
    print('Put task %d...' % n)
    task.put(n)
# 从result队列读取结果:
print('Try get results...')
for i in range(10):
    r = result.get(timeout=10)
    print('Result: %s' % r)
# 关闭:
manager.shutdown()
print('master exit.')
```

任务进程要通过网络连接到服务进程，所以要指定服务进程的IP。

现在，可以试试分布式进程的工作效果了。先启动`task_master.py`服务进程：

```plain
$ python3 task_master.py 
Put task 3411...
Put task 1605...
Put task 1398...
Put task 4729...
Put task 5300...
Put task 7471...
Put task 68...
Put task 4219...
Put task 339...
Put task 7866...
Try get results...
```

`task_master.py`进程发送完任务后，开始等待`result`队列的结果。现在启动`task_worker.py`进程：

```plain
$ python3 task_worker.py
Connect to server 127.0.0.1...
run task 3411 * 3411...
run task 1605 * 1605...
run task 1398 * 1398...
run task 4729 * 4729...
run task 5300 * 5300...
run task 7471 * 7471...
run task 68 * 68...
run task 4219 * 4219...
run task 339 * 339...
run task 7866 * 7866...
worker exit.
```

`task_worker.py`进程结束，在`task_master.py`进程中会继续打印出结果：

```plain
Result: 3411 * 3411 = 11634921
Result: 1605 * 1605 = 2576025
Result: 1398 * 1398 = 1954404
Result: 4729 * 4729 = 22363441
Result: 5300 * 5300 = 28090000
Result: 7471 * 7471 = 55815841
Result: 68 * 68 = 4624
Result: 4219 * 4219 = 17799961
Result: 339 * 339 = 114921
Result: 7866 * 7866 = 61873956
```

这个简单的Master/Worker模型有什么用？其实这就是一个简单但真正的分布式计算，把代码稍加改造，启动多个worker，就可以把任务分布到几台甚至几十台机器上，比如把计算`n*n`的代码换成发送邮件，就实现了邮件队列的异步发送。

Queue对象存储在哪？注意到`task_worker.py`中根本没有创建Queue的代码，所以，Queue对象存储在`task_master.py`进程中：
![[Pasted image 20250314211007.png]]
而`Queue`之所以能通过网络访问，就是通过`QueueManager`实现的。由于`QueueManager`管理的不止一个`Queue`，所以，要给每个`Queue`的网络调用接口起个名字，比如`get_task_queue`。

`authkey`有什么用？这是为了保证两台机器正常通信，不被其他机器恶意干扰。如果`task_worker.py`的`authkey`和`task_master.py`的`authkey`不一致，肯定连接不上。

### 小结

Python的分布式进程接口简单，封装良好，适合需要把繁重任务分布到多台机器的环境下。

注意Queue的作用是用来传递任务和接收结果，每个任务的描述数据量要尽量小。比如发送一个处理日志文件的任务，就不要发送几百兆的日志文件本身，而是发送日志文件存放的完整路径，由Worker进程再去共享的磁盘上读取文件。