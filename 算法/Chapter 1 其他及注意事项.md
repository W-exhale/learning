## 对数器
### 原理
- 一个题目会有两种解法，一种暴力解，一种最优解，通过随机获得测试值来进行比对，如果最后比对出来的结果是正确的，那么代码就正确
### 实现
- 获得一个随机数组
```java
public static int[] randomArray(int n, int v){
	int[] arr = new int[n];
	for(int i = 0; i < n; i++){
		arr[i] = (int)(Math.random() * v) + 1;
		//Math.random()会随机生成[0,1)中的一个小数，可以看成是等概率的,v是由我们自己控制的数[0,v)，加1取整数是1-v
	}
	return arr;
}
```

- 拷贝数组
```java
public static int[] copyArray(int[] arr){
	int n = arr.length;
	int[] ans = new int[n];
	for(int i = 0; i < n; i++){
		ans[i] = arr[i];
	}
	return ans
}
```

## 二分搜索
- 找到一段有序数列（升序）中>num的最左边的数
[[二分找最左边.excalidraw|二分解析]]
- 代码实现
```java
public static int findLeft(int[] arr, int num){  
    int l = 0;  
    int r = arr.length - 1;  
    int m = 0;  
    int target = -1;  //目标的数  
    while(l <= r){  
        m = l + ((r - l)>>1);//这种写法更安全，防溢出，要注意加括号>>优先级低于+
        if(arr[m] > num){  
            target = arr[m];  
            r = m - 1;  
        }else{  
            l = m + 1;  
        }  
    }  
    return target;  
}
```

- 找到小于num最右边的数
```java
package com.company.algorithm_test;  
import java.util.Arrays;  
  
public class Main {  
  
    public static void main(String[] args) {  
   // write your code here  
  
        int[] arr = randomArr(10, 20);//生成随机数组  
        Arrays.sort(arr);  
        System.out.println("随机数组："+ Arrays.toString(arr));  
        int findRight = findRight(arr,10);  
        System.out.println("最右边的数为：" + findRight);  
  
    }  
    public static int[] randomArr(int n, int area){  
        int[] arr = new int[n];  
        for(int i = 0; i < n; i++){  
            arr[i] = (int)(Math.random() * area + 1);  
        }  
        return arr;  
    }  
    //找到有序数列中小于num的最右边的数  
    public static int findRight(int[] arr, int num){  
        int left = 0, right = arr.length - 1;  
        int middle = 0;  
        int target = 0;  
        while(left <= right){  
            middle = left + ((right - left)>> 1);//防溢出  
            if(arr[middle] < num){//如果小于num，说明我们要的数在右边，符合要求，记录右移  
                target = arr[middle];  
                left = middle + 1;  
            }else{//如果大于或等于num，说明我们要的数在左边，不记录左移  
                right = middle - 1;  
            }  
        }  
        return target;  
    }  
}
```

- 找峰值
要求：一段无序数列，相邻两个数不相等，假设小于下标0和大于最大下标的数小于数组内的数，找到一个峰值就返回
[[二分峰值.excalidraw]]

```java
public static int findPeak(int[] arr) {  
    int left = 0, right = arr.length - 1;  
    int middle = 0;  
  
    if (arr == null || arr.length == 0) {  
        throw new IllegalArgumentException("Array cannot be null or empty");  
    }  
    if (arr.length == 1) {//如果数组中只有一个数，那么它就是峰值  
        return arr[0];  
    }  
    while (left <= right) {  
  
        if (arr[left] > arr[left + 1]) {//最左边的数如果大于它右边一个就返回  
            return arr[left];  
        } else if (arr[right] > arr[right - 1]) {//最右边的数如果大于它左边一个就返回  
            return arr[right];  
        } else {//如果上面两个都不符，就往里面移动  
            left = left + 1;  
            right = right - 1;  
            middle = left + ((right - left) >> 1);  
  
            if ((arr[middle] > arr[middle - 1]) && (arr[middle] > arr[middle + 1])) {  
                return arr[middle];  
            } else if (arr[middle] < arr[middle - 1]) {  
                right = middle - 1;  
            }else if(arr[middle] < arr[middle + 1]){  
                left = middle + 1;  
            }  
        }  
    }  
    throw new IllegalStateException("No peak found in the array");  
}
```
## 时间复杂度和空间复杂度
- 等差数列
一般项：$a_n = a_1+(n-1)d$
常用转换：
	$a_n=\frac{a_{n-1}+{a_{n+1}}}{2}$
	$a_m+a_n=a_p+a_q$
等差数列和：$S_n=\frac{n}{2}(a_1+a_n)$
$=\frac{n}{2}[2a_1+(n-1)d]=a_1n+d·\frac{n(n-1)}{2}$
只要是：$an^2+bn+c$的形式都可以看成是等差数列和

- 等比数列
一般项：$a_n=ar^{n-1}$ 
常用转换：
	$a_m·a_n=a_p·a_q$
等比数列和：$S_n=\frac{a_1(1-r^n)}{1-r}$ 
等比数列形式：$a_n=pq^n$

- 常数操作：固定时间的操作，执行时间和数据量无关（下面按顺序）($O(1)$)
	- 位运算（比较快）
	- $+,-,*,/$属于常数量操作，如果设置的int类型，说明无论多大都是32位
	- 寻址：数组通过下标寻值
	- hash：属于常数时间里比较慢的
- 时间复杂度：
	- 拿选择排序为例，第一个为N，第二个为N-1，...，1，这是一个等差数列，符合$an^2+bn+c$的形式，在时间复杂度中只看最高阶项，所以最后只留下$O(n^2)$
	- 更关注最差的情况（固定流程的情况下）
		- 固定流程就是无论传什么值，都是这样一套程序
		- 如果是随机，假设1，2，3中随机选择，（相邻不等），单次随机，考虑最差的情况（$O(\infty)$）
		- 假设数组的0位置是3，那么1位置就不能是3，假如说1位置我们每次选出来的都是3，那么就无穷了
		- 上面随机的这种情况，就要考虑平均复杂度或者说概率里的期望复杂度来衡量，这时时间复杂度没有意义
	- 内涵：描述算法运行时间和数据量大小的关系，当数据量很大时，排除了常数时间和低阶项的干扰
- 空间复杂度（额外空间复杂度）：
	- 一个函数的入参和出参都不算额外空间复杂度
	- 这个算法函数的内容才算
		- 假如我们只创建了几个变量，$O(1)$
		- 假如入参有一个数组，我们在函数里为了完成功能又创建了一个数组，$O(N)$
- 最优解：先满足时间复杂度最优，其次尽量少用空间的解
- 时间复杂度的均摊：比如说动态数组翻倍扩容
	- 分析：扩展分别是：1，2，4，8，...
	- 加入8个数是：2\*8，加入16个数就是2\*16，...
	- 总结来看加入N个数就是2\*N（整个过程），也就是$O(N)$
	- 但是如果是对单个数来说（均摊），就是$O(1)$
- 不能用代码结构来估计时间复杂度（看有多少个for）
	- 冒泡用一个while实现
	- 调和级数用两个for实现(N\*logN)
- 常见复杂度：（按顺序）/；$O(1),O(logN),O(N),O(N*logN),O(N^2),...,O(N^k),O(2^N),O(k^N),...,O(N!)$

## 算法和数据结构
- 硬计算类算法：精确求解，但是某些问题使用硬计算类算法，可能会让计算的复杂度较高
	大厂算法和数据结构笔试、面试题比赛或者acm形式类似的比赛
- 软计算类算法：更注重逼近解决问题，而不是精确求解，计算时间可控（比如说围棋卡住了，很难有神之一手，这时候趋向于找一个最好的解而不是精确求解，这时候也精确不了）
	模糊逻辑、神经网络、进化计算，概率理论、混沌理论、支持向量机、群体智能

算法工程师要掌握软硬计算类算法，一般程序员掌握硬计算类算法

- 数据结构：任何数据结构都是由下面两个结构组成的
	- 连续结构：
		- 可以把数组想象成一个连续结构，我们要拿里面的一个数，主要是通过算偏移量来的，数组里面每个位置都是固定的，而且是一个连续结构，所以通过算偏移量就会很快
	- 跳转结构：
		- 链表就是一个跳转结构

## 算法笔试的输入输出
### 填函数风格
leetcode中的风格

- 但不是主流
[[算法题目输入输出.excalidraw]]
### acm风格
1. 规定数据量
	1. BufferedReader
		1. 会把文件中比较多的内容读进来，也可以从里面拿东西，拿完了会自己从文件再读一大块，在内存里，快
	2. StreamTokenizer
			1. 用这个从内存拿数据，会区分空格和回车读数字
	3. PrintWriter
2. 按行读（BufferedReader、PrintWriter）：
	1. 不能用StreamTokenizer的nextToken，数据是一行一行的，还不一样大
	2. 可以用readline读一行字符串，再根据空格切分，最后转成int类型
3. 汇报答案：
	1. 和输入的思路差不多，也建立了一个内存托管，使用PrintWriter，放到这个输出托管里，等所有的答案都出来了再用一次IO一次性全部提交
4. 最好不要使用Scanner（走IO流，每次读一行，频繁在硬盘使用io效率低）来读取信息，System.out来提交答案（也是走IO），IO效率慢
5. 推荐使用全局静态空间

- 解决算法题目会用到二维数组等大体量的空间作为辅助，一般来说在循环内部创建了，这次循环结束后这个空间会得到释放
- 但是acm机制在计算的时候不会算释放的空间，只会算用了所有测试案例一共用了多少空间，所以最好是用全局静态空间，自己设置复用空间，建一个最大数据量就可以


```java
public static void main(String[] args) throws IOException{
	BufferedReader br = new BufferedReader(new InputStreamReader(System.in))
	//一个一个读数字
	StreamTokenizer in = new StreamTokenizer(br);
	//提交答案用的
	PrintWriter out = new PrintWriter(new OutputStreamWriter(System.out));
	while(in.nextToken() != StreamTokenizer.TT_EOF){ // 判断文件是否结束
	//n 二维数组的行（从数据源拿数据）
	int n = (int) in.nval;
	in.nextToken();
	// m 二维数组的列
	int m = (int) in.nval;
	// 装数字的矩阵，动态生成
	int[][] mat = new int[n][m]
	for(int i = 0; i < n; i++){
		for(int j = 0; j < m; j++){
			in.nextToken();
			mat[i][j] = (int) in.nval;
		}
	}
	out.println(maxSumSubmatrix(mat, n, m));
	}
	out.flush(); //一次性提交
	out.close();
}

public static int maxSumSubmatrix(){
	int max = Integer.MIN_VALUE;
	for(int i = 0; i < n; i++){
		//使用全局静态空间：
		/**
		* //题目给的最大数据量
		* public static int MAX_N = 201
		* public static int MAX_M = 201
		* // 申请使用矩阵空间
		* public static int[][] mat = new int[MAX_N][MAX_M]
		* // 申请的辅助空间
		* public static int[] arr = new int[MAX_M]
		*/
		Arrays.fill(arr, 0, m, 0);
		for(int j = i; j < n;j++){
			for(int k = 0;k < m; k++){
				arr[k] += mat[j][k];
			}
			max = Math.max(max, maxSumSubarray());
		}
	}
	return max;
}
```


- 按行读
```java
public static String line;
public static String[] parts;
public static int sum;

public static void main(String[] args) throws IOException{
	BufferedReader br = new BufferedReader(new InputStreamReader(System.in))
	PrintWriter out = new PrintWriter(new OutputStreamWriter(System.out));
	while((line = in.readline()) != null){
		parts = line.split(" ");
		sum = 0;
		for(String num : parts){
			sum += Integer.valueOf(num);
		}
		out.println(sum);
	}
	out.flush();
	in.close();
	out.close();
}
```

## 递归及master公式
### 递归
- 递归在系统内部是通过栈的方式来实现的
- 递归一定存在基准条件用来判定结束递归。
- 假设要求`[4,2,6,1]`中的最大值，用递归实现
[[递归图解.excalidraw]]
```java
public static int f(int[] arr, int l, int r){
	if(l == r){
		return arr[l];
	}
	int m = (l + r) / 2;
	int lmax = f(arr, l, m);
	int rmax = f(arr, m + 1, r);
	return Math.max(lmax, rmax);
}
```

- 任何递归都可以改成非递归（用栈模拟就行）
	- 我们自己的栈可以自行选择将哪些压入栈，而系统的栈是将所有的数都压进去
	- 自己的栈是内存空间，系统栈是一个独立的区域（比较贵）
	- 工程上一般都要改成非递归，除非递归量再大也不会很多层，归并排序($log_2N$)、快速排序、线段树、很多平衡树

### master公式
- 对递归的时间复杂度进行分析的公式
- 条件：所有子规模相同，比如上面代码都是$\frac{1}{2}$
- $T(n)=a*T(N/b)+O(N^c)$，a，b，c都是常数
	- 如果$log_ba<c$，复杂度为$O(N^c)$
	- 如果$log_ba>c$，复杂度为$O(N^{log_ba})$（谁更大选谁）
	- 如果$log_ba = c$，复杂度为$O(N^c * logN)$
- 使用：
	- 用上面的代码举例：$T(N)=2*T(N/2)+O(N^0)$
		- 解释：子规模只取一层，上面的代码的子规模是二分所以是$T(N/2)$，$O(N^c)$表示除了递归的内容其他的东西，上面除了递归都是$O(1)$，所以c=0，a=2，b=2
		- 时间复杂度：$O(N)$
	- 假如要选前$\frac{2}{3}$和后$\frac{2}{3}$的部分，$T(N)=2*T(N*\frac{2}{3})+O(N^0)$
		- a=2，b=$\frac{3}{2}$，c=0，
	- 假如上面代码除了递归的内容还有一个循环
		- a=2，b=2，c=1，
- 死记公式：
	- $T(N)=2*T(N/2)+O(N*logN)$，时间复杂度：$O(N*(logN)^2)$ 

## 哈希表、有序表、比较器
### 哈希表
- HashSet：可以用于实现查询某一个数在不在一个集合
	- 复杂度为：$O(1)$（大常数，CRUD都是）
	- 1 2 3
	- 根据值来，查重，输入两个值都为hello的str1和str2后查询set的size为1
- HashMap：组织结构和HashSet一样，只是多一个伴随数据
	- 1:A  2:B  3:C

- 假如key是固定、可控的，那么哈希表可以被数组替代
	- 哈希表：动态结构
	- 数组：静态结构

- 哈希表中根据值来的类型
	- Integer、Long、Double、Float
	- Byte、Short、Character、Boolean
	- String
	- 如果不是以上类型，则存的是内存地址，根据内存地址来取key

- java可以定制hashCode、equals方法

```java
hashSet.put();
hashSet.get();
hashSet.contain();
hashSet.remove();
```

### 有序表
- 有序表
	- 会去重
- TreeMap
	- 底层：红黑树
	- 会对key进行排序
```java
TreeMap<Integer, String> treeMap = new TreeMap<>();

//TreeMap中特有的
treeMap.firstKey()
treeMap.lastKey()
treeMap.floorKey(4)//离key<=4最近的key
treeMap.ceilKey() //离key>=4最近的key
```

- 时间复杂度：$O(logN)$（CRUD）

- TreeSet会去重
```java
treeSet.pollFirst()//从小到大弹出
treeSet.pollLast()//从大到小弹出
```

### 比较器
- 使用java自带的比较器
```java
public static class EmployeeComparator implements Comparator<Employee>{
	@Override
	public int compare(Employee o1, Employee o2){
		//比较器默认
		//如果返回负数，o1先
		//返回正数，o2先

		//假如比较谁年龄小
		return o1.age - o2.age;
	}
}

...
main函数中
	Arrays.sort(arr, new EmployeeComparator());
	//另一种写法，不用新写一种类,谁大谁在前，相当于上面的o2.age - o1.age
	Arrays.sort(arr, (a, b) -> b.age - a.age)


//实现两层比较,公司编号小的在前，相同谁年龄小谁在前
Arrays.sort(arr, (a, b) -> 
a.company != b.company 
	? (a.company - b.company) 
	: (a.age - b.age)
	);
```

- 对有序表来说，如果存的是自定义类型，必须传一个comparator类
	- 比较后相等的会自动去重
	- 如果不想去重可以增加比较策略，例如纳入对象的内存地址等进行比较
```java
TreeSet<Employee> treeSet = new TreeSet<>(
	(a, b) -> 
a.company != b.company 
	? (a.company - b.company) 
	: a.age != b.age 
		? (a.age - b.age) 
		: a.toString().compareTo(b.toString())
);
```

### 字典序
- 字符串比较大小
	- 长度一样根据字母顺序，谁在后面谁大
	- 长度不一样，短的后位补字典序中的最小值
## 异或运算
### 认识
- ![[Pasted image 20260307091353.png]]
	- 白+黑--> 黑（0+1--> 0）
	- 白+白 or 黑+黑 --> 白（0+0 or 1+1 --> 1）
	- 袋中有a个0，b个1，相当于将所有球异或最后1的概率
- 答案
	- ![[Pasted image 20260307091416.png]]
- 性质
	- 可以理解为无进位相加
	- 同一批数异或出来的结果一样
	- $0\oplus n = n, n\oplus n = 0$ 
	- 若整体异或和=x，其中某个部分为y，剩下部分异或和=$x\oplus y$

### 应用
1. 交换两个数
```java
a = 2 //java中异或符号为 ^
b = 3
a = a ^ b //2 ^ 3
b = a ^ b //2 ^ 3 ^ 3 = 2
a = a ^ b //2 ^ 3 ^ 2 = 3 
```

2. 不使用判断语句和比较操作，返回两个数的最大值
```java
//0变1，1变0
public static int flip(int n){
	return n ^ 1;
}

//非负数返回1，负数返回0
public static int sign(int n){
	return flip(n >>> 31); //无符号右移，左侧一律补0（有符号左侧补符号位）
}

//相比于直接用c的符号决定a还是b，避免了c溢出的情况
public static int getMax(int a, int b){
	int c = a - b;
	int sa = sign(a); //a的符号
	int sb = sign(b); //b
	int sc = sign(c); //c
	int diffAB = sa ^ sb; //ab是否异号
	int sameAB = flip(diffAB);
	
	int returnA = diffAB * sa + sameAB * sc; //ab异号时，sa是正数，ab同号时c时正数
	int returnB = flip(returnA); 
	return a * returnA + b * returnB;
}
```

3. 找到缺失的数字
```java
//题目描述：0-10，数组中缺了其中一个，其他的10个数字在该数组中都有
//思路：将缺了该数字的数组与所有数字都在的数组异或，得出来的就是缺的数字

public static int missingNumber(int[] nums){
	int eorAll = 0, eorHas = 0;
	for(int i = 0; i < nums.length; i++){
		eorAll ^= i;
		eorHas ^= nums[i];
	}
	eorAll ^= nums.length;
	return eorAll ^ eorHas;
}
```

4. 数组中1种数出现了奇数次，其他数出现了偶数次，返回出现了奇数次的数
	- 将所有数异或，偶数个的都约没了，只有奇数个的能留下

- Brian Kernighan算法
	-  提取出二进制状态中最右侧的1
```
   n: 001101 1 0
  ~n: 110010 0 1
~n+1: 110010 1 0 (除了最右侧的1其他都和原数相反，补码，-n)

第一行和最后一行&，就得到了最右侧1的位置
```

5. 数组中有2种数出现了奇数次，其他数出现了偶数次，返回这两种出现了奇数次的数
	1. 将所有数异或后得到的数为：eor1 = a $\oplus$ b（唯二的两种数异或的结果）
	2. eor1最右侧的1将a和b区分（假如说在低3位）
	3. 将整个数组分为2个部分，低3位为1的在一边，不为1的在一边
	4. 取出一边全部异或，得到的数就是a或者b
	5. 将a或b和eor1异或就可以得到剩下的数
```java
public static int[] singleNumber(int[] nums){
	int eor1 = 0;
	for(int num : nums){
		eor1 ^= num;	
	}
	int rightOne = eor1 & (-eor1);
	int eor2 = 0;
	for(int num : nums){
		if((num & rightOne) == 0){
			eor2 ^= num;	
		}	
	}
	return new int[]{eor2, eor1 ^ eor2};
}
```
- 复杂度：
	- 时间：$O(N)$
	- 空间：$O(1)$

6. 数组中只有1种数出现次数少于m次，其他都出现了m次，返回小于m次的数
	1. 统计二进制状态时每个数每一位上1出现的次数
	2. 出现了m次的数1的次数是m的整数倍次
	3. 如果不是m的整数倍，那么该就是少于m次的数
```java
public static int find(int[] arr, int n){
	//cnts[0]:0位上有多少1
	//cnts[1]:1位上有多少1
	//....
	int[] cnts = new int[32];
	for (int i = 0; i < 32; i++){
		cnts[i] += (num >> i) & 1;
	}
	int ans = 0;
	for(int i = 0; i < 32;i++){
		if((cnts[i] % m != 0){
			ans |= 1 << i; //按位或，只要有1个是1，结果就是一，这是将不等于m的所有位拼起来
		}
	}
	return ans;
}
```



## 位运算
- python在进行位运算时，如果发生溢出，不是直接丢弃，而是升位，32位溢出，则升成64位
	- 所以进行位运算后可以加上`& 0xFFFFFFFF`

- 位运算现实意义
	- 条件判断相较于赋值、位运算、算数运算稍慢
	- 实际使用尽量直白，牛逼位运算直接套用即可
### 应用
1. 判断一个整数是不是2的幂
	1. 将最右侧的1的二进制状态提取出来和该整数比较
	2. 假如相等，那么是，不等则不是
```java
public static boolean isPowerOfTwo(int n){
	return n > 0 && n == (n & -n);
}
```

2. 判断一个数的整数是不是3的幂
	```java
	//1162261467是int类型范围中最大的3的幂，3^19
	//
	public static boolean isPowerOfThree(int n){
		return n > 0 && 1162261467 % n == 0
	}
	```
3. 已知n是非负数，返回≥n的最小的2的某次方
	1. 将n-1
		1. 防止n恰好是n的某次方的情况
	2. 将-1后的n的最左侧1右边的0都改为1
	3. 将改后的n+1
```java
public static final int near2power(int n){
	if(n <= 0){
		return 1;
	}
	n--;
	n |= n >>> 1; // 移动1位实现左侧两个1
	n |= n >>> 2; //移动两位，左侧4个1
	n |= n >>> 4; //移动4位，左侧8个1
	n |= n >>> 8; //...
	n |= n >>> 16;
	return n + 1;
}
```

4. 区间`[left, right]`内所有数字&的结果
	1. 假如right≠left
	2. 将right-1，假如不等于left，说明最右侧的1留不下来，将其变为0
	3. 假如right≠left
	4. 再将变为0后的right-1，假如不等于left，重复上面的操作
	5. 直到right = left
```java
public static int rangeBitwiseAnd(int left, int right){
	while(left < right){
		right -= right & -right;
	}
	return right;
}
```


5. 反转一个二进制的状态，逆序。（int型）
	1. 将该数分组，每组两位交换（1v1）
	2. 再分组，每组四位，两位一组交换（2v2）
	3. 再分...（4v4）
	4. ...（8v8）
	5. ...（16v16）
```java
public static int reverseBits(int n){
	n = ((n & 0xaaaaaaaa) >>> 1) | ((n & 0x55555555) << 1); //java没有<<<
	n = ((n & 0xcccccccc) >>> 2) | ((n & 0x33333333) << 2);
	n = ((n & 0xf0f0f0f0) >>> 4) | ((n & 0x0f0f0f0f) << 4);
	n = ((n & 0xff00ff00) >>> 8) | ((n & 0x00ff00ff00ff) << 8);
	n = (n >>> 16) | (n << 16);
	return n;	
}
```

6. 返回一个数二进制中有几个1
	1. n和0101...&得到每组（两个）靠右的位的状态（长度为1）
	2. n>>>1后与0101...&得到每组靠左的位的状态
	3. 将上面两个得到的数相加，每组两位表示n每2位1的个数（长度为2）
	4. 新得到的数与0011...&，得到每组靠右边两位1的个数
	5. 新数>>>2与0011...&得到每组靠左两位1的个数
	6. 相加，每组（4位）表示n每4位1的个数（长度为4）
	7. 新的得到的数与00001111...&，得到每组靠右4位1的个数
	8. 新数>>>4与00001111...&，得到每组靠左4位1的个数
	9. ....（长度为8）
	10. ...（长度为16）
	11. 长度为16的两组相加得到长度为32的就是答案

```java
public static int cntOnes(int x){
	n = (n & 0x55555555) + ((n >>> 1) & 0x55555555);
	n = (n & 0x33333333) + ((n >>> 2) & 0x33333333);
	n = (n & 0x0f0f0f0f) + ((n >>> 4) & 0x0f0f0f0f);
	n = (n & 0x00ff00ff) + ((n >>> 8) & 0x00ff00ff);
	n = (n & 0x0000ffff) + ((n >>> 16) & 0x0000ffff);
	return n;
}
```
### 位图
- 原理
	- 用bit组成的数组来存放值，1、0代表存在和不存在，取值和存值操作都用位运算
	- 限制：必须为连续范围且不能过大
	- 好处：极大的节省空间，1个数字只占用1个bit的空间
- 拿哈希表举例，哈希表中每一个数占32bit，我们可以拿出来验证该数是否存在
	- 而位图只用1bit来表示

- 描述
	- 一个数32bit，可以表示32个连续的数，两个数就可以表示64个连续的数，...
	- 用数除以32，就可以得到在第几个数
	- 需要向上取整得到整个数组的长度
- 向上取整
	- 不用自带的方法
	- 给出两个数a，b（均为非负）
		- a/b：$(a+b-1)/b$ 
	- 解释
		- 已知：a = k\* b+余数
		- 余数+b-1 一定是大于b，小于2b，所以可以实现向上取整

```java
public static class Bitset{
	public int[] set;

	//n个数字（0-n-1）
	public Bitset(int n){
		//向上取整
		set = new int[(n + 31) / 32];
	}

	public void add(int num){
		//在第几个数的第几位，|实现加入
		set[num / 32] |= 1 << (num % 32);
	}

	//删除某数
	public void remove(int num){
		set[num / 32] &= ~(1 << (num % 32));
	}

	//如果有就删，没有就加上
	public void reverse(int num){
		set[num / 32] ^= 1 << (num % 32);
	}

	//查询是否在位图
	//将某数的第几位移到低1位&1来看是否存在
	public boolean contains(int num){
		return ((set[num / 32] >> (num % 32)) & 1) == 1
	}
}
```

- 使用对数器验证
	- 等概率调用三种函数
	- ![[Pasted image 20260308232443.png]]
	- ![[Pasted image 20260308232520.png]]
	- ![[Pasted image 20260308232547.png]]

### 位运算实现加减乘除
- 加法：无进位（异或）+进位信息
	- 两个数a和b$\oplus$，得到无进位
	- &再左移1位，得到进位信息
	- 将无进位和进位信息异或
	- &<<1，...
	- 直到无进位信息

```java
public static int add(int a, int b){
	int ans = a;
	while(b != 0){
		ans = a ^ b;
		b = (a & b) << 1;
		a = ans;
	}
	return ans;
}
```

- 减法：$-b = ~b+1$
	- 将a和b的相反数相加即可
```java
//得到负数
public static int neg(int n){
	return add(~n, 1);
}
//减法
public static int minus(int a, int b){
	return add(a, neg(b));
}
```

- 乘法：
	- 模拟竖式计算
	- 移动位置相加即可
```java
public static int multiply(int a, int b){
	int ans = 0;
	while(b != 0){
		//加入最右侧不为零就相加，为0移位即可
		if((b & 1) != 0){
			ans = add(ans, a);
		}
		a <<= 1;
		b >>>= 1;
	}
	return ans;
}
```

- 除法
	- 被除数=除数 \* （$2^n+2^m+...$）
	- 从大往小试
	- 找到后相减，继续找
	- 直到为0，|运算合并
```java
//必须保证a和b都不是整数最小值
//int型最小值为2^{-32}，没有对应的绝对值正数
public static int div(int a, int b){
	int x = a < 0 ? neg(a) : a;
	int y = b < 0 ? neg(b) : b;
	int ans = 0;
	for(int i = 30; i >= 0; i = minus(i, 1)){
		//从大往小试，使被除数右移（安全）
		//假如是除数左移，y可能会溢出
		if((x >> i) >= y){
			ans |= (1 << i);
			x = minus(x, y << i);
		}
	}
	return a < 0 ^ b < 0 ? neg(ans) : ans;
}
```
- 整数最小值单独分析
![[Pasted image 20260309104729.png]]


### 取模
- 当取模对象是2的n次方时可以使用位运算代替取模符号
```
ans = a % b
ans = (b-1) & a
```

- 原因
	- 当b为2的n次方时，-1后低位才全是1，可以保留低位信息
	- 非2的n次方-1低位会出现0，从而丢失信息


### N皇后位运算


## 数据结构设计高频
### setAll功能的哈希表
- 要求时间复杂度O(1)
- 将map中所有value都设置为同一个值

- 思路
	- 复用时间戳
	- 使用一个变量cnt=0表示时间
	- 准备两个变量分别负责setAll的value和使用时间
	- 每向map中put一个值时cnt++
	- 如果执行了setAll，则setAllTime = cnt，于是cnt++
	- 使用get时，先比较setAllTime和原map的最新值对应的时间戳

```java
//全局变量（只适用于算法题）
public static HashMap<Integer, int[]> map = new HashMap<>();
public static int setAllValue;
public static int setAllTime;
public static int cnt;

public static void put(int key, int val){
	if(map.containsKey(key)){ //如果有key，就更新值和时间戳
		int[] value = map.get(key);
		value[0] = val;
		value[1] = cnt++; //值和时间戳放在数组里，key:{val, cnt}
	}else{
		map.put(key, new int[]{val, cnt++});
	}
}

public static void setAll(int val){
	setAllValue = val;
	setAllTime = cnt++;
}

public static int get(int key){
	if(!map.containsKey(key)){
		return -1;
	}
	int[] value = map.get(k);
	if(value[1] > setAllTime){
		return value[0];
	}else{
		return setAllValue;
	}
}
```

### LRU缓存
- 联想：操作系统，内存管理算法LRU（least recently used）
	- 最近最少使用算法
- 使用双向链表和哈希表
	- 双向链表头表示早，尾表示晚
	- 当map满了之后，将最早替换
	- 假如修改key对应的value值
		- 将key对应的结点拿出放到尾部，剩下的连好

```java
//内部类
class LRUCache{

	//双向链表结点
	class DoubleNode{
		public int key;
		public int val;
		public DoubleNode last;
		public DoubleNode next;

		public DoubleNode(int k, int v){
			key = k;
			val = v
		}
	}

	//双向链表整条行为处理
	class DoubleList{
		private DoubleNode head;
		private DoubleNode tail;
	
		public DoubleList(){
			head = null;
			tail = null;
		}
	
		//加到链表尾部
		public void addNode(DoubleNode newNode){
			if(newNode == null){
				return;
			}
			if(head == null){
				head = newNode;
				tail = newNode;
			}else{
				tail.next = newNode;
				newNode.last = tail;
				tail = newNode;
			}
		}
	
		//移走最早到的（头节点）
		public DoubleNode removeHead(){
			if(head == null){
				return null;
			}
			DoubleNode ans = head;
			if(head == tail){
				head = null;
				tail = null;
			}else{
				head = ans.next;
				ans.next = null;
				head.last = null;
			}
			return ans;
		}
	}
	
	private HashMap<Integer, DoubleNode> keyNodeMap;
	
	//控制链表顺序
	private DoubleList nodeList;
	
	private final int capacity; //容量

	//构造方法
	public LRUCache(int cap){
		keyNodeMap = new HashMap<>();
		nodeList = new DoubleList()j;
		capacity = cap;
	}
	
	public int get(int key){
		if(keyNodeMap.containsKey(key)){
			DoubleNode ans = keyNodeMap.get(key);
			nodeList.moveNodeToTail(ans);
			return ans.val;
		}
		return -1;
	}
	
	public void put(int key, int value){
		if(keyNodeMap.containsKey(key)){
			DoubleNode node = keyNodeMap.get(key);
			node.val = value;
			nodeList.moveNodeToTail(node);
		}else{
			if(keyNodeMap.size() == capacity){
				keyNodeMap.remove(nodeList.removeHead().key);
			}
			DoubleNode newNode = new DoubleNode(key, value);
			keyNodeMap.put(key, newNode);
			nodeList.addNode(newNode);
		}
	}

}

```

### 插入、删除和获取随机元素O(1)时间的结构
- 在set中执行插入、删除、获取随机元素操作时，用的时间均为O(1)
	- set中无重复元素
	- 等概率获取随机元素
- 用hashMap记录，如果contain就不加入，value记录元素在数组中的下标
	- 保证不重复
- 在动态数组中删除元素，size需要同步变化，否则无法保证等概率获取随机元素
	- 当移出一个元素时，将size-1位置上的元素拿过来补这个空
	- size--

```java
class RandomizedSet{
	public HashMap<Integer, Integer> map;
	public ArrayList<Integer> arr;

	public RandomizedSet(){
		map = new HashMap<>();
		arr = new ArrayList<>();
	}

	public boolean insert(int val){
		if(map.containKey(val)){
			return false;
		}
		map.put(val, arr.size());
		arr.add(val);
		return true;
	}
	public boolean remove(int val){
		if(!map.containsKey(val)){
			return false;
		}
		int valIndex = map.get(val);
		int endValue = arr.get(arr.size() - 1);
		//将最后一个放到要移走的空上
		map.put(endValue, valIndex);
		arr.set(valIndex, endValue);
		//map中移走对应的数
		map.remove(val);
		//移走数组中最后一个数
		arr.remove(arr.size() - 1);
		return true;
	}
	public int getRandom(){
		return arr.get((int)(Math.random() * arr.size()));
	}
}
```

### 插入、删除和获取随机元素O(1)时间且允许有重复数字的结构
- 题意同上，增加可重复条件
	- 获取随机元素时，出现多的数字权重大

- 思路
	- 准备一个HashMap和动态数组
	- map分别为值和对应的多个下标（用容器存储）

- 重点是remove的设计
	- 最后一个替要移走的
	- 移走的数对应的下标集需要移走一个
	- 最后一个数的下标集要删掉一个，增加一个

```java
class RandomizedCollection{
	public HashMap<Integer, HashSet<Integer>> map;
	public ArrayList<Integer> arr;

	public RandomizedCollection(){
		map = new HashMap<>();
		arr = new ArrayList<>();
	}

	public boolean insert(int val){
		arr.add(val);
		//map中如果有val，就直接拿出来，如果没有就执行default位
		HashSet<Integer> set = map.getOrDefault(val, new HashSet<Integer>());
		set.add(arr.size() - 1);
		map.put(val, set);
		return set.size() == 1;//返回该数之前是否进入数组
	}

	public boolean remove(int val){
		if(!map.containsKey(val)){
			return false;
		}
		HashSet<Integer> valSet = map.get(val);
		//使用迭代器，任意选一个数（因为set无序，假如是arralist就会从第一个开始）
		int valAnyIndex = valSet.iterator.next();
		int endValue = arr.get(arr.size() - 1);
		//如果指定数恰好是最后一个直接在valSet中删除
		if(val == endValue){
			valSet.remove(arr.size() - 1);
		}else{
			//改map
			HashSet<Integer> endValueSet = map.get(endValue);
			endValueSet.add(valAnyIndex);
			//改数组
			arr.set(valAnyIndex, endValue);
			//最后一个数删除下标
			endValueSet.remove(arr.size() - 1);
			//指定数移走下标
			valSet.remove(valAnyIndex);
		}
		arr.remove(arr.size() - 1);
		if(valSet.isEmpty()){
			map.remove(val);
		}
		return true;
	}
	public int getRandom(){
		return arr.get((int)(Math.random() * arr.size()));
	}
}
```

### 快速获得数据流的中位数结构
- 即快速获取将一个数据流排序后的中位数
	- 数据流向外给数，我们随时能够获得中位数
	- 奇数个可直接获得
	- 偶数个中间两个加在一起，除以2

- 用堆
	- 准备两个堆，一个大根堆，一个小根堆
	- 新来一个数
		- 如果两个堆均为空，那么进大根堆
		- 如果≤大根堆顶，进大根堆
		- 否则进小根堆
	- 实时监测两个堆的数目，如果不平衡，将大根堆堆顶弹出到小根堆堆顶（数目差值保持在小于2）
		- 如果是奇数个，选择多的堆顶
		- 偶数个，（大根堆堆顶+小根堆堆顶）/2

- $O(logN)$

```java
class MedianFinder{
	private PriorityQueue<Integer> maxHeap;
	private PriorityQueue<Integer> minHeap;

	public MedianFinder(){
		maxHeap = new PriorityQueue<>((a, b) -> b - a);
		minHeap = new PriorityQueue<>((a, b) -> a - b);
	}

	public void addNum(int num){
		if(maxHeap.isEmpty() || maxHeap.peek() >= num){
		maxHeap.add(num);
		}else{
			minHeap.add(num);
		}
		balance();
	}
	public double findMedian(){
		if(maxHeap.size() == minHeap.size()){
			return (double)(maxHeap.peek() + minHeap.peek()) / 2;
		}else{
			return maxHeap.size() > minHeap.size() ? maxHeap.peek() : minHeap.peek();
		}
	}

	private void balance(){
		if(Math.abs(maxHeap.size() - minHeap.size()) == 2){
			if(maxHeap.size() > minHeap.size()){
				minHeap.add(maxHeap.poll());
			}else{
				maxHeap.add(minHeap.poll());
			}
		}
	}
}
```

### 最大频率栈
- 设计一个类似堆栈的数据结构，将元素推入堆栈，从堆栈中弹出出现频率最高的元素，频率一样的返回最接近栈顶的元素
- 时间复杂度：$O(1)$

- 类似堆栈，但不是堆栈
- 准备多个数组和数频表，以及一个变量记录最大数频
- 第一个数组表示出现1次及以上的，第2个表示两次及以上的
- ...

```java
class FreqStack{
	private int topTimes;
	//记录每层的数据
	private HashMap<Integer, ArrayList<Integer>> cntValues = new HashMap<>();
	//数频表
	private HashMap<Integer, Integer> valueTopTime = new HashMap<>();

	public void push(int val){
		valueTopTime.put(val, valueTopTime.getOrDefault(val, 0) + 1);
		int curTopTimes = valueTopTime.get(val);
		//假如没有该数频数组，需要新增数组
		if(!cntValues.containsKey(curTopTimes)){
			cntValues.put(curTopTimes, new ArrayList<>());
		}
		//获得当前数组号
		ArrayList<Integer> curTimeValues = cntValues.get(curTopTimes);
		//加入值
		curTimeValues.add(val);
		//更新最大数频
		topTimes = Math.max(topTimes, curTopTimes);
	}

	public int pop(){
		//得到最大数频数组
		ArrayList<Integer> topTimeValues = cntValues.get(topTimes);
		//移出该数组最后一个
		int ans = topTimeValues.remove(topTimeValues.size() - 1);

		//更新当前数频数组
		int times = valueTime.get(ans);
		if(times == 1){
			valueTimes.remove(ans);
		}else{
			valueTimes.put(ans, times - 1);
		}
		return ans;	
	}
}
```

### 全O(1)的数据结构
- 一个用于存储字符串计数的数据结构，并能够返回计数最小和最大的字符串
- 使每个函数都满足$O(1)$的平均时间复杂度
	- ![[Pasted image 20260310185110.png]]

- 双向链表+哈希表
	- 初始阶段准备两个结点（桶），0和整数最大
	- 每个结点表示词频
	- 新增的数如果在原链表有，那么词频增加
		- 若无该词频的桶，则新建，如果有就加入
		- 旧词频的桶中需要删除该数，同时如果该旧词频中没有任何数，则将其删除

```java
class AllOne{
	class Bucket{
		
		public HashSet<String> set; //字符串组
		public int cnt; //该结点代表的
		public Bucket last;
		public Bucket next;

		public Bucket(String s, int c){
			set = new HashSet<>();
			set.add(s);
			cnt = c;
		}
	}
	private void insert(Bucket cur, Bucket pos){
	/**
		假如当前结点是0
		整数最大结点向前连上pos结点
		pos向后连上整数最大
		当前结点向后连到pos
		pos向前连到当前结点
	*/
		cur.next.last = pos;
		pos.next = cur.next;
		cur.next = pos;
		pos.last = cur;
	}
	private void remove(Bucket cur){
		cur.last.next = cur.next;
		cur.next.last = cur.last;
	}

	Bucket head;
	Bucket tail;

	//用来记录某个字符串存在于哪个桶
	HashMap<String, Bucket> map;

	public AllOne(){
		head = new Bucket("", 0);
		tail = new Bucket("", Integer.MAX_VALUE);
		head.next = tail;
		tail.last = head;
		map = new HashMap<>();
	}

	//来一个新字符串
	public void inc(String key){

		//如果map中没有该字符串
		if(!map.containsKey(key)){
			//如果0结点后一个词频=1，就将该字符串加入map表示存在于1结点，同时放入1结点的set结构中（入桶）
			if(head.next.cnt == 1){
				map.put(key, head.next);
				head.next.set.add(key);
			}else{//否则新建一个1结点
				Bucket newBucket = new Bucket(key, 1);
				map.put(key, newBucket);
				insert(head, newBucket);
		}else{//如果有，找到该字符串对应的结点
			Bucket bucket = map.get(key);
			//如果有比原桶多1的桶，就直接加入，否则新建一个桶
			if(bucket.next.cnt == bucket.cnt + 1){
				map.put(key, bucket.next);
				bucket.next.set.add(key);
			}else{
				Bucket newBucket = new Bucket(key, bucket.cnt+1);
				map.put(key, newBucket);
				insert(bucket, newBucket);
			}
			//处理旧桶
			bucket.set.remove(key);
			if(bucket.set.isEmpty()){
				remove(bucket);
			}
		}
		public String getMaxKey(){
			//在最大桶中任意选一个字符串
			return tail.last.set.iterator().next();
		}
		public String getMinKey(){
			return head.next.set.iterator().next();
		}
	}
}
```





## 经典递归
- 任何递归都是dfs且非常灵活
- 带路径的递归 vs 不带路径的递归（大部分dp都是不带路径的递归）
- deep first search
### 返回字符串的全部子序列，子序列要求去重（带路径）
- 时间复杂度：$O(2^n*n)$



### 返回数组的所有组合，可以无视元素顺序，要去重（带路径）
- 时间复杂度：$O(2^n*n)$

### 返回没有重复数组的全部排列（带路径）
- 时间复杂度：$O(n!*n)$

### 返回可能有重复值数组的全部排列，要求去重（带路径）
- 时间复杂度：$O(n!*n)$

### 用递归逆序一个栈
- 时间复杂度：$O(n^2)$



### 用递归排序一个栈
- 时间复杂度：$O(n^2)$


### 打印n层汉诺塔问题的最优移动轨迹
- 时间复杂度：$O(2^n)$

```java
// 字符串的全部子序列
// 子序列本身是可以有重复的，只是这个题目要求去重
// 测试链接 : https://www.nowcoder.com/practice/92e6247998294f2c933906fdedbc6e6a
public class Code01_Subsequences {

	public static String[] generatePermutation1(String str) {
		char[] s = str.toCharArray();
		HashSet<String> set = new HashSet<>();
		f1(s, 0, new StringBuilder(), set);
		int m = set.size();
		String[] ans = new String[m];
		int i = 0;
		for (String cur : set) {
			ans[i++] = cur;
		}
		return ans;
	}

	// s[i...]，之前决定的路径path，set收集结果时去重
	public static void f1(char[] s, int i, StringBuilder path, HashSet<String> set) {
		if (i == s.length) {
			set.add(path.toString());
		} else {
			path.append(s[i]); // 加到路径中去
			f1(s, i + 1, path, set);
			path.deleteCharAt(path.length() - 1); // 从路径中移除
			f1(s, i + 1, path, set);
		}
	}

	public static String[] generatePermutation2(String str) {
		char[] s = str.toCharArray();
		HashSet<String> set = new HashSet<>();
		f2(s, 0, new char[s.length], 0, set);
		int m = set.size();
		String[] ans = new String[m];
		int i = 0;
		for (String cur : set) {
			ans[i++] = cur;
		}
		return ans;
	}

	public static void f2(char[] s, int i, char[] path, int size, HashSet<String> set) {
		if (i == s.length) {
			set.add(String.valueOf(path, 0, size));
		} else {
			path[size] = s[i];
			f2(s, i + 1, path, size + 1, set);
			f2(s, i + 1, path, size, set);
		}
	}

}
```


## 嵌套类问题使用递归解决问题


## 最大公约数、同余原理
### 最大公约数
- 使用欧几里得算法（辗转相除法）
```java
	// 证明辗转相除法就是证明如下关系：
	// gcd(a, b) = gcd(b, a % b)
	// 假设a % b = r，即需要证明的关系为：gcd(a, b) = gcd(b, r)
	// 证明过程：
	// 因为a % b = r，所以如下两个等式必然成立
	// 1) a = b * q + r，q为0、1、2、3....中的一个整数
	// 2) r = a − b * q，q为0、1、2、3....中的一个整数
	// 假设u是a和b的公因子，则有: a = s * u, b = t * u
	// 把a和b带入2)得到，r = s * u - t * u * q = (s - t * q) * u
	// 这说明 : u如果是a和b的公因子，那么u也是r的因子
	// 假设v是b和r的公因子，则有: b = x * v, r = y * v
	// 把b和r带入1)得到，a = x * v * q + y * v = (x * q + y) * v
	// 这说明 : v如果是b和r的公因子，那么v也是a的公因子
	// 综上，a和b的每一个公因子 也是 b和r的一个公因子，反之亦然
	// 所以，a和b的全体公因子集合 = b和r的全体公因子集合
	// 即gcd(a, b) = gcd(b, r)
	// 证明结束
	public static long gcd(long a, long b) { //最大公约数
		return b == 0 ? a : gcd(b, a % b);
	}

	public static long lcm(long a, long b) { //最小公倍数
		return (long) a / gcd(a, b) * b;
	}
```


### 同余原理

- ![[Pasted image 20260416110035.png]]
- 







## 对数器打表找规律


## 根据数据量猜解法


## 滑动窗口


## 双指针


## 二分答案法
- ![[Pasted image 20260416095849.png]]

```java
// 爱吃香蕉的珂珂
// 珂珂喜欢吃香蕉。这里有 n 堆香蕉，第 i 堆中有 piles[i] 根香蕉
// 警卫已经离开了，将在 h 小时后回来。
// 珂珂可以决定她吃香蕉的速度 k （单位：根/小时)
// 每个小时，她将会选择一堆香蕉，从中吃掉 k 根
// 如果这堆香蕉少于 k 根，她将吃掉这堆的所有香蕉，然后这一小时内不会再吃更多的香蕉
// 珂珂喜欢慢慢吃，但仍然想在警卫回来前吃掉所有的香蕉。
// 返回她可以在 h 小时内吃掉所有香蕉的最小速度 k（k 为整数）
// 测试链接 : https://leetcode.cn/problems/koko-eating-bananas/

	// 时间复杂度O(n * log(max))，额外空间复杂度O(1)
	public static int minEatingSpeed(int[] piles, int h) {
		// 最小且达标的速度，范围[l,r]
		int l = 1;
		int r = 0;
		for (int pile : piles) {
			r = Math.max(r, pile);
		}
		// [l,r]不停二分
		int ans = 0;
		int m = 0;
		while (l <= r) {
			// m = (l + r) / 2
			m = l + ((r - l) >> 1);
			if (f(piles, m) <= h) {
				// 达标！
				// 记录答案，去左侧二分
				ans = m;
				// l....m....r
				// l..m-1
				r = m - 1;
			} else {
				// 不达标
				l = m + 1;
			}
		}
		return ans;
	}

	// 香蕉重量都在piles
	// 速度就定成speed
	// 返回吃完所有的香蕉，耗费的小时数量
	public static long f(int[] piles, int speed) {
		long ans = 0;
		for (int pile : piles) {
			// (a/b)结果向上取整，如果a和b都是非负数，可以写成(a+b-1)/b
			// "讲解032-位图"讲了这种写法，不会的同学可以去看看
			// 这里不再赘述
			ans += (pile + speed - 1) / speed;
		}
		return ans;
	}
```




## 并查集


## 洪水填充


