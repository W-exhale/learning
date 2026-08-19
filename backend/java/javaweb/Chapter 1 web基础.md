## Part 1 介绍
-   属于 **Java EE** (Java Enterprise Platform) 的范畴。之前介绍的所有基于标准 `JDK` 的开发都是 **Java SE** (Java Platform Standard Edition)。
-   还有一个小众不太常用的 **Java ME** (Java Platform Micro Edition)，是 Java 移动开发平台（非 Android）。它们三者关系如下：
```
┌────────────────┐
│     JavaEE     │
│┌──────────────┐│
││    JavaSE    ││
││┌────────────┐││
│││   JavaME   │││
││└────────────┘││
│└──────────────┘│
└────────────────┘
```

`Java ME` 是一个裁剪后的“微型版” `JDK`，现在使用很少。**Java EE** 并非凭空产生，它完全基于 **Java SE**，只是增加了许多服务器相关的库以及 `API` 接口。所有 `Java EE` 程序仍然运行在标准的 `Java SE` 虚拟机上。

**Java EE** 更多的是一种软件架构和设计思想，可以看作是在 `Java SE` 基础上开发的一系列基于服务器的组件、`API` 标准和通用架构。

**Java EE** 最核心的组件是基于 **Servlet** 标准的 Web 服务器。开发者编写的应用程序基于 `Servlet API` 并在 Web 服务器内部运行：
```
┌─────────────┐
│┌───────────┐│
││ User App  ││
│├───────────┤│
││Servlet API││
│└───────────┘│
│ Web Server  │
├─────────────┤
│   JavaSE    │
└─────────────┘
```

此外，**Java EE** 还有一系列技术标准：

-   `EJB` (Enterprise JavaBean): 企业级 JavaBean，早期用于实现业务逻辑，现多被 `Spring` 等轻量级框架取代。
-   `JAAS` (Java Authentication and Authorization Service): 标准认证和授权服务，常用于企业内部。Web 程序通常使用更轻量级的自定义认证。
-   `JCA` (JavaEE Connector Architecture): 用于连接企业内部的 EIS 系统等。
-   `JMS` (Java Message Service): 用于消息服务。
-   `JTA` (Java Transaction API): 用于分布式事务。
-   `JAX-WS` (Java API for XML Web Services): 用于构建基于 XML 的 Web 服务。
-   ...

目前流行的基于 `Spring` 的轻量级 `Java EE` 开发架构，使用最广泛的是 `Servlet` 和 `JMS`，以及一系列开源组件。

## Part 2 Web基础
-   我们访问网站、使用 `App` 时，大多基于 **Web** 这种 **B/S 架构** (Browser/Server)。
-   **特点**：客户端只需浏览器，应用程序逻辑和数据存储在服务器端。浏览器请求服务器，获取并展示 `Web` 页面。

`Web` 页面具有强交互性。由于页面用 `HTML` 编写，表现力强，且服务器端升级后客户端无需部署即可使用新版本，因此 `B/S` 架构升级非常容易。
### 1. HTTP协议
-   在 Web 应用中，浏览器请求一个 `URL`，服务器将生成的 `HTML` 网页发送给浏览器，两者间的传输协议是 **HTTP**。
-   **HTTP** 协议基于 **TCP** 协议。在浏览器中检查网页元素可以看到 `HTML` 结构：![Pasted image 20250429152923](images/Pasted%20image%2020250429152923.png)
-   查看网络(Network)面板可以看到请求和响应：![Pasted image 20250429153135](images/Pasted%20image%2020250429153135.png)

**浏览器请求流程：**

1.  与服务器建立 `TCP` 连接。
2.  发送 `HTTP` 请求。
3.  接收 `HTTP` 响应，并在浏览器中显示网页。


**HTTP 请求示例 (Headers):**
![Pasted image 20250429153633](images/Pasted%20image%2020250429153633.png)

-   `:method`: 请求方法，如 `GET`。
-   `:path`: 请求的资源路径，如 `/mdrama/82006`。
-   `:scheme`: 使用的协议，如 `https`。
-   `:authority`: 请求的域名。
-   `User-Agent`: 客户端标识 (e.g.,Chrome浏览器是 `Mozilla/5.0 ... Chrome/79`)。
-   `Accept`: 浏览器能接收的资源类型。
-   `Accept-Language`: 浏览器偏好语言。
-   `Accept-Encoding`: 浏览器支持的压缩类型。

**HTTP 响应示例 (Headers):**![Pasted image 20250429155245](images/Pasted%20image%2020250429155245.png)
-   `Content-Type`: 响应内容的类型 (e.g., `text/html`, `image/jpeg`)。
-   `Content-Length`: 响应内容的长度 (字节数)。
-   `Content-Encoding`: 响应内容的压缩算法 (e.g., `gzip`)。
-   `Cache-Control`: 客户端缓存指示 (e.g., `max-age=300`)。

**常见 HTTP 响应状态码：**

-   `200 OK`: 成功。
-   `301 Moved Permanently`: 表示该URL已经永久重定向。
-   `302 Found`: 表示该URL需要临时重定向。
-   `304 Not Modified`: 表示该资源未修改，客户端可使用本地缓存。
-   `400 Bad Request`: 客户端发送了一个错误的请求 (如参数无效)。
-   `401 Unauthorized`: 未授权。（客户端因为身份未验证而不允许访问该URL）
-   `403 Forbidden`: 禁止访问 (权限问题)。（表示服务器因为权限问题拒绝了客户端的请求）
-   `404 Not Found`: 资源不存在。
-   `500 Internal Server Error`: 服务器内部错误。（例如无法连接数据库）
-   `502 Bad Gateway`
-   `503 Service Unavailable`: 服务暂时不可用，暂时无法处理请求。
-  `504 Gateway Timeout`

`HTTP` 请求和响应由 `HTTP Header` 和 `HTTP Body` 构成。`HTTP Header` 每行以 `\r\n` 结束。连续两个 `\r\n` 分隔 `Header` 和 `Body`。

浏览器根据 `Header` 中的 `Content-Type`、`Content-Encoding` 等信息处理 `HTTP Body` 解压后显示内容。通常第一个获取的资源是 `HTML` 网页，其中可能包含 `JavaScript`、`CSS`、图片等资源，浏览器会根据资源的URL再次向服务器请求这些资源。

更多 `HTTP` 协议细节可参考 [HTTP权威指南](https://book.douban.com/subject/10746113/) 或 [Mozilla开发者网站](https://developer.mozilla.org/zh-CN/docs/Web/HTTP)。

之前的网络编程是作为客户端请求资源，现在我们需要作为服务器响应请求，即进行 **Web 开发**。

### 2. 编写HTTP Server
-   一个 `HTTP Server` 本质上是一个 `TCP` 服务器。以下是基于 `TCP` 的多线程服务器框架：
```java
// Server.java (Simplified Structure)
import java.io.*;
import java.net.*;
import java.nio.charset.StandardCharsets;

/** Server类：
* 监听指定端口（8080）并接受客户端连接
*/
public class Server{
	public static void main(String[] args) throws IOException{
		ServerSocket ss = new ServerSocket(8080); //创建一个ServerSocket对象，监听8080端口，用于接收客户端的TCP连接
		System.out.println("server is running...");
		while(true)){
			Socket sock = ss.accept(); //阻塞等待，直到有客户端连接，返回一个Socket对象，表示与客户端的通信管道
			System.out.println("connected from " + sock.getRemoteSocketAddress());
			Thread t = new Handler(sock);
			t.start();// 每次有新连接时，创建一个新线程Handler处理该客户端，多线程设计可以同时处理多个客户端连接
			
		}
	}
}
// Handler.java (Simplified Structure)
/**Handler类
*为每个连接的客户端分配一个线程，处理该连接上的HTTP请求
*/
class Handler extends Thread{
	Socket sock;
	public Handler(Socket sock){
		this.sock = sock; //接收一个客户端Socket，保存为成员变量便于处理
	}
	@Override
	public void run(){
		try(InputStream input = this.sock.getInputStream();
		OutputStream output = this.sock.getOutputStream()){//获取客户端连接的输入流和输出流，用于接收请求和发送响应
			handle(input, output);//调用handle()方法处理具体的HTTP请求和响应逻辑
			}
		}catch(Exception e){
			// Handle exception properly in real code
            System.err.println("Client handling error: " + e.getMessage());
		}
		finally{
			try{
				this.sock.close();
			}catch(IOException ioe){
				// Log error
			}
			System.out.println("client disconnected.");
		}

	private void handle(InputStream input, OutputStream output) throw IOException{
			var reader = new BufferedReader(new InputStreamReader(input, StandardCharsets.UTF_8)); //按行读取HTTP请求。首行一般是请求行，格式为：<方法> <路径> <协议版本>。示例：GET / HTTP/1.1
			var writer = new BufferedWriter(new OutputStreamWriter(output, StandarCharsets.UTF_8));
		
		//TODO: 处理HTTP请求
		
		System.out.println("Process new http request...");
        // 读取HTTP请求:
        boolean requestOk = false;
        String firstLine = reader.readLine();
        if (firstLine != null && firstLine.startsWith("GET / HTTP/1.")) {// 检查是否是对/的GET请求，如果不是，设置requestOk为false
            requestOk = true;
        }
        // 读取请求头 (简化处理)
        while (true) {//按行读取请求头，直到遇到空行（空行表示请求头结束）
            String header = reader.readLine();
            if (header == null || header.isEmpty()) { // 读取到空行时, HTTP Header读取完毕
                break;
            }
            System.out.println(header);
        }

        System.out.println(requestOk ? "Response OK" : "Response Error");
        if (!requestOk) {//如果请求无效，返回404错误响应
            // 发送错误响应:
            writer.write("HTTP/1.0 404 Not Found\r\n");
            writer.write("Content-Length: 0\r\n");
            writer.write("\r\n"); // Header结束
            writer.flush();
        } else {
            // 发送成功响应:
            String data = "<html><body><h1>Hello, world!</h1></body></html>";
            byte[] dataBytes = data.getBytes(StandardCharsets.UTF_8);
            int length = dataBytes.length;

            writer.write("HTTP/1.0 200 OK\r\n");
            writer.write("Connection: close\r\n"); // Important for HTTP/1.0
            writer.write("Content-Type: text/html\r\n");
            writer.write("Content-Length: " + length + "\r\n");
            writer.write("\r\n"); // Header结束
            writer.flush(); // Flush headers before writing body

            output.write(dataBytes); // Write body using OutputStream for binary data
            output.flush();	
		}
	}
}
```
**程序的工作流程**
1. **服务器启动**
    - 服务器通过 `ServerSocket` 监听 8080 端口，等待客户端连接。
2. **接受客户端连接**
    - 每次有客户端连接时，创建一个 `Handler` 线程处理该连接。
3. **处理客户端请求**
    - `Handler`：
        - 解析客户端发来的 HTTP 请求（包括请求行和请求头）。
        - 判断请求是否合法。
        - 返回对应的 HTTP 响应（200 或 404）。
4. **关闭连接**
    - 处理完成后关闭客户端的 `Socket`。

在浏览器输入`http://local.liaoxuefeng.com:8080/`就可以看到响应页面：

![httpserver](https://liaoxuefeng.com/books/java/web/basic/local.jpg)

**HTTP 版本：**
-   **`HTTP/1.0`**: 早期版本，每个请求/响应对都需要一个新的 `TCP` 连接。
-   **`HTTP/1.1`**: 允许在同一 `TCP` 连接上复用多个请求/响应，提高效率（持久连接）。
-   **`HTTP 2.0`**: 支持多路复用，允许同时发送多个请求并在一个连接上接收响应（无需按顺序），进一步提高效率。
-   **`HTTP 3.0`**: 旨在通过使用 `UDP` 协议（QUIC）替代 `TCP` 来减少连接建立延迟，提高速度（处于实验阶段）。