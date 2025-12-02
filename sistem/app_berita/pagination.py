from rest_framework.pagination import PageNumberPagination


class PaginationHandler(PageNumberPagination):
    page_size = 10  # Jumlah item per halaman
    page_size_query_param = 'page_size'  # Parameter untuk mengatur ukuran halaman secara dinamis
    max_page_size = 500 # Batas maksimum ukuran halaman