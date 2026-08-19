## Part 1 基础介绍
### Section 1 门电路概念
- 逻辑门电路（门电路）：实现基本和常用逻辑运算的电子电路
- 基本门电路：与门，或门，非门（反相器），与非门....
- 逻辑0和1：分别用低电平（0-0.8V）和高电平（2.4-5V）表示
- 正逻辑和负逻辑：正逻辑是1是高电平，0是低电平；负逻辑相反。
### Section 2 半导体二极管
- 特点：具有单向导电特性
- 结构示意图：
![Pasted image 20241013095917](images/Pasted%20image%2020241013095917.png)

电流可以从P到N，不能从N到P。（P区是空穴区（B），N是多了一个电子区）
- 原理
-电子从N->P扩散，会形成一个电场（电子进入空穴区，形成如图所示电场）。于是电子扩散N->P，电子受力N<-P，当扩散的力和电场的力相等会达成一个平衡，其他电子无法另一侧扩散。
-中间存在电场的部分就是耗尽层（PN结），当外接电源时，P区接阳极，N区接阴极。当可以抵消掉内电场时，平衡打破，N区电子移向P区，可以输送电流，电路导通。但是如果反向接外部电源，耗尽层扩大，P区空穴增多。

![Pasted image 20241013103325](images/Pasted%20image%2020241013103325.png)

如图当电压小于0.5V时处于死区，也就是还没有抵消

- 二极管会有开通时间延迟和关断时间延迟，开通时间会比关断时间短得多。

### Section 3 半导体三极管
- 特点：具有放大能力，能够通过基极电流$i_B$控制其工作状态。

![Pasted image 20241013103922](images/Pasted%20image%2020241013103922.png)

集电区为普通浓度N型掺杂，基区为高浓度P型掺杂，发射区为高浓度N型掺杂，bc通正极电源，e通负极电源。

b正极电源吸走一个电子，基区出现一个空穴，但是发射区浓度太高（c也会将集电区电子输到发射区）就会有很多电子挤到基区抢那一个空穴，空穴填完后剩下的电子会扩散到集电区$i_b$电流到c就会放大$\beta$倍（$i_c=\beta i_b$）。（放大是瞬间即逝的），可以看出$i_b$的控制作用

### Section 4 MOS管
- 特点：具有放大能力，通过栅极电压控制工作状态。

![Pasted image 20241013105823](images/Pasted%20image%2020241013105823.png)

-S是源极（source），G是栅极（gate），D是漏极（drain）
- 主体是一个这样的结构：
![Pasted image 20241013111108](images/Pasted%20image%2020241013111108.png)
下面的金属板替换成了PN区域，上面金属板带正电，下面带负电。
上层金属板电子到P区后填充，连接了左右的N区，N区连通后下面部分就变成了一个PN结，同时也连通了漏极和源极。当电压高于阈值电压是导通（维持N沟道）

在数字电路中，MOS管不是工作在截止区，就是工作在可变电阻区，恒流区只是一种瞬间即逝的过渡状态。导通后$u_{GS}$对$i_D$的控制作用越强，放大作用越强。

PMOS和NMOS相反，高于阈值不导通，低于导通

## Part 2 分立元器件门电路
### Section 1 二极管与门和或门

- 与门
![Pasted image 20241013115811](images/Pasted%20image%2020241013115811.png)

![屏幕截图 2024-10-13 120052](images/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE%202024-10-13%20120052.png)

- 或门
![Pasted image 20241013120626](images/Pasted%20image%2020241013120626.png)

![Pasted image 20241013120651](images/Pasted%20image%2020241013120651.png)

### Section 2 三极管非门（反相器）
- 半导体三极管非门

![Pasted image 20241013120826](images/Pasted%20image%2020241013120826.png)

![Pasted image 20241013120805](images/Pasted%20image%2020241013120805.png)

- MOS三极管非门
![Pasted image 20241013120959](images/Pasted%20image%2020241013120959.png)

![Pasted image 20241013121022](images/Pasted%20image%2020241013121022.png)


## Part 3 CMOS集成电路

### Section 1 CMOS反相器

![Pasted image 20241013121118](images/Pasted%20image%2020241013121118.png)

- 当A接入正向偏压，NMOS导通，PMOS不导通，相当于输出$u_B$接$V_{SS}$（接地电压），输出相对低压；当A低于阈值电压（反向偏压），PMOS通，NMOS不通，接$V_{DD}$（供电电压）输出相对高压。

### Section 2 CMOS与非门、或非门
- CMOS与非门
![Pasted image 20241013121734](images/Pasted%20image%2020241013121734.png)

-工作原理
![Pasted image 20241013121802](images/Pasted%20image%2020241013121802.png)

![Pasted image 20241013121828](images/Pasted%20image%2020241013121828.png)

- CMOS或非门
![Pasted image 20241013121856](images/Pasted%20image%2020241013121856.png)

![Pasted image 20241013121942](images/Pasted%20image%2020241013121942.png)

--与一般从0下手，或一般从1手

### Section 3  与门，或门
- 其实就是上面两个门加上反相器

### Section 4 带缓冲的CMOS与非门和或非门
NMOS阈值电压为证，PMOS阈值电压为负。
输入电压上升时，NMOS导通更快。
输入电压下降时，PMOS关闭更快。

- 需要带缓冲的原因
1. 从输出端看，电路不对称，从而导致输出特性不对称
2. 使电路的电压传输特性发生偏移，阈值电压不再是0.5$V_{DD}$因此导致了噪声容限下降。

![Pasted image 20241013122600](images/Pasted%20image%2020241013122600.png)

- 在基本电路的输入端和输出端都加上反相器作为缓冲级后，其输入特性和输出特性就与反相器没有区别了，这不仅改善了电路的电器特性，同时也给使用者带来的方便。

### Section 5 CMOS与或非门和异或门
- 与或非门
![Pasted image 20241013122824](images/Pasted%20image%2020241013122824.png)

- 异或门
![Pasted image 20241013122934](images/Pasted%20image%2020241013122934.png)

![Pasted image 20241013122948](images/Pasted%20image%2020241013122948.png)

-也可以用与非门组合
![Pasted image 20241013123016](images/Pasted%20image%2020241013123016.png)

### Section 6 CMOS传输门、三态门和漏极开路门

- 传输门
![Pasted image 20241013125918](images/Pasted%20image%2020241013125918.png)

- MOS管结构是对称的，所以信号可以双向传输，C都是控制信号，u1是倍传输的模拟电压。
- 传输门实际上是一种可以传送模拟信号的压控开关，也可以传输数字信号。
![Pasted image 20241013130244](images/Pasted%20image%2020241013130244.png)

- 三态门（TSL门）
![Pasted image 20241013130259](images/Pasted%20image%2020241013130259.png)

-有三种状态：1，0，高阻态（相当于没有）

![Pasted image 20241013130501](images/Pasted%20image%2020241013130501.png)

- 漏极开路门（OD门）
1. 必须外接电源
2. 具有线与功能（可以把输出端连起来实现与运算，不用加与门）

![Pasted image 20241013130723](images/Pasted%20image%2020241013130723.png)

## Part 4 TTL集成门电路
- 特点：输入级和输出级都是半导体三极管。

### Section 1 反相器
![Pasted image 20241013131029](images/Pasted%20image%2020241013131029.png)

![Pasted image 20241013131046](images/Pasted%20image%2020241013131046.png)

![Pasted image 20241013131105](images/Pasted%20image%2020241013131105.png)

### Section 2 与非门、或非门

- 与非门
![屏幕截图 2024-10-13 131249](images/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE%202024-10-13%20131249.png)

- 或非门
![Pasted image 20241013131510](images/Pasted%20image%2020241013131510.png)

![Pasted image 20241013131532](images/Pasted%20image%2020241013131532.png)

### Section 3 与门、或门、与或非门、异或门

![Pasted image 20241013131743](images/Pasted%20image%2020241013131743.png)

- 异或
![Pasted image 20241013131811](images/Pasted%20image%2020241013131811.png)

### Section 4 集电极开路门（OC门）和三态门
![Pasted image 20241013131912](images/Pasted%20image%2020241013131912.png)

- 功能同CMOS

- 三态门
![Pasted image 20241013132033](images/Pasted%20image%2020241013132033.png)

![Pasted image 20241013132104](images/Pasted%20image%2020241013132104.png)

## Part 5 CMOS与TTL

1. 输入端不应悬空：
对TTL：悬空为1
对CMOS：悬空为0

- 处理：
	- 与，与非：接电源或输入端并联
	- 或，或非：接地或输入端并联

2. 线与功能：只有OC和OD
![Pasted image 20241013132502](images/Pasted%20image%2020241013132502.png)

