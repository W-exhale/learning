## Part 1 Lambda基础
在 Java 中，方法通常分为实例方法和静态方法（带有 `static` 关键字）。

*   **实例方法**：隐含地传入一个 `this` 变量，指向当前实例。
*   **静态方法**：不依赖于类的实例，直接通过类名调用。

这两种方法在本质上都类似于过程式语言（如 C 语言）中的函数。

**函数式编程**（Functional Programming）是一种编程范式，它将**函数**视为基本运算单元。在这种范式下：

*   函数可以赋值给变量。
*   函数可以作为参数传递给其他函数。
*   函数可以作为另一个函数的返回值。

函数式编程的理论基础之一是 **Lambda 演算**，因此支持函数式编程的编码风格常被称为 **Lambda 表达式**。

函数式编程的一个核心特点是允许将函数本身作为参数传递或作为返回值返回，这极大地增强了代码的灵活性和表达力。
### Lambda表达式
在 Java 开发中，经常会遇到只包含一个抽象方法的接口，这类接口被称为**单方法接口**。常见的例子包括：

*   `Comparator`
*   `Runnable`
*   `Callable`

以`Comparator`为例，我们想要调用`Arrays.sort()`对数组进行自定义排序时，可以传入一个`Comparator`实例，以匿名类方式编写如下：
```java
String[] array = ...;
Arrays.sort(array, new Comparator<String>()//对数组使用比较器的逻辑排序，Comparator接口用于定义自定义排序规则
{
	@Override
    public int compare(String s1, String s2) {
        return s1.compareTo(s2);
    }
});// String类实现了Comparator接口，compareTo表示按字典顺序排序
```
 从Java 8开始，我们可以用Lambda表达式替换单方法接口。改写上述代码如下：

```java
// Lambda
import java.util.Arrays;

public class Main {
    public static void main(String[] args) {
        String[] array = new String[] { "Apple", "Orange", "Banana", "Lemon" };
        Arrays.sort(array, (s1, s2) -> {
            return s1.compareTo(s2);
        });
        System.out.println(String.join(", ", array));
    }
}
```

- Lambda表达式写法，只需要写出方法定义
```
(s1, s2) -> {
    return s1.compareTo(s2);
}

(parameters) -> { body }
```

*   `(s1, s2)`：参数列表。参数类型（这里是 `String`）可以省略，编译器会自动推断。
*   `->`：Lambda 操作符，分隔参数和方法体。
*   `{ ... }`：方法体，包含具体的实现逻辑。

Lambda表达式没有`class`定义，因此写法非常简洁。

**简化写法**：
如果方法体只有一行 `return` 语句，可以进一步简化：
```java
// 省略 {} 和 return
Arrays.sort(array, (s1, s2) -> s1.compareTo(s2));
```

返回值的类型（这里是 `int`）也是由编译器根据上下文自动推断的。

### FunctionalInterface
我们把只定义了一个抽象方法的接口称为 **函数式接口**（Functional Interface），并推荐使用 `@FunctionalInterface` 注解来标记它。这个注解会强制编译器检查该接口是否确实只有一个抽象方法。

```java
@FunctionalInterface
public interface Callable<V> {
    V call() throws Exception;  // 只有一个抽象方法 call()
}
```

再来看`Comparator`接口：

```java
@FunctionalInterface
public interface Comparator<T> {
	// 唯一的抽象方法
    int compare(T o1, T o2);
	// 从 Object 类继承的方法，不计入抽象方法数量
    boolean equals(Object obj);
	// default 方法，不计入抽象方法数量
    default Comparator<T> reversed() {
        return Collections.reverseOrder(this);
    }
	// 另一个 default 方法
    default Comparator<T> thenComparing(Comparator<? super T> other) {
        ...
    }
    // 可能还有其他的 default 或 static 方法
    // ...
}
```

- 虽然`Comparator`接口有很多方法，但只有一个抽象方法`int compare(T o1, T o2)`，其他的方法都是`default`方法或`static`方法。
- 另外注意到`boolean equals(Object obj)`是`Object`定义的方法，不算在接口方法内。
- 因此，`Comparator`也是一个`FunctionalInterface`。

## Part 2 方法引用（Method Reference）
使用Lambda表达式，我们就可以不必编写`FunctionalInterface`接口的实现类，从而简化代码：

```java
Arrays.sort(array, (s1, s2) -> {
    return s1.compareTo(s2);
});
```
除了 Lambda 表达式，还可以直接传入**方法引用**（Method Reference）。

```java
import java.util.Arrays;

public class Main {
    public static void main(String[] args) {
        String[] array = new String[] { "Apple", "Orange", "Banana", "Lemon" };
        // 直接传入静态方法 cmp 的引用
        Arrays.sort(array, Main::cmp);
        System.out.println(String.join(", ", array));
    }
	// 静态方法，签名与 Comparator<String>.compare 一致
    static int cmp(String s1, String s2) {
        return s1.compareTo(s2);
    }
}
```

*   `Main::cmp` 表示对 `Main` 类中静态方法 `cmp` 的引用。

*   **方法引用**：如果某个方法的签名（参数类型列表和返回类型）与函数式接口的抽象方法一致，就可以直接传递该方法的引用。

*   `Comparator<String>` 接口的抽象方法是 `int compare(String s1, String s2)`。
*   静态方法 `int cmp(String s1, String s2)` 的签名与其匹配（忽略方法名）。
- 方法签名只看参数类型和返回类型，不看方法名称，也不看类的继承关系。

**示例：引用实例方法**
```java
import java.util.Arrays;

public class Main {
    public static void main(String[] args) {
        String[] array = new String[] { "Apple", "Orange", "Banana", "Lemon" };
        Arrays.sort(array, String::compareTo);
        System.out.println(String.join(", ", array));
    }
}
```

观察`String.compareTo()`的方法定义：
```java
public final class String {
    public int compareTo(String o) {
        ...
    }
}
```

这个方法的签名只有一个参数，为什么和`int Comparator<String>.compare(String, String)`能匹配呢？
*   因为实例方法调用时，第一个参数是隐式的 `this`。
*   `s1.compareTo(s2)` 实际上可以看作 `int compareTo(String this, String anotherString)`。
*   编译器能够匹配 `(String s1, String s2)` 到 `String::compareTo`，其中 `s1` 成为调用 `compareTo` 的 `this` 实例，`s2` 成为传递给 `compareTo` 的参数。

### 构造方法引用
除了可以引用静态方法和实例方法，我们还可以引用构造方法。

**场景**：将 `List<String>` 转换为 `List<Person>`。

```java
class Person {
    String name;
    public Person(String name) {
        this.name = name;
    }
}

List<String> names = List.of("Bob", "Alice", "Tim");
List<Person> persons = ???
```

- 传统的做法是先定义一个`ArrayList<Person>`，然后用`for`循环填充这个`List`：
```java
List<String> names = List.of("Bob", "Alice", "Tim");
List<Person> persons = new ArrayList<>();
for (String name : names) {
    persons.add(new Person(name));
}
```

**使用构造方法引用**（结合 Stream API）：
```java
// 引用构造方法
import java.util.*;
import java.util.stream.*;

public class Main {
    public static void main(String[] args) {
        List<String> names = List.of("Bob", "Alice", "Tim");
        List<Person> persons = names.stream()//创建一个Stream
        .map(Person::new)//引用Person(String name)构造方法，将每个String元素通过Person的构造函数转换为Person对象
        .collect(Collectors.toList());//将Stream中的Person对象收集到一个List中
        System.out.println(persons); // 输出: [Person:Bob, Person:Alice, Person:Tim]
    }
}

class Person {
    String name;
    public Person(String name) {
        this.name = name;
    }
    public String toString() {
        return "Person:" + this.name;
    }
}
```

   *   `map` 方法需要一个 `Function<T, R>` 接口，其方法是 `R apply(T t)`。
    *   在这里，`T` 是 `String`，`R` 是 `Person`，所以需要一个 `Person apply(String name)` 的实现。
    *   `Person` 的构造方法 `Person(String name)` 正好符合这个签名（接收 `String`，隐式返回 `Person` 实例）。
    *   构造方法引用的语法是 `ClassName::new`。
这里的`map()`需要传入的FunctionalInterface的定义是：
```java
@FunctionalInterface
public interface Function<T, R> {
    R apply(T t);
}
```

## Part 3 使用Stream
Java 8 引入了全新的 **Stream API**（位于 `java.util.stream` 包），它提供了一种声明式、函数式的方式来处理数据集合。

**注意**：`java.util.stream.Stream` 不同于 `java.io` 包中的 `InputStream` 和 `OutputStream`。：

| 特性         | `java.io` (InputStream/OutputStream) | `java.util.stream.Stream`        |
| :----------- | :----------------------------------- | :------------------------------- |
| **数据类型** | 顺序读写的 `byte` 或 `char`          | 顺序输出的任意 Java 对象实例     |
| **主要用途** | 文件/网络 I/O，序列化                | 内存计算，集合处理，业务逻辑转换 |

**Stream 与 List 的区别**：

*   **List**：是一个存储元素的**容器**，所有元素都已存在于内存中。主要用于操作一组**已存在**的对象。
*   **Stream**：代表一个**元素序列**，这些元素可能并未预先存储，而是**按需计算**（惰性计算）。主要用于对元素序列进行**计算和转换**。

| 特性         | `java.util.List`             | `java.util.stream.Stream`        |
| :----------- | :--------------------------- | :------------------------------- |
| **元素存储** | 已分配并存储在内存           | 可能未分配，实时按需计算         |
| **核心用途** | 操作一组已存在的 Java 对象   | 惰性计算，数据流转换与处理       |

**示例：无限序列**
`List` 无法表示无限序列（如所有自然数），因为内存有限。
```java
List<BigInteger> allNaturals = ??? // 不可能实现
```

`Stream` 可以表示无限序列：
```java
Stream<BigInteger> naturals = createNaturalStream(); // 假设有此方法创建自然数流
```

首先，我们可以对每个自然数做一个平方，这样我们就把这个`Stream`转换成了另一个`Stream`：

```java
Stream<BigInteger> naturals = createNaturalStream(); // 全体自然数
Stream<BigInteger> squaredNaturals = naturals.map(n -> n.multiply(n)); //全体自然数的平方 (转换操作，惰性)

// 要处理无限流，需要先限制其大小
squaredNaturals.limit(100) // 截取前 100 个 (转换操作，惰性)
.forEach(System.out::println); // 最终操作，触发计算并打印
```

和python的generator类似，
- `Stream`的特点：
	1. “存储”有限个或无限个元素。
	2. 一个`Stream`可以轻易地转换为另一个`Stream`，而不是修改原`Stream`本身。
	3. 真正的计算通常发生在最后结果的获取，也就是惰性计算。
**Stream API 基本流程**：

1.  **创建 Stream**：从数据源（集合、数组、生成器等）获取 Stream。
2.  **中间操作 (Intermediate Operations)**：进行零次或多次转换（`map`, `filter`, `sorted`, `limit` 等），每次转换返回一个新的 Stream。这些操作是惰性的。
3.  **最终操作 (Terminal Operation)**：执行计算并产生结果或副作用（`collect`, `reduce`, `forEach`, `count` 等）。触发实际计算。

```java
 int result = createSomeStream()       // 1. 创建 Stream
              .filter(n -> n % 2 == 0) // 2. 中间操作 (转换)
              .map(n -> n * n)         // 2. 中间操作 (转换)
              .limit(100)              // 2. 中间操作 (转换)
              .sum();                  // 3. 最终操作 (聚合)
```

### 1. 创建Stream
#### Stream.of()
使用静态方法 `Stream.of()`，传入可变参数，创建包含确定元素的 Stream。
```java
import java.util.stream.Stream;

public class Main {
    public static void main(String[] args) {
        Stream<String> stream = Stream.of("A", "B", "C", "D");
        // forEach()是最终操作，
        // 可传入符合Consumer接口的void accept(T t)的方法引用：
        stream.forEach(System.out::println);// 对流中的每个元素执行指定的操作（打印）
    }
}
```
虽然这种方式基本上没啥实质性用途，但测试的时候很方便。

#### 基于数组或Collection
*   **数组**: 使用 `Arrays.stream()`。
*   **Collection (List, Set, etc.)**: 调用集合实例的 `stream()` 方法。

`Stream`输出的元素就是数组或者Collection持有的元素：
```java
import java.util.*;
import java.util.stream.*;

public class Main {
    public static void main(String[] args) {
	    // 从数组创建
        Stream<String> stream1 = Arrays.stream(new String[] { "A", "B", "C" });
	    stream1.forEach(System.out::println);
	    //或者：stream1.forEach(s -> System.out.print(s + " ")); // 输出: A B C
        System.out.println();
        
        Stream<String> stream2 = List.of("X", "Y", "Z").stream();
        stream2.forEach(System.out::println);
        //stream2.forEach(s -> System.out.print(s + " ")); // 输出: X Y Z
        System.out.println();
    }
}
```
上述创建`Stream`的方法都是把一个现有的序列变为`Stream`，它的元素是固定的。

#### 基于Supplier
- 使用 `Stream.generate()` 方法，传入一个 `Supplier<T>` 接口的实例。
- `Supplier` 的 `get()` 方法会被不断调用以生成 Stream 的下一个元素。这种方式可以创建无限流。

例如，我们编写一个能不断生成自然数的`Supplier`，它的代码非常简单，每次调用`get()`方法，就生成下一个自然数：
```java
import java.util.function.*;
import java.util.stream.*;

public class Main {
    public static void main(String[] args) {
	    // 使用 Supplier 创建一个自然数序列 (无限流)
        Stream<Integer> natual = Stream.generate(new NatualSupplier());
        
        // 注意：处理无限流时，必须先用 limit() 等操作将其变为有限流
        System.out.println("First 20 natural numbers:");
        
        naturalStream.limit(20) // 截取前 20 个元素
                     .forEach(System.out::println); // 打印
    }
}
// Supplier 实现，每次调用 get() 返回下一个自然数
class NatualSupplier implements Supplier<Integer> {
    int n = 0;
    @Override
    public Integer get() {
        n++;
        return n;
    }
}
```

**警告**：对无限流直接调用 `forEach()`, `count()` 等最终操作会导致无限循环或程序挂起。
解决：用`limit()`方法可以截取前面若干个元素，这样就变成了一个有限序列，对这个有限序列调用`forEach()`或者`count()`操作就没有问题。
#### 其他方法
- 通过一些API提供的接口，直接获得`Stream`。

- **`Files.lines()`**： 可以把一个文件变成一个`Stream`，每个元素代表文件的一行内容：

```java
try (Stream<String> lines = Files.lines(Paths.get("/path/to/file.txt"))) {
    ...
}
```
此方法对于按行遍历文本文件十分有用。

- **`Pattern.splitAsStream()`**：可以直接把一个长字符串分割成`Stream`序列而不是数组：（Pattern正则表达式对象）
	```java
    import java.util.regex.Pattern;
    import java.util.stream.Stream;

    public class RegexStream {
        public static void main(String[] args) {
            Pattern p = Pattern.compile("\\s+"); // 按空白符分割
            Stream<String> words = p.splitAsStream("The quick brown fox jumps over the lazy dog");
            words.forEach(System.out::println);
        }
    }
	```

#### 基本类型 Stream

- Java的泛型不支持基本类型，所以我们无法用`Stream<int>`这样的类型，会发生编译错误。为了保存`int`，直接使用 `Stream<Integer>` 会涉及频繁自动装箱/拆箱，可能影响性能。

为此，标准库提供了针对基本类型的 Stream：(和Stream差不多主要是用来提高运行效率)
*   `IntStream`
*   `LongStream`
*   `DoubleStream`
它们提供了与 `Stream<T>` 类似的操作，并包含一些针对数值计算的特有方法（如 `sum()`, `average()`）。

```java
import java.util.Arrays;
import java.util.List;
import java.util.stream.*;

public class PrimitiveStreamDemo {
    public static void main(String[] args) {
        // int[] -> IntStream
        int[] intArray = {1, 2, 3, 4, 5};
        IntStream intStream = Arrays.stream(intArray);
        System.out.println("Sum of ints: " + intStream.sum()); // 输出: 15

        // List<String> -> LongStream
        List<String> strList = List.of("10", "20", "30");
        LongStream longStream = strList.stream()
                                       .mapToLong(Long::parseLong); // 转换成 LongStream
        System.out.println("Sum of longs: " + longStream.sum()); // 输出: 60
    }
}
```

### 2. 使用map
`Stream.map()`是`Stream`最常用的一个转换方法，它把一个`Stream`转换为另一个`Stream`。

接收一个 `Function` 函数作为参数，并将这个函数应用于 Stream 中的每个元素，生成一个新的 Stream，其元素是原 Stream 元素经过函数转换后的结果。
**概念图**：

```
    f(x) = x * x  (映射函数)

                  │
  ┌───┬───┬───┬───┼───┬───┬───┬───┐
  │   │   │   │   │   │   │   │   │
  ▼   ▼   ▼   ▼   ▼   ▼   ▼   ▼   ▼  (原始 Stream)
[ 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 ]
  │   │   │   │   │   │   │   │   │
  ▼   ▼   ▼   ▼   ▼   ▼   ▼   ▼   ▼  (应用 map 后的新 Stream)
[ 1 | 4 | 9 |16 |25 |36 |49 |64 |81 ]
```

**代码示例**：
可见，`map`操作，把一个`Stream`的每个元素一一对应到应用了目标函数的结果上。
```java
Stream<Integer> s1 = Stream.of(1, 2, 3, 4, 5);
// 使用 map 将每个数字 n 映射为其平方 n*n
Stream<Integer> s2 = s1.map(n -> n * n);
s2.forEach(n -> System.out.print(n + " ")); // 输出: 1 4 9 16 25
System.out.println();
```

如果我们查看`Stream`的源码，会发现`map()`方法接收的对象是`Function`接口对象，它定义了一个`apply()`方法，负责把一个`T`类型转换成`R`类型：
```java
<R> Stream<R> map(Function<? super T, ? extends R> mapper);
```
其中，`Function`的定义是：
```java
@FunctionalInterface
public interface Function<T, R> {
    // 将T类型转换为R:
    R apply(T t);
}
```

利用`map()`，不但能完成数学计算，对于字符串操作，以及任何Java对象都是非常有用的。
**应用示例：字符串处理**
```java
import java.util.*;
import java.util.stream.*;

public class Main {
    public static void main(String[] args) {
        List.of("  Apple ", " pear ", " ORANGE", " BaNaNa ")
            .stream() // 创建 Stream<String>
            .map(String::trim) // 移除首尾空格 -> "Apple", "pear", "ORANGE", "BaNaNa"
            .map(String::toLowerCase) // 转为小写 -> "apple", "pear", "orange", "banana"
            .forEach(System.out::println); // 打印结果
    }
}
```
### 3. 使用filter
`Stream.filter()`是`Stream`的另一个常用转换方法。

`Stream.filter()` 是一个**转换**操作，它接收一个 `Predicate` 函数作为参数。该函数对 Stream 中的每个元素进行测试，只有测试结果为 `true` 的元素会被保留下来，形成一个新的 Stream。

例如，我们对1，2，3，4，5这个`Stream`调用`filter()`，传入的测试函数`f(x) = x % 2 != 0`用来判断元素是否是奇数，这样就过滤掉偶数，只剩下奇数，因此我们得到了另一个序列1，3，5：

```
            f(x) = x % 2 != 0  (过滤条件：是否为奇数)

                  │
  ┌───┬───┬───┬───┼───┬───┬───┬───┐
  │   │   │   │   │   │   │   │   │
  ▼   ▼   ▼   ▼   ▼   ▼   ▼   ▼   ▼  (原始 Stream)
[ 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 ]
  │   X   │   X   │   X   │   X   │  (X 表示被过滤掉)
  ▼       ▼       ▼       ▼       ▼  (应用 filter 后的新 Stream)
[ 1       3       5       7       9 ]
```

用IntStream写出上述逻辑，代码如下：

```java
import java.util.stream.IntStream;

public class Main {
    public static void main(String[] args) {
        IntStream.of(1, 2, 3, 4, 5, 6, 7, 8, 9)
                 .filter(n -> n % 2 != 0) // 保留奇数
                 .forEach(n -> System.out.print(n + " ")); // 输出: 1 3 5 7 9
        System.out.println();
    }
}
```

`filter()`方法接收的对象是`Predicate`接口对象，它定义了一个`test()`方法，负责判断元素是否符合条件：
```java
@FunctionalInterface
public interface Predicate<T> {
    // 判断元素t是否符合条件:
    boolean test(T t);
}
```


`filter()`除了常用于数值外，也可应用于任何Java对象。
例如，从一组给定的`LocalDate`中过滤掉工作日，以便得到休息日：

```java
import java.time.*;
import java.util.function.*;
import java.util.stream.*;

public class Main {
    public static void main(String[] args) {
	    System.out.println("Weekends in Jan 2020:");
        Stream.generate(new LocalDateSupplier())// 生成日期流 (从 2020-01-01 开始)
                .limit(31)// 取 31 天
                .filter(ldt -> ldt.getDayOfWeek() == DayOfWeek.SATURDAY || ldt.getDayOfWeek() == DayOfWeek.SUNDAY)// 只保留周六或周日
                .forEach(System.out::println);
    }
}

// Supplier 生成连续日期
class LocalDateSupplier implements Supplier<LocalDate> {
    LocalDate start = LocalDate.of(2020, 1, 1);
    int n = -1;
    @Override
    public LocalDate get() {
        n++;
        return start.plusDays(n);
    }
}
```

### 4. 使用reduce
`map()`和`filter()`都是`Stream`的转换方法，而`Stream.reduce()`则是`Stream`的一个聚合方法，它可以把一个`Stream`的所有元素按照聚合函数聚合成一个结果。

**简单示例：求和**
```java
import java.util.stream.*;

public class Main {
    public static void main(String[] args) {
	    // reduce(初始值, 累加器函数)
        int sum = Stream.of(1, 2, 3, 4, 5, 6, 7, 8, 9)
				        .reduce(0, (acc, n) -> acc + n);
        System.out.println(sum); // 45
    }
}
```

*   `reduce()` 方法接收的第二个参数是一个 `BinaryOperator<T>` 接口的实例。
* 它定义了一个`apply()`方法，负责把上次累加的结果和本次的元素 进行运算，并返回累加的结果：
```java
@FunctionalInterface
public interface BinaryOperator<T> {
    // Bi操作：两个输入，一个输出
    T apply(T t, T u);
}
```

可见，`reduce()`操作首先初始化结果为指定值（这里是0），紧接着，`reduce()`对每个元素依次调用`(acc, n) -> acc + n`，其中，`acc`是上次计算的结果：
```plain
// 计算过程:
acc = 0 // 初始化为指定值
acc = acc + n = 0 + 1 = 1 // n = 1
acc = acc + n = 1 + 2 = 3 // n = 2
acc = acc + n = 3 + 3 = 6 // n = 3
acc = acc + n = 6 + 4 = 10 // n = 4
acc = acc + n = 10 + 5 = 15 // n = 5
acc = acc + n = 15 + 6 = 21 // n = 6
acc = acc + n = 21 + 7 = 28 // n = 7
acc = acc + n = 28 + 8 = 36 // n = 8
acc = acc + n = 36 + 9 = 45 // n = 9
```

因此，实际上这个`reduce()`操作是一个求和。


**`reduce` 不带初始值**：
如果省略初始值，`reduce` 方法返回一个 `Optional<T>`。这是因为如果 Stream 为空，则无法执行聚合操作，`Optional` 可以优雅地处理这种情况。
- **求和**
```java
import java.util.Optional;
import java.util.stream.Stream;

// Stream<Integer> stream = Stream.of(1, 2, 3, 4, 5); // 或者 Stream.empty();
Optional<Integer> opt = stream.reduce((acc, n) -> acc + n); //返回Optional对象，可以后续用来判断是否有元素

if (optSum.isPresent()) {
    System.out.println("Sum (Optional): " + optSum.get());
} else {
    System.out.println("Stream was empty, no sum calculated.");
    
}
```

**示例：求积**
```java
import java.util.stream.*;

public class Main {
    public static void main(String[] args) {
	    // 求积时，初始值必须是 1
        int s = Stream.of(1, 2, 3, 4, 5, 6, 7, 8, 9).reduce(1, (acc, n) -> acc * n);
        System.out.println("Product: " + product); // 输出: Product: 362880 (9!)
    }
}
```

注意：计算求积时，初始值必须设置为`1`。

`reduce()` 不仅限于数值计算，也可以用于聚合任意 Java 对象。例如，将配置文件（表示为 `List<String>`，每行格式 `key=value`）聚合成一个 `Map<String, String>`。

```java
import java.util.*;
import java.util.stream.*;

public class ReduceToMapDemo {
    public static void main(String[] args) {
	    // 按行读取配置文件:，模拟配置项
        List<String> props = List.of("profile=native", "debug=true", "logging=warn", "interval=500");

        Map<String, String> configMap = props.stream()
            // 1. map: 将 "k=v" 字符串转换为 Map.of(k, v)，即拆分为键值对
            .map(kv -> {
                String[] parts = kv.split("=", 2);// 按字符串按等号分为两部分，限制分割次数为2，避免配置值中可能出现额外的=
                // 创建只包含一个条目的临时 Map
                return (parts.length == 2) ? Map.of(parts[0], parts[1]) : Map.<String, String>of();//如果分割后的数组长度为2，说明拆分成功，使用Map.of创建一个只包含该键值对的不可变临时Map，如果分割失败（例如不符合key=value格式），返回一个空的Map
            })
            // 2. reduce: 将所有单条目 Map 合并到一个 HashMap
            .reduce(new HashMap<String, String>(), // 初始值是一个空的 HashMap
                    (accumulatedMap, singleEntryMap) -> {
                        accumulatedMap.putAll(singleEntryMap); // 将当前条目放入累积的 Map
                        return accumulatedMap; // 返回更新后的累积 Map
                    });

        // 打印最终聚合的 Map
        configMap.forEach((k, v) -> System.out.println(k + " = " + v));
        /*
        输出:
        profile = native
        debug = true
        logging = warn
        interval = 500
        */
    }
}
```

### 5. 输出集合 (Collecting Results)

Stream 操作可分为两类：

1.  **转换操作 (Intermediate Operations)**：如 `map()`, `filter()`。它们返回一个新的 Stream，并且是**惰性**的，即在调用最终操作前不执行计算。（不会触发计算）
2.  **聚合操作 (Terminal Operations)**：如 `reduce()`, `collect()`, `forEach()`, `count()`。它们触发 Stream 的实际计算，并产生一个最终结果（非 Stream 类型）或副作用。（确定的结果）

**惰性计算实验**：
```java
import java.util.function.Supplier; 
import java.util.stream.Stream;

public class Main {
    public static void main(String[] args)     {
	    System.out.println("Creating infinite stream pipeline...");
		Stream<Long> s1 = Stream.generate(new NatualSupplier());  // 无限自然数流
        Stream<Long> s2 = s1.map(n -> n * n);
        Stream<Long> s3 = s2.map(n -> n - 1);
        
        // 仅仅打印 Stream 对象本身，不触发计算
        System.out.println(s3); // 输出类似: Pipeline created: java.util.stream.ReferencePipeline$2@...
	    System.out.println("No computation happened yet.");
	    
    }
}

class NatualSupplier implements Supplier<Long> {
    long n = 0;
    @Override
    public Long get() {
        n++;
        return n;
    }
}
```

- 执行上述代码，既不会有任何内存增长，也不会有任何计算，因为转换操作只是保存了转换规则，无论我们对一个`Stream`转换多少次，都不会有任何实际计算发生。

而聚合操作则不一样，聚合操作会立刻促使`Stream`输出它的每一个元素，并依次纳入计算，以获得最终结果。所以，对一个`Stream`进行聚合操作，会触发一系列连锁反应：

```java

Stream<Long> s1 = Stream.generate(new NatualSupplier());
Stream<Long> s2 = s1.map(n -> n * n);
Stream<Long> s3 = s2.map(n -> n - 1);
Stream<Long> s4 = s3.limit(10);  // 仍然是转换操作

long sum = s4.reduce(0L, (acc, n) -> acc + n); // 聚合操作！触发计算

// 1. reduce() 请求 s4 的第一个元素
// 2. s4 (limit) 请求 s3 的第一个元素
// 3. s3 (map n-1) 请求 s2 的第一个元素
// 4. s2 (map n*n) 请求 s1 的第一个元素
// 5. s1 (generate) 调用 Supplier.get() 得到 1
// 6. 1 经过 s2 -> 1*1=1
// 7. 1 经过 s3 -> 1-1=0
// 8. 0 经过 s4 (limit) -> 0 (未达到限制)
// 9. reduce() 接收到 0，计算 acc = 0 + 0 = 0
// 10. reduce() 请求 s4 的第二个元素... (重复 2-9) ... 直到 limit 达到 10 个元素
```

可见，聚合操作是真正需要从`Stream`请求数据的，对一个`Stream`做聚合计算后，结果就不是一个`Stream`，而是一个其他的Java对象。

#### 输出为List

`reduce()`只是一种聚合操作，如果我们希望把`Stream`的元素保存到集合，例如`List`，因为`List`的元素是确定的Java对象，因此，把`Stream`变为`List`不是一个转换操作，而是一个聚合操作，它会强制`Stream`输出每个元素。

下面的代码演示了如何将一组`String`先过滤掉空字符串，然后把非空字符串保存到`List`中：（使用 `collect()` 方法和 `Collectors.toList()` 可以将 Stream 元素收集到一个 `List` 中）：

```java
import java.util.*;
import java.util.stream.*;

public class Main {
    public static void main(String[] args) {
        Stream<String> stream = Stream.of("Apple", "", null, "Pear", "  ", "Orange");
        List<String> list = stream
			.filter(s -> s != null && !s.isBlank())
			.collect(Collectors.toList());  // 收集到 List
        System.out.println(list);
        // 输出: [Apple, Pear, Orange]
    }
}
```

把`Stream`的每个元素收集到`List`的方法是调用`collect()`并传入`Collectors.toList()`对象，它实际上是一个`Collector`实例，通过类似`reduce()`的操作，把每个元素添加到一个收集器中（实际上是`ArrayList`）。

*   `Collectors.toList()` 提供了一个 `Collector` 实例（即`Collectors.toList()`对象），它内部（通常）使用 `ArrayList` 来收集元素。
*   类似地，`Collectors.toSet()` 可以收集到 `Set` 中（自动去重）。

#### 输出为数组
使用 `toArray()` 方法将 Stream 元素收集到数组中。需要提供一个数组构造器引用（如 `String[]::new`）。

```java
import java.util.List;
import java.util.Arrays;

public class CollectToArrayDemo {
    public static void main(String[] args) {
		List<String> list = List.of("Apple", "Banana", "Orange");
		
        // toArray 需要一个 IntFunction<A[]> generator（String[] apply(int)）
        // String[]::new 是一个符合要求的构造器引用 (int size) -> new String[size]
		String[] array = list.stream().toArray(String[]::new);
		System.out.println(Arrays.toString(stringArray)); // 输出: [Apple, Banana, Orange]
```

#### 输出为Map

使用 `Collectors.toMap()` 将 Stream 元素收集到 `Map` 中。需要提供两个函数：

1.  `keyMapper`: 将元素映射到 Map 的 Key。
2.  `valueMapper`: 将元素映射到 Map 的 Value。


```java
import java.util.*;
import java.util.stream.*;

public class Main {
    public static void main(String[] args) {
        Stream<String> stream = Stream.of("APPL:Apple", "MSFT:Microsoft");
        Map<String, String> map = stream
		        .filter(s -> s.contains(":")) // 确保格式正确
                .collect(Collectors.toMap(
                        // keyMapper: 提取冒号前的 Ticker Symbol
                        s -> s.substring(0, s.indexOf(':')),
                        // valueMapper: 提取冒号后的公司名称
                        s -> s.substring(s.indexOf(':') + 1)));
        System.out.println(map);
    }
}
```
**注意**：如果 `keyMapper` 产生重复的 Key，`Collectors.toMap()` 默认会抛出 `IllegalStateException`。可以提供第三个参数（合并函数）来处理 Key 冲突。

#### 分组输出（groupingBy）

`Collectors.groupingBy()` 是一个强大的聚合操作，用于根据指定条件将 Stream 元素分组，结果通常是一个 `Map`，其中 Key 是分组的依据，Value 是属于该组的元素集合。
```java
import java.util.*;
import java.util.stream.*;

public class Main {
    public static void main(String[] args) {
        List<String> list = List.of("Apple", "Banana", "Blackberry", "Coconut", "Avocado", "Cherry", "Apricots");
        // 按首字母分组，每组的值是包含对应水果的 List
        Map<String, List<String>> groups = list.stream()
                .collect(Collectors.groupingBy(// 分类器函数 (classifier): 提取首字母作为 Key
                s -> s.substring(0, 1).toUpperCase(),
                // 下游收集器 (downstream collector): 指定如何收集每个组内的元素
                 Collectors.toList()));// 将同组元素收集到 List
        System.out.println(groups);
        /*
        输出:每组是一个List
        {
            A=[Apple, Avocado, Apricots],
            B=[Banana, Blackberry],
            C=[Coconut, Cherry]
        }
        */
    }
}
```

*   `groupingBy` 的第一个参数是**分类器函数**（即分组的key），决定元素属于哪个组。
*   第二个参数（可选）是**下游收集器**，决定如何处理（聚合）每个组内的元素。默认为 `Collectors.toList()`。

**示例：按年级或班级对学生分组**
假设有这样一个`Student`类，包含学生姓名、班级和成绩：
```java
class Student {
    int gradeId; // 年级
    int classId; // 班级
    String name; // 名字
    int score; // 分数
    // 构造函数、getter 等省略...
}
    public int getGradeId() { return gradeId; }
    public String getName() { return name; }
    // ...
```

如果我们有一个`Stream<Student>`，利用分组输出，可以非常简单地按年级或班级把`Student`归类。

```java
Stream<Student> studentStream = ... ; // 获取学生流

// 按年级分组
Map<Integer, List<Student>> studentsByGrade = studentStream    .collect(Collectors.groupingBy(Student::getGradeId));

// 按年级分组，并统计每个年级的人数
Map<Integer, Long> countByGrade = studentStream
     .collect(Collectors.groupingBy(
         Student::getGradeId,
         Collectors.counting() // 下游收集器：统计数量
     ));
```

### 6. 其他操作
除了前面介绍的常用操作外，`Stream`还提供了一系列非常有用的方法。
#### 排序
*   `sorted()`: 对 Stream 元素进行自然排序（要求元素实现 `Comparable`）。
*   `sorted(Comparator<? super T> comparator)`: 使用自定义比较器进行排序。

```java
import java.util.*;
import java.util.stream.*;

public class Main {
    public static void main(String[] args) {
	    // 自然排序 (字典序)
        List<String> sortedList1 = List.of("Orange", "apple", "Banana")
            .stream()
            .sorted()  // 按字典序: Banana, Orange, apple
            .collect(Collectors.toList());
        System.out.println("Natural sort: " + sortedList1);
        
        // 自定义排序 (忽略大小写)
        List<String> sortedList2 = List.of("Orange", "apple", "Banana")
            .stream()
            .sorted(String::compareToIgnoreCase) // 按忽略大小写: apple, Banana, Orange
            .collect(Collectors.toList());
        System.out.println("Case-insensitive sort: " + sortedList2);
    }
}
```
注意`sorted()`只是一个转换操作，它会返回一个新的`Stream`。

#### 去重（distinct）

对一个`Stream`的元素进行去重，没必要先转换为`Set`，可以直接用`distinct()`：
```java
import java.util.List;
import java.util.stream.*;

public class DistinctDemo {
    public static void main(String[] args) {
		List.of("A", "B", "A", "C", "B", "D")
	    .stream()
	    .distinct() // 去重
	    .collect(Collectors.toList()); 
	    System.out.println("Distinct elements: " + distinctList); // 输出: [A, B, C, D]
```
#### 截取(`limit`, `skip`)

*   `limit(long maxSize)`: 截取 Stream 的前 `maxSize` 个元素。
*   `skip(long n)`: 跳过 Stream 的前 `n` 个元素。

这两个都是**转换**操作，常用于处理无限流或分页。

```java
import java.util.List;
import java.util.stream.*;

public class LimitSkipDemo {
    public static void main(String[] args) {
		List.of("A", "B", "C", "D", "E", "F")
	    .stream()
	    .skip(2) // 跳过A, B
	    .limit(3) // 截取C, D, E
	    .collect(Collectors.toList());
	System.out.println("Skipped and Limited: " + subList); // 输出: [C, D, E]
	    
```

#### 合并（concat）
使用静态方法 `Stream.concat(streamA, streamB)` 将两个 Stream 合并成一个新的 Stream。
```java
import java.util.List;
import java.util.stream.*;

public class ConcatDemo {
    public static void main(String[] args) {
		Stream<String> s1 = List.of("A", "B", "C").stream();
		Stream<String> s2 = List.of("D", "E").stream();
		
// 合并:
		Stream<String> s = Stream.concat(s1, s2);
		System.out.println(s.collect(Collectors.toList())); // [A, B, C, D, E]
```

#### flatMap

1. 将一个 `Stream<Container<T>>` (其中 Container 可以是 List, Set, Optional, 甚至 Stream 本身) “扁平化” 成一个 `Stream<T>`。
2. 它首先将每个容器映射（map）成一个 Stream，
3. 然后将这些 Stream 连接（concat）起来。

**场景**：有一个 `Stream<List<Integer>>`，想得到包含所有 List 中所有 Integer 的 `Stream<Integer>`。

```java
import java.util.*;
import java.util.stream.*;

public class FlatMapDemo {
    public static void main(String[] args) {
		Stream<List<Integer>> streamOfLists = Stream.of(
            List.of(1, 2, 3),
            List.of(4, 5),
            List.of(6, 7, 8, 9)
	    );
		// 使用 flatMap 将 Stream<List<Integer>> 转换为 Stream<Integer>
        Stream<Integer> flattenedStream = streamOfLists
            .flatMap(list -> list.stream()); // 将每个 List 转换为 Stream，然后合并
		System.out.println(flattenedStream.collect(Collectors.toList()));
        // 输出: [1, 2, 3, 4, 5, 6, 7, 8, 9]
    }
}

```

因此，所谓`flatMap()`，是指把`Stream`的每个元素（这里是`List`）映射为`Stream`，然后合并成一个新的`Stream`：

```
Stream<List<Integer>>
┌─────────────────┬───────────┬───────────────────┐
│ List[1, 2, 3]   │ List[4, 5]│ List[6, 7, 8, 9]  │
└─────────────────┴───────────┴───────────────────┘
         │              │              │
         │ map(list -> list.stream()) │
         ▼              ▼              ▼
Stream<Integer>[1,2,3] Stream[4,5] Stream[6,7,8,9]
         │              │              │
         └──────────────┼──────────────┘
                        │ concat (flatten)
                        ▼
           Stream<Integer>[1, 2, 3, 4, 5, 6, 7, 8, 9]
```

#### 并行（parallel）

将一个顺序 Stream 转换为并行 Stream，使得后续操作可能在多个线程上并行执行，以提高处理大数据量时的性能。

把一个普通`Stream`转换为可以并行处理的`Stream`非常简单，只需要用`parallel()`进行转换：
```java
import java.util.stream.LongStream;
import java.util.concurrent.TimeUnit;

public class ParallelDemo {
    public static void main(String[] args) {
		long limit = 1_000_000_000L; // 十亿
		
		// 顺序计算
        long start1 = System.nanoTime();
        long sum1 = LongStream.rangeClosed(1, limit).sum();
        long duration1 = TimeUnit.NANOSECONDS.toMillis(System.nanoTime() - start1);
        System.out.println("Sequential Sum: " + sum1 + " (took " + duration1 + " ms)");

        // 并行计算
        long start2 = System.nanoTime();
        long sum2 = LongStream.rangeClosed(1, limit).parallel().sum(); // 转换为并行流
        long duration2 = TimeUnit.NANOSECONDS.toMillis(System.nanoTime() - start2);
        System.out.println("Parallel Sum:   " + sum2 + " (took " + duration2 + " ms)");
    }
}
```

经过`parallel()`转换后的`Stream`只要可能，就会对后续操作进行并行处理。我们不需要编写任何多线程代码就可以享受到并行处理带来的执行效率的提升。

*   调用 `parallel()` 本身不保证并行执行，它只是标记该 Stream 适合并行处理。实际是否并行取决于 JVM、操作类型和数据源特性（如 `Spliterator` 的能力）。
*   并行流并非总是更快，对于小数据量或某些操作（如有序操作 `limit()`），并行开销可能超过收益。
*   需要注意并行流中的 Lambda 表达式和操作必须是线程安全的。

#### 其他聚合方法

除了`reduce()`和`collect()`外，`Stream`还有一些常用的聚合方法：

- `count()`：返回 Stream 中的元素数量 (long)。
*   `max(Comparator<? super T> comparator)`: 返回 Stream 中的最大元素 (`Optional<T>`)。
*   `min(Comparator<? super T> comparator)`: 返回 Stream 中的最小元素 (`Optional<T>`)。

针对`IntStream`、`LongStream`和`DoubleStream`，还额外提供了以下聚合方法：

- `sum()`：对所有元素求和；
- `average()`：对所有元素求平均数。

匹配操作 (`allMatch`, `anyMatch`, `noneMatch`)：

*   `allMatch(Predicate<? super T> predicate)`: 是否**所有**元素都满足条件
*   `anyMatch(Predicate<? super T> predicate)`: 是否**至少有一个**元素满足条件
*   `noneMatch(Predicate<? super T> predicate)`: 是否**没有**元素满足条件

这些操作通常是**短路**的，一旦结果确定（例如 `anyMatch` 找到一个匹配项），就不会处理剩余元素。


遍历 (`forEach`, `forEachOrdered`)

*   `forEach(Consumer<? super T> action)`: 对 Stream 的每个元素执行指定操作。这是一个**聚合**操作，没有返回值 (`void`)。对于并行流，不保证处理顺序。
*   `forEachOrdered(Consumer<? super T> action)`: 与 `forEach` 类似，但保证按 Stream 的原始顺序处理元素，即使在并行流中也是如此。

`forEach()`经常用于传入`System.out::println`来打印`Stream`的元素：
```java
Stream<String> stream = Stream.of("apple", "banana", "cherry");
stream.forEach(s -> System.out.println("Fruit: " + s));
```

### 7. 小结
*   **创建 Stream**: `Stream.of()`, `Arrays.stream()`, `collection.stream()`, `Stream.generate()`, `Files.lines()`, etc.
*   **转换操作 (Intermediate - 返回 Stream, 惰性)**:
    *   `map(Function)`: 元素一对一转换。
    *   `filter(Predicate)`: 筛选元素。
    *   `sorted()`, `sorted(Comparator)`: 排序。
    *   `distinct()`: 去重。
    *   `limit(long)`, `skip(long)`: 截取/跳过。
    *   `flatMap(Function)`: 扁平化 Stream。
    *   `peek(Consumer)`: 对每个元素执行操作（主要用于调试）。
    *   `parallel()`: 转换为并行流。
    *   `sequential()`: 转换为顺序流。
*   **聚合操作 (Terminal - 返回非 Stream 或 void, 触发计算)**:
    *   `collect(Collector)`: 收集到集合、Map 等。
    *   `reduce(identity, BinaryOperator)`, `reduce(BinaryOperator)`: 聚合为单个值。
    *   `count()`: 统计元素数量。
    *   `max(Comparator)`, `min(Comparator)`: 查找最大/最小值。
    *   `sum()`, `average()` (数值流): 求和/平均值。
    *   `forEach(Consumer)`, `forEachOrdered(Consumer)`: 遍历元素。
    *   `toArray()`, `toArray(IntFunction<A[]>)`: 转换为数组。
    *   `allMatch(Predicate)`, `anyMatch(Predicate)`, `noneMatch(Predicate)`: 条件匹配。
    *   `findFirst()`, `findAny()`: 查找元素 (`Optional<T>`)。