## 二叉树及其三种递归遍历
- 先序：中 左 右 1 2 4 5 3 6 7
- 中序：左 中 右 4 2 5 1 6 3 7（有种直接把树拍扁的感觉）
- 后序：左 右 中 4 5 2 6 7 3 1（中间的1最后，先左树，后右数）
- 树：
```java
public static class TreeNode{  
    public int val;  
    public TreeNode left;  
    public TreeNode right;  
  
    public TreeNode(int v){  
        val = v;  
    }  
}
```
### 先序
- 从1开始，1是中，直接打印，再进入左树，如果是中，打印，如果为null，返回
[[先序.excalidraw]]
```java
//先序打印  
public static void preOrder(TreeNode head){  
    if(head == null){//如果为空，返回  
        return;  
    }  
    System.out.println(head.val + " ");  
    preOrder(head.left);  
    preOrder(head.right);  
}
```

### 中序
- 遍历完左边，从左边回的时候打印
- [[中序.excalidraw]]
```java
public static void inOrder(TreeNode head){  
    if(head == null){  
        return;  
    }  
    inOrder(head.left);  
    System.out.println(head.val + " ");  
    inOrder(head.right);  
}
```

### 后序
- 遍历完左边，从右边的null回的时候打印，遍历右边，从右边的null回的时候再打印
- [[后序.excalidraw]]
```java
//后序打印  
public static void posOrder(TreeNode head){  
    if(head == null){  
        return;  
    }  
    posOrder(head.left);  
    posOrder(head.right);  
    System.out.println(head.val + " ");  
}
```

## 非递归实现三种序
### 先序
- 用栈实现，LIFO，所以先把右节点放进栈里
- root在最开始的时候push，进入循环后先把上一次的先pop，第一次就pop root
[[先序非递归.excalidraw]]

```java
public static void preOrder(TreeNode head){  
     if(head != null){  
         Stack<TreeNode> stack = new Stack<>();  
         stack.push(head);  
         while (!stack.isEmpty()){  
             head = stack.pop(); //栈里放的是树的节点，这里表示树的中节点  
             System.out.println(head.val + " ");  
             if(head.right != null){  
                 stack.push(head.right);  
             }  
             if(head.left != null){  
                 stack.push(head.left);  
             }  
         }  
         System.out.println();  
     }  
}
```

### 中序
- 和先序不同，通过栈是否空来判定是否继续循环
- 先将左边的全部push进栈
- 如果左边没了，头为空，弹栈顶，切栈顶的右节点重复上面的操作
- 栈空结束循环
```java
public static void inOrder(TreeNode head){  
     if(head != null){  
         Stack<TreeNode> stack = new Stack<>();  
         while(!stack.isEmpty() || head != null){//head不为空让root进  
             if(head != null){  
                 stack.push(head);  
                 head = head.left;  
             }else{  
                 head = stack.pop();  
                 System.out.println(head.val + " ");  
                 head = head.right;  
             }  
             System.out.println(head.val + " ");  
         }  
     }  
}
```

### 后序
- 先序：中左右，但是我们可以稍微修改一下使用中右左，刚好是后序倒过来

#### 用两个栈来实现
- 也就是先序弹出时不打印，用另一个栈收集，收集完后全部弹出就是后序
- 这种方式不省空间
```java
public static void posOrder(TreeNode head){  
    if(head != null){  
        Stack<TreeNode> stack = new Stack<>();  
        Stack<TreeNode> collect = new Stack<>();  
        stack.push(head);  
        while (!stack.isEmpty()){  
            head = stack.pop(); //栈里放的是树的节点，这里表示树的中节点  
            collect.push(head);  
            System.out.println(head.val + " ");  
            if(head.right != null){  
                stack.push(head.right);  
            }  
            if(head.left != null){  
                stack.push(head.left);  
            }  
        }  
        while (!collect.isEmpty()){  
            System.out.println(collect.pop() + " ");  
        }  
        System.out.println();  
    }  
}
```

#### 用一个栈
- 设定一个类似哨兵结点的结点h，用来表示上次打印的结点
- 假如左边不为空，h不等于左边（表示左边没有处理），h不等于右边（表示右边没有处理），就把左边的push
- 或者左边处理完了，判断右边，右边不为空，h不等于右边（右边没处理）
- 左边的右边都处理完了就打印，再弹出，用h记录这次的的弹出
- 栈空结束
```java
public static void posOrder(TreeNode head){  
    if (head != null){  
        Stack<TreeNode> stack = new Stack<>();  
        TreeNode cur = head;  
        stack.push(head);  
        while (!stack.isEmpty()){  
            cur = stack.peek();  
            if(cur.left != null && head != cur.left && head != cur.right){  
                cur = cur.left;  
                stack.push(cur);  
            }else if(cur.right != null && head != cur.right){  
                cur = cur.right;  
                stack.push(cur);  
            }else {  
                System.out.println(cur.val + " ");  
                head = stack.pop();  
            }  
        }  
    }  
}
```

### 时间复杂度分析
- 递归
	- 如果不为空，每个结点要去三次，假如有n个结点，那时间复杂度就是$O(n)$
	- 空间复杂度：树的高度$O(h)$，每一层的空间可以复用，也就是一层给一个空间，
- 非递归
	- 每个结点进栈一次，出栈一次，时间复杂度也是$O(n)$
	- 空间复杂度也是$O(h)$
- 用两个栈实现后序：不推荐，要收集所有结点，最后逆序弹出，额外空间复杂度为$O(n)$

## 二叉树高频题（不含树型dp）
### 二叉树的层序遍历
- 按层得到二叉树的元素
- 


### 二叉树的锯齿形层序遍历





### 二叉树的最大深度、最小深度


###  二叉树先序序列化和反序列化
- 中序遍历无法完成二叉树的序列化和反序列化

### 二叉树按层序列化和反序列化

### 利用先序与中序遍历构造二叉树

### 验证完全二叉树

### 求完全二叉树的节点个数
- 要求时间复杂度低于O(n)

### 普通二叉树上寻找两个节点的最近公共祖先
- 也叫lca问题
- Tarjan算法解决lca的批量查询、树链部分算法解决lca的在线查询



### 搜索二叉树上寻找两个节点的最近公共祖先


### 收集累加和等于aim的所有路径（递归恢复现场）

### 验证平衡二叉树（树型dp沾边）

### 验证搜索二叉树（树型dp沾边）


### 修剪搜索二叉树

### 二叉树打家截舍问题（树型dp沾边）


## 前缀树





### 构建前缀信息技巧


### 一维差分等差数列差分


### 二维前缀、二维差分、离散化技巧

## 最小生成树


## bfs及其扩展

- bfs求深度
```java
public int maxDepth(TreeNode root) {  
    int count = 0;  
    if(root == null) return count;  
  
    Queue<TreeNode> queue = new LinkedList<>();  
    queue.add(root);  
    while (!queue.isEmpty()){  
        int levelSize = queue.size();  
        for (int i = 0; i < levelSize; i++) {  
            TreeNode node = queue.poll();  
  
            if(node.left != null) queue.offer(node.left);  
            if (node.right != null) queue.offer(node.right);  
        }  
        count++;  
    }  
    return count;  
}
```



## 双向广搜

## dijkstra算法、分层图最短路

## A星、Floyd Bellman-Ford、SPFA


