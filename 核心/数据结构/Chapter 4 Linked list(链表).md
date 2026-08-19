将1，2，3存入内存。
如果内存中有占用，用数组存东西就不方便（很难满足 back to back），所以这时就用到链表。

但是链表，不能通过下标的方式找数据。比如说存一个数，一个int32（4字节）的数，需要8个格子，前面4个格子存数字，后面四个格子存下一个元素的地址。

## 介绍
### 什么是链表？
链表由一系列不必在内存中相连的结构组成。每一个结构均含有元素和指向该结构的下一个结构的指针（Next指针）。最后一个单元的Next指向NULL。
![Pasted image 20240704164044](images/Pasted%20image%2020240704164044.png)

### 编程细节
- 提出问题
1. 没有真正的在定义上插入列表的方法
2. 从列表前面删除时，会更改开头，一不小心就会丢失列表
3. 使用删除算法时需要我们跟踪对应的结构体

- 解决问题
使用带表头（header or dummy node）的链表：
![Pasted image 20240704172950](images/Pasted%20image%2020240704172950.png)

解决问题2，删除第一个元素时，就可以直接将2号作为表头的下一个

- 是否使用？
使用表头可以使特定情况下的代码不那么模糊不清，具体是否使用还是根据个人的喜好来

## 常见的错误
- memory access violation 或 segmentation violation
	通常表示指针变量包含虚假地址
	1. 初始化变量失败：没有对指针赋值
	2. 假如P是NULL，将一个指针赋值为P->next，就会出问题（有的编译器会自动帮你检查，但是它不在C的标准里，所以要注意）
-  when and when not to use malloc to get a new cell
	- 首先，我们需要知道声明一个指向结构体的指针不会创建结构体，只会提供足够的空间来保存地址（也就是指针所需要的空间）
	- 如果使用malloc，不仅能返回一个指向该结构体的指针，还能为结构体分配内存。（使用stdlib.h文件）
-如果没有对链表进行删除操作，那么使用malloc的次数就是表的大小，如果有表头，那么malloc次数再+1.

-对使用malloc后的处理
- 当不需要时，就需要使用free，使用free之后，P指向的地址没变，只是地址上的数据变成了未定义状态

- 循环free列表的时候不能直接free P，否则找P的下一个时会因为P指向未定义而出错，这时候应该使用一个指针将P的信息保存。
- 错误的![Pasted image 20240704184747](images/Pasted%20image%2020240704184747.png)
- 正确的![Pasted image 20240704185009](images/Pasted%20image%2020240704185009.png)
## 单链表

node ：节点
1. 找头部：O(1)
2. 找尾部：O(N)（从头找到尾）
3. 找节点n:就是O(n);找节点2，就是O(2),
4. 插入头部：1->2->3,先找到头，再在头前面开一个空间，O(1)+O(1)=O(1)。
5. 插入尾部：先把所有节点过一遍，再在尾部加一个地址，跟一个元素。O(N).
6. 插入中间：先找到要插的地方O(N)，如果要访问这个值，再加O(1),总的来说还是O(N)。
7. 搜索任意一个值：数组通过index，在链表中就得O(N).
8. 删除：同插入

尾部没有地址：尾节点。
有的尾节点会留一个位置，那么插尾部时，就只需要O(1).（这个位置一般是指向NULL）。

每一个数都表示一个节点，地址不算。

CRUD时间复杂度


- 单链表实现（C语言）

1. 注意链表迭代的方式
2. 删除特定元素时，需要标定被删除的元素
3. 使用二级指针进行指针的修改

```C
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

//单链表的C语言实现


typedef struct {
	int element;
	struct Node* next;
}Node;

Node* create_node(int element);
void insert_head(Node** Head, int element);			//插入头部
void insert_tail(Node** Head, int element);			//插入尾部
void insert_special(Node** Head, int element, int index);		//插入特殊位置

void delete_special(Node** Head, int index);		//删除特殊位置
void print_list(Node* Head);		//打印链表
void free_memory(Node** Head);

int main(void)
{
	Node* List = create_node(0);
	insert_head(&List, 2);
	insert_head(&List, 9);
	print_list(List);
	
	insert_tail(&List, 3);
	print_list(List);

	insert_special(&List, 4, 2);
	insert_special(&List, 6, 3);
	print_list(List);

	delete_special(&List, 3);
	print_list(List);

	free_memory(&List);
	return 0;
}

Node* create_node(int element) {
	Node* new_node;
	new_node = (Node*)malloc(sizeof(Node));
	if (new_node == NULL) {
		printf("Failed to mallocate!");
		return EXIT_FAILURE;
	}
	new_node->element = element;
	new_node->next = NULL;
	return new_node;
}


void insert_head(Node** Head, int element) {
	Node* new_node = create_node(element);
	new_node->next = *Head;
	*Head = new_node;
}

void insert_tail(Node** Head, int element) {
	Node* new_node = create_node(element);
	Node* current = *Head;
	while (current->next != NULL) {
		current = current->next;
	}
	current->next = new_node;
}

void insert_special(Node** Head, int element, int index) {
	Node* new_node = create_node(element);
	Node* current = *Head;
	for (uint8_t i = 0; i < index - 1; i++) {
		current = current->next;
	}

	Node* temp = current->next;
	current->next = new_node;
	new_node->next = temp;

}

void delete_special(Node** Head, int index) {
	Node* current = *Head;

	for (uint8_t i = 0; i < index - 1; i++) {
		current = current->next;
	}
	
	Node* temp = current;
	current = current->next;

	Node* delete_element = current;
	temp->next = current->next;

	free(delete_element);

}

void print_list(Node* Head) {
	while (1) {
		if (Head->next == NULL) {

			printf("%d", Head->element);
			break;
		}
		printf("%d", Head->element);
		Head = Head->next;
	}
	printf("\n");
}

void free_memory(Node** Head) {
	free(*Head);
}


```

## 双向链表

双向链表在内存中的存储方式是：
有12个格子，前面4个是value，中间4个是prev（指向上一个node），后面4个（next）指向下一个区域（即下一个节点（下一个node,就是下一组12个格子））。（自己设计）

第一个prev指向NULL，最后一个next指向NULL。

NULL<->0<->1<->2<->3<->NULL
![Pasted image 20240723185618](images/Pasted%20image%2020240723185618.png)

1. 访问头部，尾部：O(1)
2. 访问中间：O(N)
3. 插入头部，尾部：O(1)
4. 插入中间：O(N)
5. 搜索值：O(N)
6. 删除：同插入



## 循环链表

### 单向循环链表

单链表尾节点的地址指向第一个节点。

### 双向循环链表

最后一个next指向第一个node

## 链表的实际应用
  
单向链表：为堆栈，队列服务。报名顺序，看谁先到。用音乐播放器，加入播放列表（还会用到队列）。

双向链表：网页中的前进和后退。播放器中的上一首，下一首。


## 常见错误（注意事项）记录

1. 使用指针时，该指针指向是否非法（指向NULL）
  
2. 初始化变量不正确：memorry access...

3. 什么时候用malloc，什么时候不用？
- 注意：声明指向一个结构并不创建该结构，而只是给出足够空间容纳结构可能会使用的地址。
- 创建未被声明过的记录的唯一方法就是使用malloc库函数。
- malloc库函数创建一个新的结构并返回指向该结构的指针。

4. free的作用：P正在指向的地址没变，但是此地址处的数据已无定义了。

5. 当程序需要使用大量空间时，系统不满足你对新单元的要求，此时就会返回NULL。
6. 


## 与链表相关的算法
### 多项式ADT


### 基数排序


### 桶式排序


### 多重表
- 有点像把几个表合为一体，循环链表的应用（有表头）
实例：一个大学有40000名学生和2500门课程，此时需要生成两种类型的实验报告，一个列出每个课程的注册者（按课程分类），一个列出每个学生的课程（按学生分类）。

思路：可以使用二维数组来实现，但是需要很多项，于是，我们可以使用循环链表的方式来实现

![Pasted image 20240415145209](images/Pasted%20image%2020240415145209.png)

- 使用循环链表的缺点：节省空间但是要花时间
假设一个学生报名了所有课程，那么表中的每一项都需要检测来确定这个学生所有的课程名

## 链表的游标实现
- 主要用于没有指针但又需要使用链表的情况
 -首先我们需要看链表的指针实现有哪些特点：
	1. 数据存储在一组结构体中。
	2. 一个新的结构体可以通过调用malloc而从系统全局内存（global memory）得到，并且可以通过free释放

我们可以用创建一个next数组，这个数组里面是下个元素的位置，
![Pasted image 20240902194340](images/Pasted%20image%2020240902194340.png)
```C
typedef unsigned int node_ptr;
struct node
{
element_type element;
node_ptr next;
};
typedef node_ptr LIST;
typedef node_ptr position;
struct node CURSOR_SPACE[ SPACE_SIZE ];
```
游标实现的声明：结构体数组中的下标表示该链表各个结构体的序号，比如说头节点就是`CURSOR_SPACE[0]`
```C
position cursor_alloc(void)
{
position p;
p = CURSOR_SPACE[0].next;
CURSOR_SPACE[0].next = CURSOR_SPACE[p].next;
return p;
}

void cursor_free(position p)
{
CURSOR_SPACE[p].next = CURSOR_SPACE[0].next;
CURSOR_SPACE[0].next = p;
}
```


