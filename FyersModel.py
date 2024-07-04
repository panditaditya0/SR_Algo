from fyers_apiv3 import fyersModel
import Auth
class FyersModelClass:
    def __init__(self):
        self.fyers = fyersModel.FyersModel(client_id=Auth.client_id, is_async=False, token=Auth.get_cached_access_token(),
                                           log_path="")
    def get_fyers(self):
        return self.fyers