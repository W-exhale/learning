- Servlet是一个能处理HTTP请求，发送HTTP响应的小程序，而发送响应就是获取`PrintWriter`，然后输出HTML：
```java
PrintWriter pw = resp.getWriter();
pw.write("<html>");
pw.write("<body>");
pw.write("<h1>Welcome, " + name + "!</h1>");
pw.write("</body>");
pw.write("</html>");
pw.flush();
```

但是用PrintWriter输出HTML不但要正确编写HTML，还要插入各种变量。如果想要在Servlet中输出一个类似新浪首页的HTML，写对HTML基本上不太可能。

- 可以使用JSP！：JSP本身目前已经很少使用，我们只需要了解其基本用法即可。
JSP是Java Server Pages的缩写，它的文件必须放到`/src/main/webapp`下，文件名必须以`/jsp`结尾，整个文件与HTML没有太大区别，但需要插入变量，或者动态输出的地方，使用特殊指令`<% ... %>`

```jsp
<html>
<head>
	<title>Hello World - JSP</title>
</head>
<body>
	<%-- JSP Comment--%>
	<h1>Hello World!</h1>
	<p>
	<%
		out.println("Your IP address is ");	
	%>
	<span style="color:red">
	<%= request.getRemoteAddr() %>
	</span>
	</p>
</body>
</html>
```

整个JSP的内容实际上是一个HTML，但是有点不一样
- `<%-- --%>`是JSP的注释
- `<% %>`中间是Java代码
- `<%= request.getRemoteAddr() %>`可以快捷输出一个变量的值

JSP页面内置了变量：（可以直接使用）
- `out`：表示HttpServletResponse的PrintWriter；
- `session`：表示当前HttpSession对象
- `request`：表示HttpServletRequest对象

访问JSP页面时，直接指定完整路径。例如，`http://localhost:8080/hello.jsp`

- JSP和Servlet的区别：
其实没有任何区别，因为JSP在执行前首先被编译成一个Servlet。
在Tomcat的临时目录下，可以找到一个`hello_jsp.java`的源文件，这个文件就是Tomcat把JSP自动转换成Servlet源码：
```java
package org.apache.jsp;
import ...

public final class hello_jsp extends org.apache.jasper.runtime.HttpJspBase implements org.apache.jasper.runtime.JspSourceDependent, org.apache.jasper.runtime.JspSourceImports{
...
    public void _jspService(final javax.servlet.http.HttpServletRequest request, final javax.servlet.http.HttpServletResponse response)
        throws java.io.IOException, javax.servlet.ServletException {
        ...
        out.write("<html>\n");
        out.write("<head>\n");
        out.write("    <title>Hello World - JSP</title>\n");
        out.write("</head>\n");
        out.write("<body>\n");
        ...
    }
    ...
}
```

JSP本质上就是一个Servlet，不过不用配置映射路径，Web Server会根据路径查找对应的`.jsp`文件，如果找到了，就自动编译成Servlet再执行。在服务器运行过程中，如果修改了JSP的内容，服务器也会自动重新编译。

## JSP高级功能
JSP的指令非常复杂，除了`<% ... %>`，JSP页面本身可以通过`page`指令引入Java类：
```jsp
<% page import="java.io.*" %>
<%@ page import="java.util.*" %>
```

这样后续的java代码才能引用简单类名而不是完整类名。

使用`include`指令可以引入另一个JSP文件：
```jsp
<html>
<body>
    <%@ include file="header.jsp"%>
    <h1>Index Page</h1>
    <%@ include file="footer.jsp"%>
</body>
```

## JSP Tag
JSP还允许自定义输出的tag，例如：
```jsp
<c:out value = "${sessionScope.user.name}"/>
```

JSP Tag需要正确引入taglib的jar包，并且还需要正确声明，使用起来非常复杂，对于页面开发来说，_不推荐_ 使用JSP Tag，因为我们后续会介绍更简单的模板引擎，这里我们不再介绍如何使用taglib。