## 专业术语
- 介绍：栈（LIFO表）
--LIFO 后进先出（last in,first out）
---
专业术语
- top：表的末端，push和pop只能在这个位置进行
- Push例程：叠盘子（入栈）
- Pop例程：拿走盘子，在下面的盘子拿不出来，只能从上往下拿。先进后出。（出栈）
- Top例程：查看栈顶（只有栈顶是可访问的）
- 注意：
	- 不能对空栈进行Pop和Top（一般会认为是栈ADT的错误）
	- 运行Push时空间用尽（实现错误，不是ADT错误（不正确使用ADT））
![Pasted image 20240723233546](images/Pasted%20image%2020240723233546.png)



应用：
- 撤销功能
- 剪切板就是一个栈P
- 操作系统中的内存管理
- 匹配括号，（IDE中自动出后半个括号），先把左边的括号放到栈中，再看有没有匹配的右括号。
- 浏览器的历史记录，最近关闭的标签页

## 栈的实现（两种）：
- 实现栈的注意事项
1. 创建结构体
2. 使用动态内存分配
3. 在pop之后要注意释放结构体的内存
4. pop时注意判断是否是栈
5. push时注意判断栈是否已满
6. 如果使用数组的方式，空栈的top of stack为-1
#### 单链表
- 会有一个测试空表的函数
```C
int is_empty( STACK S ){
	return( S->next == NULL );
}
```
- 创建空栈
```C
STACK create_stack( void ){
STACK S;
S = (STACK) malloc( sizeof( struct node ) );
if( S == NULL )
	fatal_error("Out of space!!!");
return S;
}
//fatal_error编译器在编译代码时遇到了无法继续编译的错误

void make_null( STACK S ){
if( S != NULL )
	S->next = NULL;
else
	error("Must use create_stack first");
}
```
- push
```C
void push( element_type x, STACK S ){
node_ptr tmp_cell;
tmp_cell = (node_ptr) malloc( sizeof ( struct node ) );
if( tmp_cell == NULL )
	fatal_error("Out of space!!!");
else{
	tmp_cell->element = x;
	tmp_cell->next = S->next;
	S->next = tmp_cell;
	}
}
```
- pop
```C
void pop( STACK S ){
node_ptr first_cell;
if( is_empty( S ) )
	error("Empty stack");
else{
	first_cell = S->next;
	S->next = S->next->next;
	free( first_cell );
	}
}
```

- 链表的缺点
对malloc，free调用的开销是昂贵的
#### 数组
- 使用栈可以放在数组里，要用的时候只取最后一个数，添加也只在后面添加，不能往前塞。
- 潜在问题：需要提前声明数组的大小。但是在典型的应用程序中，即使有相当多的栈操作，在任一时刻，栈元素的实际个数不会太大，声明一个足够大的数组即可。如果用数组不能实现，就需要考虑用链表。

在数组实现中，如果是空栈，它的top of stack就是-1。当压入一个元素，$STACK[top\space of\space stack]$中的tos就加1，如果是pop操作tos就减1。注意不要用全局变量和固定名字来表示栈，在实际程序中总是存在多于一个栈。

```C
#define EMPTY_TOS -1 // 用来表示空表
#define MIN_STACK_SIZE 10
struct stack_record {
	unsigned int stack_size;
	int top_of_stack;
	int* stack_array;
};
typedef struct stack_record* STACK;
//创建一个栈
STACK create_stack(unsigned int max_elements) {
	STACK S;
	if (max_elements < MIN_STACK_SIZE) {
		error("Stack size is too small");
	}
	S = (STACK)malloc(sizeof(struct stack_record));
	if (S == NULL) {
		fatal_error("Out of space!!!");
	}
	S->stack_array = (int*)malloc(sizeof(int) * max_elements);
	if (S->stack_array == NULL) {
		fatal_error("Out of space!!!");
	}
	S->top_of_stack = EMPTY_TOS;
	S->stack_size = max_elements;
	return(S);
}

void dispose_stack(STACK S) {
	if (S != NULL) {
		free(S->stack_array);
		free(S);
	}
}

int is_empty(STACK S) {
	return(S->top_of_stack == EMPTY_TOS);
}

void make_null(STACK S) {
	S->top_of_stack = EMPTY_TOS;
}

void push(int x, STACK S) {
	if (is_full(S)) {
		error("Full stack");
	}
	else {
		S->stack_array[++(S->top_of_stack)] = x;
	}
}

int top(STACK S) {
	if (is_empty(S)) {
		error("Empty stack");
	}
	else {
		return S->stack_array[S->top_of_stack];
	}
}

void pop(STACK S) {
	if (is_empty(S)) {
		error("Empty stack");
	}
	else {
		S->top_of_stack--;
	}
}

int pop(STACK S) {//返回pop后的top
	if (is_empty(S)) {
		error("Empty stack");
	}
	else {
		return S->stack_array[S->top_of_stack--];
	}
}
```

## 栈的应用
### 平衡符号
- 解释：在编译器中

### 时间复杂度

#### push

O(1)

#### pop

O(1)

#### 查看
 - 查看栈顶元素
 Peeking at the element on the top of the stack.
 
 - 要拿编号为12的，O(N - 12),其实就是O(N)

可以用动态数组实现，单向链表也可以。

![Pasted image 20240317111210](images/Pasted%20image%2020240317111210.png)

push()叠盘子，无返回值
peek() 返回栈顶元素，但不在堆栈中删除它。  
pop() 返回栈顶元素，并在进程中删除它。

