from django.http import HttpResponse
from tools.searchNews import GetNews
from tools.news import get_url_from_index_page, get_total_content
import json
# Create your views here.

g = GetNews()


def content(request):
    # print(request.GET['content'])
    url = request.GET['content']
    print(url)
    # try:
    # news_content = g.get_page_content(url)

    news_content, pic_list = get_total_content(url)
    return HttpResponse(json.dumps({
        'news_content': news_content,
        'pic_list': pic_list
    }))
    # except Exception as e:
    # print(e)
    # return HttpResponse(status=404)
    # finally:
    # print('完成')
        # gc.collect()


def news_list(request):
    page_num = request.GET['page_num']
    page_type = request.GET['type']
    print(page_type)
    print(page_num)
    if page_num == '0':
        page = page_type
    # try:
    else:
        page = '{}/{}'.format(page_type, page_num)
    data = get_url_from_index_page(page)
    return HttpResponse(json.dumps({
        'news_list': data
    }))
    # except AttributeError:
    #     print('AttributeError')
    #     return HttpResponse(
    #         json.dumps({
    #         'page_num': page_num,
    #     }))
    # except ValueError:
    #     print('ValueError')
    #     return HttpResponse(
    #         json.dumps({
    #         'page_num': page_num,
    #         }))
    # except BaseException as e:
    #     print(e)
    #     return HttpResponse(
    #         json.dumps({
    #             'page_num': page_num,
    #         }))
    # finally:
    #     print('完成')
        # gc.collect()



