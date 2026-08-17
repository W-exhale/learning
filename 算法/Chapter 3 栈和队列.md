## 概念
### 队列
- 属性：头，尾（$[头,尾)$，所以头<尾时说明有东西，=时无）
- 方法：
	- isEmpty()
	- offer()：加入
	- poll()：出
	- peek()：查头
	- size()：The number of queue elements
- java自带的Queue是双向链表，其实单向链表就够了
- 做题时推荐使用静态数组，常数时间更好，一般会规定limit
- 上面两种在时间复杂度上是ok的，区别主要在常数时间
```java
public static class Queue1{  
    public int[] queue;  
    public int head;  
    public int tail;  
  
    public Queue1(int n){  
        queue = new int[n];  
        this.head = 0;  
        this.tail = 0;  
    }  
    public boolean isEmpty(){  
      return head == tail;  
    }  
  
    //加入队列  
    public void offer(int num){  
        queue[tail++] = num;  
    }  
  
    //从队列中取出头，并返回该元素  
    public int poll(int num){  
        return queue[head++];  
    }  
  
    //显示头  
    public int peek(){  
        return queue[head];  
    }  
    //计数  
  
    public int size(){  
        return tail - head;  
    }  
  
}
```
### 栈
- 属性：size（虚的，闭的作用）
- 方法：
	- isEmpty()
	- push()
	- pop()：弹出栈顶并返回该元素
	- peek()
	- size()：同上
- java自带的Stack用动态数组表示，也是常数时间的问题
- 用数组
```java
public static class Stack1{  
    public int size;  
    public int[] stack;  
  
    public Stack1(int num){  
        stack = new int[num];  
        size = 0;  
    }  
  
    public boolean isEmpty(){  
        return size == 0;  
    }  
  
   public void push(int num){  
        stack[size++] = num;  
   }  
  
   public int pop(){  
        return stack[--size];  
   }  
  
   public int peek(){  
       return stack[size - 1];  
   }  
  
   public int size(){  
        return size;  
   }  
}
```
## 循环队列
- [[循环队列.excalidraw]]
- 属性：头，尾,limit,size
- 方法：
622.
```java
class MyCircularQueue {  
    public int head;  
    public int tail;  
    public int size;  
    public int limit;  
    public int[] queue;  
  
    public MyCircularQueue(int k) {  
        queue = new int[k];  
        this.head = 0;  
        this.tail = 0;  
        this.size = 0;  
        this.limit = k;  
    }  
    public boolean enQueue(int value) {  
        if(isFull()){  
            return false;  
        }else{  
            queue[tail++] = value;  
            tail = limit == tail ? 0 : tail;  
            size++;  
            return true;        }  
    }  
    public boolean deQueue() {  
        if(isEmpty()){  
            return false;  
        }else{  
            head = limit == head + 1 ? 0 : head + 1;  
            size--;  
            return true;        }  
    }  
    public int Front() {  
        if(isEmpty()){  
            return -1;  
        }else{  
            return queue[head];  
        }  
    }  
  
    public int Rear() {  
        if(isEmpty()){  
            return -1;  
        }else{  
            int last = tail == 0 ? limit - 1 : tail - 1;  
            return queue[last];  
        }  
    }  
  
    public boolean isFull(){  
        return size == limit;  
    }  
    public boolean isEmpty(){  
        return size == 0;  
    }  
}
```
## 栈和队列相互实现
### 栈—>队列
- 标准栈就是只有isEmpty，pop，push，peek功能的栈
- 思路：准备两个栈，先将数据压入in栈，再将in栈的数据倒入out栈（倒了in栈就空了）
- 倒的原则：1.out空了才能倒，2.如果要倒，in栈要清空（倒完）
- 232
#### java
- 时间复杂度：每个方法都是$O(1)$ 
- 每个数进入in和out的次数是有限的，都是一次，均摊一下就是$O(1)$
```java
public class MyQueue{  
    public Stack<Integer> in;  
    public Stack<Integer> out;  
  
    public MyQueue(){  
    in = new Stack<Integer>();  
    out = new Stack<Integer>();  
    }  
  
    //倒数据  
    //从in栈将数据倒入out栈  
    //1.out空了，才能倒数据  
    //2.倒数据的时候in必须倒完  
    private void inToOut(){  
        if(out.isEmpty()){  
            while(!in.isEmpty()){  
                out.push(in.pop());  
            }  
        }  
    }  
  
    public void push(int x){  
        in.push(x);  
        inToOut();  
    }  
    public int pop(){  
        inToOut();  
        return out.pop();  
    }  
    public int peek(){  
        inToOut();  
        return out.peek();  
    }  
    public boolean empty(){  
        return out.isEmpty() && in.isEmpty();  
    }  
}
```

### 队列—>栈
- 思路：将新推入的数前面的数从头开始排到队尾
- 225
#### java
```java
class MyStack{  
  
     public Queue<Integer> queue;  
  
     public MyStack() {  
         queue = new LinkedList<Integer>();  
     }  
  
     public void push(int x){  
         int record = queue.size();  
         queue.offer(x);  
         for (int i = 0; i < record; i++) {  
             queue.offer(queue.poll());  
         }  
     }  
  
     public int pop(){  
         return queue.poll();  
     }  
  
     public int top(){  
         return queue.peek();  
     }  
  
     public boolean empty(){  
         return queue.isEmpty();  
  
     }  
}
```


## 最小栈
- 思路： 准备两个栈，一个存放数据的栈，一个最小值栈，如果val小于min栈栈顶，就push val，否则push min栈顶，也可以不压min栈栈顶除非val更小
- 可以用数组实现，更快，要指定一个最大数组容量，得看力扣的限制
- 155

```java
class MinStack{  
     public Stack<Integer> data;  
     public Stack<Integer> min;  
     public MinStack(){  
         data = new Stack<Integer>();  
         min = new Stack<Integer>();  
     }  
     public void push(int val){  
         data.push(val);  
         if(min.isEmpty() || val < min.peek()){  
             min.push(val);  
         }else{  
             min.push(min.peek());  
         }  
     }  
     public void pop(){  
        data.pop();  
        min.pop();  
     }  
     public int top(){  
         return data.peek();  
     }  
     public int getMin(){  
         return min.peek();  
     }  
}
```

## 双端队列
- 可以从头部进，头部出；尾部进，尾部出（同时实现FIFO，LIFO）
- java提供了一个Deque（双端队列）接口，可以用LinkedList实现
- 也可以用固定数组实现

- 使用deque
```java
class  MyCircularDeque{  
     public Deque<Integer> deque = new LinkedList<Integer>();  
     public int size;  
     public int limit;  
     public MyCircularDeque(int k){  
        size = 0;  
        limit = k;  
     }  
     public boolean insertFront(int value){  
        if(isFull()){  
            return false;  
        }else{  
            deque.offerFirst(value);  
            size++;  
            return true;        }  
     }  
     public boolean insertLast(int value){  
         if(isFull()){  
             return false;  
         }else{  
             deque.offerLast(value);  
             size++;  
             return true;         }  
     }  
     public boolean deleteFront(){  
         if(isEmpty()){  
             return false;  
         }else{  
             deque.pollFirst();  
             size--;  
             return true;         }  
     }  
     public boolean deleteLast(){  
         if(isEmpty()){  
             return false;  
         }else{  
             deque.pollLast();  
             size--;  
             return true;         }  
     }  
     public int getFront(){  
         if(isEmpty()){  
             return -1;  
         }  
         return deque.peekFirst();  
     }  
     public int getRear(){  
         if(isEmpty()){  
             return -1;  
         }  
         return deque.peekLast();  
     }  
     public boolean isEmpty(){  
         return size == 0;  
     }  
     public boolean isFull(){  
         return size == limit;  
     }  
}
```

- 使用固定数组
```java
class  MyCircularDeque{  
     public int[] deque;  
     public int size, limit, left, right;//left和right表示的左开右开  
     public MyCircularDeque(int k){  
         deque = new int[k];  
         size = left = right = 0;  
         limit = k;  
     }  
     public boolean insertFront(int value){  
        if(isFull()){  
            return false;  
        }else{  
            if(left == right && left == 0){  
                 deque[0] = value;  
                 left = limit - 1;  
                 right = 1;  
            } else if(left == 0){  
                deque[left] = value;  
                left = limit - 1;  
            }else{  
                deque[left--] = value;  
            }  
            size++;  
            return true;        }  
     }  
     public boolean insertLast(int value){  
         if(isFull()){  
             return false;  
         }else{  
             if(left == right && left == 0){  
                 deque[0] = value;  
                 left = limit - 1;  
                 right = 1;  
             }else if(right == limit - 1){  
                 deque[right] = value;  
                 right = 0;  
             }else{  
                deque[right++] = value;  
             }  
             size++;  
             return true;         }  
     }  
     public boolean deleteFront(){  
         if(isEmpty()){  
             return false;  
         }else{  
             if(left == limit - 1){  
                 left = 0;  
             }else{  
                 left++;  
             }  
             size--;  
             return true;         }  
     }  
     public boolean deleteLast(){  
         if(isEmpty()){  
             return false;  
         }else{  
             if(right == 0){  
                right = limit - 1;  
             }else{  
                 right--;  
             }  
             size--;  
             return true;         }  
     }  
     public int getFront(){  
         if(isEmpty()){  
             return -1;  
         }  
         return left == limit - 1 ? deque[0] : deque[left + 1];  
     }  
     public int getRear(){  
         if(isEmpty()){  
             return -1;  
         }  
         return right == 0 ? deque[limit - 1] : deque[right - 1];  
     }  
     public boolean isEmpty(){  
         return size == 0;  
     }  
     public boolean isFull(){  
         return size == limit;  
     }  
}
```

## 单调栈


## 单调队列

