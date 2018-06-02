## 系统代码
XxXdef.hpp
```c++
#ifndef __XxX_DEF_HPP__
#define __XxX_DEF_HPP__

#pragma pack(push, 4)

#include "servercommon/servercommon.h"

struct XxXParam
{
	XxXParam() { this->Reset(); }

	void Reset()
	{
		
	}
};

using XxXParamHex = char[sizeof(XxXParam) * 2 + 1];
static_assert(sizeof(XxXParamHex) < 4096, "Incorrect size");

#pragma pack(pop)

#endif  // __XxX_DEF_HPP__
```

XxX.h
```c++
#ifndef __XxX_H__
#define __XxX_H__

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

#endif // __XxX_H__
```

XxX.cpp
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