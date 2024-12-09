def render_auth_code_url(redirect_url: str, auth_code: str) -> str:
    if "{auth_code}" in redirect_url:
        return redirect_url.replace("{auth_code}", auth_code)
    return redirect_url + f"?auth_code={auth_code}"
