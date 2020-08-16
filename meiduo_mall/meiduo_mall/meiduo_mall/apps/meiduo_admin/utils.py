from rest_framework.pagination import PageNumberPagination
# 重写JWT返回结果方法
from rest_framework.response import Response
# 重写JWT返回结果方法
def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'username':user.username,
        'id':user.id
    }
# 自定义分页器
class PageNum(PageNumberPagination):

    page_size_query_param = 'pagesize'
    max_page_size = 10
    # 指定分页返回结果的方法
    def get_paginated_response(self, data):
        # return Response(OrderedDict([
        #     ('count', self.page.paginator.count),
        #     ('next', self.get_next_link()),
        #     ('previous', self.get_previous_link()),
        #     ('results', data)
        # ]))
        return Response(
            {
                'count':self.page.paginator.count,
                'lists':data,
                'page':self.page.number,
                'pages':self.page.paginator.num_pages,
                'pagesize':self.max_page_size
            }
        )
