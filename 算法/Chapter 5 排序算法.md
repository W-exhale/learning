## 冒泡排序（bubble sort）
 比较相邻的两个项，如果第一个比第二个大，那么交换

动画演示：
[排序（冒泡排序，选择排序，插入排序，归并排序，快速排序，计数排序，基数排序） - VisuAlgo](https://visualgo.net/zh/sorting)
第一遍：01比，12比，23比...（N-1）
第二遍：01比，...，（N-2）
....
等差数列和
O($n^2$)
逆序数：交换了多少次

## 选择排序(selection sort)
原址比较：找到最小的和第一个交换，再找第二小的交换（理解），找到数据结构中最小的提前，再找第二小放第二
第一遍N-1中找，
第二遍N-2中找，
....
等差数列和
O($n^2$)

## 插入排序(insertion sort)
每次排一个数组项，构建最后的排序数组。拿一个项出来，和前面的比较，找到更小的插到它后面。

```C
for(int i = 0; i < size; i++){
	int key = array[i];
	int j = i - 1;

	// shift elements that are greater than the key to the right
	while(j >= 0 && array[j] > key){
	array[j + 1] = array[j];
	j--;
	}
	//insert the key into the corrent position
	array[j + 1] = key;
}
```

O($n^2$)
对于小一点的排序内容还好，但是对于大一些的排序，就不太行
如果倒序（6，5，4，3，2，1），拿出6，前面没有比他大的不动，看5，6比5大，5往前移，一直到最后，也是等差数列和（顺序的等差）

假设是顺序，那么每个都是$O(1)$，合计就是$O(n)$，但是这是最优的，我们要考虑最坏的情况
## 归并排序（merge sort）

实际应用比较多，上面三个的算法性能不太行

- 思想：分而治之（将原始数组切分为较小的数组，知道每个数组只有一个位置，将小数组归并成大数组，直到最后只有一个排序完毕的大数组）

需要两个函数，一个把大数组分成不等份小数组，另一个用来排序

```C
#include <stdio.h>
#include<stdlib.h>
#include<string.h>

//Merges the two sorted subarrays array[left ..mid] and [mid + 1..right]
void merge(int array[], int left, int mid, int right) {

	//Calc the size of the subarays
	int left_size = mid - left + 1;
	int right_size = right - mid;

	int* left_array = (int*)malloc(left_size * sizeof(int));
	int* right_array = (int*)malloc(right_size * sizeof(int));

	left_array[left_size]; 
	right_array[right_size];

	// copy the data into the temporary arrays
	for (int i = 0; i < left_size; i++) {
		left_array[i] = array[left + i];
	}

	for (int i = 0; i < right_size; i++) {
		right_array[i] = array[mid + 1 + i];
	}

	int i = 0, j = 0, k = left;

	while (i < left_size && j < right_size) {
		if (left_array[i] <= right_array[j]) {
			array[k] = left_array[i];
			i++;
		}
		else {
			array[k] = right_array[j];
			j++;
		}

		k++;
	}

	while (i < left_size) {
		array[k] = left_array[i];
		i++;
		k++;
	}
	
	while (j < right_size) {
		array[k] = right_array[j];
		j++;
		k++;
	}
	free(left_array);
	free(right_array);
}


void merge_sort(int array[], int left, int right) {
	if (left < right) {
		int mid = left + (right - left) / 2;

		merge_sort(array, left, mid);
		merge_sort(array, mid + 1, right);
		merge(array, left, mid, right);
	}
}
int main(void) {
	int array[] = {5, 2, 7, 1, 4, 0};
	int size = sizeof(array) / sizeof(array[0]);

	merge_sort(array, 0, size - 1);

	for (int i = 0; i < size; i++) {
		printf("%d ", array[i]);
	}
	printf("\n");
	
	// O(N*log(n))

	return EXIT_SUCCESS;
}
```

先排序，再合并


### 思想
- 假设有一个数组`[3,2,5,6,1,9]`
- 将这个数组对半分进行排序，一直对半分直到最后只有一个数
- [[归并排序.excalidraw]]
- 准备两个函数一个用来递归，一个用来merge
- 相比于$O(N^2)$没有比较行为的浪费
### 用递归
912.
```java
public class MergeSort {  
  
    public static final int MAX_SIZE = 501;  
    public static int[] arr = new int[MAX_SIZE];  
    public static int[] helpArr = new int[MAX_SIZE];  
  
    public static void mergeSort(int left, int right){  
        if(left == right){  
            return;  
        }  
        int middle = (left + right) >> 1;  
        mergeSort(left,middle);  
        mergeSort(middle + 1, right);  
        merge(left, middle, right);  
    }  
  
    public static void merge(int left, int middle, int right){  
        int i = left; //左边  
        int j = middle + 1;  
        int k = left; //辅助数组索引  
  
        while (i <= middle && j  <= right){  
            helpArr[k++] = arr[i] <= arr[j] ? arr[i++] : arr[j++];  
        }  
        while (i <= middle){ //左边剩余  
            helpArr[k++] = arr[i++];  
        }  
        while (j <= right){ //右边剩余  
            helpArr[k++] = arr[j++];  
        }  
        for(int index = 0; index <= right; index++){  
            arr[index] = helpArr[index];  
        }  
    }  
}
```

- 复杂度分析：一共n个数
- $T(N)=2 * T(N/2) + O(N)$，$a=2,b=2,c=1$
- 时间复杂度根据master公式：$O(N*logN)$
- 空间复杂度：额外申请了一个辅助数组，所以是$O(N)$

### 不用递归
- 假设有一个数组`[3,2,5,6,1,9,12]`
- 有一个步长的概念，
	- 第一步：左边一个右边一个合并，也就是排好了`2、3,  5、6,  1、9,  12`
	- 第2步：左边2个右边2个合并，即`2、3`和`5、6`合并，`1、9`和`12`合并
	- 第3步：左边4个右边4个...
	- 左边8个右边8个....
	- 步长大于数组长度时就不用了（分不了了）

时间复杂度：$O(N*logN)$
空间复杂度：$O(N)$
```java
//非递归方式  
public static void mergeSort1(){  
    for (int l, m, r, step = 1; step  < n; step <<= 1) {  
        l = 0;  
        while (l < n){  
            m = l + step -1; // l也算一个，所以-1  
            if(m + 1 >= n){ //如果右边只有一个或者没有了，不用merge  
                break;  
            }  
            r = Math.min(l + (step << 1) - 1, n - 1); //合并后的右边，所以要*2  
            merge(l, m, r);  
            l = r + 1;  
        }  
    }  
}
```

### 归并分治
- 一个问题在大范围上的答案=左部分的答案+右部分的答案+跨越左右产生的答案（先排左边再排右边，再总体排）
- 计算的便利性：计算跨越左右产生的答案前，使左右有序
- 使用场景：上面两点都成立（一般）

- 可以用归并分治解决的问题，也可以用线段树、树状数组解决（也是最优解）
- 联想：“整块分治”

leetcode：493
小和：[计算数组的小和_牛客题霸_牛客网](https://www.nowcoder.com/practice/6dca0ebd48f94b4296fc11949e3a91b8?tpId=196&tqId=40415&ru=/exam/oj)

## 随机快速排序
### 经典方式

```
arr = [1, 3, 5, 3, 6, 7, 4, ...]
       0  1  2  3  4  5  6
使用随机数得到x，假如说是5
a = 4,i = 4 时，arr[i] = 6 > x，于是 a = 4,i = 5
arr[i] = 7 > x, 于是 a = 4, i = 6
arr[i] = 4 <= x ,于是 arr[a] 和 arr[i]交换，a++，i++,出循环
交换使得arr左侧区域的最右边数=x

开启第二次...
每次循环排一个数，使用递归的方式进行排序
      f(0,6)
       /   \
    f(0,4)  f(5,6)
    /   \     /  \   
f(0,...)  ...  ... ...
```
- 方式
	- 随机选一个数组中的数x，将所有数分为≤x和>x两种，要求左侧最右边的数必须=x
	- 设置三个字母a，i，xi表示下标
		- a标记左侧区域，i用于寻找≤x的数，xi用于标记等于x的数的下标
	- 遍历数组，a = 0，i = 0
		- 如果`arr[i]≤ x`，i 对应的值与 a 对应的值交换，a++，i++
		- 如果`arr[i]> x`，a不变，i++
		- 假如`arr[i] == x` ，使xi = i
		- i越界退出数组
	- 最后：使`arr[xi]`与`arr[a - 1]`的数交换

### 改进（荷兰国旗问题优化）
- 使用经典方式处理只会标记一个x，假如有很多x，就很费时间
- 将数组分为3个区域，≤x，=x，>x
- 使用三个个字母first，last表示下标，first标记左侧区域，last标记右侧区域，剩下的就是中间区域；i用于寻找左侧和右侧的数

- 方式
	- 假如`arr[i] < x`：`arr[first]`与`arr[i]`交换，且first++，i++
	- 假如`arr[i] == x`：i++
	- 假如`arr[i] > x`：`arr[last]`与`arr[i]`交换，last--，i不变
- 其他的同经典方式，这里只优化了排序方式
- 复杂度
	- 最差
		- 时间复杂度：$O(N^2)$ （每次随机的数都是靠右的数）
		- 空间复杂度：$O(N)$（需要压N层(递归n次)）
	- 最好
		- 时间复杂度：$O(N*logN)$（每次随机的数刚好都是中间的数）
			- $T(N) = 2T(N/2)+O(N)$，递归时间+除递归外划分三个部分所用的时间
		- 空间复杂度：$O(logN)$（压logN层）

## 随机选择算法
- 问题
	- 选出数组中的第n大（小）的数，假设为第52大
	- 使用常规排序比较选择一般是$O(NlogN)$
- 使用快排实现$O(N)$
- 方式
	- 排完第一层查看=x有无命中，若无命中，则选择命中一侧继续划分，另一侧丢弃
	- 第n大则从后往前找
- 复杂度
	- 最差
		- 时间复杂度：$O(N^2)$（每次随机大小最右侧的数）
		- 空间复杂度：$O(N)$（使用递归）
	- 最好
		- 时间复杂度：$O(N)$（选中间的）
			- $T(N) = T(N/2) + ...$
			- 等比数列得：$O(N)$
		- 空间复杂度：
			- $O(logN)$：使用递归
			- $O(1)$：使用循环


## 堆结构和堆排序
### 堆结构
- 堆：类似于优先级队列
	- 将数组想象成一个完全二叉树
- 父结点：$\frac{子结点-1}{2}$
- 子结点
	- $父结点×2+1$
	- $父结点×2+2$ 
- 分类：大根堆、小根堆
- 向上调整：从下向上看（heapinsert）
	- 和父节点公式比较，如果大于父节点，则和父节点交换
	- 最后得到的每棵树的父节点都是最大的，但是左边父节点不一定大于右边父节点
- 向下调整：从上向下看（heapify）
	- 2个子节点PK，找到更大的
	- 和更大的子节点（或唯一的子节点）比较，假如小于子节点，则交换
	- 直到没有子节点

- java中的堆使用
	- 默认小根堆，如果需要大根堆，则需要定制比较器
```java
PriorityQueue<Integer> heap = new PriorityQueue<>();
heap.add(3);
heap.add(3);
heap.add(4);
heap.add(4); //不去重
heap.poll() //默认小根堆，从小数开始弹出
```

### 堆排序
- 以大根堆为例
1. 将`arr[0]`与最后一个数交换
	- 并且--size，将本是最大的数隔离
2. 使用heapify将数组重新调整为大根堆
3. 重复上述操作，直至size = 0

#### 复杂度分析
1. 从顶到底建堆
	1. 每个数进堆时都需要消耗`logN`的时间
	2. 即$log1+log2+log3+log4+...+logN$
	3. 下标为0的数为默认，不用计算，上述收敛于$O(N*logN)$
-  建堆后，将最大值调后等排序操作
	1. $logN+log(N-1)+log(N-2)+...+log2+log1$
	2. 收敛于$O(N*logN)$

1. 从底到顶建堆
	1. 分析：[[从底到顶建堆(堆排序).excalidraw]]
		1. 收敛于$O(N)$
2. 排序消耗：$O(N*logN)$

-  整体：两种建堆方式都是$O(N*logN)$

- 空间复杂度：$O(1)$
	- 综合来看，只用了自带的数组空间

#### 常量增倍法
- 使用常量增倍法来分析为什么建堆是$O(N*logN)$（假如不用收敛法）
	- 假如说有N个数，那么$O(N*logN)$是上限，
		- 前面的$log1$、$log2$等都没到$logN$，但复杂度都是按$logN$算的
	- 对于2N个数来说，$O(N*logN)$是下限
		- 前N个数已经到了$logN$层，假设后N还在$logN$层，那么复杂度就是$O(N*logN)$，这是最理想的情况
	- 而对于复杂度来说是不看系数的，所以2N的复杂度应该也是$O(N*logN)$
	- 一个算法的复杂度如果上下限一样，那么说明复杂度就是这个

- 使用常量增倍法分析子矩阵数量的复杂度
	- 问题
		- 在一个n行m列的矩阵中随意框选，有多少个不同的矩形个数
	- 分析
		- 单拿一个点有$n*m$种选择方式，一个矩阵就有$n^2*m^2$种，有四种重复的方式，所以一共是$\frac{n^2*m^2}{4}$种
		- 复杂度为$O(n^2*m^2)$
	- 使用常量增倍
		- $2n*2m$的矩阵
		- 在左上角选择一个点，右下角选择一个点，可以得到$n^2*m^2$，但还有在右下角和右上角的情况
		- 下限是$n^2*m^2$（至少有$n^2*m^2$个）

### 堆结构常见题
- 合并K个有序链表


- 线段最多重合问题

- 让数组整体累加和减半的最少次数


## 基数排序
- 不基于比较的排序
	- 对于对象的数据特征有要求，不通用
	- 类似的：计数排序，桶排序

- 计数排序
	- 统计数组中每种数的频率
	- 再按大小填入数组即可
	- 要求数据量不大

- 基数排序（桶排序）
	- 数据要求：十进制的非负整数（也可以自定义设计成其他进制）
	- 方式
		- 定义桶，比如说相同个位放一个桶
		- 先进桶的先出，从小桶开始倒
		- 和计数排序类似
		- 第一轮个位，第二轮十位，第三轮百位...
	- 通过除以offset（1, 10，100，1000....）再模10来提取数字
	- 每一轮都进行词频统计，统计后使用前缀分区方式（数组存词频）

- 前缀分区：`[1,2,3,4,5,2,4,5,6,4,6,7,7,7]`
	- 统计每种数有多少个，按顺序排，再算出≤该种数的有几个
	- 1:1  2: 3  3: 4  4:7  5:9  6:11  7:14
	- 排数的时候从算出的数开始往前放，放一个，该数对应的数-1
	- 1放0位置（1-1），2放2位置（3-1），...

- 假如有负数，保证不溢出的情况下将其变为非负
	- 找到min
	- 每个数都减去min，同时找到最大值，决定需要多少轮

## 重要排序总结
- ![[Pasted image 20260306175431.png]]
- 稳定性
	- 假如说一个数组中有两个2，能够保证排完序后原来在左边的2还在左边
- 发现：包含交换功能的排序不具有稳定性
	- 冒泡属于相邻交换，设定相等时不换就可以保持稳定
	- 归并排序merge时，相等的先拷贝左边保持稳定

- 注意
	- 随机快排需要期望的复杂度，最差复杂度无意义
	- 目前在基于比较的排序中，时间复杂度$O(N*logN)$，空间复杂度低于$O(N)$，而且还稳定的算法不存在
		- TimSort也不行
		- 希尔排序（ShellSort）

- 选择
	- 数据量非常小：插入排序
	- 性能优异、实现简单且利于改进（不同业务可以选择不同划分策略）、不在乎稳定性：随机快排
	- 性能优异、不在于额外空间占用、具有稳定性：归并排序
	- 性能优异、额外空间占用要求$O(1)$、不在乎稳定性：堆排序
## 拓扑排序

### 建图、链式前向、拓扑排序


### 拓扑排序扩展




