from django.core.paginator import Paginator

host = ''


class PaginatorDefault:
    def __init__(self, data, request, name=''):
        limit = int(request.GET.get('limit'))
        page = int(request.GET.get('page'))
        p = Paginator(data, per_page=limit)
        self.count = p.count
        self.p = p.get_page(page)
        self.host = host + name

    def str(self):
        previous = self.p.previous_page_number() if self.p.has_previous() else None
        has_next = self.p.next_page_number() if self.p.has_next() else None
        return {
            'count': self.count,
            'next': has_next,
            'previous': previous,
            'results': self.p.object_list,
        }
