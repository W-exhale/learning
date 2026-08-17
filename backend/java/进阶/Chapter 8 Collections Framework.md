## Part 1 引入
### 概念
- 使用传统数组的方式进行CRUD是一件十分困难的事情
```java
public class MyTest {  
    public static final int SIZE = 3;  
    @Test  
    public void testArray(){  
        int[] array = new int[SIZE];  
  
        array[0] = 1;  
        array[1] = 2;  
        array[2] = 3;  
  
        for (int i = 0; i < array.length; i++) {  
            System.out.println(array[i]);  
        }  
    }  
}
```
- 例如上面的代码，如果我们要对array进行扩容，是一件很复杂的事情，所以实际上很少用到这种传统数组的方式。
- Java中一般会用到Java集合框架（函数库）进行Java扩容。
- **Java集合框架**（**Java collections framework**）是一个包含一系列实现可重复使用集合的数据结构的类和接口集合。虽然称为“框架”，其使用方式却像个函数库。集合框架提供了定义各式各样集合的接口和实现上述集合的类。


- 与数组的区别：
	1. 集合在声明时不需要指定固定的容量。
	2. 集合可以在新增或移除内容时自动地增加或缩减其容量。 
	3. 集合无法收纳基本数据类型，像是整数（int）、长整数（long）或者双精度浮点数（double），但是可以收纳上述基本数据类型的封装类型（Integer、Long、Double）

- 可以分为三种：有序列表（ordered lists）、映射表（maps）、集（sets）
	- 有序列表容许程序员依序地加入元素，并以同样的顺序取回元素，例如等候列表。在有序列表接口底下有两个子接口，分别为**列表**（Lists）和**队列**（Queue）。
	- 映射表使用索引来参考对象并取回其值。在映射表接口底下有一个子接口**映射表**（Map）。
	- 集是一种可供遍巡的无序集合，但当中不允许重复的对象存在。在其中有个子接口**集**（Set）。

### 结构
- Iterable：Iterable 是**迭代器的意思，作用是为集合类提供for-each循环的支持**。 由于使用for循环需要通过位置获取元素，而这种获取方式仅有数组支持，其他许多数据结构，比如链表，只能通过查询获取数据，这会大大的降低效率。 Iterable 是可以为不同的集合类提供遍历的最佳方式。（先不管）
- 一些集合实现对它们可能包含的元素有限制，例如某些实现禁止使用null元素，而某些实现对元素类型进行限制。（例如考试缺考，不是给0分，而是给null）。如果尝试添加了不合格元素就会引发异常（通常是NullPointerException或ClassCastException），若尝试查询则可能返回false。
- 主要分为两种：Collection和Map


![[Pasted image 20250112155344.png]]
![[Pasted image 20250112155359.png]]
## Part 2 ArrayList
### Section 1 介绍
- List：List接口可以自动扩容（检测到元素增加）
- ArrayList：1. 实现List接口，2. 提供一些方法来操纵内部用于存储list的数组大小。
- 每个实例都有一个容量。用于在列表中存储元素的数组大小。它总是至少与列表大小一样大。

### Section 2 泛型
- 限制类型，arraylist可以接收所有数据类型的封装类型，为了严谨，要使用泛型进行限定，否则会被认为是不安全

```java
public void arrayList1(){  
    ArrayList<String> arrayList = new ArrayList<>();  
    arrayList.add("Frank");  
    arrayList.add("Alice");  
    arrayList.add("Tom");  
    arrayList.add("Exhale");  
    System.out.println(arrayList);  
}
```
![[Pasted image 20250112165924.png]]

### Section 3 方法的使用
1. add()
2. size()：容量
3. get(int index)：获取元素
4. addAll(集合)
5. clear()
6. clone()：返回一个shallow copy的ArrayList实例
7. contains(Object o)：判断list中有无某个值，有就返回true
8. ensureCapacity(int minCapacity)：指定list的最小容量
9. foreach(Consumer\<? super E\> action)：（新特性）
10. indexOf(...)：元素对应的第一个下标
11. lastIndexOf(...)：元素对应的最后一个下标
12. isEmpty()：判断是否为空
13. remove(...)：删除某元素，如果是int类型就是删除index对应的元素
14. removeAll(集合)：删除括号中的集合
15. removeRange(int index, int index)：从某下标到某下标的都删除，但protected只能在ArrayList内部的包用
16. replaceAll()：替换，regex表示正则表达式（新特性）
17. retainAll(集合)：取交集赋给.前的数，返回boolean
18. sort()：排序（新特性），void
19. Collections.sort(list)：排序（这个类里面专门处理一些和collection有关的东西）
20. Collections.reverse(list)：置反
21. subList(int fromIndex, int toIndex)：给定下标之间的的数，后面的不包括`[fromIndex,toIndex)`
```java
public void arrayList2(){  
    ArrayList<Student> arrayList = new ArrayList<>();  
    System.out.println(new Student("Frank", 21));  
    System.out.println(new Student("Alice", 24));  
    System.out.println(new Student("Tom", 32));  
    System.out.println(new Student("Exhale", 45));  

	//插入的index必须在已存在的序列之中  
	arrayList.add(2, "Tim");
	arrayList.clear();//清空
}
-Student.java
public class Student {  
    private String name;  
    private int age;  
  
    public Student(){  
  
    }  
    public Student(String name, int age){  
        this.name = name;  
        this.age = age;  
    }  
  
    @Override  
    public String toString() {  
        return "Student{" +  
                "name='" + name + '\'' +  
                ", age=" + age +  
                '}';  
    }  
}
```
![[Pasted image 20250112170327.png]]

`//将一个数组(arrayList1)放到另一个数组(arrayList)中`  
`arrayList.addAll(arrayList1);`
也可以index指定位置，

- 遍历：不仅仅是输出，还可以对每一个元素进行操作
- foreach就是高级遍历（fori遍历需要知道控制size）
```java
for(Integer value : arrayList){
	System.out.println(value + 1);
}
```

## Part 3 LinkedList 链表
- 链表的应用：
	- 文件系统
	- git每次commit都创建一个node，node包含删减后的新文件，然后node指向前一个commit的node。git checkout、delete branch、merge、rebase这些基本上都是以链表操作为主。
	- 贪吃蛇链表？

- 要用List就用ArrayList，要用Queue就用ArrayDeque，链表用的比较少
peek()：返回头元素，如果list为空就是null
element()：返回list的头部
poll()：移出头元素
.....

## Part 4 Iterator 迭代器
- 除了fori和foreach还有iterator这种遍历方式
- Collection和Map主要是用于存储，Iterator只是用来遍历的
- 遍历对象：只能对Collection进行遍历（Collection实现了Iterator接口）

- 使用方式
```java
public void arrayList1(){  
    ArrayList<String> arrayList = new ArrayList<>();  
    arrayList.add("Frank");  
    arrayList.add("Alice");  
    arrayList.add("Tom");  
    arrayList.add("Exhale");  
    Iterator<String> iterator = arrayList.iterator();  //这里如果不使用泛型下面value的值就要用Object
    while(iterator.hasNext()){//next exists return true  
        String value = iterator.next();  
        System.out.println(value);  
    }  
}
```

使用迭代器，可以不用规定size（fori需要）和需要迭代的类型，即使类型是LinkedList，可以直接用上面的模型（可以感觉出来，迭代器有点像链表）

- 三种遍历方式的区别
	1. fori：能读能修改
	2. foreach：只能读（可以通过对象引用改）
	3. Iterator：能读能改，但是改需要通过iterator修改，不能arrayList.remove()修改，使用iterator.remove()。

- 注意：迭代器不要使用嵌套，即不要在for里用迭代器，都是next，用着用着就找不到元素了
- 其实foreach是一个小型的迭代器

- 性能问题：
	- fori取决于list大小，如果是ArrayList的列表（分配的是连续的内存空间），时间复杂度是O(1)（也叫随机访问）；如果是LinkedList，时间复杂度就是O(N)（最坏的情况）
	- 对于LinkedList来说，foreach和迭代器肯定会更快
		- 使用fori：使用索引的方式访问，需要从头遍历到第i个节点，每次至多O(n)，总体$O(n^2)$
		- 使用foreach：本质上是通过Iterator实现的遍历，通过链表内部的指针顺序访问节点，每次是O(1)，整体是O(n)
		- Iterator：同上，需要修改时用这个
	- 如果是允许随机访问的集合例如arraylist，都一样，会自动采取

## Part 5 Set
- Set和ArrayList一样都是集合的一种
- 特点：没有顺序，不能重复
- HashSet（最常见）、LinkedHashSet、TreeSet
-
### Section 1 HashSet
```java
public void hashSet1(){  
    HashSet<String> hashSet = new HashSet<>();  
    hashSet.add("Frank");  
    hashSet.add("Tom");  
    hashSet.add("Rose");  
    hashSet.add("Frank");  
    hashSet.add("Tim");  
    System.out.println(hashSet);  
}
```
![[Pasted image 20250121160139.png]]

- 可以看到输出是无序的，不是按照输入顺序来的
- 同时也不是重复的，后续添加重复的值是静止添加，不是覆盖

>Hash ：单项散列函数，使用数组和链表来实现的（1.8之前）
> 1.8之后用数组、链表、红黑树实现的

### Section 2 LinkedHashSet
- 有顺序的HashSet

```java
public void hashSet1(){  
    LinkedHashSet<String> linkedHashSet = new LinkedHashSet<>();  
  
    linkedHashSet.add("Frank");  
    linkedHashSet.add("Tom");  
    linkedHashSet.add("Rose");  
    linkedHashSet.add("Frank");  
    linkedHashSet.add("Tim");  

    Iterator<String> iterator = linkedHashSet.iterator();   
    while (iterator.hasNext()){  
        String value = iterator.next();  
        System.out.println(value);  
    }  
}
```
![[Pasted image 20250121162046.png]]

## Part 6 Map
![[Pasted image 20250112155359.png]]
### Section 1 HashMap
```java
public void hashMap1(){  
    HashMap<Integer, String> hashMap = new HashMap<>();  
    hashMap.put(100001, "Frank");  
    hashMap.put(100002, "Tom");  
    hashMap.put(100003, "Jack");  
    hashMap.put(100004, "Tim");  
    hashMap.put(100005, "Exhale");  
    hashMap.put(100006, "Frank");  
  
    System.out.println(hashMap);  
  
    String value = hashMap.get(100002);  
    System.out.println(value);  
  
    hashMap.remove(100001);  
    System.out.println(hashMap);  
  
    System.out.println(hashMap.containsKey(100001));  
}
```
![[Pasted image 20250121163549.png]]

- keySet的使用：
```java
Set<Integer> keys = hashMap.keySet();  
System.out.println(keys);
```
![[Pasted image 20250121164324.png]]
主要是用来遍历

- 装值：Entry
```java
Set<Entry<Integer, String>> entrySet = hashMap.entrySet();  
System.out.println(entrySet);
```

- 替换：replace，put 也行，但是不安全
`hashMap.replace(100001, "JJJJJ");`


### Section 2 LinkedHashMap
- 有序的Map 