## Part 1 介绍
- 多线程
### Section 1 核、线程、进程
- 提出问题：一台计算机为什么能执行多个程序，怎么执行多个程序？
- CPU：中央处理器
- 单核cpu一个脑子不能多用，就切换着用（挂起（暂停））：表面上是同时运行，实际上是切换的快
- 多个cpu就多个一起用
![Pasted image 20241127222625](images/Pasted%20image%2020241127222625.png)
可以在英特尔官网上看到这是12核16线程，这里的12核就相当于是有12个脑子

一个核操纵两个程序，通过来回切换来使用，假如说一个软件一个进程，使用其中一个程序就需要挂起另一个程序的进程（实际上一个软件还可能占用多个进程，如下图，任务管理器占用一个进程，C++blabla占用多个进程）![Pasted image 20241127223336](images/Pasted%20image%2020241127223336.png)
线程：一个程序给多个人用
[[核,线程关系.excalidraw|核，进程，线程关系]]

### Section 2 进程和线程的区别
1. 进程和线程差别主要在于他们是不同的操作系统资源管理方式，
2. 进程有独立的地址空间，一个进程崩溃后不会对其他进程产生影响，
3. 线程只是一个进程中的不同执行路径，线程有自带的堆栈和局部变量，但线程之间没有单独的地址空间，一个线程死掉就等于整个进程死掉，所以多进程的程序要比多线程的程序健壮，但在进程切换时，耗费资源较大效率要差一些，对于*一些要求同时进行并且要共享某些变量的并发操作，只能用线程，不能用进程*

- 注意事项
1. 进程在执行过程中拥有独立的内存单元，而线程共享内存，极大的提高了程序运行效率
2. 线程划分尺度小于进程，使得多线程程序并发性高？
3. 一个程序最少一个进程，一个进程最少一个线程
4. 每个独立的线程有一个程序运行的入口（多个线程多个main），顺序执行序列和程序出口（谁先进谁先出，谁先进的快谁就拿到进程给的资源）
5. 线程不能够独立执行必须依存在应用程序中，由应用程序提供多个线程执行控制

也就是说系统给到多个线程的资源是一样的，这一组的多个线程共享资源，而不是系统独立分配资源给他

### Section 3 并发与并行
- 并发：在有限的核心和有限的进程中如何运行多个应用程序（来回切换）
- 并行：一个核执行一个线程，另一个核执行另一个线程
![Pasted image 20241127231027](images/Pasted%20image%2020241127231027.png)

## Part 2 多线程执行
[[多线程的执行.excalidraw|多线程执行示意图]]
### Section 1 方式1（单继承）
- 单线程
```java
-ExhaleThread.java
public class ExhaleThread extends Thread{  
    @Override  
    public void run(){  
        while(true) {  
            System.out.println("ExhaleThread......");  
        }  
    }  
}
-main
public static void main(String[] args) {  
//java.lang.Thread 多线程的类  
    ExhaleThread exhaleThread = new ExhaleThread();  
    exhaleThread.run(); 
    while(true){  
System.out.println("main..d.....Thread...."); 
    }  
}
```

- 上面的代码会进入一直输出ExhaleThread......的死循环，而不会输出main..d.....Thread....

- 使用start()开启多线程
```java
-main
public static void main(String[] args) {  
//java.lang.Thread 多线程的类  
    ExhaleThread exhaleThread = new ExhaleThread();  
    exhaleThread.start(); //start()会多开启一个线程，然后自动调用run
    while(true){  
System.out.println("main..d.....Thread...."); 
    }  
}
```
start()会自动调用run()
这里的输出就是ExhaleThread......和main..d.....Thread....交替者输出，会有两个线程执行

### Section 2 方式2（接口）
java是单继承，使用多线程时需要继承Thread类，如果还需要继承其他类，就不行，这时候就要用到接口

使用接口的方法来实现多线程需要创建一个线程，再将实现Runnable接口的实例放进去
```java
-ExhaleThread.java
public class ExhaleThread implements Runnable{  
    @Override  
    public void run() {  
        while(true){  
            System.out.println("ExhaleThread......");  
        }  
    }  
}
-main
public static void main(String[] args) {  
//java.lang.Thread 多线程的类  
    ExhaleThread exhaleThread = new ExhaleThread();  
    Thread thread = new Thread(exhaleThread);//这里要创建一个线程 
    thread.start();  
    while(true){      System.out.println("main..d.....Thread...."); 
    }  
}
```

- 输出当前线程名字
```java
-ExhaleThread.java
public class ExhaleThread implements Runnable{  
    @Override  
    public void run() {  
        while(true){  
            System.out.println("ExhaleThread......" + Thread.currentThread().getName());  
        }  
    }  
}
-main
public static void main(String[] args) {  
//java.lang.Thread 多线程的类  
    ExhaleThread exhaleThread = new ExhaleThread();  
    new Thread(exhaleThread,"Exhale_Thread_1").start();  
    while(true){  
System.out.println("main..d.....Thread...."); 
    }  
}
```
![Pasted image 20241204211806](images/Pasted%20image%2020241204211806.png)

### Section 3 方式3 （匿名内部类）
```java
public static void main(String[] args) {  
    new Thread(new Runnable() {//new Runnable()换为() ->，jdk7一下不行  
        @Override  
        public void run() {  
            while(true){  
                System.out.println(Thread.currentThread().getName());  
            }  
        }  
    }).start();  
    while (true){  
        System.out.println("main......Thread...");  
    }  
}
```
### Section 4 实际案例
四个人抢鞋，多线程就是对共有资源进行抢占，无顺序；单继承的方式在这不适用，它一次创建一个类只能表示一个人，而这里有四个人，在加上需要循环抢占。
```java
-NikeThread.java
public class NikeThread implements Runnable {  
    private int nike = 100;  
    @Override  
    public void run() {  
        while(true){  
            if(nike > 0){  
                System.out.println(Thread.currentThread().getName() + "抢到了第" + (nike--) + "双鞋");  
            }  
        }  
    }  
}
-main
public static void main(String[] args) {  
//java.lang.Thread 多线程的类  
    NikeThread nikeThread = new NikeThread(); 
    new Thread(nikeThread,"Exhale").start();  
    new Thread(nikeThread,"Jack").start();  
    new Thread(nikeThread,"Frank").start();  
    new Thread(nikeThread,"Alice").start();  
}
```
![Pasted image 20241204212915](images/Pasted%20image%2020241204212915.png)

### Secition 5 后台守护线程
我们使用电脑可以发现进程有前台的也有后台的，如下：上面的就是前台的进程，下面就是后台的进程![Pasted image 20241204213314](images/Pasted%20image%2020241204213314.png)
- 那么相对应的，应该也存在前台的线程和后台的线程
```java
-DamonThread.java
public class DamonThread implements Runnable{  
    @Override  
    public void run() {  
        System.out.println("守护线程......");  
    }  
}
-main
public static void main(String[] args) {  
//java.lang.Thread 多线程的类  
    NikeThread nikeThread = new NikeThread(); 
    DamonThread damonThread = new DamonThread();//要先创建，守护线程优先于前台线程  
    //后台线程 -- 守护线程，用方法将普通线程变成守护线程  
    Thread dThread = new Thread(damonThread); 
    dThread.setDaemon(true);  
    dThread.start();//注意一定要放在前台线程的前面  
    //前台线程  
    new Thread(nikeThread,"Exhale").start();  
    new Thread(nikeThread,"Jack").start();  
    new Thread(nikeThread,"Frank").start();  
    new Thread(nikeThread,"Alice").start();  
}
```
![Pasted image 20241204214130](images/Pasted%20image%2020241204214130.png)

- 判断是否是守护线程
`System.out.println(dThread.isDaemon());`




