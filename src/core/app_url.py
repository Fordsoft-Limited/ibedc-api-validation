from enum import Enum

class AppUri(Enum):
    LOGIN = ('login', 'login')
    LOGOUT = ('logout', 'logout')
    CREATE_USER = ('create', 'create_user')
    LIST_USER = ('list', 'list_user')
    APPROVE_OR_REJECT_CUSTOMER = ('vet/approve-or-reject', 'approve_or_reject_customer')
    REFRESH_TOKEN = ('token/refresh', 'refresh_token')
    CUSTOMER_SINGE_VALIDATE = ('validate', 'validate_single_customer')
    CUSTOMER_BULK_VALIDATE = ('validate/bulk', 'validate_bulk_customer')
    CUSTOMER_BULK_VALIDATE_BATCH_DETAIL = ('validate/batches/<str:uid>', 'retrieve_batche_details')
    CUSTOMER_BULK_VALIDATE_BATCHES = ('validate/batches', 'list_batches')
    CUSTOMER_BULK_VALIDATE_BATCHES_PAGES = ('validate/batches-pages', 'list_batches_pagination')
    CUSTOMER_RETRIEVE = ('<str:customer_no>', 'RETRIEVE')
    CUSTOMER_LIST = ('list', 'list_customer')
    CUSTOMER_DETAIL = ('<str:uid>', 'customer_detail')
    CUSTOMER_LIST_BY_FEEDER_OR_BU = ('list/<str:filter_type>/<str:feeder>', 'list_customer_by_feeder_or_bu')
    CUSTOMER_REVIEW = ('review/<str:review_type>/<str:review_value>', 'list_customer') # review_type(FEEDER, BU, BATCH_CODE), review_value(feedername, or bu_name, or batch_code_value)


    CHANGE_PASSWORD = ('change/password', 'change_password')

    def __init__(self, uri, uri_name):
        self.uri = uri
        self.uri_name = uri_name  # Using 'uri_name' for consistency with 'uri'

    @classmethod
    def get_uri(cls, uri_name):
        """Returns the URI path based on the uri_name."""
        for item in cls:
            if item.uri_name == uri_name:
                return item.uri

    @classmethod
    def get_uri_name(cls, uri):
        """Returns the URI name based on the URI path."""
        for item in cls:
            if item.uri == uri:
                return item.uri_name