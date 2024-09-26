import cfbd
from config import API_KEY

def setup_api():
    configuration = cfbd.Configuration()
    configuration.api_key['Authorization'] = API_KEY
    configuration.api_key_prefix['Authorization'] = 'Bearer'
    client = cfbd.ApiClient(configuration)
    return {
        'games': cfbd.GamesApi(client),
        'betting': cfbd.BettingApi(client)
    }
