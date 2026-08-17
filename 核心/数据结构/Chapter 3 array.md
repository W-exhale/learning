线性表（linear list）：当提到线性表时，主要是在说下面两个东西。
1. array
2. linked list


## array的实现（连续，back to back）

比如说：查arr[0]，先找到arr[0]的地址，（比如说起点在2）
查arr[1]，直接在arr[0]的地址加4个字节，（即2+4）
如果是N，则是2+4N。
只需要知道初始地址，在加上字节（add+sizeof[N])


## Static Array的复杂度计算
如何计算时间，空间复杂度(arr[N])
1. 按照index查询，时间复杂度为O(1)T，定义数组（初始化)时空间复杂度为O(N)S
2. 修改一个值，（先找到，再把值也覆盖掉）所以时间复杂度也是O(1)T
3. [1, 2, 3, 4],将一个值插入(不能直接插，不然违反了back to back），在另一个数组开内存，copy一份O(N+1)TS，放进去，(当N够大，1可以忽略不记)，空间复杂度一般不算，因为空间复杂度一般不可测，总是改变，空间复杂度很多情况下都是变的。（（（（N+1，欠债，忽略不计？！！））））
4. 删除一个元素：
- 从末尾删：O(1)T，删除元素时要确保连续，
- 删开头（不用转移）：O(N)T，前面的删掉了，后面的要跟进，（于是后面的每一个都要往前缩进），要动N次（首地址上必须要有东西）
- 删除中间的：O(N)，用copy...
如果每次从前面删，删几次就几次O(N)（即几个O（N）相加），
“标记清除思想”，[1, 2, 3, 4]假如说我需要删除前三个数，那么就把前三个数都标记上，最后一次性都删掉，再把4以及4后面的往前推，只需要一个O(N)否则如果要删N个，就得O(N$^2$)次。



Java=>JVM，（Java的垃圾回收机制）
mark and sweep(标记，清除)

## Dynamic Array的复杂度计算（动态数组）
一般扩容概率小，数组越大，扩容的可能性越小，（越来越大，后来就不用扩了）
[1, 2, 3]如果要加，就得扩容，扩容一般是扩一倍，
  [1,       2,       3,        4,        5,       6]后面是扩容一倍扩出来的，
O(1)，O(1)，O(1)，O(3)，O(1)，O(1)
4对应O(N),也就是说在扩容的一瞬间，才有O(N)
随着数组越来越大，越往后扩容，当扩到N时， 

级数收敛：N + $\frac{N}{2}$+$\frac{N}{4}$+....
级数收敛 $\approx$ 2N

扩N+1次，

平摊分析：在计算机科学中，用于算法分析中的方法，常用于（动态数据结构），在使用平摊分析前须知各种操作所可能发生的时间，并计算出最坏情况下的操作情况并加以平均，得到操作的平均耗费时间。平摊分析只能确保最坏情况性能的每次操作耗费的平均时间，并不能确定平均情况性能。（即上述扩容的方式）

每次扩容是O(N)，不扩容就是O(1).扩容完平摊就是O(1).


扩容完之后，再删除，缩回去，扩容和缩容要满足的条件不同，扩容是每次扩一倍，缩容不是。

复杂度震荡，扩容和缩容时用的同样的原理。

## 常规数组实现

```C
#include <stdio.h>
#include <stdlib.h>

//Define a dynamic array structure that stores an array and its size
typedef struct {
	int* array;
	size_t size;
}Dynamic_array;

//Function to create a new dynamic array
Dynamic_array* create_array(size_t size) {
	Dynamic_array* arr = malloc(sizeof(Dynamic_array));
	if (arr != NULL) {
		arr->array = malloc(size * sizeof(int));
		arr->size = size;
	}
	return arr;
}

//Function to read an element from a dynamic array
int read_array(Dynamic_array* arr, size_t index) {
	if (index < arr->size) {
		return arr->array[index];
	}
	else
	{
		printf("Error:index out of bounds:%zd\n", index);
		return EXIT_FAILURE;
	}
}

//Function to update an element from a dynamic array
void update_array(Dynamic_array* arr, size_t index, int value) {
	if (index < arr->size) {
		arr->array[index] = value;
	}
	else {
		printf("Error:index out of bounds:%zd\n", index);
		return EXIT_FAILURE;
	}
}

//Function to delete a dynamic array
void delete_array(Dynamic_array* arr) {
	free(arr->array);
	free(arr);
}

int main()
{
	Dynamic_array* arr = create_array(10);

	update_array(arr, 5, 33333);

	int value = read_array(arr, 5);

	printf("The value is: %d\n", value);

	delete_array(arr);
	return EXIT_SUCCESS;
}
```


 