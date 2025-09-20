from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.api import AstrBotConfig
from zai import ZhipuAiClient

@register("bmtxt2img", "CoooooNG", "智谱文生图插件", "1.0.0", "https://github.com/CoooooNG/astrbot_plugin_bmtxt2img")
class MyPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config=config

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""
    
    @filter.command("bmimg")
    async def bmtxt2img(self, event: AstrMessageEvent):
        '''这是一个文生图指令'''
        user_name = event.get_sender_name()
        message_str = event.message_str # 用户发的纯文本消息字符串

        logger.info("调用智谱文生图api")

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
        yield event.image_result(image_url)

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
