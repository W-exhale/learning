## 1. 介绍
### 1.1 maven作用
- Maven是专门为Java项目打造的管理和构建工具，它的主要功能有：
	- 提供了一套标准化的项目结构；
	- 提供了一套标准化的构建流程（编译，测试，打包，发布……）；
	- 提供了一套依赖管理机制，自动下载、管理和添加各种第三方库（JAR 包）
### 1.2 标准 Maven 项目结构
#### 整体结构
- 用maven管理的普通的Java项目的默认目录结构
使用 Maven 管理的 Java 项目通常遵循以下默认目录结构：

```
a-maven-project/        # 项目根目录，项目名
├── pom.xml             # Maven项目的核心配置文件
├── src/
│   ├── main/
│   │   ├── java/       # 存放项目 Java 源码
│   │   └── resources/  # 存放项目资源文件 (如配置文件)
│   └── test/
│       ├── java/       # 存放测试用例 Java 源码
│       └── resources/  # 存放测试相关的资源文件
└── target/             # 存放编译和打包后的输出文件，此目录通常不纳入版本控制。 (如 .class, .jar)
```
#### pom.xml
- 分析项目描述文件pom.xml
	-  一个Maven工程就是由`groupId`，`artifactId`和`version`作为唯一标识。
		- `groupId`：项目所属的组织或公司，类似于 Java 的包名（通常使用反向域名）
		- `artifactId`：项目的唯一名称，类似于 Java 的类名（通常是项目模块名）。
		- `version`：项目的版本号。
	- `<properties>`定义了一些属性，常用的属性有：
		- `project.build.sourceEncoding`：指定项目源码的字符编码，通常应设定为`UTF-8`；
		- `maven.compiler.release`：指定编译和运行项目所需的 JDK 版本（例如 `17`, `21`）。这是 Java 9 及以后版本推荐的配置方式，它能确保源码兼容性和编译输出版本一致。
		- `maven.compiler.source`：指定编译器接受的源代码版本（如果需要与 `target` 不同）。
		- `maven.compiler.target`：指定编译器生成的字节码（`.class` 文件）版本（如果需要与 `source` 不同）。

通过`<properties>`定义的属性，就可以固定JDK版本，防止同一个项目的不同的开发者各自使用不同版本的JDK。

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <!-- 项目坐标 -->
    <groupId>com.itranswarp.learnjava</groupId>
    <artifactId>hello</artifactId>
    <version>1.0</version>
    <packaging>jar</packaging> <!-- 打包方式，默认为 jar -->

    <!-- 项目属性 -->
    <properties>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <maven.compiler.release>17</maven.compiler.release> <!-- 推荐使用 release -->
    </properties>

    <!-- 项目依赖 -->
    <dependencies>
        <dependency>
            <groupId>org.slf4j</groupId>
            <artifactId>slf4j-simple</artifactId>
            <version>2.0.16</version>
        </dependency>
        <!-- 其他依赖 -->
    </dependencies>

</project>
```

- `<dependencies>` 标签用于声明项目所依赖的第三方库。每个依赖项通过 `<dependency>` 标签定义，并使用其自身的 `groupId`、`artifactId` 和 `version` 来指定。例如，依赖`org.slfj4:slf4j-simple:2.0.16`：
```xml
<dependency>
    <groupId>org.slf4j</groupId>
    <artifactId>slf4j-simple</artifactId>
    <version>2.0.16</version>
</dependency>
```
使用`<dependency>`声明一个依赖后，Maven 会自动从配置的仓库（本地或远程）下载所需的 JAR 包，并将其添加到项目的 classpath 中。

### 1.3 下载
- 官网下载bin
- 解压缩
	- 环境变量配置
	![Pasted image 20250403094016](images/Pasted%20image%2020250403094016.png)
	- Path：`%MAVEN_HOME%\bin`
- 在conf文件里的settings.xml配置本地仓库

## 2. 依赖管理
### 2.1 依赖关系
例如，我们的项目依赖`abc`这个jar包，而`abc`又依赖`xyz`这个jar包，当我们声明了`abc`的依赖时，Maven自动把`abc`和`xyz`加入我们的项目依赖，不需要我们自己去研究`abc`是否需要依赖`xyz`
- Maven定义了几种依赖关系，分别是`compile`、`test`、`runtime`和`provided`：

| scope    | 说明                                    | 示例              |
| -------- | ------------------------------------- | --------------- |
| compile  | 编译时需要用到该jar包，运行也要（默认）                 | commons-logging |
| test     | 编译和运行测试测试代码时需要用到该jar包，正常运行不需要         | junit           |
| runtime  | 编译时不需要，但运行时需要用到                       | mysql           |
| provided | 编译和测试时需要用到，但运行时由外部环境提供（JDK、Servlet容器） | servlet-api     |

1. `compile`（默认）：Maven会把这种类型的依赖直接放入classpath，并打包到最终的应用程序（如 JAR 或 WAR）中。
2. `test`：JUnit，这些依赖只在执行 `src/test/java` 下的代码时需要，不会被打包进最终的发布包。：
```xml
<dependency>
    <groupId>org.junit.jupiter</groupId>
    <artifactId>junit-jupiter-api</artifactId>
    <version>5.3.2</version>
    <scope>test</scope>
</dependency>
```
3. `runtime`：最典型的依赖是JDBC驱动，例如MySQL驱动：
```xml
<dependency>
    <groupId>mysql</groupId>
    <artifactId>mysql-connector-java</artifactId>
    <version>5.1.48</version>
    <scope>runtime</scope>
</dependency>
```
4. `provided`：最典型的是Servlet API，编译的时候需要，但是运行时，Servlet服务器内置了相关的jar，所以运行期不需要：
```xml
<dependency>
    <groupId>jakarta.servlet</groupId>
    <artifactId>jakarta.servlet-api</artifactId>
    <version>4.0.0</version>
    <scope>provided</scope>
</dependency>
```

- Maven并不会每次都从中央仓库（[Index of /](https://repo1.maven.org/)）下载jar包。一个jar包一旦被下载过，就会被Maven自动缓存在本地目录（用户主目录的`.m2`目录），所以，除了第一次编译时因为下载需要时间会比较慢，后续过程因为有本地缓存，并不会重复下载相同的jar包。

### 2.2  唯一ID
- 对于某个依赖，Maven只需要3个变量即可唯一确定某个jar包：
	- `groupId`：属于组织的名称，类似Java的包名通常使用反向域名（如 `com.google.guava`）；
	- `artifactId`：该jar包自身的名称，类似Java的类名；
	- `version`：该jar包的版本（如 `32.1.3-jre`）。
- Maven通过对jar包进行**PGP签名**确保任何一个jar包一经发布就无法修改。修改已发布jar包的唯一方法是发布一个**新版本**。
- 注：只有以`-SNAPSHOT`结尾的版本号会被Maven视为开发版本，开发版本每次都会重复下载，这种SNAPSHOT版本只能用于内部私有的Maven repo，公开发布的版本不允许出现SNAPSHOT。

### 2.3 Maven镜像
#### 设置镜像
Maven 的 `settings.xml` 可能有两个位置：
- **全局配置**（推荐）：`MAVEN_HOME/conf/settings.xml`
- **用户配置**：`C:\Users\你的用户名\.m2\settings.xml`
    
建议修改 **用户配置** (`.m2/settings.xml`)，这样不会影响全局的 Maven 配置。
- Maven镜像仓库定期从中央仓库同步：
![Pasted image 20250403093414](images/Pasted%20image%2020250403093414.png)

- 在用户主目录下进入`.m2`目录，创建一个`settings.xml`配置文件，内容如下：
```xml
<settings>
    <mirrors>
        <mirror>
            <id>aliyun</id>
            <name>aliyun</name>
            <mirrorOf>central</mirrorOf>
            <!-- 国内推荐阿里云的Maven镜像 -->
            <url>https://maven.aliyun.com/repository/central</url>
        </mirror>
    </mirrors>
</settings>
```

#### 设置国内仓库
在 **`settings.xml`** 或 **`pom.xml`** 里，**添加国内仓库**：
🔹 **效果**：
```xml
<repositories>
    <repository>
        <id>aliyun-central</id>
        <url>https://maven.aliyun.com/repository/central</url>
        <releases>
            <enabled>true</enabled>
        </releases>
        <snapshots>
            <enabled>false</enabled>
        </snapshots>
    </repository>
</repositories>
```
- Maven **仍然会先访问中央仓库**，如果找不到，才会去 **国内仓库** 下载依赖。

#### 区别

|          | **国内仓库（repositories）**     | **镜像（mirrors）**          |
| -------- | -------------------------- | ------------------------ |
| **作用**   | 额外的依赖下载源                   | 完全替换中央仓库                 |
| **配置文件** | `settings.xml` 或 `pom.xml` | 仅 `settings.xml`         |
| **影响范围** | 只影响 **指定的仓库**              | 影响 **所有 Maven 依赖**       |
| **工作方式** | **先访问中央仓库**，找不到再访问国内仓库     | **所有请求** 都先走国内镜像，不访问中央仓库 |
| **适用场景** | 需要访问 **额外的第三方仓库**          | **加速** Maven 依赖下载        |
**如果你需要访问** **额外的仓库（比如某些国内公司内部的依赖）**，可以**使用国内仓库（repositories）**

### 2.4 其他
- 引用第三方组件，通过[search.maven.org](https://search.maven.org/)搜索关键字，找到对应的组件后，直接复制：（或者[Maven Repository: Search/Browse/Explore](https://mvnrepository.com/)）

*   **命令行构建:** 在项目根目录（包含 `pom.xml` 的目录）下，可以使用 `mvn` 命令执行构建任务。常用命令：
    ```bash
    # 清理 target 目录 (删除旧的构建输出)
    mvn clean

    # 编译项目代码 (src/main/java)
    mvn compile

    # 运行测试 (src/test/java)
    mvn test

    # 打包项目 (根据 pom.xml 中的 <packaging> 类型，通常是 jar 或 war)
    # 这个命令会先执行 compile 和 test
    mvn package

    # 清理并打包
    mvn clean package

    # 安装到本地仓库 (供本机其他项目依赖)
    # 会先执行 clean, compile, test, package
    mvn install

    # 清理并安装
    mvn clean install
    ```
    构建成功后，产物（如 `.jar` 文件）通常位于 `target/` 目录下。

### 2.5 在IDE中使用Maven
##### 为当前项目配置Maven
- 依次点击 IDEA 菜单栏 ：_File | Settings_ :
![Pasted image 20250403103300](images/Pasted%20image%2020250403103300.png)

##### 全局配置

![Pasted image 20250403103948](images/Pasted%20image%2020250403103948.png)

- 后面的步骤和上面一样

##### 创建maven项目
- new project--> maven
-  可以选择 `Create from archetype` 来使用项目模板，或者直接点击 `Next` 创建一个简单的 Maven 项目骨架。
![Pasted image 20250403104435](images/Pasted%20image%2020250403104435.png)

## 3. 构建流程
- Maven不仅有标准化的项目结构，而且有一套标准化的构建标准，可以自动化实现编译，打包，发布等等

### 3.1 生命周期（Lifecycle）和Phase
- 使用`mvn`命令，后面跟phase，Maven自动根据生命周期运行到指定的phase

- 每个生命周期由一系列有序的 **阶段 (Phase)** 组成。当你执行一个 Maven 命令指定某个阶段时，Maven 会 **按顺序执行该生命周期中从开始到指定阶段的所有阶段**。
**`default` 生命周期包含的主要阶段 (按顺序):**

*   `validate`: 验证项目是否正确，所有必要信息是否可用。
*   `initialize`: 初始化构建状态，例如设置属性。
*   `generate-sources`: 生成任何需要包含在编译过程中的源代码。
*   `process-sources`: 处理源代码，例如过滤值。
*   `generate-resources`: 生成需要包含在包中的资源文件。
*   `process-resources`: 复制并处理资源文件到目标目录，准备打包。
*   `compile`: **编译** 项目的源代码 (`src/main/java`)。
*   `process-classes`: 对编译后的文件进行后处理，例如字节码增强。
*   `generate-test-sources`: 生成任何需要包含在测试编译过程中的测试源代码。
*   `process-test-sources`: 处理测试源代码。
*   `generate-test-resources`: 生成测试所需的资源文件。
*   `process-test-resources`: 复制并处理测试资源文件到测试目标目录。
*   `test-compile`: **编译** 测试源代码 (`src/test/java`)。
*   `process-test-classes`: 对测试编译后的文件进行后处理。
*   `test`: 使用合适的单元测试框架（如 Surefire 插件运行 JUnit）**运行测试**。
*   `prepare-package`: 在实际打包前进行准备工作。
*   `package`: **打包** 编译后的代码，并以可分发的格式（如 JAR、WAR）进行打包。
*   `pre-integration-test`: 执行集成测试前的操作。
*   `integration-test`: 处理和部署包到可以运行集成测试的环境中。
*   `post-integration-test`: 执行集成测试后的操作，例如清理环境。
*   `verify`: 运行任何检查以验证包是否有效且符合质量标准。
*   `install`: 将包 **安装** 到本地 Maven 仓库 (`.m2/repository`)，供本地其他项目作为依赖使用。
*   `deploy`: 将最终的包复制到远程仓库，供其他开发人员或项目共享（通常需要配置仓库认证信息）。

**示例:**
*   执行 `mvn compile`：会依次执行 `validate`, `initialize`, ..., `process-resources`, `compile` 这些阶段。

另一个常用的生命周期是`clean`，**`clean` 生命周期包含的阶段:**
*   `pre-clean`: 执行清理前需要完成的工作。
*   `clean`: **删除** 上次构建生成的所有文件（通常是 `target/` 目录）。
*   `post-clean`: 执行清理后需要完成的工作。

更复杂的例子是指定多个phase，例如，运行`mvn clean package`，Maven先执行`clean`生命周期并运行到`clean`，然后执行`default`生命周期并运行到`package`
- pre-clean
- clean （注意这个clean是phase）
- validate （开始执行default生命周期的第一个phase）
- initialize
- ...
- prepare-package
- package

常用命令：
`mvn clean`：清理所有生成的class和jar；
`mvn clean compile`：先清理，再执行到`compile`；
`mvn clean test`：先清理，再执行到`test`，因为执行`test`前必须执行`compile`，所以这里不必指定`compile`；
`mvn clean package`：先清理，再执行到`package`。

> **注意:** 很多阶段在默认情况下并没有绑定具体的操作（插件目标），除非你在 `pom.xml` 中进行了配置。但像 `compile`, `test`, `package` 这些核心阶段都有默认的插件目标绑定。

经常用到的phase其实只有几个：
- clean：清理
- compile：编译
- test：运行测试
- package：打包

### 3.2 Goal
执行一个phase会触发一个或多个goal，**阶段 (Phase)** 只是构建过程中的一个步骤标记，实际的工作是由绑定到这些阶段的 **插件目标 (Plugin Goal)** 来完成的。

| 执行的 Phase | 默认绑定的主要 Goal(s)                     |
| :----------- | :----------------------------------------- |
| `compile`    | `compiler:compile`                         |
| `test-compile`| `compiler:testCompile`                     |
| `test`       | `surefire:test`                            |
| `package`    | `jar:jar` (如果 packaging 是 jar) <br> `war:war` (如果 packaging 是 war) |
| `install`    | `install:install`                          |
| `deploy`     | `deploy:deploy`                            |
| `clean`      | `clean:clean`                              |

goal的命名总是`abc:xyz`这种形式。

- 类比
	- **lifecycle**相当于Java的package，它包含一个或多个phase；
	- **phase**相当于Java的class，它包含一个或多个goal；
	- **goal**相当于class的method，它其实才是真正干活的。

大多数情况，我们只要指定phase，就默认执行这些phase默认绑定的goal，只有少数情况，我们可以直接指定运行一个goal，例如，启动Tomcat服务器：

```plain
$ mvn tomcat:run
```

## 4. 使用插件
### 4.1 介绍
- 使用maven构建项目就是执行lifecycle，执行到指定的phase为止，每个phase会执行自己默认的一个或多个goal。goal是最小任务单元
- 假如我们要执行`compile`这个phase：`mvn compile`
- Maven将执行`compile`这个phase，这个phase会调用`compiler`插件执行相关联的`compiler:compile`

实际上执行每个phase都是通过某个插件来执行的，Maven本身不知道怎么执行`compile`，它只负责找到`compiler`插件，然后执行goal来完成编译

使用maven就是配置好需要使用的插件，通过phase调用它们

常用的标准插件Maven已经内置：

| 插件前缀 (Prefix) | 核心 Goal(s)                | 通常绑定的 Phase              | 主要功能       |
| :------------ | :------------------------ | :----------------------- | :--------- |
| `clean`       | `clean:clean`             | `clean`                  | 清理构建目录     |
| `compiler`    | `compiler:compile`        | `compile`                | 编译主代码      |
|               | `compiler:testCompile`    | `test-compile`           | 编译测试代码     |
| `surefire`    | `surefire:test`           | `test`                   | 运行单元测试     |
| `jar`         | `jar:jar`                 | `package`                | 打包成 JAR 文件 |
| `war`         | `war:war`                 | `package`                | 打包成 WAR 文件 |
| `install`     | `install:install`         | `install`                | 安装到本地仓库    |
| `deploy`      | `deploy:deploy`           | `deploy`                 | 部署到远程仓库    |
| `resources`   | `resources:resources`     | `process-resources`      | 处理主资源文件    |
|               | `resources:testResources` | `process-test-resources` | 处理测试资源文件   |
| `site`        | `site:site`               | `site`                   | 生成项目站点     |
|               | `site:deploy`             | `site-deploy`            | 发布项目站点     |
### 4.2 自定义插件
- **声明插件:** 如果要使用非核心插件，或者需要覆盖核心插件的默认行为/版本，就需要在 `pom.xml` 的 `<build>` -> `<plugins>` 部分进行声明
- **示例 (maven-shade-plugin):** `maven-shade-plugin` 是一个常用的插件，它可以将项目及其所有依赖项打包到一个“超级 JAR”（uber-JAR）中，方便分发和执行。
    
    ```xml
    <project>
        ...
        <build>
            <plugins>
                <plugin>
                    <!-- 插件坐标 -->
                    <groupId>org.apache.maven.plugins</groupId>
                    <artifactId>maven-shade-plugin</artifactId>
                    <version>3.5.1</version> <!-- 推荐使用较新稳定版本 -->
    
                    <!-- 配置插件执行 -->
                    <executions>
                        <execution>
                            <id>shade-my-jar</id> <!-- 可选：给执行一个唯一ID -->
                            <phase>package</phase> <!-- 绑定到 package 生命周期阶段 -->
                            <goals>
                                <goal>shade</goal> <!-- 执行 shade 目标 -->
                            </goals>
                            <!-- 插件的具体配置 -->
                            <configuration>
                                <transformers>
                                    <!-- 配置 Manifest 文件，指定主类，使 JAR 可执行 -->
                                    <transformer implementation="org.apache.maven.plugins.shade.resource.ManifestResourceTransformer">
                                        <mainClass>com.yourcompany.yourapp.Main</mainClass> <!-- 替换为你的主类全名 -->
                                    </transformer>
                                    <!-- 可以添加其他 transformer 来处理资源合并等问题 -->
                                </transformers>
                                <!-- 其他配置，如过滤依赖等 -->
                                <!-- <filters>...</filters> -->
                            </configuration>
                        </execution>
                    </executions>
                </plugin>
                <!-- 可以声明其他插件 -->
            </plugins>
        </build>
        ...
    </project>
    ```
    
自定义插件往往需要一些配置，例如，`maven-shade-plugin`需要指定Java程序的入口，它的配置是：

```xml
<configuration>
    <transformers>
        <transformer implementation="org.apache.maven.plugins.shade.resource.ManifestResourceTransformer">
            <mainClass>com.itranswarp.learnjava.Main</mainClass>
        </transformer>
    </transformers>
</configuration>
```

- **插件配置 (`<configuration>`):** 大多数插件都需要通过 `<configuration>` 元素进行定制。具体的配置项需要查阅对应插件的官方文档。
    
- **执行绑定 (`<executions>`):** 通过 `<executions>` 可以将插件的特定 Goal 绑定到生命周期的某个 Phase。当执行到该 Phase 时，绑定的 Goal 就会自动执行。也可以不绑定，仅通过命令行直接调用插件 Goal (`mvn shade:shade`)。

**注意**，Maven自带的标准插件例如`compiler`是无需声明的，只有引入其它的插件才需要声明。

常用的插件：
- maven-shade-plugin：打包所有依赖包并生成可执行jar；
- cobertura-maven-plugin：生成 JaCoCo 单元测试和集成测试的代码覆盖率报告 (Cobertura 已不再积极维护，推荐 JaCoCo)。
- findbugs-maven-plugin：对Java源码进行静态分析以找出潜在问题。

## 5. 模块管理
### 介绍
- 软件开发中，把一个大项目拆分为多个模块是降低软件复杂度的有效方法
![Pasted image 20250404210544](images/Pasted%20image%2020250404210544.png)

Maven可以有效地管理多个模块，我们只需要把每个模块当作一个独立的Maven项目，它们有各自独立的`pom.xml`。例如，模块A的`pom.xml`：
```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.itranswarp.learnjava</groupId>
    <artifactId>module-a</artifactId>
    <version>1.0</version>
    <packaging>jar</packaging>

    <name>module-a</name>

    <properties>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding>
        <maven.compiler.source>11</maven.compiler.source>
        <maven.compiler.target>11</maven.compiler.target>
        <java.version>11</java.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.slf4j</groupId>
            <artifactId>slf4j-api</artifactId>
            <version>1.7.28</version>
        </dependency>
        <dependency>
            <groupId>ch.qos.logback</groupId>
            <artifactId>logback-classic</artifactId>
            <version>1.2.3</version>
            <scope>runtime</scope>
        </dependency>
        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter-engine</artifactId>
            <version>5.5.2</version>
            <scope>test</scope>
        </dependency>
    </dependencies>
</project>
```

模块B的`pom.xml`：

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.itranswarp.learnjava</groupId>
    <artifactId>module-b</artifactId>
    <version>1.0</version>
    <packaging>jar</packaging>

    <name>module-b</name>

    <properties>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding>
        <maven.compiler.source>11</maven.compiler.source>
        <maven.compiler.target>11</maven.compiler.target>
        <java.version>11</java.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.slf4j</groupId>
            <artifactId>slf4j-api</artifactId>
            <version>1.7.28</version>
        </dependency>
        <dependency>
            <groupId>ch.qos.logback</groupId>
            <artifactId>logback-classic</artifactId>
            <version>1.2.3</version>
            <scope>runtime</scope>
        </dependency>
        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter-engine</artifactId>
            <version>5.5.2</version>
            <scope>test</scope>
        </dependency>
    </dependencies>
</project>
```

可以看出来，模块A和模块B的`pom.xml`高度相似，除了name和项目名都一样，可以提出相同部分作为`parent`
```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.itranswarp.learnjava</groupId>
    <artifactId>parent</artifactId>
    <version>1.0</version>
    <packaging>pom</packaging>

    <name>parent</name>

    <properties>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding>
        <maven.compiler.source>11</maven.compiler.source>
        <maven.compiler.target>11</maven.compiler.target>
        <java.version>11</java.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.slf4j</groupId>
            <artifactId>slf4j-api</artifactId>
            <version>1.7.28</version>
        </dependency>
        <dependency>
            <groupId>ch.qos.logback</groupId>
            <artifactId>logback-classic</artifactId>
            <version>1.2.3</version>
            <scope>runtime</scope>
        </dependency>
        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter-engine</artifactId>
            <version>5.5.2</version>
            <scope>test</scope>
        </dependency>
    </dependencies>
</project>
```

注意到parent的`<packaging>`是`pom`而不是`jar`，因为`parent`本身不含任何Java代码。编写`parent`的`pom.xml`只是为了在各个模块中减少重复的配置。现在我们的整个工程结构如下：
```
multiple-project
├── pom.xml
├── parent
│   └── pom.xml
├── module-a
│   ├── pom.xml
│   └── src
├── module-b
│   ├── pom.xml
│   └── src
└── module-c
    ├── pom.xml
    └── src
```
这样模块A就可以简化为：

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>com.itranswarp.learnjava</groupId>
        <artifactId>parent</artifactId>
        <version>1.0</version>
        <relativePath>../parent/pom.xml</relativePath>
    </parent>

    <artifactId>module-a</artifactId>
    <packaging>jar</packaging>
    <name>module-a</name>
</project>
```

如果模块A依赖模块B，则模块A需要模块B的jar包才能正常编译，我们需要在模块A中引入模块B：

```xml
    ...
    <dependencies>
        <dependency>
            <groupId>com.itranswarp.learnjava</groupId>
            <artifactId>module-b</artifactId>
            <version>1.0</version>
        </dependency>
    </dependencies>
```

最后，在编译的时候，需要在根目录创建一个`pom.xml`统一编译：

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/maven-v4_0_0.xsd">

    <modelVersion>4.0.0</modelVersion>
    <groupId>com.itranswarp.learnjava</groupId>
    <artifactId>build</artifactId>
    <version>1.0</version>
    <packaging>pom</packaging>
    <name>build</name>

    <modules>
        <module>parent</module>
        <module>module-a</module>
        <module>module-b</module>
        <module>module-c</module>
    </modules>
</project>
```

这样，在根目录执行`mvn clean package`时，Maven根据根目录的`pom.xml`找到包括`parent`在内的共4个`<module>`，一次性全部编译。

### 仓库分类
- 中央仓库
	我们使用commons logging、log4j这些第三方模块，就是第三方模块的开发者自己把编译好的jar包发布到Maven的中央仓库中。
- 私有仓库
	私有仓库总是在公司内部使用，它只需要在本地的`~/.m2/settings.xml`中配置好，使用方式和中央仓位没有任何区别。
- 本地仓库

本地仓库是指把本地开发的项目“发布”在本地，这样其他项目可以通过本地仓库引用它。但是我们不推荐把自己的模块安装到Maven的本地仓库，因为每次修改某个模块的源码，都需要重新安装，非常容易出现版本不一致的情况。更好的方法是使用模块化编译，在编译的时候，告诉Maven几个模块之间存在依赖关系，需要一块编译，Maven就会自动按依赖顺序编译这些模块。

## 6. 使用mvnw
- 使用maven，基本上只会用到`mvn`，`mvnw`是Maven Wrapper的缩写，安装maven时，系统所有项目默认使用全局安装的maven版本，但是对于有些项目来说，可能必须使用某个特定的Maven版本，MavenWrapper负责给这个特定的项目安装特定版本的Maven，其他项目不受影响
### 安装Maven Wrapper
- 在项目的根目录（`pom.xml`所在的目录）运行安装命令：`mvn wrapper:wrapper`
	- 会自动使用最新版本的Maven，如果要指定使用的Maven版本，使用下面的方式，例如`3.9.0`：
	- `mvn wrapper:wrapper -Dmaven=3.9.0`
- 项目结构
```
my-project
├── .mvn
│   └── wrapper
│       └── maven-wrapper.properties
├── mvnw
├── mvnw.cmd
├── pom.xml
└── src
    ├── main
    │   ├── java
    │   └── resources
    └── test
        ├── java
        └── resources
```
- 只要将mvn命令改成mvnw就可以使用跟项目关联的Maven，例如`mvnw clean package`
	- linux或macOS上运行时需要加上`./`
	- `./mvn clean package`
- 作用2：将项目的`mvnw`、`mvnw.cmd`、`.mvn`提交到版本库中，可以使所有的开发人员使用统一的Maven版本

## 7. 发布Artifact
- 当我们使用`commons-logging`这些第三方库的时候是通过Maven自动下载它的jar包，并根据其pom.xml解析依赖，自动将相关依赖包都下载后加入classpath
- 如果我们自己写了一个开源库，将其放到Maven的repo中，别人只需要按标准引用`groupId:artifactId:version`，即可自动下载jar包及相关依赖
### 以静态文件发布
如果我们观察一个中央仓库的Artifact结构，例如Commons Math，它的groupId是`org.apche,commons`，artifactId是`commons-math3`，以版本`3.6.1`为例，发布在中央仓库的文件路径就是[https://repo1.maven.org/maven2/org/apache/commons/commons-math3/3.6.1/](https://repo1.maven.org/maven2/org/apache/commons/commons-math3/3.6.1/)，在这个文件夹下，`commons-math3-3.6.1.jar`就是发布的jar包，`commons-math-3.6.1.pom`就是它的`pom.xml`描述文件，`commons-math3-3.6.1-sources.jar`是源代码，`commons-math3-3.6.1-javadoc.jar`是文档。其他：`.asc`、`.md5`、`.sha1`分别是GPG签名，MD5摘要和SHA-1摘要
只要按照这种目录结构组织文件，它就是一个有效的Maven仓库，以how-to-bocome-rich为例
1. 创建Maven工程目录结构
```
how-to-become-rich
├── maven-repo        <-- Maven本地文件仓库
├── pom.xml           <-- 项目文件
├── src
│   ├── main
│   │   ├── java      <-- 源码目录
│   │   └── resources <-- 资源目录
│   └── test
│       ├── java      <-- 测试源码目录
│       └── resources <-- 测试资源目录
└── target            <-- 编译输出目录
```
2. 在`pom.xml`添加：
```xml
<project ...>
    ...
    <distributionManagement>
        <repository>
            <id>local-repo-release</id>
            <name>GitHub Release</name>
            <url>file://${project.basedir}/maven-repo</url>
        </repository>
    </distributionManagement>

    <build>
        <plugins>
            <plugin>
                <artifactId>maven-source-plugin</artifactId>
                <executions>
                    <execution>
                        <id>attach-sources</id>
                        <phase>package</phase>
                        <goals>
                            <goal>jar-no-fork</goal>
                        </goals>
                    </execution>
                </executions>
            </plugin>
            <plugin>
                <artifactId>maven-javadoc-plugin</artifactId>
                <executions>
                    <execution>
                        <id>attach-javadocs</id>
                        <phase>package</phase>
                        <goals>
                            <goal>jar</goal>
                        </goals>
                    </execution>
                </executions>
            </plugin>
        </plugins>
    </build>
</project>
```

[发布Artifact - Java教程 - 廖雪峰的官方网站](https://liaoxuefeng.com/books/java/maven/deploy/index.html)
