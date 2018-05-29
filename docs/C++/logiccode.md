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

## 激活一个形象
使用位运算激活一个形象
```
#include <iostream>

int main()
{
    unsigned int special_image = 0;     // 最大保存32个形象

    int active_image_id = 10;           // 想要激活的形象id

	// 模拟激活两次同一形象
    for(int i = 0; i < 2; i++)
    {
        if (1)
        {
            // 如果已经激活
            if (special_image & (1 << active_image_id))
            {
                // 提示已激活，返回
                std::cout << "You had actived the image" << std::endl;
                break;
            }
            else
            {
                special_image |= (1 << active_image_id);
            }
            std::cout << special_image << std::endl;
        }

    }

    return 0;
}
```

## 获取最小等级
用set获取套装中的最小等级
```c++
#include <iostream>
#include <set>

int main()
{
    std::set<int> get_min_level_set;
    int a[10] = { 5, 2, 55, 6, 1, 555, 14, 88, 99, 100 };
    for (int i = 0; i < 10; i++)
    {
        get_min_level_set.insert(a[i]);
    }
    if (get_min_level_set.size() > 0)
    {
        int min_level = *(get_min_level_set.begin());
        std::cout << "min_level: " << min_level << std::endl;
    }


    return 0;
}
~ 
```