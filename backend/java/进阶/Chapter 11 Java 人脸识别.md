- sdk：软件开发工具包（底层人员开发出来给上层应用使用的，也可以卖给别人提供某服务（AI服务））
- 选择一家合适的sdk
- 平台：虹软
- 人脸识别sdk
![[Pasted image 20250126212538.png]]

网络编程，gdb，udb编程？，新特性，λ表达式（为什么会有这个东西），
iop面向接口编程，
注解，反射？的编写（javaweb）
### **1. 网络编程**

#### **GDB 和 UDB？**

- **GDB**：是 GNU 调试器（GNU Debugger），主要用于调试 C/C++ 程序，与 Java 网络编程关系不大。
    
- **UDB**：可能是指 UDP（用户数据报协议），是网络通信协议。
    

#### **网络编程简介**

网络编程是使用 Java 编程语言处理网络通信的技术，核心是基于 **TCP/IP** 协议。

- **TCP 编程**：
    
    - 使用 `Socket` 和 `ServerSocket` 类。
        
    - 提供可靠的点对点连接，数据按顺序传递。
        
- **UDP 编程**：
    
    - 使用 `DatagramSocket` 和 `DatagramPacket`。
        
    - 提供无连接、快速但不可靠的通信。
        

**代码示例（TCP 客户端）**：
```java
Socket socket = new Socket("127.0.0.1", 8080); // 连接服务器 OutputStream out = socket.getOutputStream(); out.write("Hello Server!".getBytes()); out.close(); socket.close();
```
### **2. Java 新特性**

#### **Lambda 表达式（λ表达式）**

Lambda 表达式是从 Java 8 开始引入的，目的是简化匿名内部类的语法，使代码更加简洁和可读。它用于函数式编程。

**为什么会有 Lambda 表达式？**

- **背景**：Java 8 引入了函数式编程，强调高阶函数（方法作为参数或返回值）。
    
- **需求**：在处理集合流操作时，传统的匿名内部类太繁琐，Lambda 解决了这个问题。
    

**示例**：

java

复制编辑

`// 使用 Lambda 表达式代替匿名内部类 List<String> names = Arrays.asList("Alice", "Bob", "Charlie"); names.forEach(name -> System.out.println(name));`

---

### **3. 面向接口编程（IoP）**

IoP 是面向接口编程（Interface-Oriented Programming）的缩写。核心思想是通过接口而非具体实现进行编程，提升代码的灵活性和可扩展性。

#### **主要特点**：

- **解耦**：调用方只需要知道接口，而不需要关心具体实现。
    
- **扩展性强**：可以随时更换接口实现，而无需修改调用方代码。
    

#### **示例**：

java

复制编辑

`// 接口定义 public interface PaymentService {     void pay(double amount); }  // 实现类 public class AlipayService implements PaymentService {     public void pay(double amount) {         System.out.println("Paid " + amount + " using Alipay");     } }  // 调用 PaymentService payment = new AlipayService(); payment.pay(100.0);`

---

### **4. 注解与反射**

#### **注解**

注解（Annotation）是对代码的元信息描述，Java 中通过 `@` 符号定义。它在编译期或运行期提供额外信息，广泛用于框架（如 Spring）和工具（如 Lombok）。

- **内置注解**：`@Override`、`@Deprecated`、`@SuppressWarnings`。
    
- **自定义注解**：
    

java

复制编辑

`@Retention(RetentionPolicy.RUNTIME) // 注解保留到运行期 @Target(ElementType.METHOD) // 用于方法 public @interface MyAnnotation {     String value(); }`

- **应用场景**：用于依赖注入（如 `@Autowired`）、配置映射（如 `@Entity`）。
    

#### **反射**

反射是动态操作类及其成员的机制。注解通常结合反射解析，实现动态功能。

**示例（解析注解）**：

java

复制编辑

`Method method = SomeClass.class.getMethod("someMethod"); if (method.isAnnotationPresent(MyAnnotation.class)) {     MyAnnotation annotation = method.getAnnotation(MyAnnotation.class);     System.out.println(annotation.value()); }`

---

### **5. 编写反射代码（Java Web）**

在 Java Web 开发中，反射和注解常用于动态处理类和方法，比如自动注入 Bean。

#### **自动依赖注入示例**

java

复制编辑

`// 注解定义 @Retention(RetentionPolicy.RUNTIME) @Target(ElementType.FIELD) public @interface Autowired {}  // 使用反射实现注入 public class DependencyInjector {     public static void inject(Object obj) throws Exception {         Field[] fields = obj.getClass().getDeclaredFields();         for (Field field : fields) {             if (field.isAnnotationPresent(Autowired.class)) {                 field.setAccessible(true);                 Object dependency = field.getType().newInstance();                 field.set(obj, dependency);             }         }     } }`

**应用场景**：通过注解 `@Autowired` 自动注入所需对象，类似于 Spring 的 IOC 容器。

---

### **总结**

这些技术和概念构成了现代 Java 开发的基础：

- **网络编程**：实现客户端与服务器之间的通信。
    
- **新特性**：Lambda 表达式提升了函数式编程的简洁性。
    
- **面向接口编程（IoP）**：提升代码的解耦性和扩展性。
    
- **注解与反射**：注解提供元信息，反射用于动态操作对象，二者结合可实现强大的动态功能（如 Spring 的 IOC 和 AOP）。