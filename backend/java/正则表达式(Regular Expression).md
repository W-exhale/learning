## 初级

| 符号      | 说明                        | 示例 (匹配)                        |
| :------ | :------------------------ | :----------------------------- |
| `.`     | 匹配任意**一个**字符 (除换行符外)      | `a.c` -> "abc", "a_c"          |
| `\d`    | 匹配一个数字 (等价于 `[0-9]`)      | `\d\d` -> "12", "99"           |
| `\w`    | 匹配一个字母、数字或下划线             | `\w\w\w` -> "abc", "a_1"       |
| `\s`    | 匹配一个空白字符 (空格, tab, 换行等)   | `a\sb` -> "a b"                |
| `\D`    | 匹配一个**非**数字字符             | `\D` -> "a", "_"               |
| `\W`    | 匹配一个**非**字母、数字、下划线字符      | `\W` -> "+", " "               |
| `\S`    | 匹配一个**非**空白字符             | `\S` -> "a", "1"               |
| `*`     | 匹配前面的元素 0 次或多次（设定0个及以上字符） | `go*d` -> "gd", "good"         |
| `+`     | 匹配前面的元素 1 次或多次            | `go+d` -> "god", "good"        |
| `?`     | 匹配前面的元素 0 次或 1 次          | `colou?r` -> "color", "colour" |
| `{n}`   | 精确匹配前面的元素 n 次             | `A\d{3}` -> "A380"             |
| `{n,}`  | 匹配前面的元素至少 n 次             | `\d{2,}` -> "12", "123"        |
| `{n,m}` | 匹配前面的元素 n 到 m 次           | `\d{2,4}` -> "12", "1234"      |
- 使用：
```java
String re = "java|php";
System.out.println("java".matches(re));
```
使用的String.matches(String s)

## 进阶语法与分组
### 行首与行尾
-   `^`：匹配输入的**开头**。例如 `^A` 匹配以 "A" 开头的字符串。
-   `$`：匹配输入的**结尾**。例如 `z$` 匹配以 "z" 结尾的字符串。
### 字符集 `[]`
- `[]`：匹配方括号内的**任意一个**字符。
	- 规定一个7-9位数字的电话号码不能以0开头，`[123456789]\d[6,8]`，或`[1-9]\d{6,8}`
	- 匹配6位十六进制数：`[0-9a-fA-F]{6}`（去掉`{6}`匹配一个一个十六进制字符）
- `[^...]`：排除法，例如`[^1-9]{3}`，不包含1-9的任意3个字符

### 选择 `|`
- `|`：或，
	- `AB|CD|EF`可以匹配AB或CD或EF
	- 使用括号：`learn\sjava|learn\sphp|learn\sgo`，可以使用`learn\s(java|php|go)`
### 分组 `()`
##### 普通分组
- 使用括号分组匹配：
	- 匹配完电话号码后进行提取，可以将要提取的部分用括号分组
	- `\d{3,4}\-\d{6,8}`：区号-电话号
	- `(\d{3,4})\-(\d{6,8})`，引入`java.util.regex`，
		- `Pattern.compile(regex)`：编译正则表达式字符串，创建`Pattern`对象
		-  `pattern.matcher(inputString)`：使用 `Pattern` 对象创建一个 `Matcher` 对象，用于在输入字符串中进行匹配。
		- `matcher.matches()`：尝试将**整个**输入字符串与模式进行匹配。如果匹配成功，返回 `true`
		- 如果匹配成功，就可以从`Matcher.group(index)`返回子串
```java
import java.util.regex.*;

public class Main{
	public static void main(String[] args){
		//编译正则表达式，包含两个捕获组
		Pattern p = Pattern.compile("(\\d{3,4})\\-(\\d{7,8})");	
		//创建Matcher对象
		Matcher m = p.matcher("010-123456789")
		if(m.matches()){
			//提取捕获组内容
			String g1 = m.group(1);
			String g2 = m.group(2);
			System.out.println(g1);//010
			System.out.println(g2);//123456789
		}else{
			System.out.println("匹配失败！");	
		}
	}
}
```
> [!INFO] 关于 `group(index)`
>- `matcher.group(0)` 或 `matcher.group()` 返回**整个**匹配到的字符串。

> [!TIP] `Pattern` 对象效率
>- 之前用的是`String.matches()`，这个方法内部其实调用的就是`Pattern`和`Matcher`类
>- 反复使用`String.matches()`对同一个正则表达式进行多次匹配效率比较低，每次都会创建一样的`Pattern`对象，
>- 所以我们可以先创建出一个`Pattern`对象，再调用`matcher`方法（该方法返回一个`Matcher`）即可，实现编译一次，多次匹配
>- 使用`Matcher`时，必须先调用`matches()`判断是否匹配成功，匹配成功后才能调用`group()`提取子串
```java
import java.util.regex.*;

public class Main {
    public static void main(String[] args) {
        Pattern pattern = Pattern.compile("(\\d{3,4})\\-(\\d{7,8})");
        pattern.matcher("010-12345678").matches(); // true
        pattern.matcher("021-123456").matches(); // false
        pattern.matcher("022#1234567").matches(); // false
        // 获得Matcher对象:
        Matcher matcher = pattern.matcher("010-12345678");
        if (matcher.matches()) {
            String whole = matcher.group(0); // "010-12345678", 0表示匹配的整个字符串
            String area = matcher.group(1); // "010", 1表示匹配的第1个子串
            String tel = matcher.group(2); // "12345678", 2表示匹配的第2个子串
            System.out.println(area);
            System.out.println(tel);
        }
    }
}
```

## 非贪婪匹配
### 贪婪匹配 (Greedy Matching)
- 正则表达式默认使用贪婪匹配
	- `(\d+)(0*)`匹配1230000，
	-  `\d+` 是贪婪的，它会匹配所有数字 `"1230000"`。
	- 导致`0*`只能匹配空字符串
	- 结果：`group(1)` 是 `"1230000"`，`group(2)` 是 `""`。

### 非贪婪匹配 (Non-Greedy Matching / Reluctant Matching)
- 如果要让`(\d+)(0*)`中的`\d+`尽量少匹配，`0*`尽量多匹配，就要使用非贪婪匹配，
- 在`\d+`后面加个`?`
	- 用 `(\d+?)(0*)` 匹配字符串 `"1230000"`。会匹配123
	*   `0*` (仍然是贪婪的) 匹配剩余的 `"0000"`。
	*   结果：`group(1)` 是 `"123"`，`group(2)` 是 `"0000"`。
我们改写正则表达式如下：
```java
import java.util.regex.*;

public class Main {
    public static void main(String[] args) {
        Pattern pattern = Pattern.compile("(\\d+?)(0*)");
        Matcher matcher = pattern.matcher("1230000");
        if (matcher.matches()) {
            System.out.println("group1=" + matcher.group(1)); // "123"
            System.out.println("group2=" + matcher.group(2)); // "0000"
        }
    }
}
```

> [!WARNING] 注意 `?` 的双重含义
> - `\d?`：这里的 `?` 是量词，表示匹配 0 个或 1 个数字。
> - `\d+?` 或 `\d*?` 或 `\d{n,m}?`：这里的 `?` 是跟在量词后面的，表示将前面的贪婪量词变为**非贪婪**模式。
> - `\d??`：第一个 `?` 是量词 (0 或 1 次)，第二个 `?` 表示非贪婪。这种组合通常匹配 0 次（因为非贪婪）。

## 搜索和替换
### 分割字符串 (Splitting Strings)
- `String.split(regex)`方法传入的就是正则表达式
```java
"a b c".split("\\s"); // { "a", "b", "c" }
"a b  c".split("\\s"); // { "a", "b", "", "c" }
// 按逗号、分号或空白字符中的一个或多个进行分割
"a, b ;; c".split("[\\,\\;\\s]+"); // { "a", "b", "c" }
```

### 搜索字符串 (Searching Strings)
-   `Matcher.find()` 方法在输入字符串中查找下一个匹配正则表达式的**子串**。
	- 只要有就会返回，第一次调用如果有就返回true，第二次调用如果有第二个也返回`true`...
	- 如果没有了就返回`false`

```
import java.util.regex.*;

public class Main {
    public static void main(String[] args) {
        String s = "the quick brown fox jumps over the lazy dog.";
        Pattern p = Pattern.compile("\\wo\\w");//定义正则表达式模式
        Matcher m = p.matcher(s);//创建匹配器
        while (m.find()) {//每次调用都会尝试查找下一个匹配的子串，找到返回true，否则返回false
            String sub = s.substring(m.start(), m.end());//start表示当前子串的起始索引，左闭右开
            System.out.println(sub);
        }
    }
}
```
```
row
fox
dog
```
### 替换字符串 (Replacing Strings)
-   `String.replaceAll(regex, replacement)`：将输入字符串中**所有**匹配 `regex` 的子串替换为 `replacement` 字符串。
-   `String.replaceFirst(regex, replacement)`：只替换**第一个**匹配 `regex` 的子串。
```java
// regex
public class Main {
    public static void main(String[] args) {
        String s = "The     quick\t\t brown   fox  jumps   over the  lazy dog.";
        String r = s.replaceAll("\\s+", " ");
        System.out.println(r); // "The quick brown fox jumps over the lazy dog."
    }
}
```

### 反向引用 (Backreferences)

```java
// regex
public class Main {
    public static void main(String[] args) {
        String s = "the quick brown fox jumps over the lazy dog.";
        String r = s.replaceAll("\\s([a-z]{4})\\s", " <b>$1</b> ");
        System.out.println(r);
        // 输出: the quick brown fox jumps over the <b>lazy</b> dog.
    }
}
```
- `$1`表示捕获组，replaceAll()方法的第一个参数是正则表达式或子串，符合该正则表达式的第一个字串为捕获组1（即`$1`），第二个为`$2`...
## String方法匹配
Java 的 `String` 类提供了一些便捷的方法来处理正则表达式：

-   **`matches(String regex)`**: 判断**整个**字符串是否匹配给定的正则表达式。
-   **`split(String regex)`**: 使用正则表达式作为分隔符来分割字符串，返回字符串数组。
-   **`split(String regex, int limit)`**: 带限制次数的分割。
-   **`replaceAll(String regex, String replacement)`**: 替换所有匹配正则表达式的子串。
-   **`replaceFirst(String regex, String replacement)`**: 替换第一个匹配正则表达式的子串。

**注意**：`String` 类中还有一些方法**不**使用正则表达式进行匹配或替换：

-   `equals(Object anObject)`: 精确的字符串内容比较。
-   `contains(CharSequence s)`: 判断是否包含指定的字符序列（字面量匹配）。
-   `indexOf(String str)` / `lastIndexOf(String str)`: 查找子串的索引（字面量匹配）。
-   `substring(int beginIndex, int endIndex)`: 提取子串（基于索引）。
-   `replace(CharSequence target, CharSequence replacement)`: 替换所有出现的**字面量** `target` 子串为 `replacement`。

`CharSequence` 是一个接口，常见实现包括：
- **`String`**：不可变的字符序列。
- **`StringBuilder` 和 `StringBuffer`**：可变的字符序列。
- **`CharBuffer`**：基于缓冲区的字符序列。
