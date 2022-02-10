from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def paginate_queryset(request, queryset, count):
    """Pageオブジェクトを返す。

    ページングしたい場合に利用してください。

    countは、1ページに表示する件数です。
    返却するPgaeオブジェクトは、以下のような感じで使えます。::

        {% if page_obj.has_previous %}
          <a href="?page={{ page_obj.previous_page_number }}">Prev</a>
        {% endif %}

    また、page_obj.object_list で、count件数分の絞り込まれたquerysetが取得できます。

    """
    paginator = Paginator(queryset, count)
    # print(paginator.count)　querysetの数
    # print(paginator.num_pages) 全ページ数
    # print(paginator.page_range) # range(1, 8)のようにページ範囲を返す、1から始まる、全7ページの場合は第2引数は8
    # for i in paginator.page_range:
    #     print(i) とすると 1, 2, 3, 4, 5, 6, 7
    # print(paginator)
    page = request.GET.get('page')
    # print(page) リクエストから送られて来たpageのkeyに対応するvalue、リクエストしたページ番号
    # print(paginator.get_page(page)) # 引数で与えられたページ数のPageオブジェクトを返す、エラーハンドリングあり　例<Page 3 of 5>
    try:
        page_obj = paginator.page(page) # get_pageとほぼ同じ、ただし、エラーハンドリングはしない　<Page 3 of 5>
        # print(page_obj)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return page_obj

