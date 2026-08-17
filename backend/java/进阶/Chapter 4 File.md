## Part 1 文件路径类型
1. 文件 文件夹 文件路径
2. 相对路径，绝对路径
	1. 绝对路径(Absolute Path)：D:\Develop\Project\Backend(win11)；非常详细的地址（C国A市b区小区名xx号），不管在哪都可以确定去这个地方的路径
	2. 相对路径(Relative Path)：另一个地方（C区小区名xx号），可以看到C区前面的都没有了，那是相对于上面的路径的路径，只有一部分，要知道了上面的路径才能知道这个的完整路径

## Part 2 Java `File` 类 (`java.io.File`)
- `java.io.File` 类是 Java I/O API 中代表文件或目录路径名的抽象表示。它提供了操作文件和目录（如创建、删除、重命名、查询属性等）的方法，但**不包含**读写文件内容的方法。

*   **路径分隔符**:
    *   **Unix/Linux/macOS**: 使用正斜杠 `/` 作为路径分隔符。
    *   **Windows**: 使用反斜杠 `\` 作为路径分隔符。
    *   **注意**: 在 Java 字符串字面量中，反斜杠 `\` 是一个**转义字符**。因此，要表示一个实际的 Windows 路径分隔符 `\`，需要写成 `\\`。例如，Windows 路径 `D:\Develop` 在 Java 字符串中应写作 `"D:\\Develop"`。
    *   **跨平台建议**: 为了编写平台无关的代码，推荐使用 `File.separator` 静态常量，它会根据当前操作系统返回正确的路径分隔符 (`/` 或 `\`)。

## Part 3 File 类的常用方法

`File` 类提供了许多用于操作文件和目录的方法。以下是一些常用的方法：

- `list()`
*   **签名**: `public String[] list()`
*   **作用**: 返回一个**字符串数组 (String[])**，其中包含此 `File` 对象所表示的**目录**中的所有文件和子目录的**名称**。
*   **前提**:
    *   调用此方法的 `File` 对象必须代表一个**存在的目录**。
    *   程序需要有读取该目录的权限。
*   **返回值**:
    *   如果成功，返回包含目录内容的字符串数组。数组中的每个字符串仅是文件名或子目录名，不包含路径信息。
    *   如果此 `File` 对象不表示一个目录，或者目录不存在，或者发生 I/O 错误，则返回 `null`。
*   **示例**:
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
