import requests

class Osu:
    def __init__(self, client_id, client_secret, x_api_version):
        self.osuweb_base = 'https://osu.ppy.sh'
        self.base_url = f'{self.osuweb_base}/api/v2'
        self.x_api_version = x_api_version

        self.__client_id = client_id
        self.__client_secret = client_secret

        self.__login()

    def __login(self):
        url_token = f'{self.osuweb_base}/oauth/token'
        data = {
            'client_id': self.__client_id,
            'client_secret': self.__client_secret,
            'grant_type': 'client_credentials',
            'scope': 'public'
        }
        response = requests.post(url_token, data)
        if response.status_code != 200:
            return
        
        data = response.json()
        if 'access_token' not in data:
            return
        self.__token = data['access_token']

    def __get(self, path: str, params = None):
        res = requests.get(f'{self.base_url}/{path}', params, headers={
            "Authorization": f'Bearer {self.__token}',
            "x-api-version": self.x_api_version,
        })
        
        if res.status_code == 401: # unathorized
            self.__login()
            return self.__get(path, params)

        return res

    def profile(self, user, mode='',use_id=False, params=None):
        if not use_id:
            user = f'@{user}'
        return self.__get(f'users/{user}/{mode}', params)
    def user_scores(self, user_id, types, legacy_only='0', include_fails='0', mode=None, limit='1', offset='0'):
        params = {
            "legacy_only": legacy_only,
            "include_fails": include_fails,
            "mode": mode,
            "limit": limit,
            "offset": offset,
        }
        return self.__get(f'users/{user_id}/scores/{types}', params)
    def beatmap(self, beatmap_id):
        return self.__get(f'beatmaps/{beatmap_id}')