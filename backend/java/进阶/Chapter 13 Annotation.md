## Part 1 注解概要
### 什么是注解？

> [!NOTE] 定义
> 注解（Annotation）是放在 Java 源码的类、方法、字段、参数前的一种特殊“注释”。它本身不影响代码逻辑，但可以被编译器或工具读取和处理，用作标注的**元数据**（Metadata）。（元数据是描述数据的数据）

```java
// this is a component:
@Resource("hello") //应用于类的注解
public class Hello {
    @Inject  //应用于字段的注解
    int n;

    @PostConstruct //应用于方法的注解
    public void hello(@Param String name) {
//应用于参数的注解
        System.out.println(name);
    }

    @Override //Java 内建注解：是否成功覆写
    public String toString() {
        return "Hello";
    }
}
```
-   **注释 vs 注解**: 注释会被编译器直接忽略，而注解可以被编译器打包进 `.class` 文件，甚至在运行时通过反射读取。

### 注解的作用

> [!INFO] 注解的三种主要用途
> JVM 本身不识别注解，对代码逻辑没有影响，注解的功能完全由 **处理注解的工具** 决定。
>1. **编译器使用**:
>	- `@Override`：让编译器检查该方法是否正确实现了覆写
>	- `@SuppressWarnings`：告诉编译器忽略此处代码产生的警告
> 2.  **工具处理 `.class` 文件**:
> 	1. 有的工具在加载类时动态修改字节码，实现特殊功能（如AOP）
> 	2. 这类注解会被编译进 `.class` 文件，但加载后不一定存在于内存中。通常由底层库使用。
> 3.  **程序运行时读取**:
> 	1. 注解加载后一直存在于JVM中，可以通过反射API读取
> 	2. 常用，例如Spring框架通过读取`Component`，`@Autowired`等注解实现依赖注入
> 	3. 例如，`@PostConstruct`注解的方法会在调用构造方法后自动执行（Java代码读取该注解实现的功能，JVM并不会识别该注解）

### 注解的配置参数
注解可以定义配置参数，用于提供更详细的元数据。

-   **参数类型**:
    *   所有基本类型 (int, float, boolean, etc.)
    *   `String`
    *   `Class` (e.g., `Class<String>`)
    *   枚举类型 (`enum`)
    *   以上类型的数组 (e.g., `String[]`, `int[]`)
-   **参数值**: 必须是**常量**，在编译期就确定。（上述限制保证了注解在定义时就确定了每个参数的值）
-   **默认值**: 可以为参数指定 `default` 值。
-   **`value` 参数**:
    *   大部分注解会有一个名为`value`的配置参数
    *   如果注解只有一个参数且名为 `value`，或者有多个参数但只给 `value` 赋值，可以省略 `value=` 直接写值。
-   **无参数**: 如果只写注解名 `@AnnotationName`，表示所有参数都使用默认值。

```java
public class Hello {
	//定义了三个参数
    @Check(min=0, max=100, value=55)
    public int n;
	//定义了一个参数
    @Check(value=99)
    public int p;
	//和上面的一样
    @Check(99) // @Check(value=99)
    public int x;
	//所有参数使用默认值
    @Check
    public int y;
// 假设 Check 注解定义如下
/*
public @interface Check {
    int min() default 0;
    int max() default Integer.MAX_VALUE;
    int value() default -1; // 假设 value 有默认值
}
*/
}
```

## Part 2 定义注解

使用 `@interface` 关键字定义注解。

```java
public @interface Report {
    int type() default 0;
    String level() default "info";
    String value() default "";
}
```

> [!TIP] 最佳实践
> 1.  推荐为所有参数提供 `default` 值。
> 2.  将最常用的参数命名为 `value`。

### 元注解

> [!INFO] 定义
> 元注解（meta annotation）是**修饰其他注解**的注解，用于指示注解的使用方式和生命周期。

#### @Target
指定注解可以应用于哪些程序元素（类、方法、字段等）。
-   **常用 `ElementType` 值**:
    *   `TYPE`: 类、接口、枚举
    *   `FIELD`: 字段（包括枚举常量）
    *   `METHOD`: 方法
    *   `PARAMETER`: 方法参数
    *   `CONSTRUCTOR`: 构造方法
    *   `LOCAL_VARIABLE`: 局部变量
    *   `ANNOTATION_TYPE`: 注解类型
    *   `PACKAGE`: 包
-   **用法**:
    *   `@Target(ElementType.METHOD)`: 只能用于方法。
    *   `@Target({ElementType.METHOD, ElementType.FIELD})`: 可用于方法或字段。

1. 定义注解`@Report`可用在方法上，我们必须添加一个`@Target(ElementType.METHOD)`：
	```java
	@Target(ElementType.METHOD)
	public @interface Report {
	    int type() default 0;
	    String level() default "info";
	    String value() default "";
	}
```
2. 定义注解`@Report`可用在方法或字段上，可以把`@Target`注解参数变为数组`{ ElementType.METHOD, ElementType.FIELD }`：
	```java
	@Target({
	    ElementType.METHOD,
	    ElementType.FIELD
	})
	public @interface Report {
	    ...
	}
	```
实际上`@Target`定义的`value`是`ElementType[]`数组，只有一个元素时，可以省略数组的写法

#### @Retention
定义了`Annotation`的生命周期
- `RetentionPolicy.SOURCE`： 仅存在于源代码中，编译后丢弃（如 `@SuppressWarnings`）。
- `RetentionPolicy.CLASS`：保存在 `.class` 文件中，但 JVM 加载类时丢弃（默认值）。
- `RetentionPolicy.RUNTIME`：保存在 `.class` 文件中，并在 JVM 运行时保留，可以通过反射读取。

> [!IMPORTANT] 注意
> 如果`@Retention`不存在，则该`Annotation`默认为`CLASS`。自定义的注解如果需要在**运行时**通过反射处理，**必须**使用 `@Retention(RetentionPolicy.RUNTIME)`。

```java
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface Report {
    int type() default 0;
    String level() default "info";
    String value() default "";
}
```

#### @Repeatable
允许在同一个程序元素上**重复**使用同一个注解。需要一个额外的 "容器" 注解。这个注解应用不是特别广泛
```java


@Target(ElementType.TYPE) // 假设 Report 用于类
@Retention(RetentionPolicy.RUNTIME)
public @interface Reports {
    Report[] value();  // 包含一个 Report 数组
}

// 2. 使 Report 可重复，并指定容器注解
@Repeatable(Reports.class)
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
public @interface Report {
    int type() default 0;
    String level() default "info";
    String value() default "";
}
// 3. 使用
@Report(type=1, level="debug")
@Report(type=2, level="warning")
public class MyClass {
    // ...
}

```
#### @Inherited
指定注解是否可以被子类**继承**。

-   只对 `@Target(ElementType.TYPE)` 类型的注解有效。
-   只对 `class` 继承有效，对 `interface` 实现无效。

```java
@Inherited // 标记此注解可被子类继承
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
public @interface Report {
    int type() default 0;
    String level() default "info";
    String value() default "";
}

@Report
public class Person { }

// Student 类会自动继承 Person 类的 @Report 注解
public class Student extends Person { }
```

### 如何定义Annotation
1. 使用`@interface`：
	```java
	public @interface Report {
	}
	```
2. 添加参数、默认值：
	```java
	public @interface Report {
	    int type() default 0;
	    String level() default "info";
	    String value() default ""; // 假如没有默认值，则必须在使用时提供值，最好在定义设都设置默认值
	}
	```
3. 用元注解配置注解
	```java
	@Target(ElementType.TYPE)
	@Retention(RetentionPolicy.RUNTIME)
	public @interface Report {
	    int type() default 0;
	    String level() default "info";
	    String value() default "";
	}
	```
	其中，必须设置`@Target`和`@Retention`，`@Retention`一般设置为`RUNTIME`，因为我们自定义的注解通常要求在运行期读取

## Part 3 处理注解

> [!WARNING] 注解本身不执行任何操作
> Java 的注解对代码逻辑无直接影响。其效果取决于处理注解的代码（通常使用反射）。


Java的注解本身对代码逻辑没有任何影响。根据`@Retention`的配置：

- `SOURCE`类型的注解在编译期就被丢掉了；主要由编译器使用，一般只使用，不编写。
- `CLASS`类型的注解仅保存在class文件中，它们不会被加载进JVM；底层工具库使用，涉及到class的加载，一般很少用到
- `RUNTIME`类型的注解会被加载进JVM，并且在运行期可以被程序读取。经常使用编写

- 这里主要关注如何读取 `RUNTIME` 类型的注解

### 反射 API
注解定义后也是一种class，所有的注解都继承自`java.lang.annotation.Annotation`，因此，读取注解，需要使用反射API

Java 反射 API 提供了读取注解的方法：
-   **判断是否存在**: `isAnnotationPresent(Class<? extends Annotation> annotationClass)`
    *   `Class.isAnnotationPresent(...)`
    *   `Field.isAnnotationPresent(...)`
    *   `Method.isAnnotationPresent(...)`
    *   `Constructor.isAnnotationPresent(...)`
    * 判断某个注解是否存在于`Class`、`Field`、`Method`或`Constructor`：
-   **获取注解实例**: `getAnnotation(Class<T> annotationClass)`
    *   `Class.getAnnotation(...)`
    *   `Field.getAnnotation(...)`
    *   `Method.getAnnotation(...)`
    *   `Constructor.getAnnotation(...)`
    *   如果注解不存在，返回 `null`。
-   **获取所有注解**: `getAnnotations()` / `getDeclaredAnnotations()`
-   **获取方法参数注解**: `Method.getParameterAnnotations()` 返回 `Annotation[][]`

### 读取示例
**1. 读取类上的注解:**
```java
// 方式一：先判断再获取
Class<?> cls = Person.class;
if (cls.isAnnotationPresent(Report.class)) {
Report report = cls.getAnnotation(Report.class);
System.out.println("Type: " + report.type());
System.out.println("Level: " + report.level());
}

// 方式二：直接获取，判断 null
Report report = Person.class.getAnnotation(Report.class);
if (report != null) {
System.out.println("Value: " + report.value());
```
**2. 读取字段上的注解:** (类似类)

```java
Field field = Person.class.getField("name"); // 获取名为 name 的 public 字段
if (field.isAnnotationPresent(Range.class)) {
    Range range = field.getAnnotation(Range.class);
    System.out.println("Max length: " + range.max());
}
```

**3. 读取方法上的注解:** (类似类)

```java
Method method = Person.class.getMethod("setName", String.class); // 获取 setName(String) 方法
if (method.isAnnotationPresent(Deprecated.class)) { // 检查是否有 @Deprecated
    System.out.println("Method is deprecated!");
}
```


**4. 读取方法参数上的注解:** 方法参数本身可以看成一个数组，而每个参数又可以定义多个注解，所以一次获取方法参数的所有注解就必须用一个二维数组来表示。

```java
// 假设方法签名:
//public void process(@NotNull @Range(max=5) String data, @NotNull String id) {}

// 获取所有参数的注解 (二维数组)
Annotation[][] parameterAnnotations = method.getParameterAnnotations();

// 第一个参数 (data) 的注解
Annotation[] dataAnnotations = parameterAnnotations[0];
for (Annotation anno : dataAnnotations) {
    if (anno instanceof NotNull) {
        System.out.println("Parameter 'data' has @NotNull");
    } else if (anno instanceof Range range) { // Java 16+ Pattern Matching for instanceof
        System.out.println("Parameter 'data' has @Range with max=" + range.max());
    }
}

// 第二个参数 (id) 的注解
Annotation[] idAnnotations = parameterAnnotations[1];
// ... 类似处理 ...

```

### 使用注解：字段验证
注解如何使用，完全由程序自己决定。例如，JUnit是一
个测试框架，它会自动运行所有标记为`@Test`的方法。


`@Range`注解：我们希望用它来定义一个`String`字段的规则：字段长度满足`@Range`的参数定义

**1. 定义 `@Range` 注解:**
```java
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.FIELD)  // 只能用于字段
public @interface Range {
    int min() default 0;
    int max() default 255;
}
```

**2. 在 JavaBean 中使用注解:**

```java
public class Person {
    @Range(min=1, max=20)
    public String name; // 名字长度必须在 1 到 20 之间

    @Range(max=10)
    public String city;  // 城市长度最多为 10 (min 使用默认值 0)

    public int age; // 没有 @Range 注解，不检查
}
```

**3. 编写检查逻辑 (使用反射):**
这里，我们编写一个`Person`实例的检查方法，它可以检查`Person`实例的`String`字段长度是否满足`@Range`的定义：

```java
void check(Person person) throws IllegalArgumentException, ReflectiveOperationException {
    // 遍历 Person 类的所有 public 字段
    for (Field field : person.getClass().getFields()) {
        // 尝试获取字段上的 @Range 注解
        Range range = field.getAnnotation(Range.class);
        // 如果字段上有 @Range 注解
        if (range != null) {
            // 获取字段的当前值
            Object value = field.get(person);// 需要处理 ReflectiveOperationException
            // 如果值是String:
            if (value instanceof String s) {
                // 判断值是否满足@Range的min/max:
                if (s.length() < range.min() || s.length() > range.max()) {
                    throw new IllegalArgumentException("Invalid field: " + field.getName() + ". Length out of range [" + range.min() + ", " + range.max() + "]");
                }
            }
        }
    }
}
```

这样一来，我们通过`@Range`注解，配合`check()`方法，就可以完成`Person`实例的检查。注意检查逻辑完全是我们自己编写的，JVM不会自动给注解添加任何额外的逻辑。

**4. 调用检查方法:**

```java
Person p1 = new Person();
p1.name = "Xiao Ming";
p1.city = "Shanghai";
check(p1); // 通过检查

Person p2 = new Person();
p2.name = ""; // 长度 0, 小于 min=1
p2.city = "Beijing City"; // 长度 12, 大于 max=10
try {
    check(p2);
} catch (IllegalArgumentException e) {
    System.out.println("Validation failed: " + e.getMessage());
    // 输出类似: Validation failed: Invalid field: name. Length out of range [1, 20]
    // (取决于哪个字段先检查到)
}
```
