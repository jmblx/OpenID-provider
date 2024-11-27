from dishka import Provider, Scope, provide

from application.usecases.auth.change_pwd import RequestChangePasswordUseCase
from application.usecases.auth.cred_auth import AuthenticateUserUseCase
from application.usecases.auth.refresh_access_token import (
    RefreshAccessTokenUseCase,
)
from application.usecases.group.create import CreateGroupAndReadUseCase
from application.usecases.group.delete import (
    DeleteAndReadGroupUseCase,
    DeleteGroupUseCase,
)
from application.usecases.group.read import ReadGroupUseCase
from application.usecases.group.update import (
    UpdateAndReadGroupUseCase,
    UpdateGroupUseCase,
)
from application.usecases.user.delete import (
    DeleteAndReadUserUseCase,
    DeleteUserUseCase,
)
from application.usecases.user.read import ReadUserUseCase
from application.usecases.user.register import CreateUserAndReadUseCase
from application.usecases.user.set_image import SetAvatarUseCase
from application.usecases.user.update import (
    UpdateAndReadUserUseCase,
    UpdateUserUseCase,
)


class UseCaseProvider(Provider):
    create_user_and_read_use_case = provide(
        CreateUserAndReadUseCase,
        scope=Scope.REQUEST,
        provides=CreateUserAndReadUseCase,
    )

    read_user_usecase = provide(
        ReadUserUseCase, scope=Scope.REQUEST, provides=ReadUserUseCase
    )

    authenticate_user_use_case = provide(
        AuthenticateUserUseCase,
        scope=Scope.REQUEST,
        provides=AuthenticateUserUseCase,
    )

    refresh_access_token_use_case = provide(
        RefreshAccessTokenUseCase,
        scope=Scope.REQUEST,
        provides=RefreshAccessTokenUseCase,
    )

    request_change_password_use_case = provide(
        RequestChangePasswordUseCase,
        scope=Scope.REQUEST,
        provides=RequestChangePasswordUseCase,
    )
    upd_user_uc = provide(
        UpdateUserUseCase,
        scope=Scope.REQUEST,
        provides=UpdateUserUseCase,
    )
    upd_and_read_user_uc = provide(
        UpdateAndReadUserUseCase,
        scope=Scope.REQUEST,
        provides=UpdateAndReadUserUseCase,
    )
    set_user_av_uc = provide(
        SetAvatarUseCase,
        scope=Scope.REQUEST,
        provides=SetAvatarUseCase,
    )
    del_user_uc = provide(
        DeleteUserUseCase, scope=Scope.REQUEST, provides=DeleteUserUseCase
    )
    del_and_read_user_uc = provide(
        DeleteAndReadUserUseCase,
        scope=Scope.REQUEST,
        provides=DeleteAndReadUserUseCase,
    )
    create_group_and_read_uc = provide(
        CreateGroupAndReadUseCase,
        scope=Scope.REQUEST,
        provides=CreateGroupAndReadUseCase,
    )
    read_group_uc = provide(
        ReadGroupUseCase, scope=Scope.REQUEST, provides=ReadGroupUseCase
    )
    upd_group_uc = provide(
        UpdateGroupUseCase,
        scope=Scope.REQUEST,
        provides=UpdateGroupUseCase,
    )
    upd_and_read_group_uc = provide(
        UpdateAndReadGroupUseCase,
        scope=Scope.REQUEST,
        provides=UpdateAndReadGroupUseCase,
    )
    del_group_uc = provide(
        DeleteGroupUseCase, scope=Scope.REQUEST, provides=DeleteGroupUseCase
    )
    del_and_read_group_uc = provide(
        DeleteAndReadGroupUseCase,
        scope=Scope.REQUEST,
        provides=DeleteAndReadGroupUseCase,
    )
