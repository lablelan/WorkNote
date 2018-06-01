
## XxXdef.hpp
```c++
#ifndef __XXX_DEF_HPP__
#define __XXX_DEF_HPP__

#pragma pack(push, 4)

#include "servercommon/servercommon.h"

const int INT_ARRAY_MAX = 10;

struct XxXParam
{
	XxXParam() { this->Reset(); }

	void Reset()
	{
		memset(int_array, 0, sizeof(int_array));
	}

	// 四字节对齐
	int int_array[INT_ARRAY_MAX];
};

using XxXParamHex = char[sizeof(XxXParam) * 2 + 1];
static_assert(sizeof(XxXParamHex) < 4096, "Incorrect size");

#pragma pack(pop)

#endif  // __XXX_DEF_HPP__
```

## XxX.h
```c++
#ifndef __XXX_H__
#define __XXX_H__

#include "servercommon/xxxdef.hpp"
#include "obj/character/attribute.hpp"

class Role;

class XxX
{
public:
	void SetRole(Role *role) { m_role = role; }
	void InitParam(const XxXParam &param);
	void GetInitParam(XxXParam *param) { *param = m_param; }
	void ReCalcAttr(CharIntAttrs &base_add, bool is_recalc);

private:
	Role *m_role = nullptr;

	CharIntAttrs m_attrs_add;

	XxXParam m_param;
};

#endif // __XXX_H__
```

## XxX.cpp
```c++
#include "stdafx.h"

#include "gamecommon.h"
#include "xxx.h"
#include "protocal/msgxxx.h"
#include "xxxconfig.hpp"

void XxX::InitParam(const XxXParam &param)
{
	m_param = param;

	m_module.Init(m_role, this);
}

void XxX::ReCalcAttr(CharIntAttrs &base_add, bool is_recalc)
{
	if (!is_recalc)
	{
		base_add.Add(m_attrs_add.m_attrs);

		m_role->GetCapability()->AddCap(CAPABILITY_TYPE_XXX, m_other_capability);

		return;
	}

	m_attrs_add.Reset();
	m_other_capability = 0;

	// m_attrs_add加属性
	auto module_cfg = LOGIC_CONFIG->GetXxXCfg().GetModuleCfg();
	module_cfg.AddAttrs(m_attrs_add);

	base_add.Add(m_attrs_add.m_attrs);

	m_role->GetCapability()->AddCap(CAPABILITY_TYPE_XXX, m_other_capability);
}
```

## XxXcofig.hpp
```c++
// 系统配置
#ifndef __XXX_CONFIG_HPP__
#define __XXX_CONFIG_HPP__

#include "config/gameconfigcommon/gameconfigcommon.h"
#include "servercommon/xxxdef.hpp"

// 其它
struct XxXOtherConfig
{
	int times_cfg = 0;
};

// 模块配置
struct ModuleConfig
{
	struct CfgItem
	{
		int seq = 0;						// 索引
		ItemID item_id = 0;					// 激活道具

		AttributesConfig attrs_cfg;			// 属性加成
	};

	int cfg_item_count = 0;
	CfgItem cfg_item_list[XXX_ITEM_MAX_COUNT];
};

class XxXConfig
{
public:
	XxXConfig();

	bool Init(const std::string &configname, std::string *err);			// Called by LogicConfigManager::Init

	const XxXOtherConfig & GetOtherCfg() { return m_other_cfg; }
	const XxXModuleConfig::CfgItem * GetModuleCfg(int seq);
protected:
	int InitOtherCfg(RapidXmlNode *root_element);
	int InitModuleCfg(RapidXmlNode *root_element);

private:
	XxXOtherConfig m_other_cfg;
	XxXModuleConfig m_module_cfg;
};

#endif
```

## XxXconfig.cpp
```c++
#include "stdafx.h"

#include "xxxconfig.hpp"

bool XxXConfig::Init(const std::string &configname, std::string *err)
{
	PRE_LOAD_CONFIG2;

	LOAD_CONFIG2("other", InitOtherCfg);
	LOAD_CONFIG2("module", InitModuleCfg);

	return true;
}

bool XxXConfig::IsValidModuleSeq(int seq) const
{
	return seq >= 0 && seq < m_active_cfg.cfg_item_count && seq < MODULE_ITEM_MAX_COUNT;
}

const XxXModuleConfig::CfgItem * XxXConfig::GetActiveCfg(int seq)
{
	if (!this->IsValidModuleSeq(seq))
	{
		return nullptr;
	}

	return &m_module_cfg.cfg_item_list[seq];
}


int XxXConfig::InitOtherCfg(RapidXmlNode *root_element)
{
	RapidXmlNode *data_element = root_element->first_node("data");
	if (!data_element)
	{
		return -10000;
	}

	if (!ReadPositiveInt(data_element, "times_cfg", m_other_cfg.times_cfg))
	{
		return -1;
	}

	return 0;
}

int XxXConfig::InitActiveCfg(RapidXmlNode *root_element)
{
	RapidXmlNode *data_element = root_element->first_node("data");
	if (!data_element)
	{
		return -10000;
	}

	m_active_cfg.cfg_item_count = 0;

	while (data_element)
	{
		if (m_active_cfg.cfg_item_count >= MODULE_ITEM_MAX_COUNT)
		{
			return -1000;
		}
		int seq = 0;
		if (!GetSubNodeValue(data_element, "seq", seq) || seq != m_active_cfg.cfg_item_count)
		{
			return -1;
		}

		BeautyActiveConfig::CfgItem &cfg_item = m_active_cfg.cfg_item_list[m_active_cfg.cfg_item_count];
		cfg_item.seq = seq;
		if (!GetSubNodeValue(data_element, "active_item_id", cfg_item.active_item_id) || NULL == ITEMPOOL->GetItem(cfg_item.active_item_id))
		{
			return -2;
		}
		if (!cfg_item.attrs_cfg.ReadConfig(data_element))
		{
			return -100;
		}

		++m_active_cfg.cfg_item_count;
		data_element = data_element->next_sibling();
	}

	return 0;
}
```

## msgxxx.h
```c++
// XX协议
#ifndef __MSG_XXX_H__
#define __MSG_XXX_H__

#include "servercommon/userprotocal/msgheader.h"
#include "config/gameconfigcommon/gameconfigcommon.h"
#include "servercommon/xxxdef.hpp"
#include "msgrole.h"

#pragma pack(push) 
#pragma pack(4)

namespace Protocol
{
	//-------------------------------------------------------------------------------------------
	// CS Protocols

	// 通用请求类型
	enum XXX_COMMON_REQ_TYPE
	{
		XXX_COMMON_REQ_TYPE_BASE_INFO = 0,					// 基础信息请求
	};

	// 通用请求 协议号
	class CSXxXCommonReq
	{
	public:
		CSXxXCommonReq();
		MessageHeader header;

		unsigned short req_type;
		unsigned short param_1;
		unsigned short param_2;
		unsigned short param_3;
	};

	//-------------------------------------------------------------------------------------------

	// SC Protocols
	// 基础信息 协议号
	class SCXxXBaseInfo
	{
	public:
		SCXxXBaseInfo();
		MessageHeader header;

		char reserve_ch1;					
		char reserve_ch2;					
		char reserve_ch3;					
		char reserve_ch4;
	};


	//-------------------------------------------------------------------------------------------
}

#pragma pack(pop)

#endif
```