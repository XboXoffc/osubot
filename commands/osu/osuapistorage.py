from commands.osu import osuapi
import config

OSU_ID = config.OSU_CLIENT_ID
OSU_SECRET = config.OSU_CLIENT_SECRET
X_API_VERSION = config.X_API_VERSION

osu_api = osuapi.Osu(OSU_ID, OSU_SECRET, X_API_VERSION)