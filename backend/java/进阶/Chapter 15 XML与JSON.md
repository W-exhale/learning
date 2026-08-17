## XML
> XML (eXtensible Markup Language) 即可扩展标记语言，是一种用于表示和传输数据的标记语言格式。它可以描述非常复杂的数据结构，常用于配置文件、数据交换和存储。

**示例：**
一个描述书籍的XML文档可能如下：
```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE note SYSTEM "book.dtd">
<book id="1">
    <name>Java核心技术</name>
    <author>Cay S. Horstmann</author>
    <isbn lang="CN">1234567</isbn>
    <tags>
        <tag>Java</tag>
        <tag>Network</tag>
    </tags>
    <pubDate/>
</book>
```

**特点：**
*   **纯文本**：默认使用 `UTF-8` 编码。
*   **可嵌套**：适合表示结构化数据。
*   **数据传输**：XML内容经常通过网络作为消息传输。

### XML结构

1.  **声明行**：首行通常是 `<?xml version="1.0" encoding="UTF-8"?>`，声明XML版本和编码（编码可选）。
2.  **DTD (可选)**：类似 `<!DOCTYPE note SYSTEM "book.dtd">` 的声明是文档类型定义（Document Type Definition），用于验证XML结构，是可选的。
3.  **文档内容**：
    *   一个XML文档有且仅有一个**根元素**。
    *   根元素可以包含任意数量的子元素。
    *   元素可以包含**属性**（例如 `<isbn lang="CN">` 中的 `lang="CN"`）。
    *   元素必须**正确嵌套**。
4. 如果是空元素，可以用`<tag/>`表示。
5.  **特殊字符转义**：由于 `<`, `>`, `&`, `"`, `'` 等字符在XML中有特殊含义，内容中出现时需要转义。例如，`Java<tm>`必须写成：
	```xml
	<name>Java&lt;tm&gt;</name>
	```

| 字符  | 转义表示     |
| --- | -------- |
| <   | `&lt;`   |
| >   | `&gt;`   |
| &   | `&amp;`  |
| "   | `&quot;` |
| '   | `&apos;` |

>[!info] 格式正确 (Well-Formed) vs 合法 (Valid)
>*   **格式正确 (Well-Formed)**：指XML语法正确，可以被解析器正常读取。
>*   **合法 (Valid)**：指XML不仅格式正确，而且其结构和数据符合DTD或XSD（XML Schema Definition）的规定。

**验证**：验证XML文件正确性最简单的方式是将其拖拽到现代浏览器窗口中，格式错误会报错。

>[!warning] XML vs HTML
>与结构类似的HTML不同，浏览器对HTML有一定的“容错性”（例如，缺少关闭标签有时也能解析），但XML要求严格的格式，任何不正确的嵌套都会导致解析错误。

DTD文档可以指定一系列规则，例如：
- 根元素必须是`book`
- `book`元素必须包含`name`，`author`等指定元素
- `isbn`元素必须包含属性`lang`
- ...

**XML 技术体系，** 除了XML文档本身，XML还包括：
*   **DTD 和 XSD**：验证XML结构和数据。
*   **Namespace**：避免元素和属性名称冲突。
*   **XSLT**：将XML转换为其他文本格式（如HTML）。
*   **XPath**：查询XML节点和属性的语言。

>实际应用中，这些相关技术（尤其是DTD/XSD/XSLT）实现复杂，可能不如直接使用更现代的数据格式（如JSON）和库方便。

## 使用DOM解析XML

XML是一种树形结构的文档，它有两种标准的解析API：
- DOM：一次性读取XML，并在内存中表示为树形结构；
- SAX：以流的形式读取XML，使用事件回调。

> **DOM (Document Object Model)** 是一种XML解析API。它将整个XML文档一次性读入内存，并构建一个树形结构来表示文档内容。

- 如何使用DOM来读取XML。
DOM是Document Object Model的缩写，DOM模型就是把XML结构作为一个树形结构处理，从根节点开始，每个节点都可以包含任意个子节点。

我们以下面的XML为例：

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<book id="1">
    <name>Java核心技术</name>
    <author>Cay S. Horstmann</author>
    <isbn lang="CN">1234567</isbn>
    <tags>
        <tag>Java</tag>
        <tag>Network</tag>
    </tags>
    <pubDate/>
</book>
```
如果解析为DOM结构，它大概长这样：
```
                      ┌─────────┐
                      │document │
                      └─────────┘
                           │
                           ▼
                      ┌─────────┐
                      │  book   │
                      └─────────┘
                           │
     ┌──────────┬──────────┼──────────┬──────────┐
     ▼          ▼          ▼          ▼          ▼
┌─────────┐┌─────────┐┌─────────┐┌─────────┐┌─────────┐
│  name   ││ author  ││  isbn   ││  tags   ││ pubDate │
└─────────┘└─────────┘└─────────┘└─────────┘└─────────┘
                                      │
                                 ┌────┴────┐
                                 ▼         ▼
                             ┌───────┐ ┌───────┐
                             │  tag  │ │  tag  │
                             └───────┘ └───────┘
```

**Java DOM API 对象：**

*   `Document`：代表整个XML文档。
*   `Element`：代表一个XML元素（如 `<book>`, `<name>`）。
*   `Attribute`：代表元素的属性（如 `id="1"`）。
*   `Node`：所有节点的基接口（包括元素、属性、文本等）。


使用DOM API解析一个XML文档的代码如下：

```java
import javax.xml.parsers.*;
import org.w3c.dom.*;
import java.io.*;

// ...

InputStream input = Main.class.getResourceAsStream("/book.xml");
DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
DocumentBuilder db = dbf.newDocumentBuilder();
Document doc = db.parse(input); // 解析XML，可以接收InputStream，File或者URL,返回Document对象，代表了整个XML文档的树形结构

// 遍历DOM树 (示例)
printNode(doc.getDocumentElement(), 0); // 从根元素开始遍历
```

**遍历并打印节点信息 (示例方法)：**
```java
void printNode(Node n, int indent) {
    for (int i = 0; i < indent; i++) {
        System.out.print(' ');
    }
    switch (n.getNodeType()) {
    case Node.DOCUMENT_NODE: // Document节点
        System.out.println("Document: " + n.getNodeName());
        break;
    case Node.ELEMENT_NODE: // 元素节点
        System.out.println("Element: " + n.getNodeName());
        // 可以通过 n.getAttributes() 获取属性
        break;
    case Node.TEXT_NODE: // 文本
    // 注意：元素间的空白和换行也会被解析为Text节点
        String text = n.getNodeValue().trim();
            if (!text.isEmpty()) {
	            System.out.println("Text: " + text);
	        }
        break;
    case Node.ATTRIBUTE_NODE: // 属性, 通常通过Element节点访问
        System.out.println("Attr: " + n.getNodeName() + " = " + n.getNodeValue());
        break;
    default: // 其他
        System.out.println("NodeType: " + n.getNodeType() + ", NodeName: " + n.getNodeName());
    }
    // 递归遍历子节点
    NodeList children = n.getChildNodes();
    for (int i = 0; i < children.getLength(); i++) {
        printNode(children.item(i), indent + 1);
    }
}
```

解析结构如下：

```plain
Document: #document
 Element: book
  Text: #text = 
    
  Element: name
   Text: #text = Java核心技术
  Text: #text = 
    
  Element: author
   Text: #text = Cay S. Horstmann
  Text: #text = 
  ...
```

对于DOM API解析出来的结构，我们从根节点Document出发，可以遍历所有子节点，获取所有元素、属性、文本数据，还可以包括注释，这些节点被统称为Node，每个Node都有自己的Type，根据Type来区分一个Node到底是元素，还是属性，还是文本，等等。

>[!summary] DOM 优缺点
>*   **优点**：将整个文档加载到内存中，方便随机访问和修改任何节点。
>*   **缺点**：对于非常大的XML文件，内存消耗巨大。API相对繁琐，获取元素文本需要访问其Text子节点。


## 使用SAX解析XML

> **SAX (Simple API for XML)** 是另一种XML解析API。它采用**流式处理**方式，边读取XML边解析，以事件回调的方式让调用者获取数据不需要将整个文档加载到内存。


**SAX 工作方式：**
SAX解析器在读取XML文档时，会按顺序触发一系列事件，你需要提供一个处理器（Handler）来响应这些事件：

*   `startDocument()`: 文档开始。
*   `endDocument()`: 文档结束。
*   `startElement()`: 遇到元素开始标签（如 `<book>`）。
*   `endElement()`: 遇到元素结束标签（如 `</book>`）。
*   `characters()`: 遇到元素内的文本内容。


如果我们用SAX API解析XML，Java代码如下：

```java
import javax.xml.parsers.*;
import org.xml.sax.*;
import org.xml.sax.helpers.DefaultHandler;
import java.io.*;

// ...

InputStream input = Main.class.getResourceAsStream("/book.xml");
SAXParserFactory spf = SAXParserFactory.newInstance();
SAXParser saxParser = spf.newSAXParser();
MyHandler handler = new MyHandler(); // 创建自定义处理器
saxParser.parse(input, handler); // 开始解析
```

**自定义 Handler (继承 `DefaultHandler`)（传入`SAXParser.parse()`的回调对象）：**
```java
class MyHandler extends DefaultHandler {
    // 可以定义状态变量来跟踪当前解析位置
    private String currentElement;
    private StringBuilder currentText;

    @Override
    public void startDocument() throws SAXException {
        System.out.println("SAX Event: start document");
        currentText = new StringBuilder();
    }

    @Override
    public void endDocument() throws SAXException {
        System.out.println("SAX Event: end document");
    }

    @Override
    public void startElement(String uri, String localName, String qName, Attributes attributes) throws SAXException {
        System.out.println("SAX Event: start element - " + qName);
        currentElement = qName;
        currentText.setLength(0); // 清空文本缓冲区
        // 可以通过 attributes.getValue("attrName") 获取属性
        if ("isbn".equals(qName)) {
            System.out.println("  Attribute lang=" + attributes.getValue("lang"));
        }
    }

    @Override
    public void endElement(String uri, String localName, String qName) throws SAXException {
    
        print("end element:", localName, qName);
        
	System.out.println("SAX Event: end element - " + qName);
        // 在元素结束时处理收集到的文本
        if ("name".equals(qName)) {
            System.out.println("  Book Name: " + currentText.toString());
        } else if ("author".equals(qName)) {
            System.out.println("  Author: " + currentText.toString());
        }
        currentElement = null; // 清除当前元素标记
    }

    @Override
    public void characters(char[] ch, int start, int length) throws SAXException {
		// 注意：这个方法可能被多次调用来处理一个文本块
        // 也可能包含元素间的空白字符
        String text = new String(ch, start, length).trim();
        if (currentElement != null && !text.isEmpty()) {
             System.out.println("SAX Event: characters - " + text);
             currentText.append(text); // 累积文本
        }
    }

    @Override
    public void error(SAXParseException e) throws SAXException {
        System.err.println("SAX Parsing Error: " + e.getMessage());
    }

}
```

运行SAX解析代码，可以打印出下面的结果：

```plain
start document
start element:  book
characters:
     
start element:  name
characters: Java核心技术
end element:  name
characters:
     
start element:  author
...
```

1. 如果要读取`<name>`节点的文本，我们就必须在解析过程中根据`startElement()`和`endElement()`定位当前正在读取的节点，
2. 可以使用栈结构保存，每遇到一个`startElement()`入栈，每遇到一个`endElement()`出栈，
3. 读到`characters()`时我们才知道当前读取的文本是哪个节点的。可见，使用SAX API仍然比较麻烦。

>[!summary] SAX 优缺点
>*   **优点**：内存占用小，适合处理大型XML文件。解析速度通常比DOM快。
>*   **缺点**：基于事件，编程模型相对复杂，无法随机访问文档内容，需要自己维护状态来理解上下文（例如，当前在哪个元素内）。

## 使用Jackson
> 无论是DOM还是SAX，直接使用Java标准API都比较繁琐。**Jackson** 是一个流行的第三方库，可以方便地将XML（以及JSON）数据直接映射到Java对象（POJO / JavaBean）。


观察XML文档的结构：

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<book id="1">
    <name>Java核心技术</name>
    <author>Cay S. Horstmann</author>
    <isbn lang="CN">1234567</isbn>
    <tags>
        <tag>Java</tag>
        <tag>Network</tag>
    </tags>
    <pubDate/>
</book>
```

我们发现，它完全可以对应到一个定义好的JavaBean中：

```java
public class Book {
    public long id;
    public String name;
    public String author;
    public String isbn;
    public List<String> tags;
    public String pubDate;
}
```

**Maven 依赖：**
```xml
<dependency>
    <groupId>com.fasterxml.jackson.dataformat</groupId>
    <artifactId>jackson-dataformat-xml</artifactId>
    <version>2.13.0</version> <!-- 使用较新版本 -->
</dependency>
```



然后，定义好JavaBean，就可以用下面几行代码解析：

```java
import com.fasterxml.jackson.dataformat.xml.XmlMapper;
import java.io.InputStream;

// ...

InputStream input = Main.class.getResourceAsStream("/book.xml");
XmlMapper xmlMapper = new XmlMapper(); // 创建 XmlMapper,这种写法没有特殊配置
//JacksonXmlModule module = new JacksonXmlModule(); //可以对 JacksonXmlModule进行特别配置
//XmlMapper mapper = new XmlMapper(module);
Book book = xmlMapper.readValue(input, Book.class); // 直接反序列化为 Book 对象，读取XML并返回一个JavaBean

System.out.println("ID: " + book.id);
System.out.println("Name: " + book.name);
System.out.println("Author: " + book.author);
System.out.println("ISBN Value: " + book.isbnValue);
System.out.println("Tags: " + book.tags);
System.out.println("PubDate: " + book.pubDate);
```
**输出：**
```plain
ID: 1
Name: Java核心技术
Author: Cay S. Horstmann
ISBN Value: 1234567
Tags: [Java, Network]
PubDate: null
```

>[!tip] Jackson 的优势
>- 使用Jackson这类库可以大大简化XML与Java对象之间的转换，代码更简洁，可读性更高。
>- 它也支持将Java对象序列化回XML字符串。对于复杂的映射，可以查阅 [Jackson XML 文档](https://github.com/FasterXML/jackson-dataformat-xml)。
>- 如果要解析的数据格式不是Jackson内置的标准格式，那么需要编写一点额外的扩展来告诉Jackson如何自定义解析。

## 使用JSON
> **JSON (JavaScript Object Notation)** 是一种轻量级的数据交换格式，源于JavaScript的对象字面量语法，但独立于语言。由于其简洁性和易于解析，已成为Web API（尤其是RESTful API）事实上的标准数据格式。

一个典型的JSON如下：
```json
{
    "id": 1,
    "name": "Java核心技术",
    "author": {
        "firstName": "Cay S.",
        "lastName": "Horstmann"
    },
    "isbn": "123-4567",
    "tags": ["Java", "Network"],
    "published": true,
    "price": 99.90,
    "notes": null
}
```

JSON作为数据传输的格式，有几个显著的优点：

*   **简洁**：相比XML，没有冗余的标签，可读性好。
*   **易于解析**：格式简单，机器和人都容易读写。
	* JSON只允许使用双引号作为key，特殊字符用`\`转义，格式简单；
*   **UTF-8 编码**：通常只使用UTF-8编码，避免了编码混乱问题。
*   **Web 友好**：JavaScript原生支持JSON解析和序列化。(如果把数据用JSON发送给浏览器，可以用JavaScript直接处理。)
*   **数据类型有限但够用**：
    *   对象（键值对）：`{ "key": value, ... }` (Key必须是双引号字符串)
    *   数组：`[ value1, value2, ... ]`
    *   字符串：`"text"` (使用双引号)
    *   数值：整数或浮点数 (如 `100`, `3.14`)
    *   布尔值：`true` 或 `false`
    *   空值：`null`

浏览器直接支持使用JavaScript对JSON进行读写：

```javascript
// JSON 字符串 -> JavaScript 对象 (解析/反序列化)
let jsonString = '{"name": "Alice", "age": 30}';
let jsObject = JSON.parse(jsonString);
console.log(jsObject.name); // 输出: Alice

// JavaScript 对象 -> JSON 字符串 (序列化)
let person = { name: "Bob", city: "New York" };
let jsonOutput = JSON.stringify(person);
console.log(jsonOutput); // 输出: {"name":"Bob","city":"New York"}
```

>[!note] JSON 与 REST API
由于JSON的简洁性和浏览器原生支持，绝大多数现代Web服务（特别是REST API）都选择JSON作为数据传输格式。


## 使用 Jackson 处理 JSON
- 对JSON进行读写
> 同样，**Jackson** 也是处理JSON的主流Java库，提供了强大的JSON与Java对象之间的映射功能。

**Maven 依赖 (核心库)：**
```xml
<dependency>
    <groupId>com.fasterxml.jackson.core</groupId>
    <artifactId>jackson-databind</artifactId>
    <version>2.13.0</version> <!-- 使用较新版本 -->
</dependency>
```
*(如果项目中已包含 `jackson-dataformat-xml`，通常它会传递依赖 `jackson-databind`)*

在Java中，针对JSON也有标准的JSR 353 API，但还是JSON和JavaBean之间转换是最方便的。

**Java Jackson JSON 解析 (反序列化) 示例：**
假设有 `book.json` 文件和对应的 `Book` 类 (可能需要调整以匹配JSON结构)。
```java
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.DeserializationFeature;
import java.io.InputStream;

// 假设 Book 类定义如下 (匹配上面的JSON示例)
public class Book {
    public long id;
    public String name;
    public Author author; // 嵌套对象
    public String isbn;
    public List<String> tags; // 数组
    public boolean published;
    public double price;
    public String notes; // 可以为 null

    // Jackson 需要一个无参构造函数用于反序列化
    public Book() {}

    // 嵌套类也需要定义
    public static class Author {
        public String firstName;
        public String lastName;
        public Author() {}
    }
}

// --- 解析代码 ---
InputStream input = Main.class.getResourceAsStream("/book.json");
ObjectMapper objectMapper = new ObjectMapper();

// 配置：忽略JSON中有但Java类中没有的属性，防止报错
objectMapper.configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);

Book book = objectMapper.readValue(input, Book.class); // 反序列化（把JSON解析为JavaBean的过程）

System.out.println("Book Name: " + book.name);
System.out.println("Author: " + book.author.firstName + " " + book.author.lastName);
System.out.println("Tags: " + book.tags);
```

**Java Jackson JSON 生成 (序列化) 示例：**
```java
ObjectMapper objectMapper = new ObjectMapper();
Book myBook = new Book(); // ... 填充 myBook 的数据 ...

// 将 Java 对象序列化为 JSON 字符串（关键）
String jsonString = objectMapper.writeValueAsString(myBook);
System.out.println(jsonString);

// 也可以格式化输出 (带缩进)
// String prettyJson = objectMapper.writerWithDefaultPrettyPrinter().writeValueAsString(myBook);
// System.out.println(prettyJson);
```

### 高级特性与定制

**处理日期/时间类型 (如 `LocalDate`)**
如果JSON中有日期字符串 `{"pubDate": "2016-09-01"}`，需要映射到 `java.time.LocalDate`。

1.  **添加依赖：**
    ```xml
    <dependency>
        <groupId>com.fasterxml.jackson.datatype</groupId>
        <artifactId>jackson-datatype-jsr310</artifactId>
        <version>2.13.0</version>
    </dependency>
    ```
2.  **注册模块：**
    ```java
    ObjectMapper objectMapper = new ObjectMapper();
    objectMapper.registerModule(new JavaTimeModule()); // 注册 Java 8 时间模块
    // objectMapper.configure(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS, false); // 可选：序列化为字符串而非时间戳

    // 现在可以正常解析/序列化包含 LocalDate, LocalDateTime 等的类
    ```

#### 自定义序列化/反序列化
当JSON格式与Java类型不直接匹配时（如带连字符的ISBN `978-7-111-54742-6` 需要映射到 `BigInteger`），可以自定义处理器。（将图书号转化为一个没有连字符的数）
假设json文件内容为：
```
{
    "name": "Effective Java",
    "isbn": "978-0-13-468599-1"
}
```
要解析为下面的Book类

1.  **创建 Deserializer:**
    ```java
    import com.fasterxml.jackson.core.*;
    import com.fasterxml.jackson.databind.*;
    import java.io.IOException;
    import java.math.BigInteger;

    public class IsbnDeserializer extends JsonDeserializer<BigInteger> {
        @Override
        public BigInteger deserialize(JsonParser p, DeserializationContext ctxt) throws IOException, JsonProcessingException {
            String s = p.getValueAsString(); // JSON数据中获取字段值（字符串形式）
            if (s != null) {
                try {
                    // 移除连字符并转换为 BigInteger
                    return new BigInteger(s.replace("-", ""));
                } catch (NumberFormatException e) {
                    // 如果格式错误，抛出异常
                    throw new JsonParseException(p, "Invalid ISBN format: " + s, e);
                }
            }
            return null;  // 如果字段值为null，返回null
        }
    }
    ```
2.  **在 JavaBean 字段上使用注解：**
	1. Jackson的`@JsonDeserialize`注解允许为某个字段指定一个自定义的反序列化器
    ```java
    import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
    import java.math.BigInteger;

    public class Book {
        public String name;

        @JsonDeserialize(using = IsbnDeserializer.class) // 告诉Jackson，isbn字段的反序列化由isbnDeserializer
        public BigInteger isbn;

        // ... 其他字段和构造函数 ...
    }
    ```
3.  **自定义 Serializer (类似)：** 创建继承 `JsonSerializer<T>` 的类，并使用 `@JsonSerialize(using = ...)` 注解。

#### 常规使用
```json
{
    "name": "Java核心技术",
    "pubDate": "2016-09-01"
}
```

要解析为：

```java
public class Book {
    public String name;
    public LocalDate pubDate;
}
```

然后，在创建`ObjectMapper`时，注册一个新的`JavaTimeModule`：

```java
ObjectMapper mapper = new ObjectMapper().registerModule(new JavaTimeModule());
```

### 反序列化
>[!warning] 无参构造方法
>- Jackson在反序列化时，默认需要目标Java类有一个**公共的无参构造方法**来实例化对象。
>- 如果只有带参数的构造方法，可能会导致反序列化失败，除非使用特殊注解（如 `@JsonCreator` 和 `@JsonProperty`）来指定如何使用带参构造函数。


**处理 `enum` 类型**
Jackson默认将Java `enum` 序列化为其名称（`enum.name()`），反序列化时也根据名称匹配。
```java
// Java
public enum Status { PUBLISHED, DRAFT }
public class Book { public Status status = Status.PUBLISHED; }

// JSON
{ "status": "PUBLISHED" }
```

**处理 `record` 类型 (Java 14+)**
Jackson 2.12.0 及以上版本原生支持Java `record` 类型。它会自动识别 `record` 的主构造函数及其参数名，用于序列化和反序列化，无需显式添加注解或无参构造函数。
```java
// Java Record
public record Point(int x, int y) {}

// JSON
{ "x": 10, "y": 20 }

// Jackson 可以直接序列化/反序列化 Point record
```