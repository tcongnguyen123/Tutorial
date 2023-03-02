from rest_framework import pagination
from rest_framework.response import Response
from collections import OrderedDict
import math


class StandardPagination(pagination.PageNumberPagination):
    page_size = 4
    page_size_query_param = 'page_size'
    max_page_size = 10
    # Nếu page_size là 2 và max_page_size là 10, khi người dùng yêu cầu xem trang thứ 15, chúng ta sẽ trả về 10 sản phẩm trên trang đó (vì page_size là 10). 
    # Tuy nhiên, nếu người dùng yêu cầu xem trang thứ 15, chúng ta sẽ trả về trang cuối cùng (vì max_page_size là 10) chứ không phải trang trống hoặc báo lỗi.
    page_size_query_param_max = 'max_page_size'
