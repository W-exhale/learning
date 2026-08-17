## 两数之和
- 题目描述
![[Pasted image 20240513181906.png]]

```C
#include <stdio.h>
#include <stdlib.h>
#include "uthash.h"

typedef struct {
    int key;
    int val;
    UT_hash_handle hh;//表示这个结构体是一个哈希表类型，不需要为其赋值，但是一定要定义
}HashTable;

//定义一个hash结构的空指针指向hash表，必须初始化为空，uthash会根据其是否为空进行不用的操作
HashTable* hashtable = NULL;

HashTable* find(int ikey) {
    HashTable* tmp;
    HASH_FIND_INT(hashtable, &ikey, tmp);
    //参数1：空白指针，参数2：要查找的key(指针类型)，如果找到就给tmp赋值，没找到就不赋值
    return tmp;
}

void insert(int ikey, int ival) {
    //插入需要在哈希表中找到一个位置
    HashTable* it = find(ikey);
    if (it == NULL) {
        HashTable* tmp = malloc(sizeof(HashTable));
        tmp->key = ikey, tmp->val = ival;
        HASH_ADD_INT(hashtable, key, tmp);
        //参数2：对应的成员名称，参数3：要插入的数据
    }
    else {
        it->val = ival;
    }
}

int* twoSum(int* nums, int numsSize, int target, int* returnSize) {
    for (int i = 0; i < numsSize; ++i) {
        HashTable* it = find(target - nums[i]);
        //key是数组中的值，value是下标
        if (it != NULL) {//就说明重复了，值已经找到了
            int* ret = malloc(sizeof(int) * 2);
            ret[0] = it->val, ret[1] = i;
            *returnSize = 2;
            return ret;
        }
        insert(nums[i],i);
    }
    *returnSize = 0;
    return NULL;

//测试
    int main() {
    int nums[] = { 2, 7, 11, 15 };
    int numsSize = sizeof(nums) / sizeof(nums[0]);
    int target = 9;
    int returnSize;

    int* result = twoSum(nums, numsSize, target, &returnSize);

    if (returnSize == 2) {
        printf("Indices of the two numbers that add up to the target are: %d and %d\n", result[0], result[1]);
        free(result); // 不要忘记释放动态分配的内存
    }
    else {
        printf("No solution found.\n");
    }

    return EXIT_SUCCESS;
}

```

