## 继承（inheritance）
-  需求重定义
	动物都有一些共性，现在只写了一个狗的类别，如果要写其他的动物，该如何满足需求

创建一个Animal文件，将共性都放进去，其他特定的动物可以通过继承的方式引用这些共性。
```java
public class Dogs extends Animal{  
}
```
Animal就是父类，Dogs就是子类。

这样设置之后，就可以直接在main中使用那些共性
Animal里的方法一个是无参的，其他是有参的
```java
public class Animal {  
    private static String plot = "NanG";  
  
    private String name;  
    private String variety;  
    private String food;  
    private int age;  
  
    public Animal(){  
    }  
    public Animal(String name, String variety, int age) {  
        this.name = name;  
        this.variety = variety;  
        this.age = age;  
    }
    ...
```
## 多层继承
javad中不可以直接继承两个类,像下面这样（C++可以）
```java
class A extends B,C
```

但是java可以继承多个类（类似孙子，爸爸，爷爷这样）
```java
class A extends B
class C extends A
```
这样C就同时继承了B和A两个类


## 方法的重写

在子类中带有@Override的方法一定是来自父类的，但是方法中的内容不是父类的，这是子类自己拥有的特性，子类要革新，革新的内容就是方法体，这种override的方式就是重写
```java
Dogs中
   @Override  
   public void barking() {  
       System.out.println("汪汪~~~");  
   }
 Animal中
   public void barking(){  
    System.out.println("动物叫！");  
}
```

## super的使用
1. 假如说上面的@override，你就想用父类中的内容，就可以
```java
Dogs中
   @Override  
   public void barking() {  
       super.barking();  
       //System.out.println("汪汪~~~"); 
   }
 Animal中
   public void barking(){  
    System.out.println("动物叫！");  
}
```
super（超级，父类的东西）
2. 假如说你想在main中new一个Dog，不能直接用(构造方法)，继承没有这么面面俱到，所以需要在Dogs具体化一下，把儿子的内容满上,可以使用快捷方式constructor(alt+insert)
```java
-Dogs
public Dogs(){}  
  
public Dogs(String name, String variety, int age) {  
    super(name, variety, age);  
}  
  
public Dogs(String name, String variety) {  
    super(name, variety);  
}
-main
Dogs zhangDog = new Dogs("jerry","拉布拉多",2);

```
也可以自己定义，不用super

## final 的使用
最底层的设置（多层继承）
final class，最终的，最后的class最后的儿子

```java
-Dogs.java
//反例  
    public final boolean isGuideBlindness(){  
        return  false;  
    }
-Labrador.java
public final class Labrador extends Dogs{  
	@Override  
	public boolean isGuideBlindness() {  
    return true;  
	}//这里重写就报错
}

-Animal.java
private static final String COMMUNITY_NAME = "NanG";
```
![Pasted image 20240818135555](images/Pasted%20image%2020240818135555.png)

- final的特点
	1. 遗产不能继承
	2. 方法不能重写，加了final的方法子代可以用但是不能重写。
	3. 修饰变量，这个变量不能改，变成常量，但是这个单词必须全部大写用下划线隔开

- 为什么要有final？
 父代可以控制子代

idea：小写变大写：ctrl+shift+u

## 抽象类型的使用
- 如果忘记在子类重写，就会直接使用父类（Animal）的方法，就会出错
- 但是Animal是个抽象的概念，不可能会new一个动物
（抽象的目的是为了概括解释具体的事物）
`Animal animal = new Animal();`（一般不这么用）

这时候就需要用到抽象类（加上abstract，不能实例化）
```java
public abstract class Animal {
}
```
加上abstract就不能new一个Animal，会报错

- 回到刚才会直接使用父类方法的问题，可以使用抽象方法的方式。（假如说是叫声没有重写）
`public abstract void barking();`
需要注意的是抽象方法是不能有实际意义的，也就是说，它的方法没有内容，如果写了内容会报错，像下面那种方式就会报错。
```java
public abstract void barking(){  
    System.out.println("动物叫！");  
}
```

使用抽象方法时，所在类也必须是抽象的

- 当一个类继承一个抽象类的时候，该子类中必须重写父类中所有的抽象方法。

## 接口（interface）
- 假如说一个抽象类中的方法全部都是abstract，那么其实没有必要给所有的方法都加上abstract，这时就需要使用到*接口*。

new一个javaclass，但是不是选择Class，而是选interface
![Pasted image 20240925153312](images/Pasted%20image%2020240925153312.png)

![Pasted image 20240925153331](images/Pasted%20image%2020240925153331.png)

接口当中所有的方法都是抽象的
- 创建一个新的类Chinese，这时候就不能用extends，需要用到implements，意思是实现接口。（Alt + 回车，光标放到public那一行，可以快捷生成重写）
![Pasted image 20240925154122](images/Pasted%20image%2020240925154122.png)

- 这时候在main中不能new Human，要使用就得用Chinese。

接口是可以继承的
- 抽象类和接口的区别
抽象类对具体的事物进行抽象，接口是对行为进行抽象。（也就是在类中会有名字，会有年龄，但是接口中只有吃喝跑）

接口的用途：Dao service(?!!不知道)

## 多态

- 条件：一定要有继承关系（至少两个类），特点是一个实例能进行多个行为可以转换
- 通俗的比喻：花木兰替父从军

花木兰需要伪装身份，所以在打仗的时候花木兰对外介绍自己时，需要用父亲的介绍。

在创建变量时：
`HuaHu huaHu = new HuaMuLan();`

```java
-HuaMuLan.java
public class HuaMuLan extends HuaHu{  
    public String name = "HuaMuLan";  
    public int age = 19;  
  
    public void dressing(){  
        System.out.println("HuaMuLan化妆...");  
    }  
}

-HuaHu.java
public class HuaHu {  
    public String name = "HuaHu";  
    public int age = 45;  
  
    public static void sayMe(){  
        System.out.println("大家好，我叫HuaHu，我今年45！");  
    }  
  
    public void fight(){  
        System.out.println("干架！");  
    }  
}

-main中
//替父从军  
HuaHu huaHu = new HuaMuLan();  
System.out.println(huaHu.name);  
System.out.println(huaHu.age);  
//这时候在花木兰的类中没有写自我介绍，所以下面自我介绍的时候会直接使用父亲的自我介绍，这就是向上转型 
HuaHu.sayMe();  
HuaMuLan.sayMe();
huaHu.fight();//这时候的花木兰还是花弧，所以还不能化妆

//仗打完之后，需要做回自己，向下转型  
HuaMuLan huaMuLan = (HuaMuLan) huaHu;  //强制转换
System.out.println(huaMuLan.name);  
System.out.println(huaMuLan.age);  
huaMuLan.dressing();

```

## 匿名内部类

接口可以new，抽象类不行
1. 第一种方式
```java
-Human.java
//这是一个接口
public interface Human {  
    public void eat();  
  
    public void run();  
}

-main
//匿名内部类  
Human chinese = new Human() {  
    @Override  
    public void eat() {  
        System.out.println("中国菜！");  
    }  
  
    @Override  
    public void run() {  
  
    }  
};
```

- 或者是（直接就没有名字）
```java
//匿名内部类  
new Human() {  
    @Override  
    public void eat() {  
        System.out.println("中国菜！");  
    }  
  
    @Override  
    public void run() {  
  
    }  
}.eat();
```

## Object
- 所有类的父类（即使是自己写的类，也是object的子类）
所以使用[[OOP上#使用：toString|toString]]的时候会出现override（就是说Object中有一个toString），但是通常情况下都是用的注解（lombok）

- 文件读写不常用，实际要用的时候会使用到第三方架构（maven repository）

