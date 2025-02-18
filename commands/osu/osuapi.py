import requests

class Osu:
    def __init__(self, client_id, client_secret, x_api_version):
        url_token = 'https://osu.ppy.sh/oauth/token'
        data = {
            'client_id': client_id,
            'client_secret': client_secret,
            'grant_type': 'client_credentials',
            'scope': 'public'
        }
        response = requests.post(url_token, data)
        self.__token = f"Bearer {response.json().get('access_token')}"
        self.base_url = 'https://osu.ppy.sh/api/v2'
        self.x_api_version = x_api_version
    def profile(self, user, mode='',use_id=False, params=None):
        if not use_id:
            user = f'@{user}'
        full_url = f'{self.base_url}/users/{user}/{mode}'
        __headers = {
            "Authorization": self.__token,
            "x-api-version": self.x_api_version,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        return requests.get(full_url, params, headers=__headers)
    def user_scores(self, user_id, types, legacy_only='0', include_fails='0', mode=None, limit='1', offset='0'):
        full_url = f'{self.base_url}/users/{user_id}/scores/{types}'
        params = {
        "legacy_only": legacy_only,
        "include_fails": include_fails,
        "mode": mode,
        "limit": limit,
        "offset": offset,
        }
        __headers = {
            "Authorization": self.__token,
            "x-api-version": self.x_api_version,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        return requests.get(full_url, params, headers=__headers)
    def beatmap(self, beatmap_id):
        full_url = f'{self.base_url}/beatmaps/{beatmap_id}'
        __headers = {
            "Authorization": self.__token,
            "x-api-version": self.x_api_version,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        return requests.get(full_url, headers=__headers)