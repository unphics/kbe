# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
from ROLE_DATA import TRoleData
from ROLE_INFO import TRoleInfo, TRoleList

class ExAccount(KBEngine.Proxy):
	def __init__(self):
		KBEngine.Proxy.__init__(self)

	def ReqRoleList(self):
		"""
		客户端请求角色列表
		"""
		DEBUG_MSG("ExAccount[%i].ReqRoleList: Size = %i, Data = %s", % (self.id), len(self.RoleList), self.RoleList)
		# 直接发送角色列表给客户端
		self.client.OnReqRoleList(self.RoleList)

	def ReqCreateRole(self, RoleType, Name):
		"""
		客户端请求创建角色
		:param RoleType: 角色类型
		:param Name: 角色名字
		"""
		# 创建空的RoleInfo角色信息类, 用来给创建角色失败时 作为创建角色回调函数的参数
		RoleInfo = TRoleInfo()
		RoleInfo.extend([0, Name, RoleType, TRoleData().createFromDict({"DataType": 0, "DataValue": b''})])
		# 判断是否能创建角色, 是否有同名或者同类型的角色
		for key, info in self.RoleList.items():
			if info[1] == Name:
				self.client.OnCreateRole(1, RoleInfo)
				return
			if info[2] == RoleType:
				self.client.OnCreateRole(2, RoleInfo)
		# 创建ExRole


	def ReqRemoveRole(self, Name):
		"""
		客户端请求删除角色
		:param Name: 角色名字
		"""

	def onTimer(self, id, userArg):
		"""
		KBEngine method.
		使用addTimer后， 当时间到达则该接口被调用
		@param id		: addTimer 的返回值ID
		@param userArg	: addTimer 最后一个参数所给入的数据
		"""
		DEBUG_MSG(id, userArg)
		
	def onClientEnabled(self):
		"""
		KBEngine method.
		该entity被正式激活为可使用， 此时entity已经建立了client对应实体， 可以在此创建它的
		cell部分。
		"""
		INFO_MSG("account[%i] entities enable. entityCall:%s" % (self.id, self.client))
			
	def onLogOnAttempt(self, ip, port, password):
		"""
		KBEngine method.
		客户端登陆失败时会回调到这里
		"""
		INFO_MSG(ip, port, password)
		return KBEngine.LOG_ON_ACCEPT
		
	def onClientDeath(self):
		"""
		KBEngine method.
		客户端对应实体已经销毁
		"""
		DEBUG_MSG("Account[%i].onClientDeath:" % self.id)
		self.destroy()
