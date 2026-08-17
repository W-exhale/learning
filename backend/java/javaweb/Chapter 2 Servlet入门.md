## Servlet 基础
- 编写HTTP服务器只需要先编写基于多线程的TCP服务，然后在一个TCP连接中读取HTTP请求，发送HTTP响应即可。

但是，编写 HTTP 服务器需要处理许多底层细节，例如：
1. 基于多线程的 TCP 服务、
2. HTTP 请求/响应的解析和处理、
3. 连接复用、
4. 线程复用
5. IO 异常处理等。这些工作复杂且耗时。

为了简化 Web 应用程序的开发，Java EE 提供了 **Servlet API**。我们只需编写实现 Servlet API 的 **Servlet** 类来处理 HTTP 请求，而底层的 TCP 连接、HTTP 协议解析等工作则交给 **Web 服务器**（也称为 **Servlet 容器**）处理。

```text
+-----------------+      HTTP      +---------------------+
|    Browser      | <------------> |     Web Server      |
+-----------------+                | +-----------------+ |
                                   | |   My Servlet    | |
                                   | +-----------------+ |
                                   | |   Servlet API   | |
                                   | +-----------------+ |
                                   +---------------------+
```

## 一个简单的 Servlet
```java
import jakarta.servlet.*;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.*;
import java.io.IOException;
import java.io.PrintWriter;

//@WebServlet 注解表示这是一个 Servlet，并映射到地址 "/"
@WebServlet(urlPattern = "/")
public class HelloServlet extends HttpServlet{
	protected void doGet(HttpServletRequest req, HttpServletResponse resp) throw ServletException, IOException{
		//设置响应类型
		resp.setContentType("text/html")
		//获取输出流：
		PrintWriter pw = resp.getWriter();
		//写入响应：
		pw.write("<h1>Hello, world!</h1>");
		//不要忘记flush强制输出：
		pw.flush();
	}
}
```

-   Servlet 通常继承自 `HttpServlet`。
-   覆写 `doGet()` 或 `doPost()` 方法来处理对应的 HTTP 请求。

可以看到`doGet()`方法传入了`HttpServletRequest`和`HttpServletResponse`两个对象
-   `HttpServletRequest` 对象封装了 HTTP 请求信息。
-   `HttpServletResponse` 对象用于生成 HTTP 响应。

我们使用Servlet API时，并不直接与底层TCP交互，也不需要解析HTTP协议，因为`HttpServletRequest`和`HttpServletResponse`已经封装好了请求和响应。

-   以发送响应为例，我们通过 `HttpServletResponse` 设置响应类型（`setContentType`）并获取 `PrintWriter` 来写入响应内容。

## Maven 配置
Servlet API是一个jar包，我们需要通过Maven来引入，才能正常编译。编写`pom.xml`文件如下：
```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/maven-v4_0_0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.itranswarp.learnjava</groupId>
    <artifactId>web-servlet-hello</artifactId>
    <packaging>war</packaging>
    <version>1.0-SNAPSHOT</version>

    <properties>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding>
        <maven.compiler.source>17</maven.compiler.source>
        <maven.compiler.target>17</maven.compiler.target>
        <java.version>17</java.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>jakarta.servlet</groupId>
            <artifactId>jakarta.servlet-api</artifactId>
            <version>5.0.0</version>
            <scope>provided</scope>
        </dependency>
    </dependencies>

    <build>
        <finalName>hello</finalName>
    </build>
</project>

```

这个`pom.xml`与我们前面讲到的普通Java程序有区别，打包类型不是`jar`，而是`war`，表示Java Web Application Archive
-   **`<packaging>war</packaging>`**: 表示这是一个 Web 应用程序归档（Web Application Archive）。
-   **`<scope>provided</scope>`**: 表示该依赖仅在编译和测试时需要，运行时由 Web 服务器提供，因此不会打包到最终的 `.war` 文件中。（运行期Web服务器本身已经提供了Servlet API相关的jar包）

## Servlet 版本与Tomcat版本
1.  **Servlet 4.0 及之前**:
    *   维护方：Oracle
    *   Maven 依赖：`javax.servlet:javax.servlet-api`
    *   包名：`javax.servlet.*`
2.  **Servlet 5.0 及之后**:
    *   维护方：Eclipse Foundation (Jakarta EE)
    *   Maven 依赖：`jakarta.servlet:jakarta.servlet-api`
    *   包名：`jakarta.servlet.*`

这里采用最新的`jakarta.servlet:5.0.0`版本，但对于很多仅支持Servlet 4.0版本的框架来说，例如Spring 5，我们就只能使用`javax.servlet:4.0.0`版本

>[!INFO] Tomcat 版本与 Servlet 版本
需要根据使用的 Servlet API 版本选择兼容的 Tomcat 版本：
>- **Servlet <= 4.0**: 使用 Tomcat 9.x 或更低版本。
>- **Servlet >= 5.0**: 使用 Tomcat 10.x 或更高版本。
参考：[Tomcat 版本页](https://tomcat.apache.org/whichversion.html)

## 项目结构
整个工程结构如下：
```
web-servlet-hello/
├── pom.xml
└── src/
    └── main/
        ├── java/
        │   └── com/itranswarp/learnjava/servlet/
        │       └── HelloServlet.java
        ├── resources/
        └── webapp/  # 存放 Web 资源，如 HTML, CSS, JS, 图片等，没有就为空
            └── WEB-INF/
                # web.xml (高版本 Servlet 非必需)
```

-   `src/main/webapp` 目录用于存放静态资源和 `WEB-INF` 目录。
-   高版本的 Servlet (>= 3.0) 可以使用注解（如 `@WebServlet`）来配置 Servlet，`WEB-INF/web.xml` 文件不再是必需的。

## 运行 WAR 包
`.war` 文件不能直接运行，需要部署到 **Servlet 容器**（Web 服务器）中。

**常用的 Servlet 容器:**

*   **Tomcat**: Apache 出品的开源免费服务器。
*   **Jetty**: Eclipse 出品的开源免费服务器。
*   **GlassFish**: 开源的全功能 Java EE 服务器。
*   **WebLogic** (Oracle), **WebSphere** (IBM): 收费的商用服务器。

**部署到 Tomcat:**

1.  下载并解压 Tomcat。
2.  将编译生成的 `hello.war` 文件复制到 Tomcat 的 `webapps` 目录下。
3.  切换到 Tomcat 的 `bin` 目录，运行 `startup.sh` (Linux/macOS) 或 `startup.bat` (Windows)。
4.  在浏览器中访问 `http://localhost:8080/hello/`。

如果希望通过 `http://localhost:8080/` 直接访问应用：
1.  关闭 Tomcat (`shutdown.sh` / `shutdown.bat`)。
2.  删除 `webapps` 目录下的所有内容。
3.  将 `hello.war` 复制到 `webapps` 目录，并重命名为 `ROOT.war`。
4.  重新启动 Tomcat。


运行Maven命令`mvn clean package`，在`target`目录下得到一个`hello.war`文件，这个文件就是我们编译打包后的Web应用程序。

>[!WARNING] 注意
>如果执行package命令遇到Execution default-war of goal org.apache.maven.plugins:maven-war-plugin:2.2:war failed错误时，可手动指定maven-war-plugin最新版本3.3.2，参考练习工程的pom.xml。

- 如何运行`war`文件？
普通Java程序通过启动JVM，然后执行`main()`方法开始运行。但是Web应用程序不太一样，我们无法直接运行`war`文件，必须先启动Web服务器，再由Web服务器加载我们编写的`HelloServlet`，这样就可以让`HelloServlet`处理浏览器发送的请求。


要运行我们的`hello.war`，首先要下载Tomcat服务器，解压后把`hello.war`复制到Tomcat的`webapps`目录下，然后切换到`bin`目录，执行`startup.sh`或`startup.bat`启动Tomcat服务器

在浏览器输入`http://localhost:8080/hello/`即可看到`HelloServlet`的输出：

为啥路径是`/hello/`而不是`/`？因为一个Web服务器允许同时运行多个Web App，而我们的Web App叫`hello`，因此，第一级目录`/hello`表示Web App的名字，后面的`/`才是我们在`HelloServlet`中映射的路径。

- 假如要使用`/`,先关闭Tomcat（执行`shutdown.sh`或`shutdown.bat`），然后删除Tomcat的webapps目录下的所有文件夹和文件，最后把我们的`hello.war`复制过来，改名为`ROOT.war`，文件名为`ROOT`的应用程序将作为默认应用，启动后直接访问`http://localhost:8080/`即可。

实际上，类似Tomcat这样的服务器也是Java编写的，启动Tomcat服务器实际上是启动Java虚拟机，执行Tomcat的`main()`方法，然后由Tomcat负责加载我们的`.war`文件，并创建一个`HelloServlet`实例，最后以多线程的模式来处理HTTP请求.

如果Tomcat服务器收到的请求路径是`/`（假定部署文件为ROOT.war），就转发到`HelloServlet`并传入`HttpServletRequest`和`HttpServletResponse`两个对象。

因为我们编写的Servlet并不是直接运行，而是由Web服务器加载后创建实例运行，所以，类似Tomcat这样的Web服务器也称为Servlet容器。

## Servlet 生命周期与线程
*   **实例化**: Servlet 实例由 Servlet 容器创建，开发者不能直接 `new`。
*   **单例**: 对于每个 Servlet 类，容器通常只创建一个实例。
*   **多线程**: 容器使用**多线程**来处理并发请求，多个线程可能会同时调用同一个 Servlet 实例的 `doGet()` 或 `doPost()` 方法。

**线程安全注意事项:**

*   **实例变量**: 定义在 Servlet 类中的实例变量会被多个线程共享，访问时必须考虑线程安全问题（例如使用 `synchronized` 或 `java.util.concurrent` 包中的类）。
*   **局部变量**: `doGet()`/`doPost()` 方法内的局部变量（包括传入的 `HttpServletRequest` 和 `HttpServletResponse` 对象）是线程安全的，因为每个线程有自己的栈空间。（是由Servlet容器传入的局部变量，只能被当前线程访问，不存在多个线程访问的问题）
*   **`ThreadLocal`**: 如果在 Servlet 中使用了 `ThreadLocal`，务必在请求处理结束时清理（调用 `remove()` 方法），否则可能因为线程池的线程复用导致状态污染下一个请求。

因此，正确编写Servlet，要清晰理解Java的多线程模型，需要同步访问的必须同步。

## 在 IDE 中启动和调试 (嵌入式 Tomcat)

为了方便开发和调试，可以将 Tomcat 服务器嵌入到应用程序中，直接通过运行 `main()` 方法来启动。

Tomcat实际上也是一个Java程序，我们看看Tomcat的启动流程：
1. 启动JVM并执行Tomcat的`main()`方法；
2. 加载war并初始化Servlet；
3. 正常服务。

启动Tomcat无非就是设置好classpath并执行Tomcat某个jar包的`main()`方法，我们完全可以把Tomcat的jar包全部引入进来，然后自己编写一个`main()`方法，先启动Tomcat，然后让它加载我们的webapp就行。

常用于现代微服务项目（springboot）
- **优点**：
    - 简化了开发和测试流程。
    - 无需安装和配置独立的 Tomcat 服务器。
    - 更适合现代的微服务和容器化部署（例如 Docker）。
- **缺点**：
    - 在传统的大型项目中，通常还是通过外部 Tomcat 部署的方式来运行应用，因为这种方式更符合企业运维的管理方式。

**1. Maven 配置 (嵌入式)**

修改 `pom.xml`，添加 `tomcat-embed-core` 和 `tomcat-embed-jasper` 依赖：
```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.itranswarp.learnjava</groupId>
    <artifactId>web-servlet-embedded</artifactId>
    <version>1.0-SNAPSHOT</version>
    <packaging>war</packaging>

    <properties>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding>
        <maven.compiler.source>17</maven.compiler.source>
        <maven.compiler.target>17</maven.compiler.target>
        <java.version>17</java.version>
        <tomcat.version>10.1.1</tomcat.version>
    </properties>

    <dependencies>
        <dependency><!-- 引入嵌入式 Tomcat -->
            <groupId>org.apache.tomcat.embed</groupId>
            <artifactId>tomcat-embed-core</artifactId>
            <version>${tomcat.version}</version>
            <scope>provided</scope>
        </dependency>
        <dependency>
            <groupId>org.apache.tomcat.embed</groupId>
            <artifactId>tomcat-embed-jasper</artifactId>
            <version>${tomcat.version}</version>
            <scope>provided</scope>
            <!-- scope 设为 provided，如果只想在 IDE 运行 -->
            <!-- 如果要打可执行 war 包，则移除 scope -->
        </dependency>
        <!-- 无需再显式引入 servlet-api，Tomcat 依赖已包含 -->
    </dependencies>
</project>
```
**2. Servlet 代码 (示例)**

可以稍微修改 `HelloServlet` 来处理请求参数：

```java
@WebServlet(urlPatterns = "/")
public class HelloServlet extends HttpServlet {
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        resp.setContentType("text/html");
        String name = req.getParameter("name"|| name.isEmpty());
        if (name == null) {
            name = "world";
        }
        PrintWriter pw = resp.getWriter();
        pw.write("<h1>Hello, " + name + "!</h1>");
        pw.flush();
    }
}
```

**3. 启动类 (`main` 方法)**

创建一个 `Main` 类来配置和启动嵌入式 Tomcat：

```java
import org.apache.catalina.Context;
import org.apache.catalina.WebResourceRoot;
import org.apache.catalina.startup.Tomcat;
import org.apache.catalina.webresources.DirResourceSet;
import org.apache.catalina.webresources.StandardRoot;

import java.io.File;

public class Main {
    public static void main(String[] args) throws Exception {
        // 启动Tomcat:
        Tomcat tomcat = new Tomcat();
        tomcat.setPort(Integer.getInteger("port", 8080)); //设置端口，默认为8080
        tomcat.getConnector(); //初始化连接器
        // 创建webapp:
        // 参数1: Context Path (空字符串表示根路径 "/")
        // 参数2: WebApp 目录 (指向 src/main/webapp)
        Context ctx = tomcat.addWebapp("", new File("src/main/webapp").getAbsolutePath());
        
        // 配置资源映射，使 Tomcat 能找到编译后的 .class 文件,Tomcat会自动加载当前工程作为根webapp，可直接在浏览器访问 http://localhost:8080/
        WebResourceRoot resources = new StandardRoot(ctx);
        resources.addPreResources(
                new DirResourceSet(resources, "/WEB-INF/classes", // WebApp 内部的类路径
	            new File("target/classes").getAbsolutePath(), // 实际的 .class 文件位置
                 "/"));// 映射的根路径
                
        ctx.setResources(resources);
        // 启动 Tomcat 服务器
        tomcat.start();
        // 阻塞当前线程，保持服务器运行
        tomcat.getServer().await();
    }
}
```

**好处:**
1.  **启动简单**: 无需单独下载和配置 Tomcat。
2.  **调试方便**: 可以直接在 IDE 中设置断点进行调试。
3.  **部署灵活**: 使用 Maven 打包的 `war` 文件仍然可以部署到独立的 Tomcat 服务器。

>[!TIP] IDE 配置 (IntelliJ IDEA)
>如果在 `pom.xml` 中将 Tomcat 依赖的 `scope` 设置为 `provided`，在 IntelliJ IDEA 中运行 `Main` 类时，需要：
>1.  进入 `Run/Debug Configurations`。
>2.  选择你的 `Application` 配置 (运行 `Main` 的配置)。
>3.  勾选 `Include dependencies with "Provided" scope` 选项。

## 生成可执行的war包

可以让 `.war` 文件像 `.jar` 文件一样通过 `java -jar xxx.war` 直接运行。这需要将嵌入式 Tomcat 的依赖打包进去，并配置 `maven-war-plugin`。

**1. 修改 `pom.xml`**

*   移除 Tomcat 依赖的 `<scope>provided</scope>`。
*   配置 `maven-war-plugin`：
```xml
<project ...>
    ...
	<build>
		<finalName>hello</finalName>
		<plugins>
			<plugin>
				<groupId>org.apache.maven.plugins</groupId>
				<artifactId>maven-war-plugin</artifactId>
				<version>3.3.2</version>
				<configuration>
					<!-- 将编译后的 classes 复制到 war 包根目录，以便 Main 类能被找到 -->
					<webResources>
						<resource>
							<directory>${project.build.directory}/classes</directory>
						</resource>
					</webResources>
					<archiveClasses>true</archiveClasses>
					<archive>
						<manifest>
							<!-- 添加 Class-Path 到 MANIFEST.MF -->
							<addClasspath>true</addClasspath>
							<!-- Classpath 前缀，指向解压后的 lib 目录 -->
							<classpathPrefix>tmp-webapp/WEB-INF/lib/</classpathPrefix>
							<!-- 指定 Main 启动类 -->
							<mainClass>com.itranswarp.learnjava.Main</mainClass>
						</manifest>
					</archive>
				</configuration>
			</plugin>
		</plugins>
	</build>
</project>
```

生成的war包结构如下：
```
hello.war
├── META-INF
│   ├── MANIFEST.MF
│   └── maven
│       └── ...
├── WEB-INF
│   ├── classes
│   ├── lib
│   │   ├── ecj-3.18.0.jar
│   │   ├── tomcat-annotations-api-10.1.1.jar
│   │   ├── tomcat-embed-core-10.1.1.jar
│   │   ├── tomcat-embed-el-10.1.1.jar
│   │   ├── tomcat-embed-jasper-10.1.1.jar
│   │   └── web-servlet-embedded-1.0-SNAPSHOT.jar
│   └── web.xml
└── com
    └── itranswarp
        └── learnjava
            ├── Main.class
            ├── TomcatRunner.class
            └── servlet
                └── HelloServlet.class
```

用`java -jar hello.war`启动时，JVM的Class Loader不会查找`WEB-INF/lib`的jar包，而是直接从`hello.war`的根目录查找，所以要把编译后的classes复制到war包根目录

`MANIFEST.MF`生成的内容如下：

```plain
Main-Class: com.itranswarp.learnjava.Main
Class-Path: tmp-webapp/WEB-INF/lib/tomcat-embed-core-10.1.1.jar tmp-weba
 pp/WEB-INF/lib/tomcat-annotations-api-10.1.1.jar tmp-webapp/WEB-INF/lib
 /tomcat-embed-jasper-10.1.1.jar tmp-webapp/WEB-INF/lib/tomcat-embed-el-
 10.1.1.jar tmp-webapp/WEB-INF/lib/ecj-3.18.0.jar
```

注意到`Class-Path`的路径，这里定义的`Class-Path`相当于`java -cp`指定的Classpath，JVM不会在一个jar包中查找jar包内的jar包，它只会在文件系统中搜索，因此，我们要修改`main()`方法，在执行`main()`方法时，先自解压`war`包，再启动Tomcat：

**2. 修改 `Main` 类 (支持自解压)**

JVM 的标准 ClassLoader 不能直接加载 `war` 包内 `WEB-INF/lib` 下的 jar 包。因此，`Main` 类需要在启动时，先将 `war` 包内的依赖解压到一个临时目录，然后才能启动 Tomcat。

```java
public class Main {
    public static void main(String[] args) throws Exception {
        // 判定是否从jar/war启动:
        String jarFile = Main.class.getProtectionDomain().getCodeSource().getLocation().getFile();
        boolean isJarFile = jarFile.endsWith(".war") || jarFile.endsWith(".jar");
        // 定位webapp根目录:
        String webDir = isJarFile ? "tmp-webapp" : "src/main/webapp";
        if (isJarFile) {
            // 解压到tmp-webapp:
            Path baseDir = Paths.get(webDir).normalize().toAbsolutePath();
            
            if (Files.isDirectory(baseDir)) {
                Files.delete(baseDir);
            }
            Files.createDirectories(baseDir);
            System.out.println("extract to: " + baseDir);
            try (JarFile jar = new JarFile(jarFile)) {
                List<JarEntry> entries = jar.stream().sorted(Comparator.comparing(JarEntry::getName))
                        .collect(Collectors.toList());
                for (JarEntry entry : entries) {
                    Path res = baseDir.resolve(entry.getName());
                    if (!entry.isDirectory()) {
                        System.out.println(res);
                        Files.createDirectories(res.getParent());
                        Files.copy(jar.getInputStream(entry), res);
                    }
                }
            }
            // JVM退出时自动删除tmp-webapp:
            Runtime.getRuntime().addShutdownHook(new Thread(() -> {
                try {
                    Files.walk(baseDir).sorted(Comparator.reverseOrder()).map(Path::toFile).forEach(File::delete);
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }));
        }
        // 启动Tomcat:
        TomcatRunner.run(webDir, isJarFile ? "tmp-webapp" : "target/classes");
    }
}

// Tomcat启动类:
class TomcatRunner {
    public static void run(String webDir, String baseDir) throws Exception {
        Tomcat tomcat = new Tomcat();
        tomcat.setPort(Integer.getInteger("port", 8080));
        tomcat.getConnector();
        Context ctx = tomcat.addWebapp("", new File(webDir).getAbsolutePath());
        WebResourceRoot resources = new StandardRoot(ctx);
        resources.addPreResources(new DirResourceSet(resources, "/WEB-INF/classes", new File(baseDir).getAbsolutePath(), "/"));
        ctx.setResources(resources);
        tomcat.start();
        tomcat.getServer().await();
    }
}
```

现在，执行`java -jar hello.war`时，JVM先定位`hello.war`的`Main`类，运行`main()`，自动解压后，文件系统目录如下：

```
<work>
├── hello.war
└── tmp-webapp
    └── WEB-INF
        ├── lib
        │   ├── ecj-3.18.0.jar
        │   ├── tomcat-annotations-api-10.1.1.jar
        │   ├── tomcat-embed-core-10.1.1.jar
        │   ├── tomcat-embed-el-10.1.1.jar
        │   ├── tomcat-embed-jasper-10.1.1.jar
        │   └── web-servlet-embedded-1.0-SNAPSHOT.jar
        └── web.xml
```

解压后的目录结构和我们在`MANIFEST.MF`中设定的`Class-Path`一致，因此，JVM能顺利加载Tomcat的jar包，然后运行Tomcat，启动Web App。

编写可执行的jar或者war需要注意的几点：

- 必须在`MANIFEST.MF`中指定`Main-Class`和`Class-Path`；
- `Main`必须能在jar/war包的根目录下被JVM的Class Loader加载；
- `Main`负责解压jar/war，解压后的目录结构与`MANIFEST.MF`中设定的`Class-Path`一致；
- `Main`不能引用任何解压后才能被加载的类，例如`org.apache.catalina.startup.Tomcat`。

SpringBoot也支持在`main()`方法中一行代码直接启动Tomcat，并且还能方便地更换成Jetty等其他服务器。它的启动方式和我们介绍的是基本一样的，后续涉及到SpringBoot的部分我们还会详细讲解。

引入的Tomcat的scope为`provided`，在Idea下运行时，需要设置`Run/Debug Configurations`，选择`Application - Main`，钩上`Include dependencies with "Provided" scope`，这样才能让Idea在运行时把Tomcat相关依赖包自动添加到classpath中。


参考：
**2. 修改 `Main` 类 (支持自解压)**

JVM 的标准 ClassLoader 不能直接加载 `war` 包内 `WEB-INF/lib` 下的 jar 包。因此，`Main` 类需要在启动时，先将 `war` 包内的依赖解压到一个临时目录，然后才能启动 Tomcat。

```java
import org.apache.catalina.Context;
import org.apache.catalina.WebResourceRoot;
import org.apache.catalina.startup.Tomcat;
import org.apache.catalina.webresources.DirResourceSet;
import org.apache.catalina.webresources.StandardRoot;

import java.io.File;
import java.io.IOException;
import java.net.URISyntaxException;
import java.nio.file.*;
import java.util.Comparator;
import java.util.List;
import java.util.jar.JarEntry;
import java.util.jar.JarFile;
import java.util.stream.Collectors;

public class Main {
    public static void main(String[] args) throws Exception {
        // 判定是否从 jar/war 启动:
        String protocol = Main.class.getResource("").getProtocol();
        boolean isJarFile = "jar".equals(protocol);

        // 定位 webapp 根目录:
        String webDir = isJarFile ? "tmp-webapp" : "src/main/webapp";
        Path baseDir = Paths.get(webDir).toAbsolutePath();

        if (isJarFile) {
            System.out.println("Running from JAR/WAR file...");
            // 获取当前运行的 jar/war 文件路径
            Path jarFilePath = Paths.get(Main.class.getProtectionDomain().getCodeSource().getLocation().toURI());
            System.out.println("JAR/WAR file path: " + jarFilePath);

            // 清理并创建临时解压目录 tmp-webapp
            if (Files.exists(baseDir)) {
                // 递归删除目录
                Files.walk(baseDir)
                     .sorted(Comparator.reverseOrder())
                     .map(Path::toFile)
                     .forEach(File::delete);
            }
            Files.createDirectories(baseDir);
            System.out.println("Extracting to temporary directory: " + baseDir);

            // 解压 war 包内容到 tmp-webapp
            try (JarFile jar = new JarFile(jarFilePath.toFile())) {
                List<JarEntry> entries = jar.stream()
                        .filter(entry -> !entry.getName().startsWith("META-INF/")) // 排除 META-INF
                        .filter(entry -> entry.getName().startsWith("WEB-INF/")) // 只解压 WEB-INF
                        .sorted(Comparator.comparing(JarEntry::getName))
                        .collect(Collectors.toList());

                for (JarEntry entry : entries) {
                    Path entryPath = baseDir.resolve(entry.getName());
                    if (!entry.isDirectory()) {
                        Files.createDirectories(entryPath.getParent());
                        Files.copy(jar.getInputStream(entry), entryPath, StandardCopyOption.REPLACE_EXISTING);
                        // System.out.println("Extracted: " + entry.getName());
                    } else {
                         Files.createDirectories(entryPath);
                    }
                }
            }
            System.out.println("Extraction complete.");

            // 注册 JVM 关闭钩子，用于删除临时目录
            Runtime.getRuntime().addShutdownHook(new Thread(() -> {
                System.out.println("Deleting temporary directory: " + baseDir);
                try {
                    Files.walk(baseDir)
                         .sorted(Comparator.reverseOrder())
                         .map(Path::toFile)
                         .forEach(File::delete);
                } catch (IOException e) {
                    System.err.println("Failed to delete temporary directory: " + e.getMessage());
                }
            }));
        } else {
             System.out.println("Running from IDE/exploded directory...");
        }

        // 启动 Tomcat (将启动逻辑移到单独的类/方法，避免 Main 类直接依赖 Tomcat 类)
        // baseDirForClasses 指向 .class 文件位置
        String baseDirForClasses = isJarFile ? baseDir.resolve("WEB-INF/classes").toString() : "target/classes";
        TomcatRunner.run(webDir, baseDirForClasses);
    }
}

// 将 Tomcat 启动逻辑分离，避免 Main 类在解压前加载 Tomcat 类
class TomcatRunner {
    public static void run(String webDir, String baseDirForClasses) throws Exception {
        Tomcat tomcat = new Tomcat();
        tomcat.setPort(Integer.getInteger("port", 8080));
        tomcat.getConnector();

        // 注意：addWebapp 的第二个参数现在是解压后的 webDir 或源码的 webapp 目录
        Context ctx = tomcat.addWebapp("", new File(webDir).getAbsolutePath());

        WebResourceRoot resources = new StandardRoot(ctx);
        resources.addPreResources(new DirResourceSet(resources,
                "/WEB-INF/classes",
                new File(baseDirForClasses).getAbsolutePath(), // 指向正确的 classes 目录
                "/"));
        ctx.setResources(resources);

        System.out.println("Starting Tomcat on port " + tomcat.getConnector().getLocalPort() + "...");
        tomcat.start();
        System.out.println("Tomcat started. Context path: [" + ctx.getPath() + "]");
        tomcat.getServer().await();
    }
}
```

**关键点:**

*   **`MANIFEST.MF`**: `maven-war-plugin` 会在 `META-INF/MANIFEST.MF` 中生成 `Main-Class` 和 `Class-Path`。`Class-Path` 指向解压后的依赖路径（如 `tmp-webapp/WEB-INF/lib/tomcat-embed-core-*.jar`）。
*   **`Main` 类位置**: `Main.class` 需要放在 `war` 包的根目录下（通过 `webResources` 配置实现），以便 JVM 启动时能找到它。
*   **自解压**: `main()` 方法首先判断是否从 `war` 启动，如果是，则将 `WEB-INF/lib` 下的 jar 包解压到 `tmp-webapp/WEB-INF/lib` 目录。
*   **类加载**: 解压完成后，`MANIFEST.MF` 中指定的 `Class-Path` 就能被 JVM 用来加载 Tomcat 相关的类。
*   **分离启动逻辑**: 将实际的 Tomcat 启动代码（如 `new Tomcat()`）放到另一个类（`TomcatRunner`）中，避免 `Main` 类在解压完成前就尝试加载 Tomcat 类而导致 `ClassNotFoundException`。
*   **清理**: 使用 Shutdown Hook 在 JVM 退出时自动删除解压产生的临时目录。

现在，执行 `mvn clean package` 生成 `hello.war` 后，可以通过 `java -jar target/hello.war` 来启动应用。

**与 Spring Boot 对比:** Spring Boot 的可执行 jar/war 也采用了类似的原理（自定义 ClassLoader 或自解压），但提供了更完善和透明的实现。