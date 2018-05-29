## 静态断言
利用负数组下标做静态断言
```c++
#define UNSTD_STATIC_CHECK(Expr)                     UNSTD_STATIC_CHECK1(Expr, __LINE__)
#define UNSTD_STATIC_CHECK1(Expr, Line)              UNSTD_STATIC_CHECK2(Expr, Line)
#define UNSTD_STATIC_CHECK2(Expr, Line)              typedef char UnName##Line[(Expr) ? 1 : -1];
```

## rand最大值
```c++
int RandomNum(int min_num, int max_num)
{
	if (min_num > max_num)
	{
		int tmp_num = min_num;
		min_num = max_num;
		max_num = tmp_num;
	}

	int interval_num = max_num - min_num;
	if (interval_num <= 0)
	{
		return 0;
	}

	if (interval_num < RAND_MAX)
	{
		return min_num + (rand() % interval_num);
	}
	else
	{
		int rand_num = (rand() << 16) + rand(); // 两次随机数补成一个int（主要解决windows下rand最大值只有2^15的问题）
		if (rand_num < 0)
		{
			rand_num *= -1;
		}
		return min_num + int(rand_num % interval_num);
	}
}
```