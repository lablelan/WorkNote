## 发送邮件
```c++
static MailContentParam contentparam; contentparam.Reset();

// 奖励物品
for (int i = 0; i < MAX_ATTACHMENT_ITEM_NUM; i++)
{
	if (0 != cfg->reward_item_list[i].item_id && 0 != cfg->reward_item_list[i].num)
	{
		contentparam.item_list[i].item_id = cfg->reward_item_list[i].item_id;
		contentparam.item_list[i].num = cfg->reward_item_list[i].num;
		contentparam.item_list[i].is_bind = cfg->reward_item_list[i].is_bind;
	}
}
int length = SNPRINTF(contentparam.contenttxt, sizeof(contentparam.contenttxt), gamestring::g_xxx_reward_content);
if (length > 0)
{
	MailRoute::MailToUser(m_role->GetUserId(), SYSTEM_MAIL_REASON_INVALID, contentparam);
}
```