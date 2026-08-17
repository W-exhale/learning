## Part 5 接收Email

> [!INFO] 邮件接收协议
> 与发送邮件使用 SMTP 不同，从邮件服务器 (MDA) 拉取邮件到本地客户端 (MUA) 主要使用以下协议：
> *   **POP3 (Post Office Protocol version 3)**:
>     *   将邮件从服务器下载到本地，通常下载后会从服务器删除（可配置保留）。
>     * 建立在TCP连接之上的协议。
>     *   操作相对简单。
>     *   标准端口: `110`
>     *   加密端口 (SSL/TLS): `995`
> *   **IMAP (Internet Mail Access Protocol)**:
>     *   直接在服务器上管理邮件，本地客户端的操作会同步到服务器。（在本地的所有操作会自动同步到服务器上）
>     *   允许用户在邮箱服务器的收件箱上创建文件夹、标记邮件状态等。
>     *   更适合多设备访问同一邮箱。
>     *   标准端口: `143`
>     *   加密端口 (SSL/TLS): `993`

> [!NOTE] POP3 vs IMAP
> *   **POP3**: 像取信，把信拿回家，邮箱可能就空了。
> *   **IMAP**: 像直接在邮局的信箱里整理信件，在家看、在办公室看，看到的都是同一个信箱的状态。
>
> JavaMail 同时支持 POP3 和 IMAP。以下主要介绍 POP3 的使用方法。

### 连接到 Store (POP3)

`Store` 对象代表邮件存储，对于 POP3/IMAP 来说，通常指整个邮箱。

```java
import javax.mail.*;
import javax.mail.internet.*;
import java.util.Properties;

// 需要添加对 POP3 SSL 的支持，如果使用旧版 JavaMail 可能需要额外依赖
// 对于 Jakarta Mail，通常包含在内
import com.sun.mail.pop3.POP3SSLStore; // For POP3 over SSL/TLS (port 995)
// import com.sun.mail.pop3.POP3Store; // For plain POP3 (port 110)

// ...

// 准备登录信息:
String pop3Host = "pop3.example.com"; // e.g., pop.qq.com, pop.163.com
int pop3Port = 995;  // 使用加密端口
String username = "bob@example.com";
String password = "password"; // 可能需要邮箱的 POP3/IMAP 授权码

// 设置 POP3 属性
Properties props = new Properties();
props.setProperty("mail.store.protocol", "pop3"); // 协议名称
props.setProperty("mail.pop3.host", pop3Host);  // POP3主机名，服务器地址
props.setProperty("mail.pop3.port", String.valueOf(pop3Port)); // 端口号

// --- 配置 SSL/TLS (for port 995) ---
// 以下配置适用于较旧的 com.sun.mail 实现，较新版本可能自动处理或有不同配置项
props.setProperty("mail.pop3.socketFactory.class", "javax.net.ssl.SSLSocketFactory");
props.setProperty("mail.pop3.socketFactory.fallback", "false");
props.setProperty("mail.pop3.socketFactory.port", String.valueOf(pop3Port));
// 有些服务器可能需要显式启用 SSL
// props.setProperty("mail.pop3.ssl.enable", "true");

// 启动SSL:
props.put("mail.smtp.socketFactory.class", "javax.net.ssl.SSLSocketFactory");
props.put("mail.smtp.socketFactory.port", String.valueOf(port));

// 获取 Session
Session session = Session.getInstance(props, null); // POP3 通常在 connect 时验证
session.setDebug(true); // 开启 Debug

Store store = null;
try {
    // 获取 Store 对象
    store = session.getStore("pop3");

    // 连接 (使用用户名和密码)
    // 注意：对于 SSL/TLS (995)，Store 类型可能是 POP3SSLStore
    // 如果直接用 getStore("pop3") 获取，它内部可能会处理 SSL
    store.connect(pop3Host, pop3Port, username, password);

    System.out.println("Connected to POP3 store successfully.");
    // 后续使用 store 对象访问文件夹和邮件

} catch (NoSuchProviderException e) {
    System.err.println("POP3 provider not found: " + e.getMessage());
} catch (MessagingException e) {
    System.err.println("Error connecting to POP3 store: " + e.getMessage());
    // 常见的连接错误包括认证失败、服务器地址/端口错误、SSL 配置错误
}
// finally { if (store != null && store.isConnected()) { store.close(); } } // 确保关闭

```


### 访问 Folder 和 Message
连接 `Store` 后，需要打开指定的文件夹（通常是收件箱 `INBOX`）来获取邮件。

```java
Folder folder = null;

try {
	// 确保 store 已连接
    if (store == null || !store.isConnected()) {
        System.err.println("Store is not connected.");
        return; // 或者重新连接
    }
	
    // 获取收件箱 Folder 对象
    folder = store.getFolder("INBOX");
    
    // 打开文件夹 (以只读或读写模式)
    // Folder.READ_ONLY: 只读，不能修改邮件状态（如标记已读、删除）
    // Folder.READ_WRITE: 读写，可以修改邮件状态
    folder.open(Folder.READ_WRITE);
    
	// 打印邮件总数/新邮件数量/未读数量/已删除数量:
	System.out.println("Folder: " + folder.getName());
	System.out.println("Total messages: " + folder.getMessageCount());
	System.out.println("New messages: " + folder.getNewMessageCount());
	System.out.println("Unread messages: " + folder.getUnreadMessageCount());
	System.out.println("Deleted messages: " + folder.getDeletedMessageCount());  // 标记为删除但未清除
	
    // 获取所有邮件
    Message[] messages = folder.getMessages(); // 获取邮件列表 (可能只包含 Header)
    System.out.println("Processing " + messages.length + " messages...");
    // 遍历邮件
	for (int i = 0; i < messages.length; i++) {
		Message message = messages[i];
	    System.out.println("\n--- Message " + (i + 1) + " ---");
    // 打印邮件基本信息 (需要转型为 MimeMessage)
	    if (message instanceof MimeMessage) {
            printBasicInfo((MimeMessage) message);
			// 解析并打印邮件内容
            parseMessageContent(message);
            // 可以在这里标记邮件为已读或删除
            // message.setFlag(Flags.Flag.SEEN, true); // 标记为已读
			// message.setFlag(Flags.Flag.DELETED, true); // 标记为删除
	    } else {
        System.out.println("Message is not a MimeMessage instance.");
	    }
    }
} catch (MessagingException e) {
    System.err.println("Error accessing folder or messages: " + e.getMessage());
} finally {
	// 关闭 Folder (参数 true 表示应用修改，如删除标记)
	if (folder != null && folder.isOpen()) {
        try {
            // 如果以 READ_WRITE 打开并标记了删除，传入 true 会 expunge (清除) 邮件
            // 如果只想关闭连接，传入 false
            folder.close(true); // or false
            System.out.println("Folder closed.");
        } catch (MessagingException e) {
            System.err.println("Error closing folder: " + e.getMessage());
        }
    }
    // 关闭 Store
    if (store != null && store.isConnected()) {
        try {
            store.close();
            System.out.println("Store closed.");
        } catch (MessagingException e) {
            System.err.println("Error closing store: " + e.getMessage());
        }
    }
}
```

### 解析 Message 内容
当我们获取到一个`Message`对象时，可以强制转型为MimeMessage，然后打印出邮件主题、发件人、收件人等信息：需要递归解析 `Part` 对象。

```java
import java.io.IOException;
import java.io.InputStream;
import javax.mail.Part; // Part 接口
import javax.mail.internet.MimeUtility; // 用于解码文本

// 打印邮件基本信息
private static void printBasicInfo(MimeMessage msg) throws MessagingException, IOException {
    // 邮件主题:(需要解码)
    System.out.println("Subject: " + MimeUtility.decodeText(msg.getSubject()));
    // 发件人:
    Address[] froms = msg.getFrom();
    if (froms != null) {
	    InternetAddress fromAddr = (InternetAddress) froms[0];
	    String personal = address.getPersonal();
	    String from = personal == null ? fromAddr.getAddress() : (MimeUtility.decodeText(personal) + " <" + address.getAddress() + ">");
	    System.out.println("From: " + from);
    }
    // 继续打印收件人:
    Address[] tos = msg.getRecipients(Message.RecipientType.TO);
    if (tos != null) {
        for (Address addr : tos) {
            System.out.println("To: " + addr.toString());
        }
    }
    if (msg.getSentDate() != null) {
        System.out.println("Sent Date: " + msg.getSentDate());
    }
    // 邮件 ID
    System.out.println("Message ID: " + msg.getMessageID());
    // 是否已读
    System.out.println("Is Seen: " + msg.isSet(Flags.Flag.SEEN));
}

//比较麻烦的是获取邮件的正文。一个MimeMessage对象也是一个Part对象，它可能只包含一个文本，也可能是一个Multipart对象，即由几个Part构成
// 递归解析邮件内容 (正文和附件)
private static void parseMessageContent(Part part) throws MessagingException, IOException {
    String contentType = part.getContentType();
    System.out.println("  Content Type: " + contentType);

    // --- 处理文本内容 ---
    if (part.isMimeType("text/plain")) {
        System.out.println("  [Text Body]:\n" + part.getContent());
    } else if (part.isMimeType("text/html")) {
        System.out.println("  [HTML Body]:\n" + part.getContent()); // 可以用 HTML 解析库处理
    }else if (part.isMimeType("multipart/*")) {
    // --- 处理 Multipart ---
        System.out.println("  [Multipart]:");
        Multipart multipart = (Multipart) part.getContent();
        int count = multipart.getCount();
        System.out.println("    Parts count: " + count);
        for (int i = 0; i < count; i++) {
            BodyPart bodyPart = multipart.getBodyPart(i);
            System.out.println("    --- Part " + (i + 1) + " ---");
            parseMessageContent(bodyPart); // 递归解析子部分
        }
    }else if (part.isMimeType("message/rfc822")) {  // --- 处理附件或内嵌资源 ---
        // 邮件中的邮件 (转发)
        System.out.println("  [Attached Message]:");
        parseMessageContent((Part) part.getContent());
    } else {
        // 可能是附件或内嵌图片
        String disposition = part.getDisposition();
        String fileName = part.getFileName();

        if (disposition != null && (disposition.equalsIgnoreCase(Part.ATTACHMENT) || disposition.equalsIgnoreCase(Part.INLINE))) {
            if (fileName != null) {
                // 解码文件名
                fileName = MimeUtility.decodeText(fileName);
                System.out.println("  [" + disposition + "]: " + fileName);
                // 可以保存附件
                // saveAttachment(part.getInputStream(), fileName);
            } else {
                System.out.println("  [" + disposition + "]: (No filename)");
            }
        } else {
            // 其他类型，如 application/pdf 但没有 disposition
             if (fileName != null) {
                 fileName = MimeUtility.decodeText(fileName);
                 System.out.println("  [Attachment?]: " + fileName);
                 // saveAttachment(part.getInputStream(), fileName);
             } else {
                System.out.println("  [Other Content]: Type=" + contentType);
             }
        }
    }
}
   
// 示例：保存附件的方法
private static void saveAttachment(InputStream is, String filename) throws IOException {
    // 实现文件保存逻辑...
    System.out.println("    (Saving attachment: " + filename + ")");
    // try (FileOutputStream fos = new FileOutputStream(filename)) {
    //     byte[] buffer = new byte[4096];
    //     int bytesRead;
    //     while ((bytesRead = is.read(buffer)) != -1) {
    //         fos.write(buffer, 0, bytesRead);
    //     }
    // } finally {
    //     if (is != null) is.close();
    // }
}
```


> [!IMPORTANT] 关闭资源
> *   **`folder.close(expunge)`**: 关闭文件夹。
>     *   `expunge = true`: 如果以 `READ_WRITE` 模式打开，并且有邮件被标记为 `Flags.Flag.DELETED`，则**永久删除**这些邮件。
>     *   `expunge = false`: 只关闭连接，不删除标记为 DELETED 的邮件。
> *   **`store.close()`**: 关闭到邮件服务器的连接。
>
> 务必在 `finally` 块中确保 `Folder` 和 `Store` 被正确关闭，释放资源。


> [!SUMMARY] Part 5: 接收 Email (POP3/IMAP)
> *   接收邮件主要使用 POP3 (端口 110/995) 或 IMAP (端口 143/993)。
> *   POP3 通常下载邮件到本地，IMAP 在服务器上管理邮件。
> *   JavaMail 提供 `Store` 对象代表邮箱存储，`Folder` 对象代表文件夹 (如 INBOX)。
> *   连接 `Store` 需要协议、服务器地址、端口、用户名、密码/授权码，并配置 `Properties` (特别是 SSL/TLS 设置)。
> *   打开 `Folder` (READ_ONLY 或 READ_WRITE) 后，可获取 `Message` 列表。
> *   `Message` (通常是 `MimeMessage`) 包含 Header (主题、发件人等) 和 Content。
> *   邮件内容可能是复杂的多部分 (`Multipart`) 结构，需要递归解析 `Part` 来获取正文和附件。
> *   使用 `MimeUtility.decodeText()` 处理可能编码过的文本 (主题、发件人名、文件名)。
> *   处理附件需要检查 `Part` 的 `disposition` (ATTACHMENT 或 INLINE) 和 `fileName`。
> *   操作完成后必须关闭 `Folder` 和 `Store`。`folder.close(true)` 会清除标记为删除的邮件。

## Part 6 HTTP 编程
> [!INFO] 什么是 HTTP？
> HTTP (HyperText Transfer Protocol，超文本传输协议) 是万维网数据通信的基础。它是目前 Web 应用程序使用最广泛的基础协议，处理着诸如浏览器访问网站、手机 App 访问后台服务器等交互。
>
> *   它是一种建立在 **TCP** 协议之上的**请求-响应**协议。
> *   Web 服务器通常监听标准端口 `80` (HTTP) 和加密端口 `443` (HTTPS)。


当浏览器希望访问某个网站时发送HTTP请求-响应，其**交互流程**如下：
1. 浏览器（客户端）与网站服务器之间首先建立TCP连接。（服务器总是使用`80`端口和加密端口`443`）
2. 浏览器向服务器发送一个HTTP**请求**（Request）
3. 服务器受到请求后进行处理，并返回一个HTTP响应(Request)，响应中通常包含HTML网页内容
4. 浏览器解析HTML，并将网页内容渲染展示给用户

### HTTP 请求结构
一个完整的HTTP请求-响应如下：
```
            GET / HTTP/1.1
            Host: www.sina.com.cn
            User-Agent: Mozilla/5 MSIE
            Accept: */*                ┌────────┐
┌─────────┐ Accept-Language: zh-CN,en  │░░░░░░░░│
│O ░░░░░░░│──────────────────────────▶├────────┤
├─────────┤◀──────────────────────────│░░░░░░░░│
│         │ HTTP/1.1 200 OK            ├────────┤
│         │ Content-Type: text/html    │░░░░░░░░│
└─────────┘ Content-Length: 133251     └────────┘
  Browser   <!DOCTYPE html>              Server
            <html><body>
            <h1>Hello</h1>
            ...
```

- 一个 HTTP 请求由**HTTP Header**和**HTTP Body**两部分构成。

1.  **请求行 (Request Line):** 第一行总是遵循 `请求方法 路径 HTTP版本` 的格式。
    *   例如: `GET / HTTP/1.1` (表示使用 `GET` 方法请求根路径 `/`，协议版本为 `HTTP/1.1`)。
2.  **请求头 (HTTP Headers):** 随后的每一行都是 `Header名称: Value` 格式的键值对，提供关于请求的元数据。常见的请求头包括：
	-  `Host`：表示请求的域名，因为一台服务器上可能有多个网站，因此有必要依靠Host来识别请求是发给哪个网站的；
	- `User-Agent`：客户端软件的标识信息，不同的浏览器有不同的标识，服务器依靠User-Agent判断客户端类型是IE还是Chrome，是Firefox还是一个Python爬虫；
	- `Accept`：表示客户端能处理的HTTP响应格式，`*/*`表示任意格式，`text/*`表示任意文本，`image/png`表示PNG格式的图片；
	- `Accept-Language`：表示客户端接收的语言，多种语言按优先级排序，服务器依靠该字段给用户返回特定语言的网页版本。
3. **空行:** 一个空行用于分隔请求头和请求体。
4. **请求体 (HTTP Body):** 包含请求的实际数据负载 (例如表单数据、JSON)。通常用于 `POST`、`PUT` 等方法。`GET` 请求通常没有请求体，只有HTTP Header。`POST`请求，该HTTP请求带有Body，以一个空行分隔。

**示例 POST 请求 (表单数据):**
```plain
POST /login HTTP/1.1
Host: www.example.com
Content-Type: application/x-www-form-urlencoded
Content-Length: 30

username=hello&password=123456
```
- 通常要设置
	*   `Content-Type`: 指定请求体的媒体类型。
	*   `Content-Length`: 指示请求体的字节大小。
	- 这样服务器就可以根据请求的Header和Body做出正确的响应


> [!TIP] GET请求 vs. POST请求
> *   **GET请求:** 参数附加在 URL 后面，以URLEncode方式编码。适用于获取数据。受 URL 长度限制，请求的参数不能太多。
> 	* 例如：`http://www.example.com/?a=1&b=K%26R`，参数分别是`a=1`和`b=K&R`
> 	* `K%26R` 是 URL 编码，`%26` 表示字符 `&`。URL 解码后，`b` 的值是 `K&R`，而不是将 `&` 解释为另一个参数分隔符。。
> *   **POST请求:** 参数放在请求体中发送，所以没有实际的长度限制。适用于提交数据（表单、上传、复杂对象）。可以使用不同的 `Content-Type` (如 `application/json`)。
> 	* `POST`请求的参数不一定是URL编码，可以按任意格式编码，只需要在`Content-Type`中正确设置即可。

**示例 POST 请求 (JSON 数据):**
```plain
POST /login HTTP/1.1
Content-Type: application/json
Content-Length: 38

{"username":"bob","password":"123456"}
```

### HTTP 响应结构
与请求类似，HTTP 响应也包含 **响应头 (Header)** 和 **响应体 (Body)**。

1.  **状态行 (Status Line):** 第一行格式为 `HTTP版本 状态码 状态描述`。
    *   例如: `HTTP/1.1 200 OK` (表示 HTTP 版本 1.1，状态码 200，表示成功)。
2.  **响应头 (HTTP Headers):** 提供关于响应信息的键值对。常见的响应头包括：
    *   `Content-Type`: 响应体的媒体类型 (例如 `text/html`, `image/jpeg`)。
    *   `Content-Length`: 响应体的字节大小。
    *   `Set-Cookie`: 服务器用来向客户端发送 Cookie。
    *   `Location`: 用于重定向 (3xx 状态码)，指定新的 URL。
3.  **空行:** 分隔响应头和响应体。
4.  **响应体 (HTTP Body):** 包含实际请求的内容 (例如 HTML 页面、图片数据、JSON 数据)。

```plain
HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: 133251

<!DOCTYPE html>
<html><body>
<h1>Hello</h1>
</body></html>
```

> [!INFO] HTTP 状态码
> 客户端只依赖响应代码判断HTTP响应是否成功。它们被分为几类：
> *   **1xx (信息性):** 表示请求已接收（提示性响应），继续处理 (例如 `101 `表示将切换协议(`Switching Protocols`) 用于 WebSocket连接)。
> *   **2xx (成功):** 表示请求已被成功接收、理解、接受 (例如 `200 OK`, `201 Created`, `204 No Content`，206表示只发送了部分内容)。
> *   **3xx (重定向):** 表示需要采取进一步操作才能完成请求 (例如 `301 Moved Permanently`（永久重定向）, `302 Found`, `304 Not Modified`，303表示客户端应该按指定路径重新发送请求)。
> *   **4xx (客户端错误):** 表示请求包含错误语法或无法完成请求 (例如 `400 Bad Request`（表示因为Content-Type等各种原因导致的无效请求）, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`（指定的路径不存在）)。
> *   **5xx (服务器错误):** 表示服务器在处理一个看似有效的请求时失败 (例如 `500 Internal Server Error`（服务器内部故障）, `503 Service Unavailable`（服务器暂时无法响应）)。
^statuscode
1. 浏览器收到第一个HTTP响应，
2. 解析HTML后，又会发送一系列HTTP请求，
3. 例如，`GET /logo.jpg HTTP/1.1`请求一个图片，服务器响应图片请求后，会直接把二进制内容的图片发送给浏览器：
**示例图片响应:**
```plain
HTTP/1.1 200 OK
Content-Type: image/jpeg
Content-Length: 18391

????JFIFHH??XExifMM?i&??X?...(二进制的JPEG图片)
```
因此，服务器总是被动地接收客户端的一个HTTP请求，然后响应它。客户端则根据需要发送若干个HTTP请求。

### HTTP 协议的演进
*   **HTTP/1.0:** 每个请求/响应对都需要建立一个新的 TCP 连接，收到服务器响应后再关闭这个TCP连接。由于建立TCP连接比较耗时，效率较低。
*   **HTTP/1.1:** 引入了**持久连接 (Keep-Alive)**，允许在单个 TCP 连接上进行多次请求/响应。还引入了流水线 (Pipelining)，允许客户端在收到响应前发送多个请求（但响应仍需按序返回），进一步提高效率。

```
                       ┌─────────┐
┌─────────┐            │░░░░░░░░░│
│O ░░░░░░░│            ├─────────┤单个 TCP连接
├─────────┤            │░░░░░░░░░│
│         │            ├─────────┤
│         │            │░░░░░░░░░│
└─────────┘            └─────────┘
     │      request 1       │
     │─────────────────────▶│
     │      response 1      │
     │◀─────────────────────│
     │      request 2       │
     │─────────────────────▶│
     │      response 2      │
     │◀─────────────────────│
     │      request 3       │
     │─────────────────────▶│
     │      response 3      │
     │◀─────────────────────│
     ▼                      ▼
```

*   **HTTP/2.0:** 引入了**多路复用 (Multiplexing)**。允许客户端在单个 TCP 连接上并行发送多个请求，并且服务器可以乱序返回响应，只要客户端能识别响应对应的请求即可。这极大地减少了队头阻塞问题，显著提高了性能。（在1.0的基础上增加了响应乱序功能）

```
                       ┌─────────┐
┌─────────┐            │░░░░░░░░░│
│O ░░░░░░░│            ├─────────┤单个TCP连接
├─────────┤            │░░░░░░░░░│
│         │            ├─────────┤多路复用
│         │            │░░░░░░░░░│
└─────────┘            └─────────┘
     │      request 1       │
     │─────────────────────▶│
     │      request 2       │
     │─────────────────────▶│
     │      response 1      │
     │◀─────────────────────│
     │      request 3       │
     │─────────────────────▶│
     │      response 3      │
     │◀─────────────────────│
     │      response 2      │
     │◀─────────────────────│
     ▼                      ▼
```

### Java HTTP 客户端编程
HTTP 编程涉及客户端和服务器端。
- 本节**仅讨论客户端**的 HTTP 编程。
- 服务器端的 HTTP 编程（即 Web 服务器开发）是 Java EE 的核心内容，更为复杂。

浏览器也是一种HTTP客户端，所以客户端HTTP编程的行为本质上和浏览器是一样的：发送一个HTTP请求，接收并处理服务器响应内容。
- 只不过浏览器进一步把响应内容解析后渲染并展示给了用户，而我们使用Java进行HTTP客户端编程仅限于获得响应内容。

#### 旧版 API: `HttpURLConnection`

早期 JDK 版本使用 `java.net.HttpURLConnection` 进行 HTTP 操作。

```java
import java.net.URL;
import java.net.HttpURLConnection;
import java.io.InputStream;
import java.util.Map;
import java.util.List;

// ...

URL url = new URL("http://www.example.com/path/to/target?a=1&b=2");
HttpURLConnection conn = (HttpURLConnection) url.openConnection();
try {
	conn.setRequestMethod("GET");
	conn.setUseCaches(false);
	conn.setConnectTimeout(5000); // 请求超时5秒
	conn.setReadTimeout(5000); //读取超时5秒

	// 设置HTTP头:
	conn.setRequestProperty("Accept", "*/*");
	conn.setRequestProperty("User-Agent", "Mozilla/5.0 (compatible; MSIE 11; Windows NT 5.1)");

	// 连接并发送HTTP请求:（显示连接）
	conn.connect();  // 可选，getInputStream() 或 getResponseCode() 会隐式连接

// 判断HTTP响应码是否成功:
	if (conn.getResponseCode() != HttpURLConnection.HTTP_OK) { // 200
	    throw new RuntimeException("Bad response code: " + conn.getResponseCode());
	}		

	// 获取所有响应Header:
	Map<String, List<String>> headers = conn.getHeaderFields();
	for (Map.Entry<String, List<String>> entry : headers.entrySet()) {
	    System.out.println(entry.getKey() + ": " + entry.getValue());
	}
	
	// 获取响应内容:
    try (InputStream input = conn.getInputStream()) {
        // 处理输入流...
        // byte[] data = input.readAllBytes();
        // String body = new String(data, StandardCharsets.UTF_8);
        System.out.println("Response body received.");
    }
} finally {
    if (conn != null) {
        conn.disconnect(); // 关闭连接
    }
}
```

> [!NOTE] `HttpURLConnection` 的缺点
> 代码编写相对繁琐，需要手动管理连接、处理输入流(`InputStream`)，并且 API 设计不够现代化。

#### 新版 API: `java.net.http.HttpClient` (JDK 11+)
从 Java 11 开始，引入了新的 `HttpClient` API，提供了更现代、更灵活、性能更好的 HTTP 客户端实现，并原生支持 HTTP/2 和 WebSocket。

**1. 创建 HttpClient 实例:**
建议创建一个全局共享的`HttpClient`实例，因为`HttpClient`内部使用线程池优化多个HTTP连接，可以复用，提高效率：

```java
import java.net.http.HttpClient;

// 全局 HttpClient 实例 (推荐)
static HttpClient httpClient = HttpClient.newBuilder()
		.version(HttpClient.Version.HTTP_2) //优先使用 HTTP/2
		.connectTimeout(Duration.ofSeconds(10)) //设置连接超时
		//.followRedirects(HttpClient.Redirect.NORMAL)// 配置重定向策略
		.build();
```

**2. 发送 GET 请求获取文本:**

```java
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpClient.Version;
import java.time.Duration;
import java.util.*;

public class Main {
    // 全局HttpClient:
    //如上...

    public static void main(String[] args) throws Exception {
        String url = "https://www.sina.com.cn/";
        HttpRequest request = HttpRequest.newBuilder(new URI(url))
            // 设置Header:
            .header("User-Agent", "Java HttpClient")
            .header("Accept", "*/*")
            // 设置 GET 方法 (默认)
	        .GET()
            // 设置超时:
            .timeout(Duration.ofSeconds(5))
            // 设置版本:上面设置了这里应该可以不用？
            .version(Version.HTTP_2)
            .build();
        //发送同步请求，并指定响应体处理器为字符串
        // HttpResponse.BodyHandlers 提供多种处理器: ofString(), ofByteArray(), ofInputStream(), discarding(), etc.
        HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
        
    // 打印状态码和版本
	    System.out.println("Status Code: " + response.statusCode());
	    System.out.println("HTTP Version: " + response.version());
	    
        // 获取响应头，HTTP允许重复的Header，因此一个Header可对应多个Value:(HttpHeaders 是一个 Map<String, List<String>>)
        HttpHeaders headers = response.headers();
        //这里是lambda表达式，(key, value) ->...
        headers.map().forEach((key, value) -> System.out.println(key + ": " + value));
		
		// 获取响应体 (字符串)
		String body = response.body();
		System.out.println("\nResponse Body (first 1024 chars):");
		//这段代码的作用是打印字符串 body 的前 1024 个字符（如果字符串长度不足 1024，则打印整个字符串），并在末尾添加 ...，表示内容被截断。
	    System.out.println(body.substring(0, Math.min(body.length(), 1024)) + "...");
    }
}
```

> [!TIP] 处理不同类型的响应体
> *   获取**字节数组**: （类似图片这种二进制内容）`HttpResponse.BodyHandlers.ofByteArray()` -> `HttpResponse<byte[]>`
> *   获取**输入流**: `HttpResponse.BodyHandlers.ofInputStream()` -> `HttpResponse<InputStream>` (适用于大文件，不希望一次性加载到内存)
> *   **丢弃**响应体: `HttpResponse.BodyHandlers.discarding()` -> `HttpResponse<Void>`
> *   保存到**文件**: `HttpResponse.BodyHandlers.ofFile(Paths.get("response.dat"))` -> `HttpResponse<Path>`

**3. 发送 POST 请求:**
需要构建请求体 (`BodyPublisher`) （准备好要发送的Body数据）并设置 `Content-Type`。

```java
import java.net.URI;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

// ... (httpClient 定义如上)

public static void main(String[] args) throws Exception {
	String url = "http://www.example.com/login";
	String body = "username=bob&password=123456";
	
	HttpRequest request = HttpRequest.newBuilder(new URI(url))
	    // 设置Header:
		.header("Content-Type", "application/x-www-form-urlencoded")
		.header("Accept", "application/json") // 期望服务器返回 JSON
	    // 设置超时:
	    .timeout(Duration.ofSeconds(5))
	    // 设置版本:上面设置了这里应该可以不用？
	    .version(Version.HTTP_2)
	    // 设置 POST 方法并提供请求体
        // BodyPublishers 提供多种创建方式: ofString(), ofByteArray(), ofInputStream(), ofFile()
	    .POST(HttpRequest.BodyPublishers.ofString(body, StandardCharsets.UTF_8))
	    .build();

	HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());

    System.out.println("Status Code: " + response.statusCode());
    System.out.println("Response Body:");
    System.out.println(response.body());
```

> [!SUMMARY] Part 6: HTTP 编程要点
> *   HTTP 是基于 TCP 的请求-响应协议，是 Web 通信的基础。
> *   请求和响应都包含 Header 和可选的 Body。
> *   请求方法 (GET, POST 等)、URL、HTTP 版本、Header (如 Host, User-Agent, Content-Type) 是请求的关键部分。
> *   响应状态码 (2xx, 3xx, 4xx, 5xx) 和 Header (如 Content-Type, Content-Length) 是响应的关键部分。
> *   HTTP/1.1 支持持久连接，HTTP/2.0 支持多路复用，效率更高。
> *   Java 11+ 推荐使用 `java.net.http.HttpClient` API 进行 HTTP 客户端编程，它更现代、功能更强、性能更好。
> *   使用 `HttpClient` 需要创建 `HttpClient` 实例、构建 `HttpRequest`、发送请求并使用 `HttpResponse.BodyHandler` 处理响应体。

## Part 7 RMI 远程方法调用 (Remote Method Invocation)

> [!INFO] 什么是 RMI？
> RMI (Remote Method Invocation) 是一种 Java 机制，它允许在一个 Java 虚拟机 (JVM) 中运行的代码调用另一个 JVM 上的对象的方法，就像调用本地方法一样。这使得构建分布式 Java 应用程序成为可能。
>
> *   **服务器 (Server):** 提供远程服务的 JVM。
> *   **客户端 (Client):** 调用远程服务的 JVM。

### RMI 基础示例：世界时钟服务

我们将实现一个简单的 RMI 示例：
*   **服务器**提供一个 `WorldClock` 服务。
*   **客户端**可以调用该服务获取指定时区的当前时间。

即允许客户端调用下面的方法：
```java
LocalDateTime getLocalDateTime(String zoneId);
```

#### 1. 定义共享接口
RMI 的核心要求是服务器和客户端必须共享同一个**远程接口**。这个接口定义了客户端可以调用的方法。我们定义一个`WorldClock`接口，代码如下：

```java
// WorldClock.java (需要被服务器和客户端共享)
import java.rmi.Remote;
import java.rmi.RemoteException;
import java.time.LocalDateTime;

/**
 * 定义远程世界时钟服务接口。
 * 必须继承自 java.rmi.Remote。
 * 所有方法必须声明抛出 java.rmi.RemoteException。
 */
public interface WorldClock extends Remote {
    /**
     * 获取指定时区的当前本地日期和时间。
     * @param zoneId 时区 ID (例如 "Asia/Shanghai", "Europe/London")
     * @return 指定时区的 LocalDateTime 对象
     * @throws RemoteException 如果在远程调用过程中发生错误
     */
    LocalDateTime getLocalDateTime(String zoneId) throws RemoteException;
}
```

> [!IMPORTANT] RMI 接口规则
> *   接口必须继承 `java.rmi.Remote` 标记接口。
> *   接口中的每个方法都必须声明抛出 `java.rmi.RemoteException` (或其他父异常)。

#### 2. 实现服务器端服务
- 服务器需要提供远程接口的具体实现。
实现类`WorldClockService`代码如下：

```java
// WorldClockService.java (服务器端实现)
import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject; // 需要继承或使用 exportObject
import java.time.LocalDateTime;
import java.time.ZoneId;

/**
 * WorldClock 接口的服务器端实现。
 * 注意：实现类可以选择继承 UnicastRemoteObject，或者在注册时手动导出。
 * 这里我们不继承，稍后在 Server 类中手动导出。
 */
public class WorldClockService implements WorldClock {
    @Override
    public LocalDateTime getLocalDateTime(String zoneId) throws RemoteException {
        System.out.println("Server: Received call for zoneId = " + zoneId);
        // 返回指定时区的当前时间，去除纳秒部分
        return LocalDateTime.now(ZoneId.of(zoneId)).withNano(0);
    }
}
```

#### 3. 启动 RMI 服务器并注册服务
1. 我们需要通过Java RMI提供的一系列底层支持接口（创建服务实例），
2. 把上面编写的服务以RMI的形式暴露在网络上（将实例注册到RMI注册表(RMI Registry)），以便客户端查找和调用：

```java
// Server.java (服务器启动程序)
import java.rmi.RemoteException;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.rmi.server.UnicastRemoteObject;

public class Server {
    public static void main(String[] args) throws RemoteException {
		try {
	        System.out.println("create World clock remote service...");
	        // 1. 实例化一个WorldClock90(服务实现对象):
	        WorldClock worldClock = new WorldClockService();
	        // 2. 导出服务对象，使其能够接收远程调用
	        //UnicastRemoteObject.exportObject 使普通对象变为 RMI 服务对象。
	        // 参数 0 表示使用匿名端口（或由 RMI 系统选择）。
	        WorldClock skeleton = (WorldClock) UnicastRemoteObject.exportObject(worldClock, 0);
            System.out.println("Service exported.");
            
            // 3. 获取或创建 RMI 注册表 (Registry)
            //    RMI 默认使用 1099 端口。
	        Registry registry = LocateRegistry.createRegistry(1099);
            System.out.println("RMI Registry created on port 1099.");
            
            // 4. 将导出的服务绑定到注册表，并指定一个名称
            //    客户端将使用这个名称 ("WorldClock") 来查找服务。
            //    rebind() 会覆盖任何已存在的同名绑定。
	        registry.rebind("WorldClock", skeleton);
	        System.out.println("WorldClock service bound in registry.");
	        System.out.println("Server is ready.");

        } catch (RemoteException e) {
            System.err.println("Server exception: " + e.toString());
            e.printStackTrace();
        }
    }
}
```

> [!NOTE] RMI 注册表 (Registry)
> *   是一个简单的命名服务，用于存储远程对象的引用。
> *   客户端通过查询注册表来获取远程对象的引用 (Stub)。
> *   默认端口是 `1099`。

上述代码主要目的是通过RMI提供的相关类，将我们自己的`WorldClock`实例注册到RMI服务上。RMI的默认端口是`1099`，最后一步注册服务时通过`rebind()`指定服务名称为`"WorldClock"`。

#### 4. 编写客户端代码
客户端需要获取 RMI 注册表的引用，查找指定名称的服务，由于RMI要求服务器和客户端共享同一个接口，因此我们要把`WorldClock.java`这个接口文件复制到客户端，然后在客户端实现RMI调用：

**重要:** 客户端项目也需要 `WorldClock.java` 这个接口文件。
```java
// Client.java (客户端调用程序)
import java.rmi.NotBoundException;
import java.rmi.RemoteException;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.time.LocalDateTime;

public class Client {
    public static void main(String[] args) throws RemoteException, NotBoundException {
        try {
            // 1. 获取远程服务器上的 RMI 注册表引用
            //    假设服务器运行在 localhost，端口 1099。连接到服务器localhost，端口1099:
        Registry registry = LocateRegistry.getRegistry("localhost", 1099);
        System.out.println("Connected to RMI Registry.");
        
            // 2. 从注册表中查找名为 "WorldClock" 的远程服务
            //    lookup() 返回的是一个远程对象的存根 (Stub)。（强制转型为WorldClock接口）
        WorldClock worldClock = (WorldClock) registry.lookup("WorldClock");
        System.out.println("Lookup 'WorldClock' service successful.");
        // 3. 像调用本地方法一样调用远程接口方法
        System.out.println("Calling remote method getLocalDateTime('Asia/Shanghai')...");
        LocalDateTime now = worldClock.getLocalDateTime("Asia/Shanghai");
        // 打印调用结果:
        System.out.println(now);
        } catch (RemoteException | NotBoundException e) {
            System.err.println("Client exception: " + e.toString());
            e.printStackT();
        }
    }
}
```

1.  编译所有 Java 文件 (`WorldClock.java`, `WorldClockService.java`, `Server.java`, `Client.java`)。确保客户端和服务器都能访问 `WorldClock.class`。
2.  启动服务器: `java Server`。
3.  在服务器运行时，启动客户端: `java Client`。

### RMI 工作原理：Stub 和 Skeleton

RMI 的底层机制隐藏了网络通信的复杂性。

1.  **客户端 (Client):**
    *   通过 `registry.lookup()` 获取的不是实际的服务对象，而是一个称为 **存根 (Stub)** 的代理对象。
    *   Stub 实现了远程接口 (`WorldClock`)。
    *   当客户端调用 Stub 的方法 (如 `getLocalDateTime()`) 时，Stub 负责：
        *   将方法调用参数**序列化** (打包)。
        *   通过网络将打包后的数据发送给服务器。
        *   等待服务器的响应。
        *   接收网络传回的结果，**反序列化** (解包)。
        *   将结果返回给客户端调用代码。
2.  **服务器 (Server):**
    *   RMI 运行时环境监听网络连接。
    *   当接收到来自客户端 Stub 的请求时，一个称为 **骨架 (Skeleton)** 的服务器端对象 (通常由 RMI 内部生成) 负责：
        *   接收网络数据，**反序列化**参数。
        *   调用**实际的服务实现对象** (`WorldClockService` 实例) 的对应方法。
        *   获取方法的返回值。
        *   将返回值**序列化**。
        *   通过网络将序列化后的结果发送回客户端 Stub。

> [!NOTE] 序列化
> RMI 严重依赖 Java 的序列化机制来在网络上传递对象（参数和返回值）。（Java的序列化和反序列化不但涉及到数据，还涉及到二进制的字节码，即使使用白名单机制也很难保证100%排除恶意构造的字节码。）

```
┌ ─ ─ ─ ─ ─ ─ ─ ─ ┐         ┌ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┐
  ┌─────────────┐                                  ┌────────────┐
│ │   Service   │ │         │                      │  Service   │ │
  └─────────────┘                                  └────────────┘
│        ▲        │         │                            ▲        │
         │                                               │
│        │        │         │                            │        │
  ┌─────────────┐   Network    ┌───────────────┐   ┌────────────┐
│ │ Client Stub ├─┼─────────┼─▶│Server Skeleton│──▶│Service Impl│ │
  └─────────────┘              └───────────────┘   └────────────┘
└ ─ ─ ─ ─ ─ ─ ─ ─ ┘         └ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┘
```

1. 先运行服务器，再运行客户端。从运行结果可知，因为客户端只有接口，并没有实现类，因此，
2. 客户端获得的接口方法返回值实际上是通过网络从服务器端获取的。
3. 对客户端来说，客户端持有的`WorldClock`接口实际上对应了一个“实现类”，它是由`Registry`内部动态生成的，并负责把方法调用通过网络传递到服务器端。
4. 服务器端接收网络调用的服务并不是我们自己编写的`WorldClockService`，而是`Registry`自动生成的代码。
5. 我们把客户端的“实现类”称为`stub`，而服务器端的网络服务类称为`skeleton`，它会真正调用服务器端的`WorldClockService`，获取结果，然后把结果通过网络传递给客户端。
6. 整个过程由RMI底层负责实现序列化和反序列化

### RMI 的局限性和安全风险
*   **安全漏洞:** Java 序列化/反序列化机制本身可能存在安全风险 (如反序列化漏洞)。恶意构造的序列化数据可能导致远程代码执行。（而RMI严重依赖这个序列化机制0）

> [!WARNING] 安全警告
> RMI 不应直接暴露在公共网络上。它更适合用于内部网络中相互信任的 Java 应用之间的通信。确保 RMI 端口 (如 1099) 受到防火墙保护。（不要把1099端口暴露在公网上作为对外服务。）

*   **语言限制:** RMI 是 Java 特有的技术，通常只能用于 Java 程序之间的通信。其他语言很难直接调用 Java RMI 服务。
*   **版本兼容性:** 客户端和服务器使用的类（尤其是接口和作为参数/返回值的类）需要兼容，否则可能导致序列化/反序列化错误。

> [!TIP] 跨语言 RPC 替代方案
> 如果需要不同语言编写的服务进行通信，可以考虑使用更通用的 RPC (Remote Procedure Call) 框架，例如：
> *   **gRPC:** 由 Google 开发的高性能、开源通用 RPC 框架，支持多种语言。
> *   **Thrift:** 由 Facebook 开发的 RPC 框架。
> *   **RESTful API (基于 HTTP):** 虽然不是严格意义上的 RPC，但广泛用于跨语言服务通信。
