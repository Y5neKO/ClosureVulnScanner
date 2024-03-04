from mitmproxy import http, ctx
from mitmproxy import socks


class ProxyAddon:
    def __init__(self):
        self.config = ctx.options

    def request(self, flow: http.HTTPFlow):
        ctx.log.info(f"接收到请求: {flow.request.url}")
        # 在这里可以对请求进行修改和处理
        # 例如，打印请求信息、修改请求头等

    def response(self, flow: http.HTTPFlow):
        ctx.log.info(f"接收到响应: {flow.request.url}")
        # 在这里可以对响应进行修改和处理
        # 例如，打印响应信息、修改响应内容等

    def socks_setup(self, flow: socks.Socks5ProtocolHandler):
        # 在这里设置自定义的 SSL 证书
        flow.add_cert_file(self.config.ssl_certfile)


addons = [
    ProxyAddon()
]


def start():
    from mitmproxy.tools.main import mitmdump
    mitmdump(["-s", __file__, "-p", "8889"])


if __name__ == "__main__":
    # 设置自定义的 SSL 证书文件路径
    ctx.options.ssl_certfile = "test.cer"
    start()
