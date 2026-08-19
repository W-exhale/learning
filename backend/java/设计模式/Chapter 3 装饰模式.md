## 介绍
- Decorator：装饰模式
- 可以动态的给一个对象添加一些额外的职责，在增加功能方面比生成子类更为灵活（将已经有的功能动态结合起来，就不用新写一个结合起来的类）![Pasted image 20250325162026](images/Pasted%20image%2020250325162026.png)
- 主要角色：
	- 抽象构件(Component)：所有被装饰的对象的抽象
	- 具体构件(ConcreteComponent)：被装饰的对象
	- 装饰类(Decorator)：所有具体装饰的父类
	- 具体装饰类(ConcreteDecorator)：具体的装饰
**优点**
- 动态扩展对象功能，不需要修改原类。
- 遵循开闭原则（OCP）。
- 可以通过多个具体装饰类的组合实现丰富的功能。
**缺点：**
- 会增加程序的复杂性，尤其是多个装饰类嵌套时，容易导致调试困难。
- 装饰类的行为过多可能会导致系统变得难以理解。

## 人装饰实现
- 给人装饰：各种衣服...
```java
-ICharacter.java //人物对象接口  
public interface ICharacter {  
    public void show();  
}
-Person.java //被装饰的人
public class Person implements ICharacter{  
    private String name;  
    public Person(String name){  
        this.name = name;  
    }  
  
    @Override  
    public void show() {  
        System.out.println("装扮的"+name);  
    }  
}
-Finery.java //（装饰的抽象）
public class Finery implements ICharacter{  
  
    protected ICharacter component;  
    public void decorate(ICharacter component){  
        this.component = component;  
    }  
  
    @Override  
    public void show() {  
        if(this.component != null){  
            this.component.show();  
        }  
    }  
}
-Sneakers.java //具体的装饰
public class Sneakers extends Finery{  
    public void show(){  
        System.out.println("球鞋");  
        super.show();  
    }  
}
-Main.java
public class Main {  
    public static void main(String[] args) {  
       Person xm = new Person("小明");  
        System.out.println("第一种装扮：");  
        Sneakers sneakers = new Sneakers();  
        sneakers.decorate(xm);  
        //...  
        xm.show();  
    }  
}
```

## 商场收银程序升级
### 介绍
- 先打8折，再满300反100
- 如果加上装饰模式，可以将普通收费模式变为具体的被装饰类，CashSuper改成普通类，实现ISale接口作为装饰类，CashContext用来进行包装，要注意包装的顺序，context还是负责客户端的内容
![Pasted image 20250325205510](images/Pasted%20image%2020250325205510.png)

### 具体实现
```java
-ISale.java
public interface ISale {  
    public double acceptCash(double price, int num);  
}
-CashNormal.java
public class CashNormal implements ISale{  
    //正常收费，原价返回  
    @Override  
    public double acceptCash(double price, int num) {  
            return price * num;  
    }  
}
-CashSuper.java
public class CashSuper implements ISale{  
    protected ISale component;  
  
    //装饰对象  
    public void decorate(ISale component){  
        this.component = component;  
    }  
  
    public double acceptCash(double price, int num){  
        double result = 0d;  
        if(this.component != null){  
            //若装饰对象存在，则执行装饰算法运算  
            result = this.component.acceptCash(price, num);  
        }  
        return result;  
    }  
  
}
-CashRebate.java
public class CashRebate extends CashSuper{  
    private double moneyRebate = 1d;  
  
    //打折，初始化必须输入折扣率  
    public CashRebate(double moneyRebate){  
        this.moneyRebate = moneyRebate;  
    }  
    //计算收费要乘以折扣率  
    public double acceptCash(double price, int num){  
        double result = price * num * this.moneyRebate;  
        return super.acceptCash(result, 1);  
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
        return super.acceptCash(result, 1);  
    }  
}
-CashContext.java
public class CashContext {  
    private ISale iSale; //声明一个ISale对象  
  
    //通过构造方法，传入具体的收费策略,参数为收费模式编号  
    public CashContext(int cashType){  
        switch(cashType){  
            case 1:  
                this.iSale = new CashNormal();  //正常收费  
                break;  
            case 2:  
                this.iSale = new CashRebate(0.8); //打八折  
                break;  
            case 3:  
                this.iSale = new CashRebate(0.7); //打七折  
                break;  
            case 4:  
                this.iSale = new CashReturn(300d, 100d); //满300返100  
                break;  
            case 5:  
                CashNormal cashNormal = new CashNormal();  
                CashReturn cashReturn = new CashReturn(300d, 100d);  
                CashRebate cashRebate = new CashRebate(0.8d);  
  
                cashReturn.decorate(cashNormal); // 用满减包装原算法  
                cashRebate.decorate(cashReturn); // 8折包装满减  
                this.iSale = cashRebate;  
                break;  
        }  
    }  
    public double getResult(double price, int num){  
        //根据收费模式的不同，获得计算结果  
        return this.iSale.acceptCash(price, num);  
    }  
}
```
- 客户端不变
- 这样我们要什么功能直接写新的类，然后在Context里面加case就行