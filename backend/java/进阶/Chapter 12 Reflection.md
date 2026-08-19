## 🎯 什么是反射 (Reflection)？
- Java 的反射机制是指在 **运行期间** 获取任何一个类的结构信息（如成员变量、方法、构造器等）。

- **核心目的：** 解决在程序运行时，对于某个对象实例的具体类型一无所知的情况下，如何调用其方法或访问其字段的问题。

通常情况下如果我们要调用一个对象的方法或者访问一个对象的字段，会传入对象实例，但是如果没有对应参数，就不能使用。但是通过反射，即使只有Object引用，也可以知道其内部结构并且进行操作

## 🧩 `Class` 类：类型的元信息
在 Java 中，`class`（包括 `interface`）本质上是一种 **数据类型 (Type)**。不同继承关系的数据类型之间不能随意赋值：
```java
Number n = new Double(123.456); // OK
String s = new Double(123.456); // compile error!
```
### JVM 与 `Class` 实例
1.  **动态加载：** JVM 在执行 Java 程序时，并不会一次性加载所有用到的 `.class` 文件。而是在 **首次需要使用** 某个类时，才将其对应的 `.class` 文件加载到内存中。
2.  **`Class` 实例的创建：** 每加载一种 `class` 或 `interface` 到内存中，JVM 就会为其创建一个 **`java.lang.Class` 类型的实例**（`Class`的实例），并将这个实例与加载的类型关联起来。

> [!INFO] `Class` 类本身
> `java.lang.Class` 是 JDK 提供的一个类，用于表示 JVM 中加载的类和接口。
> ```java
> public final class Class {
>     private Class() {} // 构造方法是 private 的
> }
> ```
> 由于构造方法是私有的，我们无法手动创建 `Class` 实例，只有 JVM 可以在加载类时创建它，我们自己的Java程序是无法创建`Class`实例的。。

例如，当 JVM 加载 `String` 类时：
1.  读取 `String.class` 文件内容到内存。
2.  为 `String` 类创建一个 `Class` 实例（可以想象成 `Class cls = new Class(String);`，但这只是概念表示，实际由 JVM 完成）。
3. 这个 `Class` 实例就代表了 `String` 这个数据类型本身，并且 **在 JVM 中是唯一的**。![Pasted image 20250422163151](images/Pasted%20image%2020250422163151.png)![Pasted image 20250422163214](images/Pasted%20image%2020250422163214.png)
#### `Class` 实例的作用
JVM 为每个加载的类型创建的 `Class` 实例中，保存了该类型的 **所有信息**：
*   类名 (Full Name)
*   简单名称 (Simple Name)
*   包名 (Package Name)
*   父类 (Superclass)
*   实现的接口 (Interfaces)
*   所有方法 (Methods)
*   所有字段 (Fields)
*   构造器 (Constructors)
*   注解 (Annotations)
*   ... 等等
因此，只要我们能获取到某个类型的 `Class` 实例，就能通过这个实例 **反向获取** 该类型的所有信息。这种机制就是 **反射 (Reflection)**。

#### 如何获取 `Class` 实例
1. **通过类名的 `.class` 静态变量：**
    ```java
    Class cls = String.class;
    Class intCls = int.class; // 基本类型也有 Class 实例
    Class runnableCls = Runnable.class; // 接口也有 Class 实例
    ```
2. **通过对象的 `getClass()` 方法**
    ```java
    String s = "Hello";
    Class cls = s.getClass(); // 获取 s 对象的实际类型对应的 Class 实例
    ```
3.  **通过类的完整限定名 `Class.forName()` 静态方法：** (需要处理 `ClassNotFoundException`)
    ```java
    try {
        Class cls = Class.forName("java.lang.String");
    } catch (ClassNotFoundException e) {
        System.err.println("类未找到: " + e.getMessage());
    }
    ```

> [!TIP] 同一类型的 `Class` 实例是唯一的
> 由于 JVM 对每个加载的类型只创建一个 `Class` 实例，因此上述三种方法获取到的同一个类型的 `Class` 实例是完全相同的。

#### `instnceof` 与 \=\= 判断 `Class` 实例
*   `instanceof`：判断一个对象是否是 **某个类型或其子类型** 的实例。
*   `a.getClass() == B.class`：**精确判断** 一个对象的类型是否 **正好是** `B` 类型，不考虑子类。
```java
Integer n = 123;

// instanceof 判断
boolean b1 = n instanceof Integer; // true (n 是 Integer 类型)
boolean b2 = n instanceof Number;  // true (n 是 Number 的子类 Integer 类型)

// == 判断 Class 实例
boolean b3 = n.getClass() == Integer.class; // true (n 的实际类型就是 Integer)
boolean b4 = n.getClass() == Number.class;  // false (n 的实际类型是 Integer, 不是 Number)
```

**使用场景：**
*   通常应优先使用 `instanceof` 进行类型判断，符合面向抽象编程的原则（关心"是不是"某种能力，不关心具体实现）。
*   只有在需要 **精确判断** 对象的确切类型时，才使用 == 比较 `Class` 实例。
#### 通过 `Class` 实例获取类型信息
- 反射的目的是为了获得某个实例的信息。
- 获取`Class`实例后，我们可以通过反射获取该类的详细信息：
```java
// reflection
public class Main {
    public static void main(String[] args) {
        printClassInfo("".getClass());        // String
        printClassInfo(Runnable.class);     // interface java.lang.Runnable
        printClassInfo(java.time.Month.class); // enum java.time.Month
        printClassInfo(String[].class);      // class [Ljava.lang.String; (数组)
        printClassInfo(int.class);          // int (基本类型)
    }

    static void printClassInfo(Class<?> cls) {// 使用泛型 <?> 更佳
        System.out.println("Class name: " + cls.getName());         // 完整名称
        System.out.println("Simple name: " + cls.getSimpleName());   // 简单名称
        if (cls.getPackage() != null) {
            System.out.println("Package name: " + cls.getPackage().getName());  // 包名
        } else {
            System.out.println("Package Name: (无包名, e.g., 基本类型, 数组)");
        }
        System.out.println("is interface: " + cls.isInterface());
        System.out.println("is enum: " + cls.isEnum());
        System.out.println("is array: " + cls.isArray());
        System.out.println("is primitive: " + cls.isPrimitive());    // 是否基本类型
    }
}
```
**注意：**
*   数组类型（例如`String[]`）也是一种 `Class`，而且不同于`String.class`，其名称比较特殊（如 `[Ljava.lang.String;`）。
*   基本类型（如 `int`, `boolean`）也有对应的 `Class` 实例（如 `int.class`）,通过`int.class`访问。
**输出示例：**
![Pasted image 20250422175010](images/Pasted%20image%2020250422175010.png)


#### 通过 `Class` 实例创建对象
- 获取到了一个`Class`实例后，可以使用 `Class` 实例的 `newInstance()` 方法来创建该类型的一个新实例。
```java
// 获取 String 的 Class 实例
Class<String> cls = String.class;

try {
    // 创建一个 String 实例 (调用无参构造函数)
    String s = cls.newInstance(); // 在 Java 9+ 中已废弃，推荐使用 getDeclaredConstructor().newInstance()
    System.out.println("Created empty string: [" + s + "]");

    // Java 9+ 推荐方式:
    String s2 = cls.getDeclaredConstructor().newInstance();
     System.out.println("Created empty string (new way): [" + s2 + "]");

} catch (InstantiationException e) {
    // 类是抽象类、接口、数组类、基本类型，或者没有无参构造函数
    e.printStackTrace();
} catch (IllegalAccessException e) {
    // 无参构造函数不是 public
    e.printStackTrace();
} catch (NoSuchMethodException e) {
    // 没有找到无参构造函数 (使用 getDeclaredConstructor() 时)
    e.printStackTrace();
} catch (java.lang.reflect.InvocationTargetException e) {
    // 构造函数内部抛出异常 (使用 getDeclaredConstructor().newInstance() 时)
    e.printStackTrace();
}
```

> [!WARNING] `Class.newInstance()` 的局限性 (Java 9+ 已废弃)
> *   只能调用类的 **`public` 无参数构造方法**。
> *   如果类没有 `public` 无参构造方法，或者构造方法是 `private`/`protected`/`package-private`，或者需要传递参数，`newInstance()` 就会失败。
> *   **推荐使用 `Constructor` API：** `clazz.getDeclaredConstructor(paramTypes...).newInstance(args...)`，这种方式更灵活，可以调用任意访问权限、任意参数的构造器（需要处理访问权限）。

### 动态加载 (Dynamic Loading)

*   **机制：** JVM 不会在启动时加载所有可能用到的类，而是在代码执行过程中 **第一次遇到** 需要使用的类时，才去查找并加载对应的 `.class` 文件。

```java
// Main.java
public class Main {
    public static void main(String[] args) {
        if (args.length > 0) {
            create(args[0]);
        }
    }
    static void create(String name) {
        Person p = new Person(name);
    }
}
```

- 当执行`Main.java`时，用到了`Main`，JVM会把`Main.class`加载到内存。但是不会加载`Person.class`，除非执行到`create()`方法，JVM发现需要用`Person`时才会加载`Person.class`

- 利用动态加载特性，可以在运行时根据条件（如配置文件、环境变量、是否存在某个库）来决定加载和使用哪个具体的实现类。

*   **示例：日志框架的选择 (如 Commons Logging)**
    Commons Logging 会尝试按特定顺序查找并使用不同的日志实现库（如 Log4j, JDK Logging）。它通过 `Class.forName()` 检查某个日志库的核心类是否存在于 classpath 中，如果存在，就加载并使用该库；否则，尝试下一个。
```java
   // 伪代码：演示 Commons Logging 的逻辑
LogFactory factory = null;

if (isClassPresent("org.apache.logging.log4j.Logger")) {
    factory = createLog4j();
} else {
    factory = createJdkLog();
}
    // 辅助方法：检查类是否存在
boolean isClassPresent(String name) {
    try {
        Class.forName(name);
        return true;
    } catch (Exception e) {
        return false;
    }
}
```
这就是为什么我们只需要把Log4j的jar包放到classpath中，Commons Logging就会自动使用Log4j的原因。

## 🔩 访问字段 (Accessing Fields)
- 对于任何一个`Object`实例，只要我们获取了它的`Class`，就可以获取它的一切信息。
- 通过`Class`实例，我们可以获取该类及其父类的字段（成员变量）信息。

- `Class`类提供了以下几个方法来获取字段：
	- `Field getField(String name)`：获取指定的 **`public`** 字段（包括从父类继承的）。
	- `Field getDeclaredField(String name)`：根据字段名获取当前类的某个field（不包括父类，但**包括** `private`, `protected`, `package-private` 字段）
	- `Field[] getFields()`：获取所有 **`public`** 字段（包括从父类继承的）
	- `Field[] getDeclaredFields()`：获取当前类的所有所有字段（**不包括** 父类，但**包括** 所有访问修饰符的字段）。

示例代码：
```java
// reflection
import java.lang.reflect.Field;

public class Main {
    public static void main(String[] args) throws Exception {
        Class<?> stdClass = Student.class; // 使用 Class<?> 更通用

        // 获取 public 字段 "score" (当前类)
        Field scoreField = stdClass.getField("score");
        System.out.println(scoreField);

        // 获取继承的 public 字段 "name" (父类)
        Field nameField = stdClass.getField("name");
        System.out.println(nameField);

        // 获取 private 字段 "grade" (当前类声明)
        // 注意：getField("grade") 会抛出 NoSuchFieldException，因为它不是 public
        Field gradeField = stdClass.getDeclaredField("grade");
        System.out.println(gradeField);

        System.out.println("\n--- All Declared Fields ---");
        // 获取 Student 类自己声明的所有字段
        for (Field f : stdClass.getDeclaredFields()) {
            System.out.println(f);
        }

        System.out.println("\n--- All Public Fields (including inherited) ---");
        // 获取 Student 类及其父类的所有 public 字段
        for (Field f : stdClass.getFields()) {
            System.out.println(f);
        }
    }
}
```

**输出：**
```plaintext
public int Student.score
public java.lang.String Person.name
private int Student.grade

--- All Declared Fields ---
public int Student.score
private int Student.grade

--- All Public Fields (including inherited) ---
public int Student.score
public java.lang.String Person.name
```

一个`Field`对象包含了一个字段的所有信息：
- `getName()`：返回字段名称，例如，`"name"`；
- `getType()`：返回字段类型，也是一个`Class`实例，例如，`String.class`；
- `getModifiers()`：返回字段的修饰符，是一个 `int` 值，不同的bit表示不同的含义。（可以使用 `java.lang.reflect.Modifier` 类的静态方法 (如 `isPublic`, `isPrivate`, `isFinal`) 来解析这个整数值。）

以`String`类的`value`字段为例，它的定义是：
![Pasted image 20250422193436](images/Pasted%20image%2020250422193436.png)
```java
Field f = String.class.getDeclaredField("value");
System.out.println("Name: " + f.getName());       // "value"
System.out.println("Type: " + f.getType());       // class [B (byte array) 或 class [C (char array)
int modifiers = f.getModifiers();
System.out.println("Is Private? " + Modifier.isPrivate(modifiers)); // true
System.out.println("Is Final?   " + Modifier.isFinal(modifiers));   // true
```


### 获取字段
- 还可以拿到一个实例对应的该字段的值。
- 通过 `Field` 对象的 `get(Object obj)` 方法实现，其中 `obj` 参数是目标实例。

**示例：获取 `Person` 实例的 `name` 字段值**
```java
// reflection
import java.lang.reflect.Field;
public class Main {

    public static void main(String[] args) throws Exception {
        Object p = new Person("Xiao Ming");
        Class<?> c = p.getClass(); //获取Person 类的 Class 实例
        // 获取Field实例，获取名为 "name" 的字段 (它是 private)
        Field f = c.getDeclaredField("name");
        Object value = f.get(p);
        // 尝试直接访问 private 字段会失败
        // Object value = f.get(p); // 这会抛出 IllegalAccessException
        // ---- 关键步骤：解除访问限制 ----
        f.setAccessible(true); // 允许访问 private 字段，也可以将name改为public
	    // 现在可以获取字段值了
        Object value = f.get(p);
        //获取指定实例的指定字段的值
        System.out.println(value); // "Xiao Ming"
        // 使用完后，可以考虑恢复访问限制（虽然不常见）
        // f.setAccessible(false);
    }
}

class Person {
    private String name;

    public Person(String name) {
        this.name = name;
    }
}
```

> [!IMPORTANT] `setAccessible(true)`
> *   调用 `f.setAccessible(true)` 是为了 **临时取消 Java 的访问控制检查**（`private`, `protected` 等）。这使得我们可以通过反射访问和修改通常无法直接访问的字段。
> *   **注意：** 这是一种 **强力** 的机制，破坏了类的封装性。应谨慎使用，通常用于框架、序列化库或测试等场景。

**关于封装性：**
*   常规编程中，我们通过对象的 `public` 方法（如 `p.getName()`）来访问字段，编译器会进行访问控制（`public`, `private` 等），保证封装性。
*   反射提供了一种 **绕过** 编译时检查的机制，允许在运行时访问内部状态。但是代码非常繁琐，其次，它更多地是给工具或者底层框架来使用，目的是在不知道目标实例任何信息的情况下，获取特定字段的值。
*   `setAccessible(true)` 的调用 **可能失败**。如果 Java 程序运行在 `SecurityManager` 环境下，安全策略可能会禁止这种操作，特别是对于核心库（如 `java.*`, `javax.*` 包下的类），以保护 JVM 核心库的安全和稳定。

### 设置字段值 (Setting Field Values)
- 通过Field实例可以设置字段的值。
通过 `Field` 对象的 `set(Object obj, Object value)` 方法实现：
*   `obj`: 目标实例。
*   `value`: 要设置的新值。

**示例：修改 `Person` 实例的 `name` 字段值**
```java
// reflection
import java.lang.reflect.Field;

public class Main {
    public static void main(String[] args) throws Exception {
        Person p = new Person("Xiao Ming");
        System.out.println(p.getName()); // "Xiao Ming"
        Class<?> c = p.getClass();
        Field f = c.getDeclaredField("name");
        // ---- 同样需要解除访问限制 ----
        f.setAccessible(true);
        // ---- 设置新值 ----
        f.set(p, "Xiao Hong");
        System.out.println(p.getName()); // "Xiao Hong"
    }
}

class Person {
    private String name;

    public Person(String name) {
        this.name = name;
    }
    // 提供 public getter 以便外部验证
    public String getName() {
        return this.name;
    }
}
```

> [!NOTE]
> 修改非 `public` 字段时，同样 **必须** 先调用 `f.setAccessible(true)` 来解除访问限制，否则 `set()` 方法会抛出 `IllegalAccessException`。

## 📞 调用方法 (Invoking Methods)
反射不仅可以访问字段，还可以动态地调用对象的方法。`java.lang.reflect.Method` 类代表一个方法。
### 获取方法
与获取字段类似，`Class` 实例提供了获取 `Method` 对象的方法：
*   `getMethod(String name, Class<?>... parameterTypes)`: 获取指定的 **`public`** 方法（包括从父类继承的）。需要提供方法名和 **参数类型列表** 来唯一确定一个方法（因为方法可以重载）。
- `Method getDeclaredMethod(String name, Class<?>... parameterTypes)`: ： 获取 **当前类声明** 的指定方法（**不包括** 父类，但**包括** `private`, `protected`, `package-private` 方法）。同样需要提供方法名和参数类型列表。
- `Method[] getMethods()`：获取所有`public`的`Method`（包括父类）
- `Method[] getDeclaredMethods()`：获取当前类的所有`Method`（不包括父类）

```java
import java.lang.reflect.Method;

// reflection
public class Main {
    public static void main(String[] args) throws Exception {
        Class<?> stdClass = Student.class;
        // 获取public方法getScore，参数类型为 String.class
        Method mGetScore = stdClass.getMethod("getScore", String.class);
        System.out.println(mGetScore);
        // 获取继承的public方法getName，无参数:
        Method mGetName = stdClass.getMethod("getName"); // 或者 getMethod("getName", (Class<?>[]) null) 或 getMethod("getName", new Class<?>[0])
        System.out.println(mGetName);

        // 获取 private 方法 getGrade，参数类型为 int.class
        // 注意：getMethod("getGrade", int.class) 会失败，因为它不是 public
        Method mGetGrade = stdClass.getDeclaredMethod("getGrade", int.class);
        System.out.println(mGetGrade);

        System.out.println("\n--- All Declared Methods ---");
        for (Method m : stdClass.getDeclaredMethods()) {
            System.out.println(m);
        }

        System.out.println("\n--- All Public Methods (including inherited) ---");
        for (Method m : stdClass.getMethods()) {
            // 过滤掉 Object 类的方法，使输出更清晰
            if (!m.getDeclaringClass().equals(Object.class)) {
                 System.out.println(m);
            }
        }

    }
}

class Student extends Person {
    public int getScore(String type) {
        return 99;
    }
    private int getGrade(int year) {
        return 1;
    }
}

class Person {
    public String getName() {
        return "Person";
    }
}
```
```plaintext
public int Student.getScore(java.lang.String)
public java.lang.String Person.getName()
private int Student.getGrade(int)

--- All Declared Methods ---
public int Student.getScore(java.lang.String)
private int Student.getGrade(int)

--- All Public Methods (including inherited) ---
public int Student.getScore(java.lang.String)
public java.lang.String Person.getName()
```

一个`Method`对象包含一个方法的所有信息：

- `getName()`：返回方法名称，例如：`"getScore"`；
- `getReturnType()`：返回方法返回值类型，也是一个Class实例，例如：`String.class`；
- `getParameterTypes()`：返回方法的参数类型，是一个`Class<?>[]` 数组，例如：`{String.class, int.class}`；
- `getModifiers()`：返回方法的修饰符，同样是一个 `int` 值，，不同的bit表示不同的含义，可用 `Modifier` 类解析。

### ▶️ 调用方法 (Invoking Methods)
获取到 `Method` 对象后，最核心的操作就是通过 `invoke` 方法来调用它。

`Object invoke(Object obj, Object... args)`

*   `obj`: **目标对象实例**。调用哪个对象上的这个方法。
    *   如果方法是 **静态 (static)** 的，`obj` 参数应传入 **`null`**。
*   `args`: **方法参数**。按照方法声明的参数顺序传入，是一个可变参数列表。
    *   如果方法没有参数，可以不传或传入 `null` 或空数组 `new Object[0]`。
*   **返回值**: 方法执行后的返回值。
    *   如果方法返回类型是 `void`，`invoke` 返回 `null`。
    *   如果方法返回基本类型（如 `int`），`invoke` 返回对应的包装类型（如 `Integer`）。

#### 1. 调用实例方法 (Instance Method)
- 常规
```java
String s = "Hello world";
String r = s.substring(6); // "world"
```
- 使用反射
```java
// reflection
import java.lang.reflect.Method;

public class Main {
    public static void main(String[] args) throws Exception {
        // String对象:
        String s = "Hello world";
        // 1. 获取 Method 对象: String.substring(int startIndex)
        Method mSubstring = String.class.getMethod("substring", int.class);

        // 2. 调用 invoke:
        //    - obj: s (在哪个 String 实例上调用)
        //    - args: 6 (传递给 substring 方法的参数)
        String r = (String) mSubstring.invoke(s, 6);

        System.out.println(r); // 输出: world
    }
}
```

获取`String substring(int, int)`方法。
```java
// 获取 String.substring(int beginIndex, int endIndex)
Method mSubstring2 = String.class.getMethod("substring", int.class, int.class);
// 调用 invoke，传入实例 s 和两个参数 6, 11
String r2 = (String) mSubstring2.invoke(s, 6, 11); // "world"
System.out.println(r2);
```

#### 2. 调用静态方法 (Static Method)
由于无需指定实例对象，所以`invoke` 的第一个参数 `obj` 必须传 `null`。
**示例：调用 `Integer.parseInt(String)`**：

```java
// reflection
import java.lang.reflect.Method;

public class Main {
    public static void main(String[] args) throws Exception {
        // 1. 获取 Method 对象: Integer.parseInt(String s)
        Method mParseInt = Integer.class.getMethod("parseInt", String.class);

        // 2. 调用 invoke:
        //    - obj: null (因为是静态方法)
        //    - args: "12345" (传递给 parseInt 方法的参数)
        Integer n = (Integer) mParseInt.invoke(null, "12345");

        System.out.println(n); // 输出: 12345
    }
}
```

#### 3. 调用非 `public` 方法
与访问非 `public` 字段类似，调用非 `public` 方法（`private`, `protected`, `package-private`）前，需要先获取 `Method` 对象（使用 `getDeclaredMethod`），然后调用 `m.setAccessible(true)` 来解除访问限制。

**示例：调用 `Person` 的 `private` 方法 `setName
```java
// reflection
import java.lang.reflect.Method;

public class Main {
    public static void main(String[] args) throws Exception {
        // 1. 获取 private Method 对象: setName(String name)
        Method mSetName = Person.class.getDeclaredMethod("setName", String.class);

        // 2. 解除访问限制
        mSetName.setAccessible(true);

        // 3. 调用 invoke:
        //    - obj: p (在哪个 Person 实例上调用)
        //    - args: "Bob" (传递给 setName 方法的参数)
        mSetName.invoke(p, "Bob"); // 返回值是 void，所以 invoke 返回 null

        // 验证结果 (假设 name 字段是 package-private 或有 public getter)
        System.out.println(p.name); // 输出: Bob
    }
}

class Person {
    String name;
    private void setName(String name) {
        this.name = name;
    }
}
```

> [!WARNING]
> 调用 `setAccessible(true)` 同样会破坏封装性，并且可能在 `SecurityManager` 环境下失败。

### 🧬 多态与反射 (Polymorphism and Reflection)
即使通过父类的 `Class` 对象获取了某个 `Method`，当你在子类实例上调用 `invoke` 时，如果子类覆写 (override) 了该方法，实际执行的将是 **子类的覆写版本**。

```java
// reflection
import java.lang.reflect.Method;

public class Main {
    public static void main(String[] args) throws Exception {
        // 1. 从 Person.class 获取 hello() 方法
        Method h = Person.class.getMethod("hello");
        // 2. 创建一个 Student 实例
        Student student = new Student();
        // 3. 在 Student 实例上调用从 Person 获取的 hello 方法
        System.out.print("Invoking Person.hello() on Student instance: ");
        h.invoke(student); // 传入的是 Student 实例
        // 对比：在 Person 实例上调用
        System.out.print("Invoking Person.hello() on Person instance: ");
        h.invoke(new Person());
    }
}

class Person {
    public void hello() {
        System.out.println("Person:hello");
    }
}

class Student extends Person {
	@Override
    public void hello() {
        System.out.println("Student:hello");
    }
}
```

**输出：**

```plaintext
Invoking Person.hello() on Student instance: Student:hello
Invoking Person.hello() on Person instance: Person:hello
```

反射代码：
```java
Method m = Person.class.getMethod("hello");
m.invoke(new Student());
```
实际上相当于：
```java
Person p = new Student();
p.hello();
```

>[!NOTE] 结论
>反射调用 `m.invoke(obj, args)` 的行为类似于常规的多态调用 `obj.method(args)`。
>JVM 会在运行时确定 `obj` 的 **实际类型**，并调用该实际类型中对应的方法（或者是继承而来的方法，如果子类没有覆写）。

## 🏗️ 调用构造方法 (Invoking Constructors)
### 常规 vs. 反射创建实例

*   **常规方式：**
    ```java
    Person p = new Person();
    ```
*   **早期反射方式 (`Class.newInstance()`):**
    ```java
    // 已废弃，且有局限性
    Person p = Person.class.newInstance();
    ```

> [!WARNING] `Class.newInstance()` 的局限性
> *   只能调用类的 **`public` 无参数构造方法**。
> *   如果构造方法带有参数，或者不是 `public`（`private`, `protected`, `package-private`），`Class.newInstance()` 无法使用。
> *   在 Java 9+ 中已被标记为 **废弃 (deprecated)**。

### 使用 `Constructor` API (推荐方式)
为了能够调用 **任意** 的构造方法（包括带参数的、非 `public` 的），Java 反射提供了 `java.lang.reflect.Constructor` 类。

`Constructor` 对象包含了关于一个构造方法的所有信息，并且可以通过它的 `newInstance()` 方法来创建类的实例。

`Constructor`对象和Method非常类似，不同之处仅在于它是一个构造方法，并且，调用结果总是返回实例：
```java
import java.lang.reflect.Constructor;

public class Main {
    public static void main(String[] args) throws Exception {
        // 1. 获取构造方法 Integer(int value)
        Constructor<Integer> cons1 = Integer.class.getConstructor(int.class);
        // 调用构造方法:
        Integer n1 = (Integer) cons1.newInstance(123);
        System.out.println(n1); // 输出: 123

        // 2. 获取构造方法 Integer(String s)
        Constructor<Integer> cons2 = Integer.class.getConstructor(String.class);
        Integer n2 = (Integer) cons2.newInstance("456");
        System.out.println(n2); // 输出: 456
    }
}
```

`Class` 类提供了以下方法来获取 `Constructor` 对象：

*   `getConstructor(Class<?>... parameterTypes)`: 获取指定的 **`public`** 构造方法。需要提供构造方法的参数类型列表。
*   `getDeclaredConstructor(Class<?>... parameterTypes)`: 获取 **当前类声明** 的指定构造方法（**不包括** 父类，但**包括** `private`, `protected`, `package-private` 构造方法）。需要提供参数类型列表。
- `getConstructors()`：获取所有`public`的`Constructor`；
- `getDeclaredConstructors()`：获取所有`Constructor`（不包括父类）。

> [!NOTE] 构造方法与继承
> `Constructor` 对象总是代表 **当前类定义** 的构造方法，与父类无关，因此不存在像方法那样的多态问题。


- 与调用非 `public` 方法或访问非 `public` 字段类似：
1.  使用 `getDeclaredConstructor()` 获取 `Constructor` 对象。
2.  调用 `constructor.setAccessible(true)` 来解除访问限制。
3.  调用 `constructor.newInstance(args...)` 创建实例。

> [!IMPORTANT] `setAccessible(true)`
> *   同样需要注意，这破坏了封装性。
> *   在 `SecurityManager` 环境下可能失败。

## 🌳 获取继承关系 (Retrieving Inheritance Hierarchy)
- 获取 `Class` 实例（3种方式）
1.  `ClassName.class` (e.g., `String.class`)
2.  `instance.getClass()` (e.g., `"hello".getClass()`)
3.  `Class.forName("fully.qualified.ClassName")` (e.g., `Class.forName("java.lang.String")`)

### 获取父类 (Superclass)
使用 `getSuperclass()` 方法可以获取一个类的直接父类的 `Class` 实例。
```java
// reflection
public class Main {
    public static void main(String[] args) throws Exception {
        Class<?> currentClass = Integer.class;
        int level = 0;
        while (currentClass != null) {
            String indent = "  ".repeat(level);
            //根据当前的层级 level，生成对应数量的空格缩进。repeat(level) 是 String的方法，用于重复空格两次（" ")以表示继承层次。
            System.out.println(indent + currentClass.getName());
            currentClass = currentClass.getSuperclass(); // 获取父类
            level++;
        }
    }
}
```
**输出：**
```plaintext
java.lang.Integer
  java.lang.Number
    java.lang.Object
```

*   `Integer` 的父类是 `Number`。
*   `Number` 的父类是 `Object`。
*   `Object` 是所有类的根，它的 `getSuperclass()` 返回 `null`。
*   除了 `Object`，任何非 `interface` 的类都有一个非 `null` 的父类。

### 获取实现的接口 (Interfaces)
使用 `getInterfaces()` 方法可以获取一个类 **直接实现** 的所有接口的 `Class` 实例数组。

例如，查询`Integer`实现的接口：
```java
// reflection
import java.util.Arrays;

public class Main {
    public static void main(String[] args) throws Exception {
        System.out.println("Integer 实现的接口:");
        Class<?>[] intInterfaces = Integer.class.getInterfaces();
        Arrays.stream(intInterfaces).forEach(i -> System.out.println("  - " + i.getName()));
        //Arrays.stream(intInterfaces)：将数组转换为一个流，以便使用流式操作来处理。
        //forEach 方法：遍历流中的每个接口，并执行传入的 Lambda 表达式。
        //i.getName()获取接口的全限定类名（包括包名）。使用 `" - "` 作为前缀，用于更清晰地格式化输出。
        System.out.println("\nNumber (Integer的父类) 实现的接口:");
        Class<?>[] numInterfaces = Integer.class.getSuperclass().getInterfaces();
        Arrays.stream(numInterfaces).forEach(i -> System.out.println("  - " + i.getName()));
    }
}
```
```
Integer 实现的接口:
  - java.lang.Comparable
  - java.lang.constant.Constable
  - java.lang.constant.ConstantDesc

Number (Integer的父类) 实现的接口:
  - java.io.Serializable
```
**关键点：**
*   `getInterfaces()` **只返回当前类直接实现的接口**，不包括父类实现的接口。
*   如果一个类没有实现任何接口，`getInterfaces()` 返回一个空数组。
*   对 **接口** 的 `Class` 对象调用 `getSuperclass()` 总是返回 `null`。
*   要获取一个接口 **继承** 的父接口，也需要使用 `getInterfaces()`。
```java
System.out.println(java.io.DataInputStream.class.getSuperclass()); // java.io.FilterInputStream，因为DataInputStream继承自FilterInputStream
System.out.println(java.io.Closeable.class.getSuperclass()); // null，对接口调用getSuperclass()总是返回null，获取接口的父接口要用getInterfaces()
```

### 判断类型兼容性 (`isAssignableFrom`)
- `Class` 对象的 `isAssignableFrom(Class<?> cls)` 方法用于判断一个类型是否可以赋值给当前 `Class` 对象所代表的类型（即，`this = cls` 是否成立）。
```java
// Integer i = ?
Integer.class.isAssignableFrom(Integer.class); // true，因为Integer可以赋值给Integer
// Number n = ?
Number.class.isAssignableFrom(Integer.class); // true，因为Integer可以赋值给Number
// Object o = ?
Object.class.isAssignableFrom(Integer.class); // true，因为Integer可以赋值给Object
// Integer i = ?
Integer.class.isAssignableFrom(Number.class); // false，因为Number不能赋值给Integer
```

## 🎭 动态代理 (Dynamic Proxy)
Java 提供了一种强大的机制，允许在 **运行时** 动态地创建一个实现了指定接口的 **代理对象**，而无需手动编写实现类。

我们来比较Java的`class`和`interface`的区别：
- `class`可以实例化（非`abstract`）；
- `interface`不能实例化。

- **动态代理的目标：** 在不编写 `MyImplementation` 类的情况下，创建一个 `MyInterface` 类型的实例。

### 静态代理 vs. 动态代理
*   **静态代理 (常规方式):**
    1.  定义接口 `Hello`。
    2.  编写实现类 `HelloWorld implements Hello`。
    3.  创建实例 `Hello hello = new HelloWorld();`。
*   **动态代理:**
    1.  定义接口 `Hello`。
    2.  **不编写** 实现类。
    3.  使用 `java.lang.reflect.Proxy` 类在运行时 **动态创建** 一个实现了 `Hello` 接口的对象。
- 这种没有实现类但是在运行期动态创建了一个接口对象的方式，我们称为动态代码。
- JDK提供的动态创建接口对象的方式，就叫动态代理。

### 如何使用动态代理
核心是 `Proxy.newProxyInstance()` 方法和 `InvocationHandler` 接口。

```java
import java.lang.reflect.InvocationHandler;
import java.lang.reflect.Method;
import java.lang.reflect.Proxy;

public class Main {
    public static void main(String[] args) {
    //1. 创建 InvocationHandler 实例。定义了当代理对象的方法被调用时，应该执行什么逻辑。
        InvocationHandler handler = new InvocationHandler() {
            @Override
            public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
                System.out.println("--> Invoking method: " + method.getName() + " on proxy instance");
                // 根据方法名进行不同的处理
                if ("morning".equals(method.getName()))) {
                    System.out.println("Good morning, " + args[0] + "!");
                }
                return null; //void方法
            }
            if("echo".equals(method.getName())){
	            String result = "Echo: " + args[0];
				System.out.println("Returning: "+ result);
				return result; //返回方法期望类型
				}
				//如果有其他未处理的方法，可以抛异常或返回默认值
				System.out.println("Unhandled method: " + method.getName());
				return null;
			}
        };
        // 2. 使用 Proxy.newProxyInstance() 创建代理对象
        Hello helloProxy = (Hello) Proxy.newProxyInstance(
            Hello.class.getClassLoader(),   // a) 类加载器: 通常使用接口的类加载器
            new Class<?>[] { Hello.class }, // b) 要实现的接口数组: 必须至少包含一个接口
            handler                         // c) InvocationHandler: 处理方法调用的实例
            );   
        // 3.像调用普通接口一样使用代理对象
        System.out.println("\nCalling proxy methods:");
        helloProxy.morning("Alic
        e");
        String response = helloProxy.echo("Testing Proxy");
        System.out.println("Proxy response: " + response);

		// 尝试调用一个未在InvocationHandler中明确处理的方法（如果有接口的话）
		// helloProxy.someOtherMethod(); //会进入invoke方法的 unhandled分支
    }
}

// 定义接口
	interface Hello {
	    void morning(String name);
	    String echo(String message); // 添加一个带返回值的方法
	}
}
```

在运行期动态创建一个`interface`实例的方法如下：

1. 定义一个`InvocationHandler`实例，它负责实现接口的方法调用；
2. 通过`Proxy.newProxyInstance()`创建`interface`实例
3. 将返回的`Object`强制转型为接口。

**`Proxy.newProxyInstance()` 参数详解:**

1.  **`ClassLoader loader`**: 指定用哪个类加载器来加载动态生成的代理类。通常使用被代理接口的类加载器 (`TargetInterface.class.getClassLoader()`)。
2.  **`Class<?>[] interfaces`**: 一个 `Class` 对象数组，指定代理对象需要实现哪些接口。
3.  **`InvocationHandler h`**: 一个实现了 `InvocationHandler` 接口的对象。**所有** 对代理对象的方法调用，最终都会转发到这个 `handler` 的 `invoke` 方法上。

**`InvocationHandler.invoke()` 方法详解:**

`Object invoke(Object proxy, Method method, Object[] args)`
*   `proxy`: 动态生成的代理对象实例本身。**注意：** 通常不在 `invoke` 方法内部直接调用 `proxy` 上的方法，否则可能导致无限递归。
*   `method`: 被调用的接口方法的 `Method` 对象 (例如 `Hello` 接口的 `morning` 方法对应的 `Method` 对象)。你可以通过 `method.getName()` 获取方法名，`method.getParameterTypes()` 获取参数类型等。
*   `args`: 调用方法时传递的参数数组。如果方法无参数，则为 `null` 或空数组。
*   **返回值**: `invoke` 方法的返回值会作为代理对象方法调用的返回值。如果接口方法返回 `void`，`invoke` 应返回 `null`。如果返回基本类型，`invoke` 应返回对应的包装类型。

### 动态代理的原理
实际上，`Proxy.newProxyInstance()` 在运行时：

1.  根据你提供的接口 (`Hello.class`)，在JVM运行期**动态地生成** 一个新的 `class` 的字节码。这个类实现了 `Hello` 接口。
2.  这个生成的类内部大概是这样的（伪代码）：
  ```java
    // JVM 动态生成的类 (我们看不到源码)
    public final class $Proxy0 extends Proxy implements Hello {
        private InvocationHandler handler;

        // 构造方法接收 InvocationHandler
        public $Proxy0(InvocationHandler h) {
            super(h); // Proxy 类需要 InvocationHandler
            this.handler = h;
        }

        // 实现接口中的方法
        @Override
        public void morning(String name) {
            try {
                // 将调用转发给 InvocationHandler 的 invoke 方法
                Method method = Hello.class.getMethod("morning", String.class);
                this.handler.invoke(this, method, new Object[]{name});
            } catch (Throwable e) {
                // 处理异常...
            }
        }

        @Override
        public String echo(String message) {
             try {
                Method method = Hello.class.getMethod("echo", String.class);
                // 将调用转发给 InvocationHandler，并返回其结果
                return (String) this.handler.invoke(this, method, new Object[]{message});
            } catch (Throwable e) {
                // 处理异常...
                return null; // 或抛出异常
            }
        }
        // ... 其他接口方法类似 ...
    }
    ```
3. 其实就是JVM帮我们自动编写了一个上述类（不需要源码，可以直接生成字节码），创建了这个类的实例并返回，所以本质还是class的实例而不是interface实力胡。

所以，当你调用 `helloProxy.morning("Alice")` 时，实际上是调用了动态生成的 `$Proxy0` 类的 `morning` 方法，而这个方法内部又调用了你提供的 `InvocationHandler` 的 `invoke` 方法。

> [!INFO] 应用场景
> 动态代理广泛应用于 AOP (面向切面编程)、RPC (远程过程调用) 框架、数据库连接池、事务管理、日志记录、权限控制等场景，用于在不修改原始代码的情况下，为接口方法调用添加额外的通用逻辑。