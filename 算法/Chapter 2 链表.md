## 介绍与创建
### python
```python
#单链表
class SingleListNode:
    def __init__(self, value, next=None):
        """
        :param value:节点的值
        :param next: 下一个节点（默认为None）"""
        self.value = value
        self.next = next
#双链表
class DoubleListNode:
    def __init__(self, value, last=None, next = None):
        """
        初始化双链表节点
        :param value: 节点的值
        :param last:上一个节点（默认为None）
        :param next:下一个节点（默认为None）
        """
        self.value = value
        self.last = last
        self.next = next
```
### java
```java
public static class SingleListNode{  
    public int value;  
    public SingleListNode next;  
  
    public SingleListNode(int value){  
        this.value = value;  
    }  
  
    public SingleListNode(int value, SingleListNode next){  
        this.value = value;  
        this.next = next;  
    }  
}  
public static class DoubleListNode{  
    public int value;  
    public DoubleListNode last;  
    public DoubleListNode next;  
  
    public DoubleListNode(int value){  
        this.value = value;  
    }  
  
    public DoubleListNode(DoubleListNode last,int value, DoubleListNode next){  
        this.value = value;  
        this.last = last;  
        this.next = next;  
    }  
  
}
```

## 链表反转
### java
```java
public static SingleListNode reverseList(SingleListNode head){  
    SingleListNode pre = null;  
    SingleListNode next = null;  
  
    while(head != null){  
        next = head.next;  
        head.next = pre;  
        pre = head;  
        head = next;  
    }  
    return pre;  
}  
  
public static DoubleListNode reverseList(DoubleListNode head){  
    DoubleListNode pre = null;  
    DoubleListNode next = null;  
  
    while(head != null){  
        next = head.next;  
        head.last = next;  
        head.next = pre;  
        pre = head;  
        head = next;  
    }  
    return pre;  
}
```

### python
```python

def reverse_list(head):
    """
    Reverse a singly linked list.
    :param head: The head node of the singly linked list
    :return: The new head node of the reversed singly linked list
    """
    pre = None
    next = None
    while head:
        # Temporarily store the next node
        next = head.next
        # Reverse the 'next' pointer of the current node
        head.next = pre
        # Move the 'pre' pointer to the current node
        pre = head
        # Move to the next node in the original list
        head = next
    # 'pre' now points to the new head of the reversed list
    return pre
```
## 合并两个有序链表
### java
```java
public static SingleListNode mergeTwoLists(SingleListNode head1, SingleListNode head2){  
	//特殊情况
    if(head1 == null || head2 == null){  
        return head1 == null ? head2 : head1;  
    }  
  
    SingleListNode head = head1.value <= head2.value ? head1 : head2;  
  
    SingleListNode cur1 = head.next; //head开头的那一行  
    SingleListNode cur2 = head == head1 ? head2 : head1; //另一行  
    SingleListNode pre = head; //负责连接节点  
    while(cur1 != null && cur2 != null){  
        if(cur1.value > cur2.value){  
            pre.next = cur2;  
            cur2 = cur2.next;  
        }else {  
            pre.next = cur1;  
            cur1 = cur1.next;  
        }  
        pre = pre.next;  
    }  
    pre.next = cur1 == null ? cur2 : cur1;  
    return head;  
}
```
### python
```python
def mergeTwoLists(head1, head2):
    # Handle edge cases where one of the lists is empty
    if not head1 or not head2:
        return head2 if not head1 else head1
    # Determine the starting head of the merge list
    head = head1 if head1.value <= head2.value else head2
    cur1 = head.next # Advance the pointer of the selected starting list
    cur2 = head2 if head == head1 else head1# Set the other list
    pre = head # Pointer to connect nodes

    # Traverse both lists until ont of them is exhausted
    while cur1 and cur2:
        if cur1.value > cur2.value:
            pre.next = cur2
            cur2 = cur2.next
        else:
            pre.next = cur1
            cur1 = cur1.next
        pre = pre.next
    
    # Connect the remaining part of the non-exhausted list
    pre.next = cur1 if cur1 else cur2

    return head
```

## 链表相加
- 两个非空的链表，表示两个非负的整数，逆序存储每个节点一位数字，将两个数字相加，返回一个表示和的链表，假设除了0之外，两个数都不会以0开头（逆序加法，有进位）

### java
```java
public static SingleListNode addTwoNumbers(SingleListNode head1, SingleListNode head2){  
    //如果为空  
    if(head1 == null || head2 == null){  
        return head1 == null ? head2 : head1;  
    }  
  
    int carry = (head1.value + head2.value) / 10;  
    int sum = (head1.value + head2.value) % 10;  
    SingleListNode head = new SingleListNode(sum);  
  
    SingleListNode pre = head;  
    SingleListNode cur1 = head1.next;  
    SingleListNode cur2 = head2.next;  
  
    while(cur1 != null || cur2 != null){  
        //提取值  
        int value1 = (cur1 == null ? 0 : cur1.value);  
        int value2 = (cur2 == null ? 0 : cur2.value);  
  
        //计算和、进位  
        sum = (value1 + value2 + carry) % 10;  
        carry = (value1 + value2 + carry) / 10;  
        //创建新节点  
        pre.next = new SingleListNode(sum);  
        pre = pre.next;  
  
        if(cur1 != null) cur1 = cur1.next;  
        if(cur2 != null) cur2 = cur2.next;  
    }  
    if(carry > 0){  
        pre.next = new SingleListNode(carry);  
    }  
    return head;  
}
```
### python
```python

def addTwoNumber(head1, head2):
    """
    Add two numbers represented by two singly linked lists.
    Each node contains a single digit, and digits are stored in reverse order
    
    :praram head1: The head node of the first linked list
    :praram head2: The head node of the second linked list
    :return: The head node of the resulting linked list
    """
    # If one of the lists is empty, return the other list
    if not head1 or not head2:
        return head2 if not head1 else head1
    
    # Calculate the initial sum and carry
    carry = (head1.value + head2.value) // 10
    sum_value = (head1.value + head2.value) % 10

    # Create the head of the result list
    head = SingleListNode(sum_value)
    pre = head
    cur1 = head1.next
    cur2 = head2.next

    # Iterate through both lists
    while cur1 or cur2:
        # Get the current values(0 if the node is None)
        value1 = cur1.value if cur1 else 0
        value2 = cur2.value if cur2 else 0

        # Calculate the sum and carry
        sum_value = (value1 + value2 + carry) % 10
        carry = (value1 +value2 + carry) // 10

        # Create a new node for the sum
        pre.next = SingleListNode(sum_value)
        pre = pre.next

        # Advance to the next nodes
        if cur1:
            cur1 = cur1.next
        if cur2:
            cur2 = cur2.next
    # If there's a carry left, add a new node for it 
    if carry > 0:
        pre.next = SingleListNode(carry)
    return head

```
## 划分链表
### java
```java
public static SingleListNode partition(SingleListNode head ,int x){  
    SingleListNode leftHead = null; //小于x表头  
    SingleListNode rightHead = null;//大于等于x表头  
    SingleListNode next = null;//记录下一个节点  
    SingleListNode leftPre = null;//左边表尾  
    SingleListNode rightPre = null;//右边表尾  
  
    while(head != null) {  
        next = head.next;  
        head.next = null;  
        if(head.value < x){  
            if(leftHead == null) {//初始化左表头，左表尾  
                leftHead = head;  
                leftPre = head;  
            }else {  
                leftPre.next = head;//连接新表尾  
                leftPre = head; //更新左表表尾  
            }  
        }else{  
            if(rightHead == null) {//初始化右表头，右表尾  
                rightHead = head;  
                rightPre = head;  
            }else {  
                rightPre.next = head;  
                rightPre = head;  
            }  
        }  
        head = next;  
    }  
  
    if(leftHead == null){  
        return rightHead;  
    }  
    leftPre.next = rightHead;  
    return leftHead;  
}
```

### python
```python
def partition(head, x):
    """
    Partition a linked list around a value x,such that all nodes with values less than x come before nodes with values greaterr than or equal to x.
    :param head: The head of the singly linked list
    :param x: The partition value
    :return: The head of the modified linked list
    """
    leftHead = None # Head of the list for nodes < x
    rightHead = None # Head of the list for nodes >= x
    leftPre = None # Tail of the left list
    rightPre = None # Tail of the right list

    while(head):
        next = head.next # store the next node
        head.next = None # Isolate the current node

        if head.value < x:
            # Add to the left list
            if not leftHead:
                leftHead = head #Initial left list head
                leftPre = head # Initial left list tail
            else:
                leftPre.next = head # Append to the left list
                leftPre = head # Update the left list tail
        else:
            # Add to the right list
            if not rightHead:
                rightHead = head # Initialize right list head
                rightPre = head # Initialize right list taill
            else:
                rightPre.next = head # Append to the right list
                rightPre = head # Update the right list tail
        head = next # Move to the next node
    # Combine the two lists
    if not leftHead:
        return rightHead # If the left list is empty, return the right list
    leftPre.next = rightHead #Connect the end of the left list to the right list
    return leftHead #Return the head of the combined list
```


## 高频题
- 如果空间要求不严格，直接使用容器解决
- 如果空间要求严格，或者在面试中强调空间的优化，需要额外使用空间复杂度$O(1)$的方法，不宜使用容器
- 常用技巧——快慢指针
- 往往考验coding能力

- 锻炼的coding能力，空间上讨巧不建议
	- 只用有限几个变量将链表问题解决即可

### 返回两个无环链表相交的第一个节点
- 相交：两个不同链表的其中某一个节点指向同一个节点
- 判断
	- 相交的两个链表最后一个节点相等（内存地址一样）
- 容器法
	- 使用hashSet
	- 将其中一个链表存入hashSet，另一个链表一个一个拿出来看hashSet里有没有
	- 第一个有的就是相交的第一个节点

- 使用有限变量解决
```java
public static ListNode getIntersectionNode(ListNode h1, ListNode h2){
	if(h1 == null || h2 == null){
		return null;
	}
	ListNode a = h1, b = h2;
	int diff = 0;
	//diff表示两个链表的个数差值
	while(a.next != null){
		a = a.next;
		diff++;
	}
	while(b.next != null){
		b = b.next;
		diff--;
	}
	if(diff >= 0){
		//a表示更长的部分
		a = h1;
		b = h2;
	}else{
		a = h2;
		b = h1;
	}
	diff = Math.abs(diff);
	while(diff-- != 0){ //先判断不等于0，再-1
		a = a.next;
	}
	while(a != b){
		a = a.next;
		b = b.next;
	}
}
```

### 每k个节点一组翻转链表
- 每组k个节点逆序，不足k个节点保持
- 容器法
	- 将所有数装到一个数组中，使用下标进行交换

- 使用有限变量
	- 循环
		- 先判断有无k个结点，够返回尾结点，不够返回null
			- 拿到当前的头节点和尾结点
		- 每组分别进行链表反转，反转后修改头节点和尾结点
			- （reverse中实现：尾节点暂时指向后面一个）
			- 第2组处理完后修改头节点和尾结点，即，将前一组的尾结点连到该 当前头结点
		- 直到不足k个结点
	- 第1组反转后需要额外记录头节点（特殊处理）
		- 第1组单拿出来，其他的进循环
	- 链表反转逻辑
		- 反转后尾节点暂时指向后面一组的第一个
	
```java
public static ListNode reverseKGroup(ListNode head, int k){
	ListNode start = head;
	//是否够k个结点，够就返回第k个，不够返回null
	ListNode end = teamEnd(start, k);
	if(end == null){
		return head;
	}

	//第1组单拎出来
	head = end;
	//将尾结点连到下一组的第一个也在链表反转中一并处理
	reverse(start, end);
	
	//翻转后第1组的start称为上1组的尾结点
	ListNode lastTeamEnd = start;
	//第2组进循环
	while(lastTeamEnd.next != null){
		start = lastTeamEnd.next;
		end = teamEnd(start, k);
		if(end == null){
			return head;
		}
		reverse(start, end);
		lastTeamEnd.next = end;//老上一组
		lastTeamEnd = start;//新上一组	
	}
	return head;
}
```

### 复制带随机指针的链表
- 结点结构中不止有val和next，还有random（随机指向某个结点）

- 容器法
	- 使用hashMap
	- 每个结点都生成一个复制体结点，原结点位于key，复制体结点位于value
	- 原结点指哪，复制体指哪

- 使用必要的空间和额外几个变量
	- 准备需要的结点，分别插入给的链表
	- 复制体1号结点（假设是1‘）插入1和2中间
	- 2’插入2和3中间
	- ...
	- 复制体和原结点为一组分开
	- 例如，1‘根据1号找到1的random结点，并指向对应结点的复制体结点

```java
public static Node copyRandomList(Node head){
	if(head == null){
		return null;
	}
	Node cur = head;
	Node next = null;

	while(cur != null){
		//原链表的下一个结点
		next = cur.next;
		//1'，2'，...的插入
		//1->1'->2->2'->...
		cur.next = new Node(cur.val);
		//当前结点下一个的下一个才是原链表
		cur.next.next = next;
		cur = next;
	}
	cur = head;
	Node copy = null;

	// 取得随机指针位置
	while(cur != null){
		next = cur.next.next;
		copy = cur.next;
		copy.random = cur.random != null ? cur.random.next : null;
		cur = next;
	}

	Node ans = head.next;
	cur = head;
	//新老链表分离
	while(cur != null){
		next = cur.next.next;
		copy = cur.next;
		cur.next = next;
		copy.next = next != null ? next.next : null;
		cur = next;
	}
	return ans;
}
```

### 技巧：快慢指针找中点
#### 判断链表是否是回文结构
- 容器法
	- 将链表放入栈中再弹出

- 使用快慢指针
	- 准备两个指针，s走一步，f走2步
	- 等f无路可走时，s在大概中点的位置
	- 将s后面的节点倒过来指，中点s指null
	- left和right对比，相同则是回文
	- 用完后倒回来
```java
public static boolean isPalindrome(ListNode head){
	if(head == null || head.next == null){
		return true;
	}
	ListNode slow = head, fast = head;

	//找中点
	while(fast.next != null && fast.next.next != null){
		slow = slow.next;
		fast = fast.next.next;
	}

	//中点为slow，中点后面的节点逆序
	ListNode pre = slow;
	ListNode cur = pre.next;
	ListNode next = null
	pre.next = null //中点指null
	while(cur != null){
		next = cur.next;
		cur.next = pre;
		pre = cur;
		cur = next;
	}

	//左右比较
	boolean ans = true;
	ListNode left = head;
	ListNode right = pre;
	while(left != null && right != null){
		if(left.val != right.val){
			ans = false;
			break;
		}
		left = left.next;
		right = right.next;
	}

	//还原链表
	cur = pre.next;
	pre.next = null;
	next = null;
	while(cur != null){
		next = cur.next;
		cur.next = pre;
		pre = cur;
		cur = next;
	}
	return ans;
}
```

#### 返回链表的第一个入环结点
- 链表一旦入环就出不去
- slow走1步，fast走2步
	- 当fast遇到null说明无环
	- 与slow相遇，说明有环
- 相遇后，fast回到开头，一步一步走
- slow和fast再次相遇一定在入环节点（建议死记）

```java
public static ListNode detectCycle(ListNode head){
	if(head == null || head.next == null || head.next.next == null){
		return null;
	}
	ListNode slow = head.next;
	ListNode fast = head.next.next;
	while(slow != fast){
		if(fast.next == null || fast.next.next == null){//3个点以下是null说明无环
			return null;
		}
		slow = slow.next;
		fast = fast.next.next;
	}

	//slow和fast相遇后
	fast = head;
	while(slow != fast){
		slow = slow.next;
		fast = fast.next;
	}
	return slow;
}
```
 

### 在链表上排序
- 要求
	- 时间复杂度：$O(N*logN)$
	- 空间复杂度：$O(1)$
	- 具有稳定性

- 分析
	- 数组无法实现，时间复杂度：$O(N*logN)$
	- 递归无法实现，空间复杂度：$O(1)$
		- 递归合并的时候最好也就$O(logN)$

- 交换思想
	- 使用步长
	- 1：每组两个比较（1v1）
	- 2：每组4个（2v2）
	- 3：每组8个（4v4）
	- 4：...
	- ...（n/2 v n/2）
```java
public static ListNode start;
public static ListNode end;

//l1...r1,每组比较的左边部分
//l2...r2,每组比较的右边部分
//merge起来
public static void merge(ListNode l1, ListNode r1, ListNode l2, ListNode r2){
	ListNode pre;
	//第1组单拎出来，确定头节点
	if(l1.val <= l2.val){
		start = l1;
		pre = l1;
		l1 = l1.next;
	}else{
		start = l2;
		pre = l2;
		l2 = l2.next;
	}

	//后面的进循环
	while(l1 != null && l2 != null){
		if(l1.val <= l2.val){
			pre.next = l1; //箭头更新
			pre = l1; //左部分前数更新，进入下一次
			l1 = l1.next;//左部分当前数更新
		}else{
			pre.next = l2;
			pre = l2;
			l2 = l2.next;
		}
	}
	if(l1 != null){
		pre.next = l1;
		end = r1;
	}else{
		pre.next = l2;
		end = r2;
	}
}
```



## 约瑟夫环（难点）
- Josephus问题
分析：[约瑟夫环问题详解（图文结合）--C语言-CSDN博客](https://blog.csdn.net/qq_63412763/article/details/124514192)

- 常规：挑一个从头开始，再挑一个从头开始...
- 利用取余来优化程序

