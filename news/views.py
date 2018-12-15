import gc

from django.shortcuts import render
from django.http import HttpResponse
from tools.searchNews import GetNews
from tools.news import get_url_from_index_page
import json
# Create your views here.

g = GetNews()


def content(request):
    # print(request.GET['content'])
    url = request.GET['content']
    # print(url)
    # try:
    news_content = g.get_page_content(url)
    return HttpResponse(json.dumps({
        'news_content': news_content
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
    if page_num != '1':
        page_type = page_num
    try:
        data = get_url_from_index_page(page_type)
        # print(result_list)
        return HttpResponse(json.dumps({
            'news_list': data
        }))
    except AttributeError:
        return HttpResponse(
            json.dumps({
            'page_num': page_num,
        }))
    except ValueError:
        return HttpResponse(
            json.dumps({
            'page_num': page_num,
            }))
    except BaseException as e:
        print(e)
        return HttpResponse(
            json.dumps({
                'page_num': page_num,
            }))
    finally:
        print('完成')
        # gc.collect()



