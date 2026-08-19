## Part 1 什么是测试
*   **本地测试方法的局限性**：不推荐在 `main` 函数中直接进行测试。
*   **开发流程**：程序员每次修改代码后，至少应进行一次单元测试。
*   **独立性**：理想的测试用例应该是独立的，即一个方法对应一个测试案例，互不干扰。
*   **`main` 方法的职责**：`main` 方法应保持简洁，避免包含过多的业务逻辑（如 `if-else`）或功能性语句（如 `System.out.println`），这些功能应抽离到单独的方法中。

## Part 2 Junit介绍
*   **JUnit** 是 Java 语言中最常用的单元测试框架，主要供**程序员**使用，而非测试人员。
*   **单元测试（或模块测试）**：针对程序模块（软件设计的最小单位）来进行正确性检验的测试工作。程序单元是应用的最小可测试部件。
	* 在过程化编程中，一个单元就是单个程序、函数、过程等；
	* 对于面向对象编程，最小单元就是方法，包括基类（超类），抽象类、或者派生类（子类中的方法）
## Part 3 JUnit 手动导入 JAR 包
java自带的API里面没有相应的功能，就需要引入jar包，jar包也可以用构建工具（maven）导入更加方便，这里用的是手动导入的方式
### 官网下载对应的jar包
- maven repository
![Pasted image 20241113200310](images/Pasted%20image%2020241113200310.png)

![Pasted image 20241113200351](images/Pasted%20image%2020241113200351.png)

![Pasted image 20241113200427](images/Pasted%20image%2020241113200427.png)

### 增加依赖，不然用不了
发现会报错，这是缺少依赖
![Pasted image 20241106183038](images/Pasted%20image%2020241106183038.png)

所以需要在下载junit的jar页面往下翻找到compile dependency，点击version下载，再次导入jar包
![Pasted image 20241113200535](images/Pasted%20image%2020241113200535.png)

### 右击项目创建lib的directory
![Pasted image 20241106173209](images/Pasted%20image%2020241106173209.png)

导入成功后右击jar包add as library，点击ok，能展开就是可以用了

## Part 4 使用
1. 创建测试类
通常为需要测试的类创建一个对应的测试类，例如 `Main` 类对应 `MainTest` 类。

```java
package com.company.demo;

import org.junit.Test;
import org.junit.Assert; // 引入断言类
import java.util.concurrent.ThreadLocalRandom;

public class MainTest {

    // 使用 @Test 注解标记测试方法
    @Test
    public void testSum() {
        // 准备测试数据
        int numberA = 1;
        int numberB = 2;
        // 调用被测试的方法
        int actualSum = Main.sum(numberA, numberB);
        // 预期结果
        int expectedSum = 3;
        // 使用断言验证结果
        System.out.println("计算结果: " + actualSum); // 可以在测试中打印信息帮助调试
        Assert.assertEquals(expectedSum, actualSum); // 断言预期值与实际值相等
    }

    // 另一个测试方法，使用随机数进行更广泛的测试
    @Test
    public void testSumWithRandomNumbers() {
        int numberA = ThreadLocalRandom.current().nextInt(1000); // 生成随机数
        int numberB = ThreadLocalRandom.current().nextInt(1000);
        int actualSum = Main.sum(numberA, numberB);
        int expectedSum = numberA + numberB; // 计算机自动计算预期结果
        Assert.assertEquals(expectedSum, actualSum);
    }

    // 每个需要独立运行的测试方法前都需要加 @Test 注解
    // 测试用例应该是独立的
}
```

2. 使用断言
*   断言用于验证测试结果是否符合预期。
*   `org.junit.Assert` 类提供了多种断言方法，如：
    *   `assertEquals(expected, actual)`: 验证预期值和实际值是否相等。
    *   `assertTrue(condition)`: 验证条件是否为真。
    *   `assertFalse(condition)`: 验证条件是否为假。
    *   `assertNotNull(object)`: 验证对象是否不为 null。
![Pasted image 20241106183808](images/Pasted%20image%2020241106183808.png)

下面是√就表示通过

![Pasted image 20241106183949](images/Pasted%20image%2020241106183949.png)

- 但是有的数值不能通过人工计算，应该让计算机自己去计算
![Pasted image 20241106184605](images/Pasted%20image%2020241106184605.png)

## Part 5 断言
### 介绍与使用
Java 的 `assert` 关键字与 JUnit 的 `Assert` 类是不同的概念。`assert` 是 Java 语言内置的调试工具，而 `Assert` 是 JUnit 框架提供的测试工具类。
*   语法：
    *   `assert condition;`
    *   `assert condition : message;` (如果条件为 `false`，抛出带消息的 `AssertionError`)
我们先看一个例子：

```java
public static void main(String[] args) {
    double x = Math.abs(-123.45);
    assert x >= 0;
    System.out.println(x);
}
```

语句`assert x >= 0;`即为断言，断言条件`x >= 0`预期为`true`。如果计算结果为`false`，则断言失败，抛出`AssertionError`。
```java
assert x >= 0 : "x must be non-negative";
```
这样，断言失败的时候，`AssertionError`会带上消息`x must be non-negative`，更加便于调试。

*   **特点**：
    *   断言失败时抛出 `AssertionError`，导致程序终止。
    *   **默认关闭**：JVM 默认忽略 `assert` 语句。需要给jvm传递通过 `-enableassertions` 或 `-ea` 命令行参数启用。
    *   **适用场景**：仅用于**开发和测试阶段**，断言会直接导致程序结束，所以不应用于可恢复的程序错误（应使用异常处理）。
*   **局限性**：实际开发中较少使用，单元测试（如 JUnit）是更常用、更强大的方法。

- 对于可恢复的程序错误，不应该使用断言，因为断言失败程序就结束了。例如：
```java
void sort(int[] arr) {
    assert arr != null;
}
```
应该抛出异常并在上层捕获：
```java
void sort(int[] arr) {
    if (arr == null) {
        throw new IllegalArgumentException("array cannot be null");
    }
}
```
### 启用
```plain
$ java -ea Main.java
Exception in thread "main" java.lang.AssertionError
	at Main.main(Main.java:5)
```

- 可以有选择地对特定地类启用断言，命令行参数是：`-ea:com.itranswarp.sample.Main`，表示只对`com.itranswarp.sample.Main`这个类启用断言。

- 对特定地包启用断言，命令行参数是：`-ea:com.itranswarp.sample...`（注意结尾有3个`.`），表示对`com.itranswarp.sample`这个包启动断言。
## Part 6 Logging
### 1. JDK Logging
日志（Logging）是记录应用程序运行时信息的关键机制，用于替代简单的 `System.out.println()`。

输出日志，而不是用`System.out.println()`，有以下几个好处：
1. 可以设置输出样式，避免自己每次都写`"ERROR: " + var`；
2. 可以设置输出级别，禁止某些级别输出。例如，只输出错误日志；
3. 可以被重定向到文件，这样可以在程序运行结束后查看日志；
4. 可以按包名控制日志级别，只输出某些包打的日志；
5. 可以……

- 使用日志
Java标准库内置了日志包`java.util.logging`，我们可以直接用。先看一个简单的例子：

```java
// logging
import java.util.logging.Level;
import java.util.logging.Logger;

public class Hello {
    public static void main(String[] args) {
        Logger logger = Logger.getGlobal();
        logger.info("start process...");
        logger.warning("memory is running out...");
        logger.fine("ignored.");// 默认级别 INFO，低于 INFO 的不输出
        logger.severe("process will be terminated...");
    }
}
```
运行上述代码，得到类似如下的输出：
```plain
Mar 02, 2019 6:32:13 PM Hello main
INFO: start process...
Mar 02, 2019 6:32:13 PM Hello main
WARNING: memory is running out...
Mar 02, 2019 6:32:13 PM Hello main
SEVERE: process will be terminated...
```
发现，4条日志，只打印了3条，`logger.fine()`没有打印。这是因为，日志的输出可以设定级别。JDK的Logging定义了7个日志级别，从严重到普通：
*   **日志级别** (从高到低):
    *   `SEVERE` (严重)
    *   `WARNING` (警告)
    *   `INFO` (信息 - 默认级别)
    *   `CONFIG` (配置)
    *   `FINE` (详细)
    *   `FINER` (更详细)
    *   `FINEST` (最详细)

因为默认级别是INFO，因此，INFO级别以下的日志，不会被打印出来。使用日志级别的好处在于，调整级别，就可以屏蔽掉很多调试相关的日志输出。

*   **局限性**：
    *   配置不灵活，通常在 JVM 启动时通过配置文件 (`logging.properties`) 或启动参数 (`-Djava.util.logging.config.file=<config-file-name>`) 指定，运行时无法修改。
    *   使用相对不广泛。

### 2. Commons Logging
- 第三方日志库：可以挂接不同的日志系统，并通过配置文件指定挂接的日志系统。默认情况下自动搜索使用Log4j（Log4j是另一个流行的日志系统），如果没有找到Log4j，再使用JDK Logging

*   **使用步骤**：
    1.  添加 `commons-logging.jar` 到 classpath。
    2.  通过 `LogFactory.getLog()` 获取 `Log` 实例。
    3.  调用 `log` 实例的方法记录日志。
---
*   **编译和运行**：需要将 `commons-logging.jar` 加入编译和运行时的 classpath。
    *   编译: `javac -cp commons-logging-1.2.jar Main.java`
    *   运行 (Windows): `java -cp .;commons-logging-1.2.jar Main`
    *   运行 (Linux/macOS): `java -cp .:commons-logging-1.2.jar Main`
- 如果编译成功，那么当前目录下就会多出一个`Main.class`文件：
>[!WARNING] 注意
>传入的`classpath`有两部分：一个是`.`，一个是`commons-logging-1.2.jar`，用`;`分割。`.`表示当前目录，如果没有这个`.`，JVM不会在当前目录搜索`Main.class`，就会报错。

*   **日志级别** (从高到低):
    *   `FATAL`
    *   `ERROR`
    *   `WARNING`
    *   `INFO` (默认级别)
    *   `DEBUG`
    *   `TRACE`

默认级别是`INFO`。

```java
    import org.apache.commons.logging.Log;
    import org.apache.commons.logging.LogFactory;

    public class Main {
        // 获取 Log 实例，通常传入当前类，如果在静态方法中引用Log，通常直接定义一个静态类型变量
        private static final Log log = LogFactory.getLog(Main.class);

        public static void main(String[] args) {
            log.info("start...");
            log.warn("end.");
            try {
                // ... 可能抛出异常的代码 ...
                throw new RuntimeException("Something went wrong");
            } catch (Exception e) {
                // 记录异常信息，推荐使用带 Throwable 参数的方法，还有info(String)
                log.error("An error occurred!", e);
            }
        }
    }
```
```plain
Mar 02, 2019 7:15:31 PM Main main
INFO: start...
Mar 02, 2019 7:15:31 PM Main main
WARNING: end.
```

- 在实例方法中引用`Log`，通常定义一个实例变量：
```java
// 在实例方法中引用Log:
public class Person {
    protected final Log log = LogFactory.getLog(getClass());

    void foo() {
        log.info("foo");
    }
}
```

实例变量log的获取方式有两种方式：
1. `LogFactory.getLog(getClass())`，子类可以直接使用该`log`实例。(推荐，子类可直接复用，且日志记录器名称为子类名)
2. `LogFactory.getLog(Person.class)`
```java
// 在子类中使用父类实例化的log:
public class Student extends Person {
    void bar() {
        log.info("bar");
    }
}
```
由于Java类的动态特性，子类获取的`log`字段实际上相当于`LogFactory.getLog(Student.class)`，但却是从父类继承而来，并且无需改动代码。

### 3. Log4j
前面的Commons Logging，可以作为“日志接口”来使用。而真正的“日志实现”可以使用Log4j (最新版本是 Log4j 2)。

当我们使用Log4j输出一条日志时，Log4j自动通过不同的Appender把同一条日志输出到不同的目的地。Log4j是一个组件化设计的日志系统，它的架构大致如下：
*   **核心组件**:
    *   **Logger**: 日志记录器，应用程序通过它记录日志。
    *   **Appender**: 定义日志输出目的地（控制台、文件、数据库等）。
    *   **Filter**: 控制哪些日志事件应该被处理。（过滤哪些log需要被输出，哪些log不需要被输出。例如，仅输出`ERROR`级别的日志）
    *   **Layout**: 控制日志输出格式。（格式化日志信息，例如，自动添加日期、时间、方法名称等信息。）
    *   console：输出到屏幕；
	-   file：输出到文件；
	-   socket：通过网络输出到远程计算机；
	-    jdbc：输出到数据库
```
log.info("User signed in.");
 │
 │   ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
 ├──▶│ Appender │───▶│  Filter  │───▶│  Layout  │───▶│ Console  │
 │   └──────────┘    └──────────┘    └──────────┘    └──────────┘
 │
 │   ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
 ├──▶│ Appender │───▶│  Filter  │───▶│  Layout  │───▶│   File   │
 │   └──────────┘    └──────────┘    └──────────┘    └──────────┘
 │
 │   ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
 └──▶│ Appender │───▶│  Filter  │───▶│  Layout  │───▶│  Socket  │
     └──────────┘    └──────────┘    └──────────┘    └──────────┘
```
我们在实际使用的时候，不需要关心Log4j的API，而是通过配置文件来配置它。
*   **配置**: Log4j 主要通过配置文件进行配置 (如 `log4j2.xml`, `log4j2.properties`)。配置文件需要放在 classpath 下。
    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <Configuration status="WARN"> <!-- status: Log4j内部日志级别 -->
        <Properties>
            <Property name="LOG_PATTERN">%d{yyyy-MM-dd HH:mm:ss.SSS} [%t] %-5level %logger{36} - %msg%n</Property>
            <!-- 
            [%t]:表示线程名称，追踪日志是哪一个线程记录的
            %-5level:日志级别 %5表示日志级别左对齐，占用5个字符宽度，
            %logger{36}：日志记录器名称，最多显示36个字符，例如com.example.MyClass
            - 分隔日志信息的标记字符
            %msg 表示日志的实际消息内容
            %n 换行符
            -->
            <Property name="FILE_PATH">logs</Property> <!-- 日志文件目录 -->
        </Properties>
        <Appenders>
            <!-- 将日志输出到控制台 -->
            <Console name="Console" target="SYSTEM_OUT">
                <PatternLayout pattern="${LOG_PATTERN}" />
            </Console>
            <!-- RollingFile Appender: 将日志输出到文件，并在达到特定条件是创建归档文件（滚动日志） -->
            <RollingFile name="File" fileName="${FILE_PATH}/app.log"
                         filePattern="${FILE_PATH}/app-%d{yyyy-MM-dd}-%i.log.gz">
            <!-- 
            name="File"：给该 Appender 起名为 File，方便引用。
	        fileName="${FILE_PATH}/app.log"：当前日志文件的路径和文件名，FILE_PATH 是一个占位符变量（可以定义为目录路径，如 /var/logs）。
	        filePattern="${FILE_PATH}/app-%d{yyyy-MM-dd}-%i.log.gz"：定义滚动日志的文件名格式。
		        %i：按索引编号归档，例如 app-2025-04-18-1。
			    .gz：日志文件会被压缩为 Gzip 格式，节省存储空间。
            -->
                <PatternLayout pattern="${LOG_PATTERN}" />
                <!-- PatternLayout：指定日志格式。 -->
                <Policies>
				<!-- 定义日志滚动的触发策略 -->
					<TimeBasedTriggeringPolicy /> 
                    <!-- 按时间滚动，例如每天创建一个新文件 -->
                    <SizeBasedTriggeringPolicy size="10 MB"/> 
                    <!-- 按大小滚动，当文件达到 10MB 时创建新文件。 -->
                </Policies>
                <DefaultRolloverStrategy max="10"/> 
                <!-- 最多保留10个归档文件，超过后会删除最旧的文件。 -->
            </RollingFile>
        </Appenders>
        <Loggers>
        <!-- Root Logger: 全局默认日志配置，适用于所有未单独指定Logger的日志记录请求 -->
            <Root level="info"> 
            <!-- 设置根Logger级别为 info -->
                <AppenderRef ref="Console"/> 
                <!-- 引用名为 `Console` 的 Appender，将日志输出到控制台。 -->
                <AppenderRef ref="File"/>    
                <!-- 引用名为 `File` 的 Appender，将日志写入文件 -->
            </Root>
            <!-- 也可以为特定包配置不同的级别 -->
            <!-- <Logger name="com.yourcompany.specific.package" level="debug" additivity="false">
                <AppenderRef ref="Console"/>
            </Logger> -->
        </Loggers>
    </Configuration>
    ```

- 对上面的配置文件，凡是`INFO`级别的日志，会自动输出到屏幕，而`ERROR`级别的日志，不但会输出到屏幕，还会同时输出到文件。并且，一旦日志文件达到指定大小（10MB），Log4j就会自动切割新的日志文件，并最多保留10份。

*   **与 Commons Logging 结合**:
    1.  在项目中添加 Commons Logging API (`commons-logging.jar`)。
    2.  添加 Log4j 2 的实现 JAR 包 (`log4j-api.jar`, `log4j-core.jar`)。
    3.  添加 Log4j 2 对 Commons Logging 的桥接包 (`log4j-jcl.jar`)。
    4.  将 `log4j2.xml` 配置文件放在 classpath 下。
    5.  应用程序代码**无需修改**，只需要按Commons Logging的写法写，不需要改动任何代码，就可以得到Log4j的日志输出，Commons Logging 会自动检测并使用 Log4j 2 作为底层实现。如下：
```plain
03-03 12:09:45.880 [main] INFO  com.itranswarp.learnjava.Main
Start process...
```

- 如果需要把日志写入文件，只需要把正确的配置文件和Log4j相关的jar包放入`classpath`，就可以自动把日志切换成使用Log4j写入，无需修改任何代码。
- 只有扩展Log4j时，才需要引用Log4j的接口（例如，将日志加密写入数据库的功能，需要自己开发）。

## Part 7 使用SLF4J和Logback
Commons Logging和Log4j一个负责充当日志API，一个负责实现日志底层，搭配使用非常便于开发。

SLF4J类似于Commons Logging，也是一个日志接口，而Logback类似于Log4j，是一个日志的实现。

*   **背景**:
    *   Java 开源生态丰富，同一功能常有多种选择。
    *   **SLF4J (Simple Logging Facade for Java)**: 因对 Commons Logging 接口设计不满意而创建，提供了更简洁、高效的 API。它是一个**日志门面**。
    *   **Logback**: 由 Log4j 原作者创建，旨在改进 Log4j 的性能和功能。它是一个**日志实现**，通常被认为是 Log4j 的继任者。

*   **SLF4J 接口改进**:
    *   **Commons Logging 痛点**: 需要手动拼接字符串。
	```java
	int score = 99;
	p.setScore(score);
	log.info("Set score " + score + " for Person " + p.getName() + " ok.");
	```
    *   **SLF4J 优点**: 使用**占位符 `{}`**，代码更简洁、易读，且性能更好（仅在日志级别启用时才进行字符串格式化）。
	```java
	int score = 99;
	p.setScore(score);
	logger.info("Set score {} for Person {} ok.", score, p.getName());
	```
SLF4J的日志接口传入的是一个带占位符的字符串，用后面的变量自动替换占位符，所以看起来更加自然。
*   **如何使用 SLF4J**:
    *   API 与 Commons Logging 非常相似。
    *   获取 Logger 实例：
	```java
	import org.slf4j.Logger;
	import org.slf4j.LoggerFactory;
	
	class Main {
        // 使用 LoggerFactory 获取 Logger 实例
	    final Logger logger = LoggerFactory.getLogger(getClass());
	    public void someMethod() {
            logger.info("Using SLF4J logger.");
        }
	}
	```

对比一下Commons Logging和SLF4J的接口：

|Commons Logging|SLF4J|
|---|---|
|org.apache.commons.logging.Log|org.slf4j.Logger|
|org.apache.commons.logging.LogFactory|org.slf4j.LoggerFactory|

不同之处就是`Log`变成了`Logger`，`LogFactory`变成了`LoggerFactory`。

*   **使用 SLF4J 和 Logback**:
    1.  **添加依赖**: 将以下 JAR 包添加到项目的 classpath 中（或使用 Maven/Gradle 管理依赖）：
        *   `slf4j-api-x.y.z.jar` (SLF4J 核心 API)
        *   `logback-classic-x.y.z.jar` (Logback 实现，包含 `logback-core`)
        *   `logback-core-x.y.z.jar` (Logback 核心库)
        *   *注意*: `logback-classic` 通常会自动引入 `slf4j-api` 和 `logback-core`。
    2.  **编写代码**: 使用 SLF4J 的 `Logger` 和 `LoggerFactory` 接口编写日志代码。
    3.  **添加配置文件**: 在 classpath 的根目录下创建 Logback 的配置文件，通常命名为 `logback.xml` 或 `logback-test.xml`。
---
```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <!-- Console Appender: 输出到控制台 -->
	<appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
		<encoder>
		<!-- 日志格式 -->
			<pattern>%d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n</pattern>
		</encoder>
	</appender>
	<!-- RollingFile Appender: 输出到滚动文件 -->
	<appender name="FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
		<encoder>
			<pattern>%d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n</pattern>
			<charset>utf-8</charset>
			<!-- 指定字符集 -->
		</encoder>
		<file>log/output.log</file>
		<!-- 日志文件路径 -->
		<rollingPolicy class="ch.qos.logback.core.rolling.FixedWindowRollingPolicy">
		<!-- 滚动策略: 固定窗口大小 -->
			<fileNamePattern>log/output.log.%i</fileNamePattern>
			<!-- 归档文件名模式 -->
		</rollingPolicy>
		<!-- 触发策略: 基于文件大小 -->
		<triggeringPolicy class="ch.qos.logback.core.rolling.SizeBasedTriggeringPolicy">
			<MaxFileSize>1MB</MaxFileSize>
			<!-- 文件达到1MB时触发滚动 -->
		</triggeringPolicy>
	</appender>
	<!-- Root Logger 配置 -->
	<root level="INFO">
	<!-- 设置根 Logger 的级别为 INFO -->
		<appender-ref ref="CONSOLE" />
		<!-- 将 CONSOLE Appender 附加到 Root Logger -->
		<appender-ref ref="FILE" />
		<!-- 将 FILE Appender 附加到 Root Logger -->
	</root>
	 <!-- 可以为特定包设置更详细的日志级别 -->
        <!--
        <logger name="com.yourcompany.specific.package" level="DEBUG" additivity="false">
            <appender-ref ref="CONSOLE"/>
        </logger>
        -->
</configuration>
```
运行即可获得类似如下的输出：
```plain
13:15:25.328 [main] INFO  com.itranswarp.learnjava.Main - Start process...
```
从目前的趋势来看，越来越多的开源项目从Commons Logging加Log4j转向了SLF4J加Logback。