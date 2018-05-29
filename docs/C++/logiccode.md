## 抽奖大致流程
```c++
#include <iostream>
#include <vector>
#include <ctime>

struct DrawReward
{
    int item_id = 0;    // 奖励物品id
    int weight = 0;     // 奖励权重
};

int main()
{
    int total_weight = 0;               // 总权重
    std::vector<DrawReward> cfg_vec;    // 奖励配置
    
    // 设置权重
    for (int i = 0; i < 10; i++)
    {
        DrawReward dr;
        dr.item_id = 1000 + i;
        dr.weight = 10 + i * 10;
        cfg_vec.push_back(dr);
        total_weight += dr.weight;
    }

    srand(time(NULL));                  // 改变种子(程序开始初始化一次就足够)
    int rand_weight = rand() % total_weight;
    for (auto iter = cfg_vec.begin(); iter != cfg_vec.end(); ++iter)
    {
        if (rand_weight > iter->weight)
        {
            rand_weight -= iter->weight;// 权重不在该段,减去该段权重
        }
        else
        {
            std::cout << iter->item_id << std::endl;
            break;
        }
    }


    return 0;
}
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

## 静态断言
利用负数组下标做静态断言
```c++
#define UNSTD_STATIC_CHECK(Expr)                     UNSTD_STATIC_CHECK1(Expr, __LINE__)
#define UNSTD_STATIC_CHECK1(Expr, Line)              UNSTD_STATIC_CHECK2(Expr, Line)
#define UNSTD_STATIC_CHECK2(Expr, Line)              typedef char UnName##Line[(Expr) ? 1 : -1];
```
