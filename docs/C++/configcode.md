## 读取物品列表配置
execle添加一列

| cs,itemlist |
| -: |
| 字段名称 |
| item_id:num:is_bind,item_id:num:is_bind |

读itemlist接口
```c++
inline bool ReadItemListConfig(TiXmlElement *data_element, const char *item_str, std::vector<ItemConfigData> &item_list)
```

## 读取基础属性配置
AttributesConfig
```c++
// 读取配置属性
bool ReadConfig(TiXmlElement * data_element)
bool ReadConfig(rapidxml::xml_node<> * data_element)

// 将配置属性加到人物基础属性
void AddAttrs(CharIntAttrs &attrs, double factor = 1.0) const;
// 将配置属性加到人物战斗属性
void AddFightAttrs(CharIntAttrs &attrs, double factor = 1.0) const;
```

## 读取坐标列表配置
PointListConfig
格式：50,50|50,65
```c++
// 读取坐标
bool ReadConfig(TiXmlElement * data_element, const char *node)
// 返回坐标数量
int Count()
```

## 随机项目配置

| seq | weight |
|  | -: |
| 索引 | 权重 |
| 1 | 2222 |

RandItemConfig
```c++
// 读取权重列表，函数内部会读取seq
bool ReadConfig(TiXmlElement *data_element, const char *weight_str)
bool ReadConfig(RapidXmlNode *data_element, const char *weight_str)

// 随机一个项目，RandItem中的seq就是随机到的索引
const RandItem * Rand() const;
```

## 其他读取函数
```c++
// 读MonsterID
extern bool ReadMonsterID(TiXmlElement *data_element, const char *name, UInt16 &monster_id);
extern bool ReadMonsterID(rapidxml::xml_node<> *data_element, const char *name, UInt16 &monster_id);

// 读TaskID
extern bool ReadTaskID(TiXmlElement *data_element, const char *name, TaskID &task_id);
extern bool ReadTaskID(RapidXmlNode *data_element, const char *name, TaskID &task_id);

// 读正整数
inline bool ReadPositiveInt(TiXmlElement *data_element, const char *name, int &value)
inline bool ReadPositiveInt(rapidxml::xml_node<> *data_element, const char *name, int &value)

// 读非负浮点数
inline bool ReadNonNegativeDouble(TiXmlElement *data_element, const char *name, double &value)
inline bool ReadNonNegativeDouble(RapidXmlNode *data_element, const char *name, double &value)

// 读正浮点数
inline bool ReadPositiveDouble(TiXmlElement *data_element, const char *name, double &value)

// 读非负整数
inline bool ReadNonNegativeInt(TiXmlElement *data_element, const char *name, int &value)

// 读非负整数
inline bool ReadNonNegativeInt(rapidxml::xml_node<> *data_element, const char *name, int &value)

// 读HHMM
inline bool ReadHHMM(TiXmlElement *data_element, const char *name, short &hhmm)
inline bool ReadHHMM(rapidxml::xml_node<> *data_element, const char *name, short &hhmm)

```