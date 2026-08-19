## 简单工厂模式
- Simple Factory Pattern
- 创建一个专门的工厂类，根据传入的参数决定创建哪一种具体的对象。（选择性实例化）
- 主要角色：
	- 工厂类（Factory）：负责对象创建
	- 抽象产品类（Product）：产品的公共接口或抽象类
	- 具体产品类（ConcreteProduct）：实现抽象产品的具体类

- 优点：
	- 客户端无需依赖具体类，只用看工厂类
	- 对象的创建主要在工厂中
- 缺点：工厂类的职责太重如果增加新的产品种类就要改工厂类，违反开闭原则？

![Pasted image 20250310223845](images/Pasted%20image%2020250310223845.png)


### 商场收银软件，使用Simple Factory Pattern
[[收银系统.excalidraw|收银系统]]

- 假设使用简单工厂模式：
![Pasted image 20250311133350](images/Pasted%20image%2020250311133350.png)

- 实现：
```java
-CashFactory.java
package com.company.demo3;  
public class CashFactory {  
    public static CashSuper createCashAccept(int cashType){  
        CashSuper cashSuper = null;  
        switch(cashType){  
            case 1:  
                cashSuper = new CashNormal();  //正常收费  
                break;  
            case 2:  
                cashSuper = new CashRebate(0.8); //打八折  
                break;  
            case 3:  
                cashSuper = new CashRebate(0.7); //打七折  
                break;  
            case 4:  
                cashSuper = new CashReturn(300d, 100d); //满300返100  
                break;  
        }  
        return cashSuper;  
    }  
}
-CashSuper.java
public abstract class CashSuper {  
    //收费方式的抽象方法，参数为单价和数量  
    public abstract double acceptCash(double price, int num);  
}
-CashNormal.java
public class CashNormal extends CashSuper{  
    public double acceptCash(double price, int num){  
        return price * num;  
    }  
}
-CashReturn.java
public class CashReturn extends CashSuper{  
    private double moneyCondition = 0d;//返利条件  
    private double moneyReturn = 0d; //返利值  
  
    //返利后的收费，初始化需要输入返利条件和返利值  
    public CashReturn(double moneyCondition, double moneyReturn){  
        this.moneyCondition = moneyCondition;  
        this.moneyReturn = moneyReturn;  
    }  
  
    public double acceptCash(double price, int num){  
        double result = price * num;  
        if(moneyCondition > 0 && result>= moneyCondition){  
            result = result - Math.floor(result / moneyCondition) * moneyReturn;  
        }  
        return result;  
    }  
}
-CashRebate.java
public class CashRebate extends CashSuper{  
    private double moneyRebate = 1d;  
  
    //初始化时必须输入折扣  
    public CashRebate(double moneyRebate){  
        this.moneyRebate = moneyRebate;  
    }  
    //计算收费要乘以折扣率  
    public double acceptCash(double price, int num){  
        return price * num * this.moneyRebate;  
    }  
}
-客户端
public class Main {  
    Scanner input = new Scanner(System.in);  
    public static double price = 0d; //当前商品的价格  
    public static int num = 0; //当前商品的数量  
    public static double totalPrices = 0d; //当前商品的合计  
    public static double total = 0d; //所有商品的合计  
    public static String ch = ""; //判断是否继续  
  
    public static void main(String[] args) {  
   // write your code here  
        Scanner input = new Scanner(System.in);  
        do {  
            System.out.print("请输入您想选择的模式（1.正常 2.打八折 3.打七折 4. 满300减100）：");  
            int option = input.nextInt();  
            System.out.print("请输入商品价格：");  
            double price = input.nextDouble();  
            System.out.print("请输入商品数量：");  
            int num = input.nextInt();  
            System.out.print("是否继续（yes or no）：");  
            String ch = input.next();  
  
            CashSuper cashSuper = CashFactory.createCashAccept(option);  
            double totalPrices = cashSuper.acceptCash(price, num); //计算单个商品价格  
            total = totalPrices + total; //合计  
        }while (ch == "yes");  
  
        System.out.println("合计为：" + total);  
    }  
}
```


## UML类图
![Pasted image 20250310231620](images/Pasted%20image%2020250310231620.png)

## 策略模式
- Strategy：将每种算法都独立封装为一个类，使其可以互相互换，使算法的变化不会影响到算法的用户（可以避免使用很多条件语句）
- 主要角色：
	- 上下文（context）：提供给客户端调用的接口，负责将客户端的请求委托给具体的策略类完成。
	- 策略接口（Strategy Interface）：定义供context使用的接口，各种不同的类实现这个接口
	- 具体策略类（Concrete Stratery）：实现策略接口的具体类，封装算法逻辑，可以在运行时动态替换
### 商城收银软件，使用Strategy

![Pasted image 20250311192446](images/Pasted%20image%2020250311192446.png)

- 将CashFactory换成CashContext
```java
public class CashContext {  
    private CashSuper cashSuper; //声明一个CashSuper对象  
    //通过构造方法，传入具体的收费策略  
    public CashContext(CashSuper cashSuper){  
        this.cashSuper = cashSuper;  
    }  
    public double getResult(double price, int num){  
        //根据收费模式的不同，获得计算结果  
        return this.cashSuper.acceptCash(price, num);  
    }  
}
-客户端

```


- 但是如果这样，对收费模式的选择就要放在客户端，更加不符
- 所以我们可以将Simple Factory和Strategy结合
### 使用Simple Factory和Strategy
- 修改context，通过构造方法选收费模式，函数返回acceptCash方法计算后的结果获得当前商品的合计，客户端只用创建context，传入模式编号
- Simple Factory：在factory中创建函数选择收费模式，客户端创建CashSuper实例来获取当前商品价格
- Strategy：在客户端选择收费模式（给context传入各种模式的算法），在context中获得返回的当前商品的合计，客户端只需要用到context

```java
-CashContext.java
public class CashContext {  
    private CashSuper cashSuper; //声明一个CashSuper对象  
    //通过构造方法，传入具体的收费策略,参数为收费模式编号  
    public CashContext(int cashType){  
        switch(cashType){  
            case 1:  
                cashSuper = new CashNormal();  //正常收费  
                break;  
            case 2:  
                cashSuper = new CashRebate(0.8); //打八折  
                break;  
            case 3:  
                cashSuper = new CashRebate(0.7); //打七折  
                break;  
            case 4:  
                cashSuper = new CashReturn(300d, 100d); //满300返100  
                break;  
        }  
    }  
    public double getResult(double price, int num){  
        //根据收费模式的不同，获得计算结果  
        return this.cashSuper.acceptCash(price, num);  
    }  
}
-客户端
public class Main {  
    Scanner input = new Scanner(System.in);  
    public static double price = 0d; //当前商品的价格  
    public static int num = 0; //当前商品的数量  
    public static double totalPrices = 0d; //当前商品的合计  
    public static double total = 0d; //所有商品的合计  
    public static String ch = ""; //判断是否继续  
  
    public static void main(String[] args) {  
   // write your code here  
        Scanner input = new Scanner(System.in);  
        do {  
            System.out.print("请输入您想选择的模式（1.正常 2.打八折 3.打七折 4. 满300减100）：");  
            int option = input.nextInt();  
            System.out.print("请输入商品价格：");  
            double price = input.nextDouble();  
            System.out.print("请输入商品数量：");  
            int num = input.nextInt();  
            System.out.print("是否继续（yes or no）：");  
            String ch = input.next();  
  
            CashContext cashContext = new CashContext(option);  
            double totalPrices = cashContext.getResult(price, num); //当前商品合计  
            total = totalPrices + total; //合计  
            }while (ch == "yes");  
  
        System.out.println("合计为：" + total);  
    }  
}
```

- 即使如此，如果要增加满200减50的算法还是要在context修改switch语句

