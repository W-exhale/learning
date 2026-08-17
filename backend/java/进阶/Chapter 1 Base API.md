- **API**：应用程序接口（Application Programming Interface），给客户用的
 - **Java API**：java自带的函数，类，规范就是API（给Java开发人员用的）

## Part 1 Scanner
获取用户输入
-   `next()`: 读取到空格或换行符之前的内容作为字符串。
-   `nextLine()`: 读取到换行符之前的所有内容作为字符串（包括空格）。
-   `nextInt()`, `nextDouble()`, etc.: 读取相应类型的输入。
    -   `nextInt(int radix)`: 可以指定读取的进制（如 2、8、10、16）。默认是十进制。
-   `hasNext()` / `hasNextInt()` etc.: 判断是否还有下一个输入项（对应类型）。

> [!TIP] 使用 `hasNext()`
> 可以在读取前使用 `hasNext()` 或其变体来判断是否有输入，避免程序因无输入而出错。

## Part 2: Number 类与包装类
![[Pasted image 20241029172046.png]]
-   **包装类 (Wrapper Classes)**：Java 为每种基本数据类型（`byte`, `short`, `int`, `long`, `float`, `double`, `char`, `boolean`）提供了对应的类（`Byte`, `Short`, `Integer`, `Long`, `Float`, `Double`, `Character`, `Boolean`），数据类型都放在这些类里面，Byte,Short...类都是包装类。这些类都继承自抽象类 `Number` (除了 `Character` 和 `Boolean`)。

-   **装箱 (Boxing)**：编译器把内置类型装箱为包装类（一个Number箱子，往里面添加Byte，Short...等等），也就是编译器自动将基本数据类型转换为对应的包装类对象
- **拆箱 (Unboxing)**：也可以把一个对象拆箱为内置类型，也就是编译器自动将包装类对象转换为对应的基本数据类型。

```java
public class Test{
	public static void main(String[] args){
	//int x = 5,结果是一样的
		Integer x = 5;// 自动装箱：int 5 被包装成 Integer 对象
		x =  x + 10;// 自动拆箱：x 被拆箱成 int，+10 后，结果再次自动装箱赋给 x

		int primitive_x = 5;
		Integer x = primitive_x; // 装箱
		int temp = x.intValue(); // 显式拆箱
		temp = temp + 10;
		x = Integer.valueOf(temp); // 显式装箱

		System.out.println(x); 
   }
}
```

> [!INFO] 基本类型 vs 包装类
> -   `int` 是基本数据类型，不能调用方法。
> -   `Integer` 是一个 `final` 类，是对象，可以调用方法。

### xxxValue()
-   **描述**: 将 `Number` 对象转换为对应的基本数据类型的值并返回。
-   **方法**: `byteValue()`, `shortValue()`, `intValue()`, `longValue()`, `floatValue()`, `doubleValue()`
-   **返回类型**: 对应的基本数据类型 (`byte`, `short`, `int`, `long`, `float`, `double`)

```java
public class Test{ 
 
   public static void main(String args[]){
      Integer x = 5;
      // 返回 byte 原生数据类型
      System.out.println( x.byteValue() );
 
      // 返回 double 原生数据类型
      System.out.println(x.doubleValue());
 
      // 返回 long 原生数据类型
      System.out.println( x.longValue() );      
   }
}
-结果
5
5.0
5
```

### equals(Object o)
-   **描述**: 判断当前的 `Number` 对象与参数对象 `o` 是否相等。（数值，参数类型等）
-   **返回类型**: `boolean`，public ，o是任何对象，
-   **注意**: 不仅比较数值，还会比较对象的类型。如果类型不同，即使数值相同也返回 `false`。（同时Number对象（o）不为Null）
```java
public class Test{
	public static void main(String args[]){
		Integer x = 5;
		Integer y = 10;
		Integer z =5;
		Short a = 5;

		System.out.println(x.equals(y));  
		System.out.println(x.equals(z)); 
		System.out.println(x.equals(a));
	}
}
-结果
false
true
false
```

### compareTo(NumberSubClass referenceName)
-   **描述**: 比较当前 `Number` 对象与referenceName的数值大小。
-   **返回类型**: `int`public
-   **返回值**:
    -   `1`: 当前对象 > 参数对象
    -   `0`: 当前对象 == 参数对象
    -   `-1`: 当前对象 < 参数对象

> [!WARNING] 类型限制
> `compareTo` 方法通常用于比较相同数据类型的包装类对象。

```java
public class Test {
    public static void main(String args[]) {
        Integer x = 5;
        System.out.println(x.compareTo(3)); // 5 > 3
        System.out.println(x.compareTo(5)); // 5 == 5
        System.out.println(x.compareTo(8)); // 5 < 8
    }
}
// 结果:
// 1
// 0
// -1
```

### valueOf(...)
-   **描述**: 静态方法，将基本数据类型或字符串转换为对应的包装类对象。
-   **返回类型**: 对应的包装类（`Integer`, `Double`, `Float`, etc.）
-   **常用形式**:
    -   `valueOf(int i)` / `valueOf(double d)` etc.: 将基本类型转换为包装类。
    -   `valueOf(String s)`: 将字符串转换为包装类（按十进制解析）。
    -   `valueOf(String s, int radix)`: 将字符串按指定进制 `radix` 解析并转换为包装类。
-   **Static**: Yes


static，i是Integer对象的整数，s是Integer对象的字符串，radix是在解析字符串s时使用的进制数。

-返回括号里的数的小数点前面对象的值，
```java
public class Test{ 
	public static void main(String args[]){
        Integer x =Integer.valueOf(9);
        Double c = Double.valueOf(5);
        Float a = Float.valueOf("80");               

        Integer b = Integer.valueOf("444",16);   // 使用 16 进制

        System.out.println(x); 
        System.out.println(c);
        System.out.println(a);
        System.out.println(b);
    }
}
-结果
9
5.0
80.0
1092
```

### toString()
-   **描述**: 将数值转换为字符串。
-   **形式**:
    -   `toString()`: 给实例用的，返回当前包装类对象的字符串表示。无static
    -   `toString(int i)` / `toString(double d)` etc.: 静态方法，将指定的基本类型数值转换为字符串。有static，将整数放到括号里用，前面要加Integer
---
```java
public class Test{
    public static void main(String args[]){
        Integer x = 5;
		System.out.println(x.toString());  // 实例方法
		System.out.println(Integer.toString(12)); // 静态方法
    }
}
-结果
5
12
```

### parseInt(...)/parseDouble(...)
-   **描述**: 静态方法，将字符串解析为对应的基本数据类型。
-   **返回类型**: 对应的基本数据类型 (`int`, `double`, etc.)
-   **常用形式**:
    -   `parseInt(String s)`: 将字符串按十进制解析为 `int`。
    -   `parseInt(String s, int radix)`: 将字符串按指定进制 `radix` 解析为 `int`。
    -   `parseDouble(String s)`: 将字符串解析为 `double`。
---
```java
public class Test{
    public static void main(String args[]){
        int x =Integer.parseInt("9");
        double c = Double.parseDouble("5");
        int b = Integer.parseInt("444",16);

        System.out.println(x);
        System.out.println(c);
        System.out.println(b);
    }
}
-结果
9
5.0
1092
```
## Part 3: Math 类
> [!TIP] 静态方法
> `Math` 类中的方法几乎都是静态的 (`static`)，可以直接通过 `Math.方法名()` 调用，无需创建 `Math` 类的实例。（前提是对应方法也要是static）
### random()
-   **描述**: 返回一个 `double` 类型的伪随机数，范围是 `[0.0, 1.0)` (包含 0.0，不包含 1.0)。
-   **返回类型**: `double`
-   **Static**: Yes
-   **参数**: 无
```java
public class Test{
    public static void main(String args[]){
        System.out.println( Math.random() );
        System.out.println( Math.random() );
    }
}
-结果
0.5444085967267008
0.7960235983184115
```

### 计算相关
-   `abs(x)`: 返回 `x` 的绝对值。
-   `min(a, b)`, `max(a, b)`: 返回两个数中的较小/较大值。
-   `exp(x)`: 返回 $e^x$ 的值。
-   `log(x)`: 返回 `x` 的自然对数（以 $e$ 为底）。
-   `log10(x)`: 返回 `x` 的以 10 为底的对数。
-   `pow(x, y)`: 返回 $x^y$ 的值。
-   `sqrt(x)`: 返回 `x` 的正平方根。
-   `sin(a)`, `cos(a)`, `tan(a)`: 三角函数（参数 `a` 为弧度）。
-   `asin(x)`, `acos(x)`, `atan(x)`: 反三角函数。
-   `atan2(y, x)`: 将笛卡尔坐标 `(x, y)` 转换为极坐标 `(r, theta)`，并返回角度 `theta`（弧度）。
-   `toDegrees(angrad)`: 将弧度转换为角度。
-   `toRadians(angdeg)`: 将角度转换为弧度。
### 取整
-   `floor(x)`: 向下取整，返回小于或等于 `x` 的最大整数（`double` 类型）。例：`floor(1.9) = 1.0`
-   `ceil(x)`: 向上取整，返回大于或等于 `x` 的最小整数（`double` 类型）。例：`ceil(1.1) = 2.0`
-   `round(x)`: 四舍五入。返回 `long` (如果参数是 `double`) 或 `int` (如果参数是 `float`)。例：`round(1.1) = 1`, `round(1.5) = 2`
-   `rint(x)`: 返回最接近 `x` 的整数值（`double` 类型）。如果 `x` 到两个整数的距离相等，则返回偶数。例：`rint(1.5) = 2.0`, `rint(2.5) = 2.0`

## Part 4: Random 类
用于生成伪随机数。
### 构造方法（constructors）
-   `Random()`: 创建一个新的随机数生成器，使用当前时间相关的种子。（时间戳）
-   `Random(long seed)`: 创建一个新的随机数生成器，使用指定的 `seed` 作为种子。

> [!INFO] 种子 (Seed)
> 种子决定了随机数序列。如果使用相同的种子创建 `Random` 对象，它们将生成相同的随机数序列。不指定种子时，通常使用当前时间的某个值（如纳秒）作为种子，以产生不同的序列。

> [!INFO] 时间戳
> 时间戳（Timestamp）通常是一个长整型数字，表示自某个特定时间点（如 1970 年 1 月 1 日 UTC）以来经过的毫秒数或纳秒数。
> ![[Pasted image 20241029205139.png|300]]
- 字符串型时间戳
![[Pasted image 20241029205139.png|300]]

种子就是数字型的时间戳
- 随机数生成算法（种子？）·
-2038年问题：某些软件可能无法正常工作（UNIX时间）

> [!NOTE] `Math.random()` vs `Random`
> `Math.random()` 内部实际上也是使用 `Random` 类，但它只能生成 `[0.0, 1.0)` 范围的 `double` 值。如果需要生成其他类型（如 `int`）或指定范围、种子的随机数，应使用 `Random` 类。
> 
![[Pasted image 20241029190023.png]]
可以看出属于Random类
![[Pasted image 20241029190215.png]]

### `nextInt()` / `nextInt(int bound)`
-   `nextInt()`: 返回一个随机的 `int` 值（可能为正、负或零）。
-   `nextInt(int bound)`: 返回一个 `[0, bound)` 范围内的随机 `int` 值。`bound` 必须为正数。

```java
import java.util.Random;

public class Test {
    public static void main(String args[]) {
        Random random = new Random();

        int i1 = random.nextInt(); // 生成任意 int
        System.out.println("Random int: " + i1);

        int i2 = random.nextInt(10); // 生成 [0, 10) 范围内的 int
        System.out.println("Random int [0, 10): " + i2);
    }
}
```

### `nextDouble()` / `nextFloat()`
-   `nextDouble()`: 返回一个 `[0.0, 1.0)` 范围内的随机 `double` 值。
-   `nextFloat()`: 返回一个 `[0.0, 1.0)` 范围内的随机 `float` 值。

```java
import java.util.Random;

public class Test {
    public static void main(String args[]) {
        Random random = new Random();
        double d = random.nextDouble(); // 生成 [0.0, 1.0) 范围内的 double
        System.out.println("Random double [0.0, 1.0): " + d);
    }
}
```

> [!NOTE] `nextDouble()` 范围限制
> `Random` 类的 `nextDouble()` 没有直接提供设置范围的重载方法。如果需要特定范围的 `double`，可以使用 `ThreadLocalRandom` 或通过数学计算实现（例如：`min + random.nextDouble() * (max - min)`）。

### `ThreadLocalRandom` (推荐用于多线程环境或需要范围)
`java.util.concurrent.ThreadLocalRandom` 是 `Random` 的子类，在多线程环境下性能更好，并且提供了方便的方法来生成指定范围的随机数。

-   **获取实例**: 使用静态方法 `ThreadLocalRandom.current()` 获取当前线程的 `ThreadLocalRandom` 实例。静态方法（返回当前线程的ThreadLocalRandom类），所以不能直接只用下面的函数，current表示当前线程
    ![[Pasted image 20241029211042.png]]
-   **常用方法**:
    -   `nextInt(int origin, int bound)`: 返回 `[origin, bound)` 范围的随机 `int`。
    -   `nextDouble(double origin, double bound)`: 返回 `[origin, bound)` 范围的随机 `double`。
    -   `nextDouble(double bound)`: 返回 `[0.0, bound)` 范围的随机 `double`。
---

```java
import java.util.concurrent.ThreadLocalRandom;

public class Test {
    public static void main(String args[]) {
        // 生成 [1.9, 3.4) 范围内的 double
        double d = ThreadLocalRandom.current().nextDouble(1.9, 3.4);
        System.out.println("Random double [1.9, 3.4): " + d);

        // 生成 [10, 20) 范围内的 int
        int i = ThreadLocalRandom.current().nextInt(10, 20);
        System.out.println("Random int [10, 20): " + i);
    }
}
```

### javadoc查看方式：
![[屏幕截图 2024-10-29 190953.png]]

例如，`SecureRandom` 是 `Random` 的子类，提供了更强的随机性。secureRandom就有三层
![[Pasted image 20241029202903.png]]

## Part 5: 时间日期相关类 
- 使用java.time
- LocalDataTime
	- 纳米级，value-based class
		- instance（实例）是值
	- 需要注意identity-sensitive operations
		- 例如，相等不推荐使用 == （是否指向内存中的同一个地址），应使用equals
			- 因为是value-based，所以JVM可能会进行内部优化。从而对对象进行缓存或在内存中移动对象
		- 身份哈希码（基于内存地址...），同步锁

- 

## Part 7: `java.lang.System` 类
`System` 类包含一些有用的类字段和方法。它不能被实例化，所有成员都是静态的。
### 标准流 (字段)
-   `static InputStream in`: 标准输入流。通常对应于键盘输入或由主机环境或用户指定的另一个输入源。
-   `static PrintStream out`: 标准输出流。通常对应于显示器输出或由主机环境或用户指定的另一个输出目标。
-   `static PrintStream err`: 标准错误输出流。通常对应于显示器输出，用于显示错误消息或用户通常期望立即看到的其他信息。
### 常用方法
-   **`static void arraycopy(Object src, int srcPos, Object dest, int destPos, int length)`**:
    -   **描述**: 从源数组 `src` 的指定起始位置 `srcPos` 开始，复制 `length` 个元素到目标数组 `dest` 的指定起始位置 `destPos`。
    -   **性能**: 通常比手动循环复制数组元素更快，因为它通常由 JVM 底层实现优化。
    -   **链接**: [Javadoc](https://docs.oracle.com/javase/9/docs/api/java/lang/System.html#arraycopy-java.lang.Object-int-java.lang.Object-int-int-)
    - （src表示元素组，srcPos表示元素组的起始位置，dest是目标数组，destPos表示目标数组的位置，length表示数组的长度）

- [arraycopy](https://docs.oracle.com/javase/9/docs/api/java/lang/System.html#arraycopy-java.lang.Object-int-java.lang.Object-int-int-)​([Object](https://docs.oracle.com/javase/9/docs/api/java/lang/Object.html "class in java.lang") src, int srcPos, [Object](https://docs.oracle.com/javase/9/docs/api/java/lang/Object.html "class in java.lang") dest, int destPos, int length)：从指定位置开始将数组复制到目标数组，这个是系统的方法，与Array里的不太一样，性能会更高一点。（src表示元素组，srcPos表示元素组的起始位置，dest是目标数组，destPos表示目标数组的位置，length表示数组的长度）

-   **`static long currentTimeMillis()`**：获取当前时间戳
-   **`static Console console()`**:
    -   **描述**: 返回与当前 Java 虚拟机关联的唯一 `Console` 对象（如果可用）。可用于从控制台读取密码等。
-   **`static void gc()`**:
    -   **描述**: 运行垃圾回收器。这是一个建议（hint），JVM 不保证立即执行垃圾回收。
    -   **注意**: 通常不建议显式调用 `gc()`，让 JVM 自行管理内存通常更高效。
-   **`static long nanoTime()`**:
    -   **描述**: 返回 Java 虚拟机的高精度时间源的当前值（以纳秒为单位）。
    -   **用途**: 主要用于精确测量代码执行时间，不适合表示日期或时间。其起点是任意的，可能在 JVM 重启后改变。

## Part 8: `java.lang.String` 类
### 不可变性 (Immutability)
> [!IMPORTANT] String 是不可变的
> 一旦 `String` 对象被创建，它的值（字符序列）就不能被改变。所有看似修改 `String` 的操作（如 `concat()`, `substring()`, `replace()` 等）实际上都会创建一个新的 `String` 对象，而原始对象保持不变。

String类型一旦创建就不能更改了
下面是垃圾回收机制的一种：下面总共创建了3个对象（s1没有被回收，三个同时存在，详见垃圾回收）
- s1指向了s1+s2的地址，原来的s1如果后序不被引用，最终会被垃圾回收
![[Pasted image 20241113203707.png]]

### 常用操作
`String` 类提供了大量用于操作字符串的方法，例如：
-   获取长度: `length()`
-   比较: `equals()`, `equalsIgnoreCase()`, `compareTo()`
-   查找: `contains()`, `indexOf()`, `lastIndexOf()`, `startsWith()`, `endsWith()`
-   截取: `substring()`
-   替换: `replace()`, `replaceAll()`, `replaceFirst()`
-   大小写转换: `toLowerCase()`, `toUpperCase()`
-   去除空白: `trim()`
-   **分割**: `split(String regex)` - 根据给定的正则表达式分割字符串，返回字符串数组 `String[]`。
-   格式化: `static String format(...)`

## Part 9: `StringBuffer` 和 `StringBuilder`
- 由于 `String` 的不可变性，当需要频繁地修改字符串内容（如拼接、插入、删除）时，使用 `String` 会产生大量中间对象，导致性能下降和内存消耗增加。

为了解决这个问题，Java 提供了两个可变的字符序列类：`StringBuffer` 和 `StringBuilder`。

-   **可变性**: 它们的对象内容可以直接修改，而不会创建新的对象。
-   **效率**: 对于大量修改操作，比 `String` 的 `+` 或 `concat()` 效率高得多。

### 链式调用 (Fluent Interface)
```java
public class Test {
    public void demo() {
        StringBuilder stringBuilder = new StringBuilder();
        // 链式调用 append 方法
        stringBuilder.append("Hello")
                     .append(" World")
                     .append("!");
        System.out.println(stringBuilder.toString()); // 输出: Hello World!
    }
}
```

### `StringBuffer` vs `StringBuilder`

| 特性         | `StringBuffer`                     | `StringBuilder`                     |
| :----------- | :--------------------------------- | :---------------------------------- |
| **线程安全** | **是** (方法是 `synchronized` 的) | **否** (方法不是同步的)           |
| **性能**     | 相对较低 (因为同步开销)            | 相对较高 (没有同步开销)           |
| **使用场景** | 多线程环境下共享的可变字符串       | 单线程环境下的可变字符串操作 (推荐) |

> [!RECOMMENDATION] 选择建议
> -   在单线程环境中，优先使用 `StringBuilder`，因为它性能更好。
> -   在多线程环境中，如果多个线程需要共享并修改同一个可变字符串，必须使用 `StringBuffer` 来保证线程安全。


