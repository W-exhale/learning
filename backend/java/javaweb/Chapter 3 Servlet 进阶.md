## Servlet 映射与覆写
### Servlet映射
一个 Web App 由一个或多个 Servlet 组成，每个 Servlet 通过注解 **`@WebServlet`** 说明自己能处理的路径。

```java
@WebServlet(urlPatterns = "/hello")
public class HelloServlet extends HttpServlet {
    // ...
}
```

上述`HelloServlet`能处理`/hello`这个路径的请求。

>[!NOTE] 提示
>早期的Servlet需要在web.xml中配置映射路径，但最新Servlet版本只需要通过注解就可以完成映射。

- 浏览器发送请求时，会指定请求方法（HTTP Method），即`GET`、`POST`、`PUT`等不同类型的请求。

- 要处理`GET`请求，我们要覆写`doGet()`方法：
```java
@WebServlet(urlPatterns = "/hello")
public class HelloServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        // ... 处理 GET 请求 ...
    }
}
```

- 要处理`POST`请求，就需要覆写`doPost()`方法。
	- 如果没有覆写`doPost()`方法，服务器会直接返回405（Method Not Allowed）或400（Bad Request）错误。
- 一个Servlet如果映射到`/hello`，那么所有请求方法都会由这个Servlet处理，能不能返回200要看有没有覆写对应的请求方法。

### 多个Servlet与请求分发(Dispatch)
一个Webapp可以有多个Servlet，分别映射不同的路径
```java
@WebServlet(urlPatterns = "/hello")
public class HelloServlet extends HttpServlet {
    ...
}

@WebServlet(urlPatterns = "/signin")
public class SignInServlet extends HttpServlet {
    ...
}

@WebServlet(urlPatterns = "/")
public class IndexServlet extends HttpServlet {
    ...
}
```

- **请求分发**(dispatch)：浏览器发出的HTTP请求总是由Web Server先接收，然后，根据Servlet配置的映射，不同的路径转发到不同的Servlet：
```
               ┌ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┐

               │            /hello    ┌───────────────┐│
                          ┌────────▶│ HelloServlet  │
               │          │           └───────────────┘│
┌───────┐    ┌──────────┐ │ /signin   ┌───────────────┐
│Browser│─▶│Dispatcher │─┼──────────▶│ SignInServlet ││
└───────┘    └──────────┘ │           └───────────────┘
               │          │ /         ┌───────────────┐│
                          └────────▶│ IndexServlet  │
               │                      └───────────────┘│
                              Web Server
               └ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┘
```

- 特殊映射`/`：
映射到`/`的`IndexServlet`比较特殊，它实际上会接收所有未匹配的路径，相当于`/*`，因为Dispatcher的逻辑可以用伪代码实现如下：
```java
String path = request.getRequestURI();
if (path.equals("/hello")) {
    dispatchTo(helloServlet);
} else if (path.equals("/signin")) {
    dispatchTo(signinServlet);
} else {
    // 所有未匹配的路径均转发到"/"
    dispatchTo(indexServlet);
}
```

## HttpServletRequest
`HttpServletRequest`封装了一个HTTP请求的所有信息，继承自`ServletRequest`（早期设计目标是支持 HTTP 以外的协议，所以单独抽出了`ServletRequest`接口，但实践中主要用于 HTTP）。

通过`HttpServletRequest`提供的接口方法可以拿到HTTP请求的几乎全部信息，常用方法：

- `getMethod()`：返回请求方法，例如`"GET"`，`"POST"`；
- `getRequestURI()`：返回请求路径，不含查询参数，例如`"/hello"`
- `getQueryString()`：返回 URL 中的查询字符串，例如，`"name=Bob&a=1&b=2"`
- `getParameter(name)`：返回请求参数，GET请求从URL读取参数，POST请求从Body中读取参数
- `getContentType()`：获取请求Body的 MIME 类型，例如，`"application/x-www-form-urlencoded"`；
- `getContextPath()`：获取当前Webapp挂载的路径（WebApp 的部署路径 (Context Path)），对于ROOT来说，总是返回空字符串`""`
- `getCookies()`：返回请求中携带的所有 Cookie 对象数组 (`Cookie[]`).
- `getHeader(name)`：获取指定的Header，Header名称不区分大小写
- `getHeaderNames()`：返回所有Header名称的枚举(`Enumeration<String>`).
- `getInputStream()`：获取用于读取请求体内容的二进制输入流 (`ServletInputStream`).
- `getReader()`：获取用于读取请求体内容的字符输入流 (`BufferedReader`).
- `getRemoteAddr()`：返回客户端的IP地址；
- `getScheme()`：返回协议类型，例如：`http`，`https`

> [!WARNING] 注意
> 调用 `HttpServletRequest` 的方法时，务必查阅文档，了解其可能的返回值，特别是可能返回 `null` 的情况（如 `getQueryString()`）。

**请求范围属性**:
- `HttpServletRequest` 还提供了 **`setAttribute(String name, Object o)`** 和 **`getAttribute(String name)`** 方法
- get允许在请求处理过程中附加数据，这使得 `HttpServletRequest` 可以像一个 `Map<String, Object>` 一样在同一次请求的不同处理阶段（例如，在 Filter 和 Servlet 之间，或在 Servlet 转发到 JSP 时）传递信息。

## HttpServletResponse
- **`HttpServletResponse`** 对象用于封装 HTTP 响应。构建响应时，必须遵循 HTTP 协议的规则：**先设置 Header，再写入 Body**。

常用的设置Header的方法有：

*   **`setStatus(int sc)`**: 设置 HTTP 响应状态码 (e.g., `HttpServletResponse.SC_OK` 即 200)。默认是 200。
*   **`setContentType(String type)`**: 设置响应体的 MIME 类型 (e.g., `"text/html"`）
*   **`setCharacterEncoding(String charset)`**: 设置响应的字符编码 (e.g., `"UTF-8"`). 通常应与 `setContentType` 结合使用，如 `response.setContentType("text/html;charset=UTF-8")`.
*   **`setHeader(String name, String value)`**: 设置一个 Header 的值。如果已存在同名 Header，此方法会覆盖旧值。
*   **`addHeader(String name, String value)`**: 添加一个 Header。允许存在多个同名的 Header。
*   **`addCookie(Cookie cookie)`**: 向响应中添加一个 `Set-Cookie` Header。

**写入响应体**:（二选一）
*   通过 **`getOutputStream()`** 获取二进制输出流 (`ServletOutputStream`)。
*   通过 **`getWriter()`** 获取字符输出流 (`PrintWriter`)。

**关于 `Content-Length` 和流的关闭**:
- 写入响应前，无需设置`setContentLength()`，因为底层服务器会根据写入的字节数（数据量）自动设置，或者在数据量较大时使用 Chunked Transfer Encoding。
	- 如果写入的数据量很小，实际上会先写入缓冲区
	- 如果写入的数据量很大，服务器会自动采用Chunked编码让浏览器能识别数据结束符而不需要设置Content-Length头
- 写入响应数据后，必须调用输出流的`flush()`方法，确保缓冲区内容被发送到客户端。

> [!IMPORTANT] 关键点
> 写入响应体后，调用 `flush()` 而不是 `close()`。因为Web服务器通常会复用TCP连接(HTTP Keep-Alive)，调用`close()`会关闭底层TCP连接，阻止复用


有了`HttpServletRequest`和`HttpServletResponse`这两个高级接口，我们就无需关心底层 HTTP 协议的细节和具体 Web 服务器的实现。
我们编写的Web应用程序只关心接口方法，并不需要关心具体实现的子类。

## Servlet 多线程模型
*   **单实例**: 对于每个 Servlet 类，Web 服务器通常只创建一个实例。
*   **多线程处理**: 每个进入的 HTTP 请求由一个单独的线程处理。这意味着同一个 Servlet 实例的 `doGet()`, `doPost()` 等方法会被**多线程并发执行**。

如果在 Servlet 中定义了实例变量（成员变量），必须特别注意**线程安全**问题，因为多个线程会同时访问这些共享变量：
```java
public class HelloServlet extends HttpServlet {
    // 这个 map 会被多个线程并发访问，需要使用线程安全的集合
    private Map<String, String> map = new ConcurrentHashMap<>();

    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        // 注意读写map字段是多线程并发的:
        this.map.put(key, value);
    }
}
```

*   **请求/响应对象的线程安全性**：对于每个请求，Web服务器会创建唯一的`HttpServletRequest`和`HttpServletResponse`实例，
* `HttpServletRequest`和`HttpServletResponse`实例只有在当前处理线程中有效，它们总是局部变量，不存在多线程共享的问题。

## 重定向与转发
### Redirect (重定向)
- **重定向 (Redirect)**：一种服务器指令，告知浏览器当前请求的资源已移动到新的 URL，浏览器需要向这个新 URL **重新发起请求**。
假如我们已经编写了一个能处理`/hello`的HelloServlet，如果收到的路径为`/hi`，希望能重定向到`/hello`，可以再编写一个`RedirectServlet`：
```java
@WebServlet(urlPatterns = "/hi")
public class RedirectServlet extends HttpServlet{
	protected void doGet(HttpServletRequest req, HttpServletResponse resp) throw ServletException, IOException{
		//构造重定向的路径：
		String name = req.getParameter("name");
		String redirectToUrl = "/hello" + (name == null ? "" : "?name=" + name); // 保留参数
		// 发送重定向响应 (默认 302)
		resp.sendRedirect(redirectToUrl);
	}
}
```

**过程**:
1.  浏览器发送 `GET /hi?name=Bob` 请求。
2.  `RedirectServlet` 处理请求，调用 `resp.sendRedirect("/hello?name=Bob")`。
3.  服务器返回一个 **302 Found** 响应给浏览器，其中 `Location` Header 指向 `/hello?name=Bob`。浏览器会收到如下响应
```plain
HTTP/1.1 302 Found
Location: /hello
```
4.  浏览器收到 302 响应后，自动向 `Location` 指定的新 URL (`/hello?name=Bob`) 发起一个新的 `GET` 请求。
5.  `HelloServlet` 处理这个新的请求并返回最终响应。
```
┌───────┐   GET /hi       ┌───────────────┐
│Browser│ ────────────▶ │RedirectServlet│
│       │ ◀──────────── │               │
└───────┘   302           └───────────────┘


┌───────┐  GET /hello     ┌───────────────┐
│Browser│ ────────────▶ │ HelloServlet  │
│       │ ◀──────────── │               │
└───────┘   200 <html>    └───────────────┘
```

可以在浏览器的网络请求中看到两次HTTP请求，并且地址栏路径自动更新为`/hello`：![[Pasted image 20250430145950.png]]
- 重定向有两种：
    *   **302 Found**: 临时重定向。浏览器下次访问 `/hi` 仍会先请求 `/hi`。`resp.sendRedirect()` 默认使用 302。
    *   **301 Moved Permanently**: 永久重定向。浏览器可能会缓存这个重定向关系，下次直接请求 `/hello`。可以通过 `setStatus` 和 `setHeader` 实现：
```java
resp.setStatus(HttpServletResponse.SC_MOVED_PERMANENTLY); // 301
resp.setHeader("Location", "/hello");
```

- 重定向目的：当Web应用升级后，如果请求路径发生了变化，可以将原来的路径重定向到新路径，从而避免浏览器请求原路径找不到资源
### Forward (转发)
Forward：内部转发。在 **服务器内部** 将当前请求的处理权交给另一个 Servlet（或 JSP 等资源）。这个过程对浏览器是透明的。

假如我们已经编写了一个能处理`/hello`的`HelloServlet`，继续编写一个能处理`/morning`的`ForwardServlet`：
```java
@WebServlet(urlPatterns = "/morning")
public class ForwardServlet extends HttpServlet{
	protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException{
		// 将请求转发给路径为 "/hello" 的 Servlet 处理
		req.getRequestDispatcher("/hello").forward(req, resq);
		// 注意：forward之后，当前 Servlet 不应再向 response 写入任何内容
	}
}
```

**过程**:
1.  浏览器发送 `GET /morning` 请求。
2.  `ForwardServlet` 开始处理请求。
3.  `ForwardServlet` 调用 `req.getRequestDispatcher("/hello").forward(req, resp)`。
4.  Web 服务器内部将同一个 `HttpServletRequest` 和 `HttpServletResponse` 对象传递给 `/hello` 对应的 `HelloServlet`。
5.  `HelloServlet` 继续处理请求，并最终生成响应发送给浏览器。

```
                          ┌────────────────────────┐
                          │      ┌───────────────┐ │
                          │ ──▶│ForwardServlet │ │
┌───────┐  GET /morning   │      └───────────────┘ │
│Browser│ ─────────────▶ │              │         │
│       │ ◀───────────── │              ▼         │
└───────┘    200 <html>   │      ┌───────────────┐ │
                          │ ◀──│ HelloServlet  │ │
                          │      └───────────────┘ │
                          │       Web Server       │
                          └────────────────────────┘
```

*   **浏览器行为**: 浏览器只发出了一次 `GET /morning` 请求，并收到了最终的响应。地址栏的 URL **保持不变** (`/morning`)。浏览器不知道服务器内部发生了转发。
*   **请求对象**: 转发过程中使用的是**同一个** `HttpServletRequest` 和 `HttpServletResponse` 对象。这意味着在 `ForwardServlet` 中通过 `req.setAttribute()` 设置的属性，可以在 `HelloServlet` 中通过 `req.getAttribute()` 获取到。
*   **用途**: 常用于 MVC 模式中，Controller (Servlet) 处理业务逻辑后，将数据放入 `request` 域，然后 forward 到 View (JSP) 进行渲染。

> [!TIP] Redirect vs Forward 关键区别
> *   **Redirect**: 浏览器参与，发起两次请求，URL 地址栏改变。
> *   **Forward**: 服务器内部完成，浏览器只发起一次请求，URL 地址栏不变。

## 使用Session和Cookie

- 在Web应用程序中，跟踪用户状态至关重要。当一个用户登录成功后，如果继续访问其他页面，Web程序需要识别该用户

- HTTP协议是一个无状态协议，即Web应用程序无法区分收到的两个HTTP请求是否是同一个浏览器发出的。
- 为了解决这个问题并实现状态跟踪，Web服务器通常采用以下机制：
	*   服务器为每个用户（或更准确地说，每个浏览器会话）分配一个唯一的ID。
	* 这个唯一ID以 **Cookie** 的形式发送到用户的浏览器
	* 浏览器后续向该服务器发出的所有请求中，都会附带此Cookie
	* 服务器通过检查请求中的Cookie（特别是这个唯一ID），就能够识别用户并恢复其会话状态。

### Session
- 这种基于唯一ID识别和跟踪用户身份的机制称为**Session**（会话）。

**核心概念**:
*   **Session ID**: 用户首次和启用了会话管理的Web应用间交互时（或者当应用需要存储会话数据时），服务器会创建一个唯一的Session ID。这个ID随后会通过Cookie（通常是名为`JSESSIONID`的Cookie）发送给浏览器。
*   **服务器端存储**: 与Cookie主要存储在客户端不同，Session的主要数据（如用户登录信息、购物车内容、用户偏好设置等）存储在**服务器端**。浏览器只存储Session ID。
*   **生命周期**: 如果用户在一段时间后没有与服务器进行任何交互，Session会自动失效(timeout)。失效后，即使浏览器再次发送相同的旧Session ID，服务器认为是一个新用户，会分配一个新的Session ID，开始一个新的Session

JavaEE的Servlet机制内建了对Session的支持。我们可以通过`HttpServletRequest`对象轻松获取或创建`HttpSession`对象，用于存储和检索特定于用户会话的数据。

**1. 用户登录 (`SignInServlet`)**
当用户尝试登录时，如果验证成功，通过 `req.getSession()` 获取`HttpSession`对象，然后调用 `session.setAttribute("user", name)` 将用户名存入Session。
```java
@WebServlet(urlPatterns = "/signin")
public class SignInServlet extends HttpServlet{
	//模拟一个数据库：
	private Map<String, String> users = Map.of("bob", "bob123", "alice", "alice123", "tom", "tomcat");

	//GET请求时显示登录页：
	@Override
	protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException{
	resp.setContentType("text/html");
	PrintWriter pw = resp.getWriter();
        pw.write("<h1>Sign In</h1>");
        pw.write("<form action=\"/signin\" method=\"post\">");
        pw.write("<p>Username: <input name=\"username\"></p>");
        pw.write("<p>Password: <input name=\"password\" type=\"password\"></p>");
        pw.write("<p><button type=\"submit\">Sign In</button> <a href=\"/\">Cancel</a></p>");
        pw.write("</form>");
        pw.flush();
	}

	//POST请求时处理用户登录：
	@Override
	protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException{
		String name = req.getParameter("username");
		String password = req.getParameter("password");//从请求中获取表达中名为password的参数值，赋值给password
		String expectedPassword = users.get(name.toLowerCase());//校验用户身份
		if(expectedPassword != null && expectedPassword.equals(password)){
			//登录成功：
			req.getSession().setAttribute("user", name);//将用户名存储到当前会话中，标记用户已登录。
			resp.sendRedirect("/");//重定向到根路径
		} else{
				resp.sendError(HttpServletReponse.SC_FORBIDDEN);//登陆失败返回HTTP状态码403，禁止访问
				
		}
	}
}
```

**2. 首页 (`IndexServlet`)**
在其他页面，可以从`HttpSession`中取出已存入的信息来识别用户。
在`IndexServlet`中，可以从`HttpSession`取出用户名：
```java
@WebServlet(urlPatterns = "/")
public class IndexServlet extends HttpServlet {
	@Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
		//从HttpSession获取当前用户名：
		String user = (String) req.getSession().getAttribute("user");
		resp.setContentType("text/html");
		resp.setCharacterEncoding("UTF-8");
		resp.setHeader("X-Powered-By", "JavaEE Servlet");
		PrintWriter pw = resp.getWriter();
		pw.write("<h1>Welcome," + (user != null ? user : "Guest") + "</h1>");
		if(user == null){
			//未登录，显示登录链接
			pw.write("<p><a href=\"/signin\">Sign In</a></p>");
		} else{
			//已登录，显示登出链接：
			pw.write("<p><a href=\"/signout\">Sign Out</a></p>");	
		}
		pw.flush();
    }
}
```

**3. 用户登出 (`SignOutServlet`)**
用户登出时，需要从Session中移除相关信息。

- 如果用户已经登录，可以通过访问`/signout`登出。登出逻辑从`HttpSession`中移除用户相关信息：
```java
@WebServlet(urlPatterns = "/signout")
public class SignOutServlet extends HttpServlet {
	@Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        // 从HttpSession移除用户名:
        req.getSession().removeAttribute("user");
        // 或者 session.invalidate(); 销毁整个Session
        resp.sendRedirect("/"); // 重定向到首页
    }
}
```

**Session的工作机制**:
- 对于Web应用程序来说，我们总是通过`HttpSession`这个高级接口访问当前Session。Session的底层原理可以理解为：Web服务器在内存中自动维护了一个ID到`HttpSession`的映射表

```
           ┌ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ── ─ ─ ─ ─ ─ ─ ─ ─ ─  ─ ┐

           │        ┌───────────────┐                      │
             ┌───▶│ IndexServlet  │◀─────────────┐
           │ │      └───────────────┘               ▼      │
┌───────┐    │      ┌───────────────┐        ┌──────────┐
│Browser│──┼─┼───▶│ SignInServlet │◀────▶│Sessions  │  │
└───────┘    │      └───────────────┘        └──────────┘
           │ │    ┌───────────────┐                 ▲      │
             └───▶│SignOutServlet │◀─────────────┘
           │      └───────────────┘                        │

           └ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┘
```

而服务器识别Session的关键就是依靠一个通常名为`JSESSIONID`的Cookie。
- 在Servlet中第一次调用`req.getSession()`时，如果当前请求没有有效的Session ID，Servlet容器自动创建一个Session，并为其分配一个唯一的Session ID。
- 然后这个ID通过一个名为`JSESSIONID`的Cookie发送给浏览器
* 浏览器在后续的请求中会自动带上这个Cookie，服务器从而能够识别并关联到正确的`HttpSession`对象。

![[Pasted image 20250506182237.png]]


>[!IMPORTANT] 关于 `JSESSIONID` 和登录逻辑
>- `JSESSIONID`由Servlet容器自动创建和管理，主要目的是**维护浏览器与服务器之间的会话状态**，它本身与应用的登录逻辑没有直接关系。
>- 应用登录和登出的业务逻辑是我们通过在`HttpSession`中存取特定属性（例如`user`）来判断的。用户登出（清楚了`user`属性）后，`JSESSIONID`本身可能仍然存在且有效，Session也可能继续存在，直到它超时或被明确销毁
>- 即使Web应用没有登录功能，仍然可以用`HttpSession`来追踪匿名用户的行为或存储临时信息，例如用户的偏好设置、购物内容等。

>[!TIP] 其他Session追踪方式
>除了使用Cookie机制实现Session，还可以通过URL重写（在URL末尾附加Session ID）或隐藏表单字段来传递Session ID。但是很少用，常用的还是Cookie。

**Session存储和扩展性考量**:
*   **内存消耗**: 使用Session时，服务器把所有用户的Session都存储在内存中。如果并发用户量大，或者Session中存储的数据过多，会消耗大量服务器内存
	* 所以放入的Session的对象要小，通常只存储必要的标识信息或少量状态数据：
	```java
	public class User {
	public long id; // 唯一标识
	public String email;
	public String name;
	}
	```
*   **持久化**: 如果内存不足，某些Servlet容器会将部分不活动的Session序列化到磁盘上（Passivation），并在需要时重新加载会内存（Activation）。但是这会增加I/O开销，大大降低服务器的运行效率。

*   **集群环境下的Session管理**: 
在使用多台服务器构成集群时，使用Session会遇到一些额外的问题。通常多台服务器集群使用反向代理作为网站入口
```
                                        ┌────────────┐
                                 ┌───▶│Web Server 1│
                                 │      └────────────┘
┌───────┐       ┌─────────────┐   │      ┌────────────┐
│Browser│────▶ │Reverse Proxy│──┼───▶│Web Server 2│
└───────┘       └─────────────┘   │      └────────────┘
                                 │      ┌────────────┐
                                 └───▶│Web Server 3│
                                        └────────────┘
```

如果多台Web Server采用无状态(无法区分HTTP请求是否是同一个浏览器发出)集群，那么反向代理总是以轮询方式将请求依次转发给每台Web Server，这会造成一个用户在Web Server 1存储的Session信息，在Web Server2和3上不存在，即从Web Server 1登录后，如果后续请求被转发到Web Server 2 或 3，那么用户看到的仍然是未登录
- 解决
    1.  **Session复制 (Session Replication)**: 在所有Web Server之间进行Session复制，但这样会严重消耗网络带宽，而且每个Web Server的内存均存储所有用户Session，内存使用率很低。
   2.  **粘滞会话 (Sticky Sessions)**: 即反向代理在转发请求的时候根据JSESSIONID的值，相同的JSESSIONID总是转发到固定的Web Server，但这个需要反向代理的支持，并且可能导致负载不均。
   3.  **集中式Session存储**: 将Session数据存储在外部共享存储中（如Redis、Memcached等数据库）。所有Web服务器都从该中央存储读取和写入Session数据。这是目前构建可伸缩Web应用推荐的方式。

>[!WARNING] Session的适用性
>由于上述内存和集群扩展性的问题，传统的基于内存的`HttpSession`更适用于中小型Web应用程序。对于大型、高并发的Web应用程序，通常需要采用集中式Session管理方案，或者设计成无状态服务以完全避免使用服务器端Session。

### Cookie
- Servlet提供的`HttpSession`本质上是通过一个名为`JSESSIONID`的Cookie来跟踪用户会话。除了这个名称外，其他名称的Cookie我们可以任意使用。
- Cookie是服务器发送到用户浏览器并保存在本地的一小块数据。（浏览器之后向同一服务器发送的每个请求都会带上这些Cookie）。

- 如果我们要设置一个Cookie，例如，记录用户选择的语言，可以写一个`LanguageServlet`：
**1. 设置Cookie (`LanguageServlet`)**
```java
@WebServlet(urlPatterns = "/pref")
public class LanguageServlet extends HttpServlet {

    private static final Set<String> LANGUAGES = Set.of("en", "zh");//支持的语言
    
	@Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String lang = req.getParameter("lang");
        if (lang != null && LANGUAGES.contains(lang.toLowerCase())) {
		//创建一个新的Cookie：
		Cookie cookie = new Cookie("lang", lang);
		//该Cookie生效的路径范围：（对整个Web应用生效）
		cookie.setPath("/");
		//该Cookie有效期：
		cookie.setMaxAge(8640000);//100天
		// cookie.setSecure(true); // 如果只在HTTPS连接下发送，要加上
        // cookie.setHttpOnly(true); // 如果禁止JavaScript访问此Cookie，取消此行注释 (增强安全性)
		//将该Cookie添加到HTTP响应：
		resp.addCookie(cookie);
    }
	resp.sendRedirect(req.getContextPath() + "/");
}
```

**Cookie的关键属性**:
*   **名称 (Name) 和值 (Value)**: `Cookie(String name, String value)`
*   **路径 (Path)**: `setPath(String url)`
    *   指定了Cookie的有效范围。浏览器只会向Path属性匹配的路径发送Cookie。例如，如果设置为`/app/`，则只有访问`/app/*`下的资源时才会发送该Cookie。设置为`/`表示对整个域名下的所有路径都有效。
*   **有效期 (Max Age)**: `setMaxAge(int expiry)`
    *   设置Cookie的生存时间，单位为秒。
        *   正数：表示Cookie在这么多秒后过期。浏览器会将Cookie持久化到磁盘。
        *   负数（通常为-1）：表示Cookie仅在当前浏览器会话期间有效，关闭浏览器后即被删除（会话Cookie）。这是默认行为。
        *   零：表示立即删除该Cookie。
*   **安全标志 (Secure)**: `setSecure(boolean flag)`
	* 如果设置为`true`，则该Cookie只会在通过HTTPS协议加密传输时才会发送给服务器
	* 如果是访问https网页，还要调用`setSecure(true)`，否则浏览器不会发送该Cookie。
*   **HttpOnly标志**: `setHttpOnly(boolean isHttpOnly)`
    *   如果设置为`true`，则该Cookie不能通过客户端脚本（如JavaScript的`document.cookie`）访问。这有助于防范XSS（跨站脚本）攻击。


>[!INFO] 服务器发送的Set-Cookie响应头
因此，要注意：浏览器在请求某个URL时，是否携带指定的Cookie，取决于Cookie是否满足以下要求
>- URL前缀是设置Cookie时的Path；
>- Cookie在有效期内；
>- Cookie设置了secure时必须以https访问
>
>当服务器通过`resp.addCookie(cookie)`添加Cookie后，它会在HTTP响应头中包含一个或多个`Set-Cookie`字段，如下所示：![[Pasted image 20250506201830.png]]

**2. 读取Cookie (`IndexServlet`)**
我们可以从`HttpServletRequest`对象中读取浏览器发送过来的Cookie。
例如，在`IndexServlet`中，读取名为`lang`的Cookie以获取用户设置的语言，如下：
```java
private String parseLanguageFromCookie(HttpServletRequest req){
	//获取请求附带的所有Cookie：
	Cookie[] cookies = req.getCookies();
	//如果获取到Cookie：
	if (cookies != null){
		//循环每个Cookie：
		for(Cookie cookie : cookies){
			//如果Cookie名称为lang：
			if(cookie.getName().equals("lang")){
			//返回Cookie的值：
			return cookie.getValue();
			}
		}
	}
	return null;
}
```

*   **读取Cookie的逻辑**:
    *   通过 `req.getCookies()` 方法可以获取一个 `Cookie` 对象数组，包含了浏览器随请求发送过来的所有Cookie。
    *   如果没有任何Cookie，`getCookies()` 方法会返回 `null`。
    *   需要遍历这个数组，通过 `cookie.getName()` 检查每个Cookie的名称，找到我们需要的Cookie（例如，名为 "lang" 的Cookie），然后通过 `cookie.getValue()` 获取其值。

> [!TIP] 提示
> 读取Cookie主要依靠遍历 `HttpServletRequest` 附带的所有Cookie。因此，如果Cookie数量较多，这个操作可能会有轻微的性能开销。

**浏览器发送Cookie的条件**:
浏览器在向服务器发送请求时，并非无条件地发送所有存储的Cookie。一个Cookie是否会被包含在请求中，取决于它是否满足以下主要条件：

1.  **路径匹配 (Path)**:
    *   请求的URL路径必须与Cookie设置时指定的`Path`属性相匹配（或者是其子路径）。例如，如果Cookie的`Path`为`/app/`，则只有访问`/app/somepage`或`/app/subdir/anotherpage`等路径时，浏览器才会发送该Cookie。如果`Path`为`/`，则对该域名下的所有路径都有效。

2.  **有效期 (Max-Age / Expires)**:
    *   Cookie必须在其有效期内。已过期的Cookie不会被发送，并且通常会被浏览器删除。

3.  **安全标志 (Secure)**:
    *   如果Cookie设置了`Secure`标志，那么它只会在通过HTTPS加密连接请求时才会被发送。对于普通的HTTP请求，即使其他条件满足，这个Cookie也不会被发送。

4.  **域名匹配 (Domain)** (未在上述示例中设置，但也很重要):
    *   Cookie的`Domain`属性必须与请求的服务器域名匹配，或者是其父域名（如果`Domain`属性以`.`开头，如`.example.com`，则表示对所有子域名如`www.example.com`、`api.example.com`都有效）。如果未设置`Domain`，则默认为当前文档的来源主机（不包括子域名）。

5.  **HttpOnly标志**:
    *   这个标志主要影响客户端脚本对Cookie的访问，而不是浏览器是否发送它。但值得注意的是，`HttpOnly` Cookie仍然会正常发送给服务器。

因此，在调试Cookie相关问题时（例如，服务器未能按预期接收到某个Cookie），检查这些条件是否都已满足是非常重要的。