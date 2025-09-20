from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.api import AstrBotConfig
from zai import ZhipuAiClient

@register("bmtxt2img", "CoooooNG", "智谱文生图插件", "1.0.0")
class MyPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config=config

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""
    
    # 注册指令的装饰器。指令名为 helloworld。注册成功后，发送 `/helloworld` 就会触发这个指令，并回复 `你好, {user_name}!`
    @filter.command("bmimg")
    async def helloworld(self, event: AstrMessageEvent):

        #"""这是一个 hello world 指令""" # 这是 handler 的描述，将会被解析方便用户了解插件内容。建议填写。

        user_name = event.get_sender_name()
        message_str = event.message_str # 用户发的纯文本消息字符串
        message_chain = event.get_messages() # 用户所发的消息的消息链 # from astrbot.api.message_components import *

        # Initialize client
        client = ZhipuAiClient(api_key=self.config.token)

        # 图像生成
        response = client.images.generations(
            model=self.config.model,
            prompt=message_str,
            size="1024x1024",
            quality="standard",
        )

        image_url = response.data[0].url

        logger.info(message_chain)
        yield event.image_result({image_url})

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
