from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
from .models import Group, Chat
import json
import asyncio
from channels.db import database_sync_to_async

class MySyncConsumer(SyncConsumer):
	def websocket_connect(self, event):
		print('Websocket Connected...', event)
		print('Channels Layer..', self.channel_layer)
		self.send({
			'type':'websocket.accept'
		})
		print(self.channel_name)
		self.group_name=self.scope['url_route']['kwargs']['group_name']
		async_to_sync(self.channel_layer.group_add)(self.group_name,self.channel_name)
		
	def websocket_receive(self, event):
		print('Messaged Received...', event)
		print('Messaged is ', event['text'])
		data = json.loads(event['text'])
		group = Group.objects.get(name=self.group_name)
		chat = Chat.objects.create(content = data.get('msg'), group = group)
		async_to_sync(self.channel_layer.group_send)(self.group_name,{
			'type':'chat.message',
			'message':event['text']
		})
	
	def chat_message(self,event):
		print(event)
		self.send({
			'type':'websocket.send',
			'text': event['message']
		})

	def websocket_disconnect(self, event):
		print('Websocket Disconnected...', event)
		print(self.channel_name)
		async_to_sync(self.channel_layer.group_discard)('programmers',self.channel_name)
		raise StopConsumer()


class MyAsyncConsumer(AsyncConsumer):
	async def websocket_connect(self, event):
		await self.send({
			'type':'websocket.accept'
		})
		self.group_name=self.scope['url_route']['kwargs']['group_name']
		await self.channel_layer.group_add(self.group_name,self.channel_name)
		
	async def websocket_receive(self, event):
		data = json.loads(event['text'])
		group = await database_sync_to_async(Group.objects.get)(name=self.group_name)
		chat = await database_sync_to_async(Chat.objects.create)(content = data.get('msg'), group = group)
		await self.channel_layer.group_send(self.group_name,{
			'type':'chat.message',
			'message':event['text']
		})

	async def chat_message(self,event):
		await self.send({
			'type':'websocket.send',
			'text': event['message']
		})

	async def websocket_disconnect(self, event):
		await self.channel_layer.group_discard(self.group_name,self.channel_name)
		raise StopConsumer()