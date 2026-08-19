## Part 1 传输层提供的服务

- 功能
	- 传输层实现了“端到端”（进程到进程）的通信
	- 在TCP或UDP报文段首部指明源端口和目的端口
- ![Pasted image 20251231153145](images/Pasted%20image%2020251231153145.png)
- ![Pasted image 20251231153459](images/Pasted%20image%2020251231153459.png)
- 
- ![Pasted image 20251231153052](images/Pasted%20image%2020251231153052.png)
- 有连接与无连接
	- ![Pasted image 20251231154016](images/Pasted%20image%2020251231154016.png)
- 可靠传输与不可靠传输
	- ![Pasted image 20251231154054](images/Pasted%20image%2020251231154054.png)
- ![Pasted image 20251231153747](images/Pasted%20image%2020251231153747.png)



- 传输层寻址与端口

- 无连接服务和面向连接服务

## Part 2 UDP协议
### 1. UDP数据报
- ![Pasted image 20260101003819](images/Pasted%20image%2020260101003819.png)
- 格式
	- ![Pasted image 20260101003938](images/Pasted%20image%2020260101003938.png)
	- ![Pasted image 20260101003958](images/Pasted%20image%2020260101003958.png)
- ![Pasted image 20260101004021](images/Pasted%20image%2020260101004021.png)


### 2. UDP检验
- 检验方法
	- ![Pasted image 20260101004132](images/Pasted%20image%2020260101004132.png)
	- ![Pasted image 20260101004205](images/Pasted%20image%2020260101004205.png)
- ![Pasted image 20260101004242](images/Pasted%20image%2020260101004242.png)
- ![Pasted image 20260101004257](images/Pasted%20image%2020260101004257.png)
- ![Pasted image 20260101004332](images/Pasted%20image%2020260101004332.png)

- ![Pasted image 20260101004442](images/Pasted%20image%2020260101004442.png)

## Part 3 TCP
- ![Pasted image 20260101003856](images/Pasted%20image%2020260101003856.png)
- TCP段
	- ![Pasted image 20260101004515](images/Pasted%20image%2020260101004515.png)
	- ![Pasted image 20260101005124](images/Pasted%20image%2020260101005124.png)
	- ![Pasted image 20260101004709](images/Pasted%20image%2020260101004709.png)
	- ![Pasted image 20260101004743](images/Pasted%20image%2020260101004743.png)
	- ![Pasted image 20260101004946](images/Pasted%20image%2020260101004946.png)
	- ![Pasted image 20260101005051](images/Pasted%20image%2020260101005051.png)
	- ![Pasted image 20260101005303](images/Pasted%20image%2020260101005303.png)
	- ![Pasted image 20260101004837](images/Pasted%20image%2020260101004837.png)
	- ![Pasted image 20260101004901](images/Pasted%20image%2020260101004901.png)
	- ![Pasted image 20260101005206](images/Pasted%20image%2020260101005206.png)
	- ![Pasted image 20260101005405](images/Pasted%20image%2020260101005405.png)

- ![Pasted image 20260101004610](images/Pasted%20image%2020260101004610.png)
- ![Pasted image 20260101005013](images/Pasted%20image%2020260101005013.png)
- ![Pasted image 20260101004640](images/Pasted%20image%2020260101004640.png)

- TCP连接管理
	- ![Pasted image 20260101005500](images/Pasted%20image%2020260101005500.png)
	- ![Pasted image 20260101005509](images/Pasted%20image%2020260101005509.png)
	- ![Pasted image 20260101005530](images/Pasted%20image%2020260101005530.png)
	- ![Pasted image 20260101005631](images/Pasted%20image%2020260101005631.png)
	- ![Pasted image 20260101005710](images/Pasted%20image%2020260101005710.png)
	- ![Pasted image 20260101005725](images/Pasted%20image%2020260101005725.png)
	- ![Pasted image 20260101005833](images/Pasted%20image%2020260101005833.png)
	- ![Pasted image 20260101005856](images/Pasted%20image%2020260101005856.png)
	- ![Pasted image 20260101005924](images/Pasted%20image%2020260101005924.png)
	- ![Pasted image 20260101005942](images/Pasted%20image%2020260101005942.png)

- TCP可靠传输与流量控制
	- ![Pasted image 20260101010040](images/Pasted%20image%2020260101010040.png)
	- ![Pasted image 20260101010103](images/Pasted%20image%2020260101010103.png)
	- ![Pasted image 20260101010122](images/Pasted%20image%2020260101010122.png)
	- ![Pasted image 20260101010138](images/Pasted%20image%2020260101010138.png)
	- ![Pasted image 20260101010534](images/Pasted%20image%2020260101010534.png)
	- ![Pasted image 20260101010202](images/Pasted%20image%2020260101010202.png)
	- ![Pasted image 20260101010249](images/Pasted%20image%2020260101010249.png)
	- ![Pasted image 20260101010322](images/Pasted%20image%2020260101010322.png)
	- ![Pasted image 20260101010506](images/Pasted%20image%2020260101010506.png)
	- ![Pasted image 20260101010559](images/Pasted%20image%2020260101010559.png)
	- ![Pasted image 20260101010644](images/Pasted%20image%2020260101010644.png)
	- ![Pasted image 20260101010653](images/Pasted%20image%2020260101010653.png)
	- ![Pasted image 20260101010723](images/Pasted%20image%2020260101010723.png)
 
- TCP拥塞控制
	- ![Pasted image 20260101010849](images/Pasted%20image%2020260101010849.png)
	- ![Pasted image 20260101010914](images/Pasted%20image%2020260101010914.png)
	- ![Pasted image 20260101010935](images/Pasted%20image%2020260101010935.png)
	- ![Pasted image 20260101010951](images/Pasted%20image%2020260101010951.png)
	- ![Pasted image 20260101011007](images/Pasted%20image%2020260101011007.png)
	- ![Pasted image 20260101011031](images/Pasted%20image%2020260101011031.png)
	- ![Pasted image 20260101011105](images/Pasted%20image%2020260101011105.png)
	- ![Pasted image 20260101011157](images/Pasted%20image%2020260101011157.png)
	- ![Pasted image 20260101011306](images/Pasted%20image%2020260101011306.png)
	- ![Pasted image 20260101011317](images/Pasted%20image%2020260101011317.png)
	- 
	- 

![Pasted image 20260101005230](images/Pasted%20image%2020260101005230.png)