import gc

from django.shortcuts import render
from django.http import HttpResponse
from tools.searchNews import GetNews
import json
# Create your views here.

g = GetNews()


def content(request):
    # print(request.GET['content'])
    url = request.GET['content']
    # print(url)
    try:
        news_content = g.get_page_content(url)

        return HttpResponse(json.dumps({
            'news_content': news_content
        }))
    except Exception as e:
        print(e)
        return HttpResponse(status=500)
    finally:
        gc.collect()


def news_list(request):
    page_num = request.GET['page_num']
    page_type = request.GET['type']
    print(page_num)
    try:
        html = g.change_page(page_num, page_type)
        result_list = g.get_page_url(html)
        # print(result_list)
        return HttpResponse(json.dumps({
            'news_list': result_list
        }))
    except AttributeError:
        return HttpResponse(
            json.dumps({
            'page_num': int(page_num),
        }))
    except ValueError:
        return HttpResponse(
            json.dumps({
                'page_num': int(page_num),
            }))
    except BaseException as e:
        print(e)
        return HttpResponse(
            json.dumps({
                'page_num': int(page_num),
            }))
    finally:
        gc.collect()



