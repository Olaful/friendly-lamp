from scrapy.contracts import Contract
from scrapy.exceptions import ContractFail

class HeaderCheck(Contract):
    """ Demo contract which checks the presence of a custom header
        @has_header X-CustomHeader
    """

    name = 'has_header'

    #该函数在sample request接收到response后，传送给回调函数前被调用，运行测试
    def pre_process(self, response):
        # args即传给request的参数
        for header in self.args:
            if header not in response.headers:
                raise ContractFail('X-CustomHeader not present')