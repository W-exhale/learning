![[OOP上.png]]
## 问题的产生和引导
- 伪代码
即不写全的代码，有一个大概的逻辑框架。

程序的编写，讲究顺序。“过程”
1. 思考一些过程
2. 思考第一步怎么做
3. 思考第二步怎么做
4. 接着怎么做
5. ...
6. 最后怎么做（return 0）

## OOP与POP
- POP语言：面向过程（从main开始）
你想做一个事情然后再去做一件事情...，这就是过程。

走一步看一部的过程：没有目标没有理想的咸鱼
缺点：目标不明确，不适用于大众。

- OOP语言：面向对象
1. 该程序，要大众化
2. 有目标
3. 不强调过程

例如：明确目标——Java工程师
规划一下——设计它，
当你执行完计划的时候——达到目标了

OOP：站在更高的层面看待事物
（设计一个总的方案）
## 实操（实例）
比如说设计一个狗管理程序

![[Pasted image 20240708221727.png]]

- 对象（object）与实例的区别（差不多）
```java
//对象--实例 
//对象：对象可能要大于实例
//实例：现实生活中的一个东西，对抽象的东西进行表示出来的产物，是唯一的，比如说张大爷家的狗就是一个实例。

Dogs zhangDog = new Dogs();  
  
zhangDog.name = "jerry";  
zhangDog.age = 2;  
zhangDog.variety = "拉布拉多";
```

## 一些概念
### 类（class）
- 类：如下就是一个关于狗的类，程序中的狗都具有这种属性（特性，共性）
`public class Dogs {}`
- 类当中的变量和方法都称为属性。
### 成员变量
- 类当中的变量称为“成员变量”：它们组成和构成类，所以我们这 么命名。
```java
public String name;  
public String variety;  
public int age;  
public String food;
```
- 类中的方法叫“行为”
```java
public void eat(){  
    System.out.println("吃饭！");  
}
```
### this
- this：表示调用对象
```java
public void eat(){  
    System.out.println(this.name + "吃饭！");  
}
```
---
`zhangDog.eat();`
输出：Jerry吃饭！
- 串用
```java
public void eat(){  
    System.out.println("吃饭！");  
}  
public void sleep(){  
    System.out.println(this.name + "狗睡觉");  
    this.eat();  
}
```
## 空指针异常（NullPointerException）
```java
zhangDog.name = "jerry";  
zhangDog.age = 2;  
zhangDog.variety = "拉布拉多";  
  //账户注销
zhangDog = null;  
System.out.println("zhangDog name=" + zhangDog.name);
```
上述代码就会出现空指针异常的情况，zhangDog指向了一个对象，账户注销后，对象就没了，找不到了，zhangDog指向了一个null

## OOP封装
- 对年龄范围的限制（使用private）
主线程：
```java
zhangDog.setAge(2);  
System.out.println(zhangDog.getAge());
```
Dog.java程序
```java
private int age;
public void setAge(int age) { 
	if(age < 0 || age > 100){
    this.age = 0;  
    }else{
	    this.age = age;
    }
}  
public int getAge() {  
    return age;  
}
```

- 上述方式就是oop的封装（使用private）
对每一个private的成员变量都设置两个方法（getset），可以避免用户的不合法输入，甚至可以对用户的一些信息进行检查。
当设置的成员变量很多时，可以使用快捷方式一键生成所有成员变量的getset。

win使用alt+insert+（fn），选择geter and setter快捷生成。
或者使用另一种方式：@getter and@setter有一个叫lombok(赋值方法)的jar包，可以在官网上看如何在idea上安装使用，这样就不用每个成员变量后面跟两个方法

## jar导入、class和lombook

安装插件
settings->plugins->搜索lombok,下载
在Dog.java文件中输入：
`@Getter`
`@Setter`
再点击Alt+enter（这时还不能用，会报错）

- 需要添加lombok依赖：
搜索maven 库（repository），点击进入后，搜索lombok，下载自己需要的jar包
1. 可以通过maven引入
2. 也可以下载jar压缩包来引入
	1. 右击项目名new Directory，取名jar（都行）
	2. 加下载的jar包拖到jar文件夹里
	3. 右击jar文件（不是文件夹），点击add as library，在弹出的窗口选择Project Library

导入成功后就可以用了，先要`import lombok.Getter;`导包，将鼠标光标分别放在`@Getter`，`@Setter`按alt+enter可以快速导包

- 出错
lombok找不到符号
setting->build,...->Annotation Process->勾起Enable annotation processing->点击build中的rebuild project

如果是由特殊要求的方法，还是要但单独写（方法的重写）
- 注意：`@Getter @Setter`并列与某个成员变量写在同一行的时候就只对这一个变量起作用
```java
@Getter @Setter private int age;
```

所以一般`@Getter @Setter`写在类上面
```java
@Getter
@Setter
public class Dogs{}
```

### classpath
`classpath`是JVM用到的一个环境变量，它用来指示JVM如何搜索`class`。

因为Java是编译型语言，源码文件是`.java`，而编译后的`.class`文件才是真正可以被JVM执行的字节码。因此，JVM需要知道，如果要加载一个`abc.xyz.Hello`的类，应该去哪搜索对应的`Hello.class`文件。

事实上，根本不需要告诉JVM如何去Java核心库查找`class`，系统默认当然是知道在哪的

>[!WARNING] 注意
 >不要把任何Java核心库添加到classpath中！JVM根本不依赖classpath加载核心库！

更好的做法是，不要设置`classpath`！默认的当前目录`.`对于绝大多数情况都够用了。

### jar包
如果有很多`.class`文件，散落在各层目录中，肯定不便于管理。如果能把目录打一个包，变成一个文件，就方便多了。

jar包就是用来干这个事的，它可以把`package`组织的目录层级，以及各个目录下的所有文件（包括`.class`文件和其他文件）都打成一个jar文件，这样一来，无论是备份，还是发给客户，就简单多了。

jar包实际上就是一个zip格式的压缩文件，而jar包相当于目录。如果我们要执行一个jar包的`class`，就可以把jar包放到`classpath`中：

```plain
java -cp ./hello.jar abc.xyz.Hello
```

这样JVM会自动在`hello.jar`文件里去搜索某个类。

- 如何创建jar包？

因为jar包就是zip包，所以，直接在资源管理器中，找到正确的目录，点击右键，在弹出的快捷菜单中选择“发送到”，“压缩(zipped)文件夹”，就制作了一个zip文件。然后，把后缀从`.zip`改为`.jar`，一个jar包就创建成功。

假设编译输出的目录结构是这样：

```
package_sample
└─ bin
   ├─ hong
   │  └─ Person.class
   │  ming
   │  └─ Person.class
   └─ mr
      └─ jun
         └─ Arrays.class
```

这里需要特别注意的是，jar包里的第一层目录，不能是`bin`，而应该是`hong`、`ming`、`mr`。如果在Windows的资源管理器中看，应该长这样：

![hello.zip.ok](https://liaoxuefeng.com/books/java/oop/basic/classpath-jar/good-jar.jpg)

如果长这样：

![hello.zip.invalid](https://liaoxuefeng.com/books/java/oop/basic/classpath-jar/bad-jar.jpg)

上面的`hello.zip`包含有`bin`目录，说明打包打得有问题，JVM仍然无法从jar包中查找正确的`class`，原因是`hong.Person`必须按`hong/Person.class`存放，而不是`bin/hong/Person.class`。

jar包还可以包含一个特殊的`/META-INF/MANIFEST.MF`文件，`MANIFEST.MF`是纯文本，可以指定`Main-Class`和其它信息。JVM会自动读取这个`MANIFEST.MF`文件，如果存在`Main-Class`，我们就不必在命令行指定启动的类名，而是用更方便的命令：

```plain
java -jar hello.jar
```

在大型项目中，不可能手动编写`MANIFEST.MF`文件，再手动创建jar包。Java社区提供了大量的开源构建工具，例如[Maven](https://liaoxuefeng.com/books/java/maven/index.html)，可以非常方便地创建jar包。


## 构造方法
### 什么是构造方法
- 比如用户注册时，使用：
```java
Dogs zhangDog = new Dogs();
zhangDog.setAge(2);  
zhangDog.setName("jerry");  
zhangDog.setVariety("拉布拉多");
```
这种方式还是不恰当，类似于先定义后使用，这段代码想表达的意思是：
1. 用户创建了一个新账户，然后再补充资料
2. 注册完成之后再补充资料

如果我们想使用初始化的方式，
- 在Dog.java文件中
可以快捷生成alt+insert选择construct（不要加类型）
```java
public Dogs(String name, String variety, int age) {  
    this.name = name;  
    this.variety = variety;  
    this.age = age;  
}
```
- main中
`Dogs zhangDog = new Dogs("jerry","拉布拉多",2);`
上面这种方法称为构造方法

在new一个对象的时候，（类似于定义的那个）会有一个构造方法出现，但是它不显示：`public Dogs(){}`，这是默认创建的，只要创建类，就存在无参数构造函数（无参构造器）

- 构造器的作用：初始化对象（实例） 

### 构造方法的重载

[[基础知识#方法重载|重载]]
```java
public Dogs(){  
}
public Dogs(String name, String variety, int age) {  
    this.name = name;  
    this.variety = variety;  
    this.age = age;  
}  
  
public Dogs(String name, String variety) {  
    this.name = name;  
    this.variety = variety;  
}
```
在初始化的时候就可以使用无参数，两个参数，三个参数

## 垃圾回收机制
- 之前用过的一种方法可行，但是不太好，并没有真正的释放内存
`zhangDog = null;`

- 使用函数：`System.gc();`就可以释放（垃圾回收机制）
一般来说是会自动垃圾回收的，如果我们想手动回收，就使用上述方式

java 提供了一个系统级的线程，即垃圾收集器（garbage collection），来跟踪每一块分配出去的内存空间，当java虚拟机处于空闲循环时，garbage collection 会自动检查每一块分出去的内存空间，然后自动回收每一块可以回收的无用的内存块。

## static
建立在类的基础上
### 静态变量和静态方法
假设使用这个东西的人都在同一个小区(plot)
```java
-Dog.java的文件
//小区名  
public static String plot = "NanG";
-main
System.out.println("Dogs.plot = " + Dogs.plot);
```
NanG小区不属于某一个对象，是属于这个类(Dog)的
这个小区名plot就是静态变量。
- 假如说所有dog都要打疫苗，那么这时可以使用静态方法进行设计，所有的狗都有的
```java
-Dog.java
public static void injection(){  
    System.out.println("所有狗月底打疫苗");  
}
-main
Dog.injection();
```
即使将实例注销，该功能还是有，因为是直接用类名进行访问的。

### private static
- public static 容易出现问题，可以在main中修改public的值，上述例子就可以把小区名改掉。

如果要用private,就要使用get方法，进行oop封装
- 我们可以通过对象（zhangDog）来调取`zhangDog.getPlot()`（如果使用了@getter，可以不在Dog.java中写，直接用（不同的getter不太一样感觉是有的可以有的不行，待验证）），但是这样就不符合我们的目的——即通过类名来调用
这里的getplot和下面的不一样

- 所以这里要使用另一种方法（用了这种方法就不能通过对象调用小区名）
```java
Dog.java
private static String plot = "NanG";  
public static String getPlot() {  
    return plot;  
}
-main
System.out.println("Dogs.plot = " + Dog.getPlot());
```
-好处就是与类相关，与对象无关，即使没有对象它也存在，静态的就不用写this

- （看书）先加载静态代码块，只会加载一次...（使用static，在内存中只有一次）
### static 单例模式
-创建一个类earth
```java
-Earth.java
public class Earth {  
    private static Earth earthInstance = new Earth();  
  
    private Earth(){  
    }  
  
    public static Earth getInstance() {  
        return earthInstance;  
    }  
	public void hello(){  
	    System.out.println("hello!");  
	}
}
-main
Earth earth = Earth.getInstance();  
earth.hello();
```

- 注意：主线程中的earth只有一个，不可以
```java
Earth earth1 = new Earth();  
Earth earth2 = new Earth();
```
只有一个地球，只能通过前面那种方式定义，不能new两个，这就是static的单例设计模式，关键在于`private Earth(){}  `这句，只有一次new的机会

### 静态初始化器　
静态初始化器是由关键字static引导的一对大括号括起的语句组。它的作用与类的构造函数有些相似，都用来完成初始化的工作，但是静态初始化器与构造函数有三点根本的不同：  
　　(1)构造函数是对每个新创建的对象初始化，而静态初始化器是对每个类进行初始化；  
　　(2)构造函数是在用new运算符产生新对象时由系统自动执行，而静态初始化器则是在它所属的类加载入内存时由系统调用运行的；  
　　(3)不同于构造函数，静态初始化器不是方法，没有方法名、返回值和参数列表。

静态初始化器(静态块)是针对类的，构造函数是针对对象的，当然是先有类，再有对象；而且静态块在给类分配内存的时候就会被执行，和静态变量一样。所以静态初始化器先于构造函数。

static语句块只执行一次，当该类第一次被初始化时调用，且只运行一次，是在构造函数之前执行的。  

  static 与实例无关，哪怕你创建实例后，你在销毁实例后，static里面的东西依然存在，直到线程over。  
   JAVA在执行程序的时候首先装载类，然后找main()  
所以，在装载类的时候，遇到static马上执行，
```
static { 
	for (int i = 0; i < 10; i++) {
		stuData[i] = new Student("学生" + (i + 1), 18 + i); // 假设学生有姓名和年龄属性 
		num++; 
		}
```
## 内部类
- 不常用
一般一个类会单独写一个文件，内部类就是在类里面写一个类，但是注意一个类里面只能有一个public的class。

- 静态内部类
```java
-Dogs.java
public static class Sun{  
    public String action;  
}
-main
Dogs.Sun zhangDog = new Dogs.Sun();  
zhangDog.action = "eat";
```

加了static只能用静态变量，如果去掉就可以用其他的（也可以不用），例如`private String variety;`中的variety就可以用

- 方法内部类
在方法中写一个类，这个类只能在这个方法里用（这种方式不利于维护）

## 使用：toString
- 什么是toString？
如果想要输出整个对象的内容，如果使用`System.out.println("zhangDog = " + zhangDog);`的方式是不行的，会输出：`zhangDog =com.company.bean.Dogs@7c30a502`后面是这个类的地址

这时候就要使用toString
在Dog.java的文件中alt+insert 点击toString就会出现
```java
@Override  
public String toString() {  
    return "Dogs{" +  
            "name='" + name + '\'' +  
            ", variety='" + variety + '\'' +  
            ", age=" + age +  
            '}';  
}```
@+英语单词是注解：Override 是重写的意思
有的时候是性能的忧患（再说，先不管）

- 还可以使用lombok
在类前面输入@ToString
如果想用equal(),hushcode 和tostring可以用@Data
