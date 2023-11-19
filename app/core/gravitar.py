from urllib import parse

from pydantic import EmailStr, HttpUrl

GRAVITAR__design = "retro"
GRAVITAR__size = 200
GRAVITAR__url = "https://gravatar.com/avatar/"


def generate(email_address: EmailStr) -> HttpUrl:
    email_address_encoded = parse.quote(email_address)
    return HttpUrl(f"{GRAVITAR__url}{email_address_encoded}?s={GRAVITAR__size}&d={GRAVITAR__design}")
