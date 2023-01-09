from django.core.paginator import Paginator


class PaginatorDefault:
    def __init__(self, data, request):
        self.path = (
                f'{str(request.scheme)}://'
                + str(request.META["HTTP_HOST"])
                + str(request.path)
                + '?page='
        )
        limit = int(request.GET.get('limit', 10))
        page = int(request.GET.get('page', 1))
        p = Paginator(data, limit)
        self.count = p.count
        self.p = p.get_page(page)

    def str(self):
        previous = self.path + str(self.p.previous_page_number()) if self.p.has_previous() else None
        has_next = self.path + str(self.p.next_page_number()) if self.p.has_next() else None
        return {
            'count': self.count,
            'next': has_next,
            'previous': previous,
            'results': self.p.object_list,
        }
