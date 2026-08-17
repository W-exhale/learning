## 一、文件路径 (File Path)

### 1. 基本概念

*   **文件 (File)**: 存储数据的基本单位。
*   **文件夹 (Folder/Directory)**: 用于组织文件和其他文件夹的容器。
*   **文件路径 (File Path)**: 描述文件或文件夹在文件系统中位置的字符串。

### 2. 路径类型

*   **绝对路径 (Absolute Path)**:
    *   从文件系统的**根目录**开始的完整路径。
    *   无论当前工作目录在哪里，绝对路径都能唯一地指向一个文件或文件夹。
    *   **示例 (Windows)**: `D:\Develop\Project\Backend`
    *   **示例 (Unix/Linux/macOS)**: `/home/user/documents`
    *   **比喻**: 非常详细的地址（例如：“中国北京市海淀区中关村大街1号XX大厦10层101室”），无论你身在何处，都能根据这个地址找到唯一的位置。

*   **相对路径 (Relative Path)**:
    *   相对于**当前工作目录** (Current Working Directory) 或某个基准路径的路径。
    *   路径不从根目录开始。
    *   **示例**:
        *   如果当前目录是 `D:\Develop\Project\`，那么 `Backend` 就是一个相对路径，指向 `D:\Develop\Project\Backend`。
        *   如果当前目录是 `/home/user/`，那么 `documents/report.txt` 就是一个相对路径，指向 `/home/user/documents/report.txt`。
    *   **比喻**: 部分地址（例如：“中关村大街1号XX大厦10层101室”），你需要知道你当前所在的城市和区域（即当前工作目录），才能确定这个地址的具体位置。

## 二、Java `File` 类 (`java.io.File`)

`java.io.File` 类是 Java I/O API 中代表文件或目录路径名的抽象表示。它提供了操作文件和目录（如创建、删除、重命名、查询属性等）的方法，但**不包含**读写文件内容的方法。
### 1. 路径表示
*   在 Java 代码中，路径通常使用**字符串 (String)** 来表示。
*   **路径分隔符**:
    *   **Unix/Linux/macOS**: 使用正斜杠 `/` 作为路径分隔符。
    *   **Windows**: 使用反斜杠 `\` 作为路径分隔符。
    *   **注意**: 在 Java 字符串字面量中，反斜杠 `\` 是一个**转义字符**。因此，要表示一个实际的 Windows 路径分隔符 `\`，需要写成 `\\`。例如，Windows 路径 `D:\Develop` 在 Java 字符串中应写作 `"D:\\Develop"`。
    *   **跨平台建议**: 为了编写平台无关的代码，推荐使用 `File.separator` 静态常量，它会根据当前操作系统返回正确的路径分隔符 (`/` 或 `\`)。

### 2. 路径名的组成 (根据官方文档)

`File` 类将路径名视为由可选的**前缀 (prefix)** 和零个或多个**名称 (name)** 组成的序列。

> 1.  An optional system-dependent _prefix_ string, such as a disk-drive specifier, `/` for the UNIX root directory, or `\\` for a Microsoft Windows UNC pathname.
>     *(译: 一个可选的、与系统相关的前缀字符串，例如磁盘驱动器标识符（如 `C:`）、UNIX 根目录 `/` 或 Microsoft Windows UNC 路径名 `\\`。)*

*   **对于 UNIX 平台**:
    *   绝对路径名的前缀总是 `/`。
    *   相对路径名没有前缀。
    *   表示根目录的抽象路径名具有前缀 `/` 和一个空的名称序列。

*   **对于 Microsoft Windows 平台**:
    *   包含驱动器说明符（如 `C:`）的路径名，其前缀由驱动器号后跟 `:` 组成。如果该路径是绝对路径，则后面可能还会跟一个 `\`（例如 `C:\`）。
    *   UNC 路径名（网络共享路径）的前缀是 `\\`。主机名和共享名是名称序列中的前两个名称（例如 `\\hostname\sharename\file`）。
    *   未指定驱动器的相对路径名没有前缀。

## 三、`File` 类的常用方法

`File` 类提供了许多用于操作文件和目录的方法。以下是一些常用的方法：
#### 1. `list()`
*   **签名**: `public String[] list()`
*   **作用**: 返回一个**字符串数组 (String[])**，其中包含此 `File` 对象所表示的**目录**中的所有文件和子目录的**名称**。
*   **前提**:
    *   调用此方法的 `File` 对象必须代表一个**存在的目录**。
    *   程序需要有读取该目录的权限。
*   **返回值**：
    *   如果成功，返回包含目录内容的字符串数组。数组中的每个字符串仅是文件名或子目录名，不包含路径信息。
    *   如果此 `File` 对象不表示一个目录，或者目录不存在，或者发生 I/O 错误，则返回 `null`。
*   **示例**：
    ```java
    File dir = new File("C:\\Users\\Public\\Documents"); // 注意 Windows 路径需要转义 \
    if (dir.isDirectory()) {
        String[] entries = dir.list();
        if (entries != null) {
            System.out.println("目录内容:");
            for (String entry : entries) {
                System.out.println(entry);
            }
        } else {
            System.out.println("无法读取目录内容或目录为空。");
        }
    } else {
        System.out.println("指定的路径不是一个目录或不存在。");
    }
    ```
*   **截图说明**:
    ![[Pasted image 20241118211105.png]]
    (这张截图展示了 `list()` 方法的文档或使用示例，说明了其基本功能。)
