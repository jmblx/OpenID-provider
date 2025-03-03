from application.common.id_provider import IdentityProvider


class IdentifyByCookiesQueryHandler:
    def __init__(self, idp: IdentityProvider):
        self.idp = idp

    async def handle(self):
        user = await self.idp.get_current_user()

        return {
            "email": user.email.value,
            "id": user.id.value,
            "avatar_path": user.avatar_path,
        }
