from rest_framework.throttling import SimpleRateThrottle


class SaleOrderRateThrottle(SimpleRateThrottle):
    scope = 'sale_order'

    def get_cache_key(self, request, view):
        return self.get_ident(request)