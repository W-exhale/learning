
> [!NOTE] Java 网络编程优势
> 使用 Java 进行网络编程时，Java 虚拟机 (JVM) 封装了底层复杂的网络协议。开发者只需调用 Java 标准库提供的 API，即可简单高效地编写网络程序。

## Part 1 网络编程基础

### 计算机网络与互联网
*   **计算机网络**: 两台或更多的计算机组成的网络，在同一个网络内，遵循**相同网络协议**的计算机可以直接通信。

*   **互联网 (Internet)**: 网络的网络，将全球范围内的不同计算机网络连接起来。

*   **TCP/IP 协议**: 为了让使用不同内部协议的网络能够互联，接入互联网**必须**使用 TCP/IP 协议簇。

### IP地址
> [!INFO] 定义
>在互联网中，一个IP地址用于唯一标识一个网络接口（Network Interface）。一台联入互联网的计算机肯定有一个IP地址，但也可能有多个IP地址。
*   **IP地址版本**:
    *   **IPv4**: 32 位地址 (e.g., `101.202.99.12`)，约 42 亿个地址，已经耗尽。
    *   **IPv6**: 128 位地址 (e.g.,`2001:0DA8:100A:0000:0000:1020:F2F3:1428`)，（大约340万亿亿亿亿）数量巨大，足以满足未来需求。
*   **类型**:
    *   **公网 IP**: 可在互联网上直接访问。
    *   **内网 IP**: 仅在局域网内部访问 (e.g., `192.168.x.x`, `10.x.x.x`)。
*   **特殊地址**:
    *   **本机地址 (localhost)**: 总是 `127.0.0.1`。

*   **IPv4 与整数**: IPv4 地址本质上是一个 32 位整数。
    ```
    1707762444 (Decimal)
    = 0x65ca630c (Hex)
    = 65  ca  63  0c (Hex bytes)
    = 101.202.99.12 (Dotted Decimal)
    ```

### 网络通信基础

*   **多网卡**: 一台计算机可以有多个网卡，每个网卡有自己的 IP 地址，可以接入不同的网络。（不包括网卡，电脑自己有个本机IP地址）
*   **路由器/交换机**: 连接不同网络的设备，至少有两个 IP 地址，用于在网络间转发数据。
*   **同一网络通信**: 如果两台计算机的**网络号**相同，则它们在同一网络，可以直接通信。
    *   **网络号**: 通过 IP 地址和**子网掩码**进行按位与运算 (`&`) 得到。（转化为二进制算完了转回十进制）
    *   **示例**:
        ```plain
        IP      = 101.202.99.2
        Mask    = 255.255.255.0
        Network = IP & Mask = 101.202.99.0
        ```
*   **不同网络通信**: 如果网络号不同，不能直接通信，则需要通过**网关**（通常是路由器）进行间接通信。
*   **网关 (Gateway)**: 连接多个网络，负责将数据包从一个网络路由到另一个网络。（将一个网络的数据包发到另一个网络的过程叫路由）

- 一台计算机的一个网卡会有3个关键配置：
	![Pasted image 20250423120312](images/Pasted%20image%2020250423120312.png)
    1.  **IP 地址**: e.g., `192.168.112.117`
    2.  **子网掩码**: e.g., `255.255.255.0`
    3.  **网关 IP 地址**: e.g., `192.168.112.116`

### 域名 (Domain Name)
*   **目的**: 由于 IP 地址难于记忆，使用域名来访问网络服务。
*   **DNS (Domain Name System)**: 域名解析服务器，负责将域名翻译成对应的 IP 地址。

- 客户端再根据IP地址访问服务器。

*   **`nslookup` 命令**: 用于查询域名对应的 IP 地址。
    ```plain
    $ nslookup liaoxuefeng.com
    Server:  xxx.xxx.xxx.xxx  # DNS 服务器地址
    Address: xxx.xxx.xxx.xxx#53 # DNS 服务器地址和端口

    Non-authoritative answer: # 非权威应答
    Name:    liaoxuefeng.com  # 查询的域名
    Address: xxx.xxx.xxx.xxx  # 域名对应的 IP 地址
    ```

*   **特殊域名**: `localhost` 总是解析为本机地址 `127.0.0.1`。
### 网络模型

> [!INFO] 分层模型
> 为了简化复杂性、标准化接口，计算机网络采用分层模型。

**OSI**（Open System Interconnect）网络模型是ISO组织定义的一个计算机互联的标准模型，注意它只是一个定义，目的是为了简化网络各层的操作，提供标准接口便于实现和维护。

*   **OSI 七层模型 (理论模型)**:
	- 应用层，提供应用程序之间的通信；
	- 表示层：处理数据格式，加解密等等；
	- 会话层：负责建立和维护会话；
	- 传输层：负责提供端到端的可靠传输；
	- 网络层：负责根据目标地址选择路由来传输数据；
	- 链路层和物理层负责把数据进行分片并且真正通过物理网络传输，例如，无线网、光纤等。

*   **TCP/IP 模型 (实际使用)**:

| OSI 模型             | TCP/IP 模型     | 主要协议/功能        |
| :------------------- | :-------------- | :------------------- |
| 应用层、表示层、会话层 | **应用层**      | HTTP, FTP, SMTP, DNS |
| 传输层               | **传输层**      | TCP, UDP             |
| 网络层               | **IP 层 (网络层)** | IP, ICMP, ARP        |
| 数据链路层、物理层   | **网络接口层**  | Ethernet, Wi-Fi      |

### 常用协议
*   **IP (Internet Protocol)**:
    *   网络层协议。
    *   负责数据包的寻址和路由（分组交换）。
    *   **无连接**，**不可靠**传输（不保证到达、顺序或无差错）。
    * 只负责发数据包，不保证顺序和正确性
*   **TCP (Transmission Control Protocol)**:
    *   传输层协议，建立在 IP 之上。
    *   **面向连接的协议**: 通信前需建立连接（三次握手），结束后需断开连接（四次挥手）。
    *   **可靠传输**: 通过序列号、确认应答 (ACK)、超时重传、流量控制、拥塞控制等机制保证数据正确、有序到达。
    *   **双向通信**: 允许双方同时收发数据。
    *   应用广泛，是 HTTP, SMTP, FTP 等协议的基础。
    * 负责控制数据包传输，它在传输数据之前需要先建立连接，建立连接后才能传输数据，传输完后还需要断开连接。
*   **UDP (User Datagram Protocol)**:
    *   数据报文协议，传输层协议，建立在 IP 之上。
    *   **无连接**: 通信前无需建立连接。
    *   **不可靠传输**: 不保证数据包到达、顺序或无差错，尽力而为。
    *   **效率高**: 开销比 TCP 小。（因为UDP协议在通信前不需要建立连接）
    *   适用于能容忍少量数据丢失的场景，如实时音视频、DNS 查询。


> [!SUMMARY] 网络基础概念回顾
> *   **计算机网络**: 多台计算机组成的集合。
> *   **互联网**: 连接网络的网络。
> *   **IP 地址**: 网络接口的唯一标识。
> *   **网关**: 连接不同网络的设备，负责路由。
> *   **网络协议**: 通信规则，互联网主要使用 TCP/IP 协议簇。
> *   **IP 协议**: 分组交换，不可靠。
> *   **TCP 协议**: 面向连接，可靠传输。
> *   **UDP 协议**: 无连接，不可靠传输，效率高。

## Part 2 TCP编程
### Socket 概念
> [!INFO] Socket 定义
> Socket（套接字）是网络编程中的一个**抽象概念**。
> 应用程序通过 Socket 来建立远程连接并进行数据传输。
> 操作系统负责 Socket 底层的 TCP/IP 实现。（Socket内部通过TCP/IP协议把数据传输到网络）
> ![Pasted image 20250423142520](images/Pasted%20image%2020250423142520.png)
> Java 的 `java.net.Socket` 和 `java.net.ServerSocket` 类是对操作系统 Socket 接口的封装。
> - Socket、TCP和部分IP的功能都是由操作系统提供的，不同的编程语言只是提供了对操作系统调用的简单的封装。

*   **为什么需要 Socket?**:
    *   仅凭 IP 地址无法区分同一台主机上的不同网络应用程序（如浏览器、QQ）。
	    * 同一台计算机同一时间会运行多个网络应用程序，例如，浏览器、QQ、邮件客户端等。
	    * 当操作系统接收到一个数据包的时候，如果只有IP地址，它没法判断应该发给哪个应用程序。
    *   操作系统使用 Socket（IP 地址 + **端口号**（范围是0-65535））来将接收到的数据包正确地分发给对应的应用程序。
	    * 操作系统抽象出Socket接口，每个应用程序需要各自对应到不同的Socket，数据包才能根据Socket正确地发到对应地应用程序
*   **端口号 (Port)**:
    *   0 - 65535 之间的数字。
    *   用于标识主机上的特定应用程序或服务。
    *   **0 - 1023**: 特权端口（Well-known Ports），通常分配给标准服务（如 `HTTP:80`,` HTTPS:443`），需要管理员权限才能监听。
    *   **1024 - 65535**: 动态或私有端口，可由普通用户程序使用。
*   **Socket = IP 地址 + 端口号**:
    *   e.g., `101.202.99.2:1201` (浏览器), `101.202.99.2:1304` (QQ)

### TCP Client/Server 模型
使用Socket进行网络编程时，本质是**进程间通信**。

其中一个进程必须充当服务器端，会主动监听某个指定的端口；
另一个进程必须充当客户端，必须主动连接服务器的IP地址和指定端口

*   **服务器端 (Server)**:
    *   被动方。
    *   启动后监听**指定**的 IP 地址和端口号，等待客户端连接。
*   **客户端 (Client)**:
    *   主动方。
    *   需要知道服务器的 IP 地址和端口号，并发起连接请求。
*   **连接建立**:
    *   一旦连接成功，就建立了一个 TCP 连接。
    *   服务器端的 Socket 是: `服务器IP:指定端口`。
    *   客户端的 Socket 是: `客户端IP:随机端口` (由操作系统分配)。
    *   双方可以通过各自的 Socket 进行双向数据传输。

### 服务器端实现 (Java)
> [!NOTE] 使用 `ServerSocket`
要使用Socket编程，我们要首先编写服务器端程序。
Java 标准库使用 `java.net.ServerSocket` 来实现服务器端的监听。

```java
import java.io.*;
import java.net.*;
import java.nio.charset.StandardCharsets;

public class Server {
    public static void main(String[] args) throws IOException {
        // 1. 创建 ServerSocket，监听指定端口 (6666)
        //    不指定 IP 表示监听本机所有网络接口
		ServerSocket ss = new ServerSocket(6666); 
        System.out.println("Server is running on port 6666...");
        // 2. 无限循环，等待客户端连接
        for (;;) {
        // 3. 接受连接: accept() 方法会阻塞，直到有客户端连接，
        //新的客户端连接进来后，就返回一个Socket实例，这个Socket实例就是用来和刚连接的客户端进行通信的。
            Socket sock = ss.accept(); 
            System.out.println("connected from " + sock.getRemoteSocketAddress());
            
            // 4. 为每个连接创建一个新线程处理，实现并发，因为客户端很多，所以必须为每个新的Socket创建一个新线程来处理
            //    (也可使用线程池提高效率)
            Thread t = new Handler(sock); 
            //这样，主线程的作用就是接收新的连接，每当收到一个新连接后，就创建一个新线程进行处理。
            t.start();
        }
         // 注意：实际应用中 ServerSocket 也应在合适的时机关闭，
        //      例如通过添加关闭服务器的逻辑。
    }
}
// 处理客户端连接的线程
class Handler extends Thread {
    Socket sock;

    public Handler(Socket sock) {
        this.sock = sock;
    }

   @Override
    public void run() {
        // 使用 try-with-resources 确保流和 Socket 被关闭
        try (InputStream input = this.sock.getInputStream();
             OutputStream output = this.sock.getOutputStream())
        {
            handle(input, output);
        } catch (Exception e) {
            System.out.println("Client disconnected: " + sock.getRemoteSocketAddress() + " Error: " + e.getMessage());
        } finally {
            try {
                // 确保 Socket 在任何情况下都被关闭
                this.sock.close();
            } catch (IOException ioe) {
                // ignore
            }
        }
    }
	// 处理具体通信逻辑
    private void handle(InputStream input, OutputStream output) throws IOException {
	    // 使用 BufferedReader 和 BufferedWriter 提高效率
        var writer = new BufferedWriter(new OutputStreamWriter(output, StandardCharsets.UTF_8));
        var reader = new BufferedReader(new InputStreamReader(input, StandardCharsets.UTF_8));
        
        // 发送欢迎消息
        writer.write("Welcome!\n");
        writer.flush(); // 确保消息发送出去

		// 循环读取客户端消息
        for (;;) {
            String s = reader.readLine();// 读取一行
            if (s == null || s.equalsIgnoreCase("bye")) {  // 客户端断开或发送 "bye"
                writer.write("bye\n");
                writer.flush();
                break;
            }
            // 回显消息
            writer.write("Server received: " + s + "\n");
            writer.flush(); // 每次写入后刷新缓冲区
        }
    }
}
```

*   **`accept()` 行为**:
    *   如果没有客户端连接进来，阻塞等待连接。
    *   若同时有多个连接请求，`ServerSocket` 会将它们放入队列，`accept()` 逐个取出处理。
*   **并发处理**: 使用多线程或线程池是必要的，避免主线程阻塞，能够同时服务多个客户端。

### 客户端实现 (Java)

> [!NOTE] 使用 `Socket`
> Java 标准库使用 `java.net.Socket` 来实现客户端连接。

```java
import java.io.*;
import java.net.*;
import java.nio.charset.StandardCharsets;
import java.util.Scanner;

public class Client {
    public static void main(String[] args) throws IOException {
	    // 1. 创建 Socket，指定服务器 IP (或域名) 和端口，如果连接成功，将返回一个Socket实例，用于后续通信。
        //    "localhost" 或 "127.0.0.1" 表示本机
        Socket sock = new Socket("localhost", 6666); 
        System.out.println("Connected to server " + sock.getRemoteSocketAddress());
        // 2. 使用 try-with-resources 获取输入输出流并确保关闭
        try (InputStream input = sock.getInputStream()) {
            try (OutputStream output = sock.getOutputStream()) {
                handle(input, output);
            }
        }
        // 3. 关闭 Socket 连接
        sock.close();
        System.out.println("disconnected.");
    }
	// 处理具体通信逻辑
    private static void handle(InputStream input, OutputStream output) throws IOException {
        var writer = new BufferedWriter(new OutputStreamWriter(output, StandardCharsets.UTF_8));
        var reader = new BufferedReader(new InputStreamReader(input, StandardCharsets.UTF_8));
        Scanner scanner = new Scanner(System.in);  // 用于读取用户控制台输入
        // 读取服务器的欢迎消息
        System.out.println("[Server] " + reader.readLine());

		// 循环发送和接收消息
        for (;;) {
            System.out.print(">>> "); // 提示用户输入
            String s = scanner.nextLine(); // 读取一行输入
            // 发送消息到服务器
            writer.write(s);
            writer.newLine();  // 发送换行符，因为服务器端使用 readLine()
            writer.flush();  // 刷新缓冲区，确保数据发送
            // 读取服务器响应
            String resp = reader.readLine();
            if (resp == null) { // 服务器断开连接
	            System.out.println("[Server] Connection closed.");
	            break;
	        }
	            
            System.out.println("<<< [Server] " + resp);
            // 如果收到 "bye"，则退出循环
            if (resp.equalsIgnoreCase("bye")) {
                break;
            }
        }
    }
}
```

### Socket流
*   TCP 是**基于流**的协议，数据像水流一样传输。
*   所以Java 使用 `InputStream` 和 `OutputStream` 来封装 Socket 的数据流，操作方式与文件 IO 流类似。

```java
// 获取输入流，用于从 Socket 读取数据
InputStream in = sock.getInputStream();
// 获取输出流，用于向 Socket 写入数据
OutputStream out = sock.getOutputStream();
```

*   **缓冲与 `flush()`**:

> [!WARNING] `flush()` 的重要性
> 当使用 `OutputStream` (特别是包装后的 `BufferedWriter` 或 `BufferedOutputStream`) 向 Socket 写入数据时，数据通常会先写入**内存缓冲区**。
> 只有当缓冲区满或**显式调用 `flush()`** 时，数据才会被真正发送到网络。
> **忘记调用 `flush()` 可能导致对方长时间收不到数据！**
> 这是为了提高网络传输效率

## Part 3 UDP编程

> [!INFO] UDP 特点
> *   **简单性**: UDP 编程比 TCP 简单。
> *   **无连接**: 不需要建立和断开连接。
> *   **数据包导向**: 一次收发一个完整的数据包 (`DatagramPacket`)。
> *   **无流概念**: 不像 TCP 那样使用 `InputStream`/`OutputStream`。
> *   **仍需 Socket**: 应用程序需要通过 `DatagramSocket` 指定 IP 和端口来收发数据。

> [!NOTE] TCP vs UDP 端口
> TCP 端口和 UDP 端口是**独立**的两套系统。一个应用程序使用 TCP 占用了端口 8080，不影响另一个应用程序使用 UDP 占用端口 8080。


### 服务器端 (UDP)

> [!NOTE] 使用 `DatagramSocket` 监听
> Java 使用 `java.net.DatagramSocket` 来监听指定的 UDP 端口并接收数据包。

**核心步骤**:

1.  **创建 `DatagramSocket`**: 绑定到要监听的端口。
2.  **准备缓冲区**: 创建 `byte[]` 数组用于接收数据。
3.  **创建 `DatagramPacket`**: 将缓冲区与 `DatagramPacket` 关联，用于接收。
4.  **接收数据**: 调用 `ds.receive(packet)`，此方法会**阻塞**直到收到一个 UDP 包。
5.  **处理数据**: 从 `packet` 中提取数据、来源 IP 和端口。
6.  **（可选）发送响应**: 创建新的 `DatagramPacket`（或重用收到的 `packet` 并修改其内容和目标地址/端口），然后调用 `ds.send(packet)` 发送。

```java
import java.net.*;
import java.nio.charset.StandardCharsets;

public class UdpServer {
    public static void main(String[] args) throws Exception {
		// 1. 监听指定端口 (e.g., 6666)
		DatagramSocket ds = new DatagramSocket(6666); 
		System.out.println("UDP Server is running on port 6666...");
//如果没有其他应用程序占据这个端口，那么监听成功，我们就使用一个无限循环来处理收到的UDP数据包：
		for (;;) { // 无限循环
		    // 2. 准备接收缓冲区:准备一个byte[]缓冲区接收一个UDP数据包
		    byte[] buffer = new byte[1024];
		    
		    //3. 创建 DatagramPacket 用于接收
		    DatagramPacket packet = new DatagramPacket(buffer, buffer.length);
		    
		    try {
			    // 4. 接收 UDP 数据包 (阻塞)
			    ds.receive(packet); 
			    
			    // 5. 处理数据
			    //指定收取到的数据在缓冲区（buffer）的长度
			    int len = packet.getLength();
			    //指定数据在缓冲区的起始位置
	            int offset = packet.getOffset();
	            // 将其按UTF-8编码转换为String:（假设收取到的是String）
			    String s = new String(packet.getData(), offset, len, StandardCharsets.UTF_8);
			    
				// 获取客户端地址和端口
				InetAddress clientAddr = packet.getAddress();
				int clientPort = packet.getPort();
				System.out.println("Received from " + clientAddr + ":" + clientPort + " -> " + receivedData);
				
				//6. 发送响应（ACK）
				byte[] responseData = ("ACK: " + receivedData).getBytes(StandardCharsets.UTF_8);
				// 重用 packet 对象，设置响应数据、目标地址和端口
				packet.setData(responseData);
				
				// packet.setAddress(clientAddr); // 地址已在 packet 中
				// packet.setPort(clientPort);   // 端口已在 packet 中
				
			    ds.send(packet);
			    System.out.println("Sent ACK to " + clientAddr + ":" + clientPort);
			} catch (Exception e) {
	                System.err.println("Error processing packet: " + e.getMessage());
	        }
	    }
    }  
}
```

> [!IMPORTANT] 服务器响应
> 服务器收到 UDP 包后，通常需要**立即回复**。因为 UDP 是无连接的，服务器只能通过收到的 `DatagramPacket` 获取客户端的 IP 和端口信息，以便将响应发送回去。如果不回复，客户端可能无法确认服务器是否收到消息。

### 客户端 (UDP)

> [!NOTE] 使用 `DatagramSocket` 发送和接收
> 客户端也使用 `DatagramSocket`，但通常不指定端口（由操作系统分配），只需要直接向服务器端发送UDP包，然后接收返回的UDP包。

**核心步骤**:

1.  **创建 `DatagramSocket`**: 通常不指定端口。
2.  **（可选）设置超时**: 使用 `ds.setSoTimeout()` 防止 `receive()` 无限期阻塞。后续接收UDP包时，等待时间最多不会超过1秒，否则在没有收到UDP包时，客户端会无限等待下去。
	1. 这一点和服务器端不一样，服务器端可以无限等待，因为它本来就被设计成长时间运行。
3.  **（可选）连接服务器**: 使用 `ds.connect()` 指定默认的服务器地址和端口。这不是真正的连接，只是设置默认目标，并进行安全检查。
	1. 它是为了在客户端的DatagramSocket实例中保存服务器端的IP和端口号，
	2. 确保这个DatagramSocket实例只能往指定的地址和端口发送UDP包，不能往其他地址和端口发送。
	3. 这么做不是UDP的限制，而是Java内置了安全检查。
4.  **准备数据**: 将要发送的数据转换为 `byte[]`。
5.  **创建 `DatagramPacket`**: 包含数据、数据长度、目标服务器地址和端口。
6.  **发送数据**: 调用 `ds.send(packet)`。
	1. 通常来说，客户端必须先发UDP包，因为客户端不发UDP包，服务器端就根本不知道客户端的地址和端口号。
7.  **（可选）接收响应**: 准备缓冲区和 `DatagramPacket`，调用 `ds.receive(packet)`。
8.  **（可选）断开连接**: 使用 `ds.disconnect()` 清除 `connect()` 设置的默认目标。
	1. 不是真正地断开连接，它只是清除了客户端DatagramSocket实例记录的远程服务器地址和端口号，这样，DatagramSocket实例就可以连接另一个服务器端。
9.  **关闭 `DatagramSocket`**: 调用 `ds.close()`。


```java
import java.net.*;
import java.nio.charset.StandardCharsets;
import java.util.Scanner;

public class UdpClient {
    public static void main(String[] args) throws Exception {
		// 1. 创建 DatagramSocket (不指定端口，由 OS 分配)
		DatagramSocket ds = new DatagramSocket();
		
		// 2. 设置接收超时 (1 秒)
		ds.setSoTimeout(1000);// 1000ms = 1s
		
		// 3. "连接" 到服务器 (设置默认目标地址和端口)
		InetAddress serverAddr = InetAddress.getByName("localhost");
        int serverPort = 6666;
        ds.connect(serverAddr, serverPort); 
        
		//也可以直接用Hello代表message
		 Scanner scanner = new Scanner(System.in);
		System.out.print("Enter message to send: ");
		String message = scanner.nextLine();
		
		// 4. 准备数据
		byte[] data = message.getBytes(StandardCharsets.UTF_8);
        // 5. 创建 DatagramPacket (使用 connect 后，无需指定地址和端口)
        DatagramPacket packetToSend = new DatagramPacket(data, data.length);
        // 6. 发送数据
        ds.send(packetToSend);
        System.out.println("Sent: " + message);
        
        // 7. 接收响应
        try {
			byte[] buffer = new byte[1024];
            DatagramPacket packetToReceive = new DatagramPacket(buffer, buffer.length);
            ds.receive(packetToReceive); // 等待最多 1 秒
            
            String response = new String(packetToReceive.getData(), packetToReceive.getOffset(), packetToReceive.getLength(), StandardCharsets.UTF_8);
            System.out.println("Received ACK: " + response);
        } catch (SocketTimeoutException e) {
            System.out.println("Receive timed out.");
        }
		// 8. 断开 "连接" (清除默认目标)
		ds.disconnect();
		System.out.println("UDP Client disconnected (default target cleared).");
		
        // 9. 关闭 Socket
        ds.close();
        System.out.println("UDP Client closed.");
        scanner.close();
    }
}

```

> [!TIP] 客户端必须先发送
> 通常，UDP 客户端必须先发送数据包给服务器，这样服务器才能知道客户端的 IP 地址和端口号，从而能够将响应发送回来。

### 向多个服务器发送 UDP 包

如果客户端需要与多个不同的 UDP 服务器通信，有两种主要方式：

1.  **创建多个 `DatagramSocket`**: 每个 `DatagramSocket` 实例使用 `connect()` 连接到一个特定的服务器。
2.  **使用一个 `DatagramSocket` (不 `connect`)**: 在创建每个 `DatagramPacket` 时，**显式指定**目标服务器的 `InetAddress` 和端口号。


不调用`connect()`方法的代码如下：
```java
import java.net.*;
import java.nio.charset.StandardCharsets;

public class UdpMultiSendClient {
    public static void main(String[] args) throws Exception {
        // 创建 DatagramSocket (不 connect)
        DatagramSocket ds = new DatagramSocket();
        ds.setSoTimeout(1000); // 设置接收超时

        // 服务器 1 地址和端口
        InetAddress server1Addr = InetAddress.getByName("localhost");
        int server1Port = 6666;
        // 服务器 2 地址和端口
        InetAddress server2Addr = InetAddress.getByName("localhost"); // 假设是同一台机器
        int server2Port = 8888;

        // 发送到服务器 1
        byte[] data1 = "Hello Server 1".getBytes(StandardCharsets.UTF_8);
        DatagramPacket packet1 = new DatagramPacket(data1, data1.length, server1Addr, server1Port);
        ds.send(packet1);
        System.out.println("Sent to " + server1Addr + ":" + server1Port);
        // (可以尝试接收 server1 的响应)

        // 发送到服务器 2
        byte[] data2 = "Hi Server 2".getBytes(StandardCharsets.UTF_8);
        DatagramPacket packet2 = new DatagramPacket(data2, data2.length, server2Addr, server2Port);
        ds.send(packet2);
        System.out.println("Sent to " + server2Addr + ":" + server2Port);
        // (可以尝试接收 server2 的响应)

        // 关闭 Socket
        ds.close();
        System.out.println("UDP Client closed.");
    }
}
```

## Part 4 发送Email

> [!INFO] 邮件传输过程
> 传统的邮件发送
> - 邮件——>邮局-->另一个邮局——>用户的邮箱
> 
> 电子邮件的发送也涉及几个关键角色：
> *   **MUA (Mail User Agent)**: 邮件用户代理，即我们使用的邮件客户端软件（如 Outlook, Foxmail）或网页版邮箱。
> *   **MTA (Mail Transfer Agent)**: 邮件传输代理，即邮件服务器，负责将邮件从 MUA 转发出去，或在不同的邮件服务器之间传递。
> *   **MDA (Mail Delivery Agent)**: 邮件投递代理，邮件最终到达的服务器，负责将邮件存入用户的邮箱，等待用户收取。
>
> **流程**: MUA (发件人客户端) -> MTA (发件服务器) -> ... -> MTA (中转服务器) -> MDA (收件服务器) -> MUA (收件人客户端)
>
>邮件一到MDA就不动了，通常存储在MDA服务器的硬盘上，等收件人通过软件或者登录浏览器查看邮件

MUA 到 MTA 发送邮件使用的协议是 **SMTP (Simple Mail Transport Protocol)**。
*   **标准端口**: `25`
*   **加密端口**: `465` (SSL/TLS) 或 `587` (STARTTLS)

MTA和MDA这样的服务器软件通常是现成的，我们不关心这些服务器内部是如何运行的。要发送邮件，我们关心的是如何编写一个MUA的软件，把邮件发送到MTA上。

> [!NOTE] JavaMail API
> SMTP 是一个基于 TCP 的协议。使用 Java 发送邮件时，我们不需要手动实现 SMTP 协议细节，可以使用 **JavaMail API** 这个标准库来简化操作。

### 准备SMTP登录信息
要发送邮件（例如，从 `me@example.com` 发给 `xiaoming@somewhere.com`），你需要知道：

1.  **MTA 服务器地址**: 通常格式为 `smtp.服务商域名` (e.g., `smtp.qq.com`, `smtp.163.com`, `smtp.gmail.com`, `smtp.office365.com`)。
2.  **端口号**: 由邮件服务商指定（`25`, `465`, 或 `587`）。
3.  **登录信息**:
    *   **用户名**: 通常是你的完整邮箱地址。
    *   **密码/授权码**: 邮箱登录密码或专门为 SMTP 设置的授权码/应用密码（出于安全考虑，很多服务商推荐使用授权码）。

**常用邮箱 SMTP 信息示例**:
*   **QQ邮箱**: `smtp.qq.com`, 端口 `465`/`587`
*   **163邮箱**: `smtp.163.com`, 端口 `465`
*   **Gmail邮箱**: `smtp.gmail.com`, 端口 `465`/`587`
*   **Outlook/Office365**: `smtp.office365.com`, 端口 `587`


1. 我们需要创建一个Maven工程，并把JavaMail相关的两个**依赖**加入进来：
![Pasted image 20250424084124](images/Pasted%20image%2020250424084124.png)
*(注意: 旧版本可能使用 `javax.mail` groupId)

2. **连接 SMTP 服务器 (JavaMail)**:
```java
import javax.mail.*;
import javax.mail.internet.*;
import java.util.Properties;

//1. 基本信息
// 服务器地址:
String smtpHost = "smtp.office365.com"; // e.g., Outlook
// 端口号 (使用 STARTTLS):
String smtpPort = "587";
// 登录用户名 (完整邮箱地址):
String username = "your-email@outlook.com";
// 登录口令 (密码或授权码):
String password = "your-password-or-app-code";

//2. 准备Properties对象，填入相关信息
// 连接到SMTP服务器587端口:
Properties props = new Properties();
props.put("mail.smtp.host", smtpHost); // SMTP主机名
props.put("mail.smtp.port", smtpPort); // 主机端口号
props.put("mail.smtp.auth", "true"); // 是否需要用户认证
props.put("mail.smtp.starttls.enable", "true"); // 启用 STARTTLS 加密 (对于 587 端口)

// 如果使用 465 端口 (SSL/TLS)，则配置可能不同:
// props.put("mail.smtp.socketFactory.port", "465");
// props.put("mail.smtp.socketFactory.class", "javax.net.ssl.SSLSocketFactory");
// props.put("mail.smtp.ssl.enable", "true"); // 显式启用 SSL

// 3. 获取 Session 实例 (带身份验证)，需要认证传入Authenticator对象，并返回指定的用户名和口令
Session session = Session.getInstance(props, new Authenticator() {
	@Override
    protected PasswordAuthentication getPasswordAuthentication() {
        return new PasswordAuthentication(username, password);
    }
});
//4. 开启 Debug 模式，打印详细通信过程，便于调试
session.setDebug(true);
System.out.println("Session created successfully.");
// 后续使用 session 对象发送邮件
```

> [!TIP] 调试模式
> `session.setDebug(true);` 会在控制台打印详细的 SMTP 命令交互过程，非常有助于排查连接和认证问题。

### 发送邮件
获取 `Session` 后，构造一个 `MimeMessage` 对象，调用`Transport.send(Message)`即可完成发送：

```java
try {
	//1. 创建MimeMessage 对象
	MimeMessage message = new MimeMessage(session);
	//设置发件人（From），通常与登录用户名一致
	message.setFrom(new InternetAddress(username)); //使用登录邮箱作为发件人
	
	// 设置收件人（To）:
	message.setRecipient(Message.RecipientType.TO, new InternetAddress("xiaoming@somewhere.com"));

    // 可添加多个收件人、抄送 (CC)、密送 (BCC)
    // message.addRecipient(Message.RecipientType.CC, new InternetAddress("cc@example.com"));
    // message.addRecipient(Message.RecipientType.BCC, new InternetAddress("bcc@example.com"));

	// 设置邮件主题:
	message.setSubject("Hello", "UTF-8"); // 指定 UTF-8 编码防止乱码
	
	// 设置邮件正文 (Body) - 纯文本
	message.setText("Hi Xiaoming...", "UTF-8");
	// 发送邮件
	Transport.send(message);
	System.out.println("Email sent successfully!");
} catch (MessagingException e) {
    System.err.println("Error sending email: " + e.getMessage());
    e.printStackTrace();
}
```

> [!WARNING] 发件人地址
> 大多数邮件服务器要求 `setFrom()` 设置的发件人地址必须与 SMTP 登录时使用的用户名（邮箱地址）**完全一致**，否则会因权限问题（如 `SendAsDeniedException`）导致发送失败。

**SMTP 通信示例 (Debug 输出)**:
![Pasted image 20250424084556](images/Pasted%20image%2020250424084556.png)

SMTP 是一个请求-响应协议。客户端发送命令（如 `EHLO`, `AUTH LOGIN`, `MAIL FROM`, `RCPT TO`, `DATA`），然后等待服务器响应，服务器响应返回状态码和信息。信息是用于调试的文本。以下是状态码
*   `2xx`: 成功
*   `3xx`: 需要进一步操作
*   `4xx`: 临时性错误
*   `5xx`: 永久性错误
(参考: [SMTP Enhanced Status Codes](https://www.iana.org/assignments/smtp-enhanced-status-codes/smtp-enhanced-status-codes.txt))
![Pasted image 20250424084839](images/Pasted%20image%2020250424084839.png)

### 发送HTML邮件
只需在 `setText` 时指定 `contentType` 为 `text/html`：

```java
message.setText(body, "UTF-8");
//改为
message.setText(body, "UTF-8", "html");
```

传入的`body`是类似`<h1>Hello</h1><p>Hi, xxx</p>`这样的HTML字符串即可。

```java
// ... 创建 message 对象 ...
String htmlBody = "<h1>Hello!</h1><p>This is an <b>HTML</b> email sent from <a href='https://www.example.com'>JavaMail</a>.</p>";

// 设置 HTML 正文，传入的htmlBody是类似<h1>Hello</h1><p>Hi, xxx</p>这样的HTML字符串即可。
message.setContent(htmlBody, "text/html; charset=utf-8"); // 指定 MIME 类型和字符集

// ... 设置其他属性并发送 ...
Transport.send(message);
```

HTML 邮件在客户端会渲染成网页样式：
![Pasted image 20250424084815](images/Pasted%20image%2020250424084815.png)

### 发送附件
- 不能之间调用`message.setText()`方法，要构造一个`Multipart`对象来组合邮件的不同部分（正文、附件等）。

```java
import javax.activation.DataHandler;
import javax.activation.FileDataSource; // 用于从文件添加附件

// import javax.mail.util.ByteArrayDataSource; // 用于从字节数组添加附件

// ... 创建 message 对象 ...
//...

// 1. 创建 Multipart 对象 (用于组合邮件内容)
Multipart multipart = new MimeMultipart();

// 2. 添加text:
BodyPart messageBodyPart = new MimeBodyPart();
String htmlBody = "<p>Please find the attached file.</p>";
//BodyPart依靠setContent()决定添加的内容，如果添加文本，用setContent("...", "text/plain;charset=utf-8")添加纯文本
//用setContent("...", "text/html;charset=utf-8")添加HTML文本
messageBodyPart.setContent(htmlBody, "text/html; charset=utf-8");
multipart.addBodyPart(messageBodyPart); // 添加到 Multipart

// 3. 添加image:(创建附件部分)
BodyPart attachmentBodyPart = new MimeBodyPart();
String filename = "path/to/your/attachment.pdf"; //文件路径

DataSource source = new FileDataSource(filename);
attachmentBodyPart.setDataHandler(new DataHandler(source)); // 设置附件数据源
attachmentBodyPart.setFileName("document.pdf"); // 设置在邮件中显示的文件名
//传入文件的MIME类型。二进制文件可以用application/octet-stream，Word文档则是application/msword。
// 可选: 设置 Content-Type (通常 JavaMail 会自动检测)
// attachmentBodyPart.setHeader("Content-Type", "application/pdf");
multipart.addBodyPart(attachmentBodyPart);   // 添加到 Multipart
// 4. 将 Multipart 设置为邮件内容
message.setContent(multipart);

// ... 设置其他属性 (From, To, Subject) 并发送 ...
Transport.send(message);
```
![Pasted image 20250424085650](images/Pasted%20image%2020250424085650.png)

*   `setContent(body, "text/html;charset=utf-8")` 用于设置 HTML 正文。
*   `setContent(body, "text/plain;charset=utf-8")` 用于设置纯文本正文。
*   附件通过 `setDataHandler()` 添加，使用 `DataSource` (如 `FileDataSource` 或 `ByteArrayDataSource`)。
*   `setFileName()` 指定附件在邮件中显示的名字。
*   常见的 MIME 类型：`application/octet-stream` (通用二进制), `application/pdf`, `application/msword`, `image/jpeg`, `image/png`。


### 发送内嵌图片的HTML邮件

> [!WARNING] 外部图片链接
> HTML 邮件中的 `<img src="http://...">` 外部图片链接通常会被邮件客户端阻止显示，以保护用户隐私和安全。要可靠地显示图片，应将其**内嵌**到邮件中。

内嵌图片实际上也是一个附件，即邮件本身也是`Multipart`，但需要在 HTML 中通过 `cid:` (Content-ID) 引用，并在附件部分设置对应的 `Content-ID` Header。

```java
// ... 创建 message 对象 ...

// 1. 创建 Multipart 对象 (类型为 "related" 表示内嵌资源)
Multipart multipart = new MimeMultipart("related");

// 2. 创建 HTML 正文部分 (引用 cid)
BodyPart htmlPart = new MimeBodyPart();
String htmlBody = "<h1>Check this out!</h1><p>Here is an embedded image: <img src=\"cid:image01\"></p>";
textpart.setContent("<h1>Hello</h1><p><img src=\"cid:img01\"></p>", "text/html;charset=utf-8");
htmlPart.setContent(htmlBody, "text/html; charset=utf-8");

// 3. 创建图片附件部分 (设置 Content-ID)
BodyPart imagepart = new MimeBodyPart();
String imagePath = "path/to/your/image.jpg";
DataSource imageSource = new FileDataSource(imagePath);
imagePart.setDataHandler(new DataHandler(imageSource));
imagePart.setFileName("logo.jpg"); // 可选的文件名
// 关键：设置 Content-ID，与 HTML 中的 <img src="cid:image01"> 对应
imagePart.setHeader("Content-ID", "<image01>");
// 设置为 inline，表示是内嵌资源
imagePart.setDisposition(MimeBodyPart.INLINE);
multipart.addBodyPart(imagepart);

// 4. 将 Multipart 设置为邮件内容
message.setContent(multipart);

// ... 设置其他属性并发送 ...
Transport.send(message);
```

*   HTML 中使用 `<img src="cid:some-unique-id">`。
*   对应的图片 `BodyPart` 需要设置 `setHeader("Content-ID", "<some-unique-id>")`。
*   设置 `setDisposition(MimeBodyPart.INLINE)` 告知客户端这是内嵌资源。

### 常见问题
*   **`535 Authentication Failed` / `Authentication unsuccessful`**:
    *   原因：用户名或密码/授权码错误。
    *   检查：确认邮箱地址和密码/授权码正确，确认邮箱开启了 SMTP 服务并允许了客户端登录。
```plain
DEBUG SMTP: AUTH LOGIN failed
Exception in thread "main" javax.mail.AuthenticationFailedException: 535 5.7.3 Authentication unsuccessful [HK0PR03CA0105.apcprd03.prod.outlook.com]
```

*   **`554 SendAsDeniedException` / `Client not authenticated to send anonymous mail`**:
    *   原因：`setFrom()` 设置的发件人地址与 SMTP 登录用户不匹配，服务器不允许代发。
    *   检查：确保 `setFrom()` 的地址就是登录 SMTP 的邮箱地址。

```plain
DEBUG SMTP: MessagingException while sending, THROW: 
com.sun.mail.smtp.SMTPSendFailedException: 554 5.2.0 STOREDRV.Submission.Exception:SendAsDeniedException.MapiExceptionSendAsDenied;
```

*   **`554 DT:SPM` / 被识别为垃圾邮件**:
    *   原因：邮件内容（主题、正文）过于简单、包含敏感词、发送频率过高、发件人信誉低等。
    *   尝试：丰富邮件内容，避免常用垃圾邮件特征，检查发件邮箱是否被列入黑名单。

```plain
DEBUG SMTP: MessagingException while sending, THROW: 
com.sun.mail.smtp.SMTPSendFailedException: 554 DT:SPM
```

> [!TIP] 排查错误
> 仔细查看 `session.setDebug(true)` 输出的 SMTP 交互日志，特别是服务器返回的 `5xx` 错误码和描述信息，这是定位问题的关键。

> [!SUMMARY] Part 4: 发送 Email (SMTP)
> *   邮件发送涉及 MUA, MTA, MDA，使用 SMTP 协议 (端口 25, 465, 587)。
> *   JavaMail API 简化了邮件发送过程。
> *   需要配置 SMTP 服务器地址、端口、用户名、密码/授权码，并设置 `Properties`。
> *   使用 `Session` 和 `Authenticator` 进行连接和认证。
> *   `MimeMessage` 用于构建邮件，设置发件人、收件人、主题、正文。
> *   `Transport.send()` 发送邮件。
> *   HTML 邮件通过 `message.setContent(html, "text/html")` 发送。
> *   附件和内嵌图片需要使用 `Multipart` 和 `BodyPart` 构建。
> *   内嵌图片通过 `cid:` 和 `Content-ID` Header 关联。
> *   常见错误包括认证失败 (535)、代发拒绝 (554)、垃圾邮件 (554)。开启 Debug 模式有助于排查。
