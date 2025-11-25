from django.core.cache import cache

from apps.authentication.models.perms import CustomPermission


class PermissionLists:
    """
    Permissions Lists for Each APIS
    eg : Products AIO Create needs create permissions for Product,ProductCategory and Other related fields
    """

    HTTP_GET_METHOD = "GET"
    HTTP_POST_METHOD = "POST"
    HTTP_PATCH_METHOD = "PATCH"
    # HTTP_PUT_METHOD = "PUT"
    # HTTP_DELETE_METHOD = "DELETE"

    # --------------------SUPPORT ROLE NAME ------------------
    SUPPORT_ROLE_NAME = "SUPPORT"

    # ------------- Authentication APP --------------------

    CUSTOM_USER = "custom_user"
    USER_PROFILE = "user_profile"
    CUSTOM_PERMISSION = "custom_permission"
    PERMISSION_CATEGORY = "permission_category"
    ROLES = "roles"
    ROLE_NAME = "SUPPORT"
    USER_PERMISSION_CACHE_KEY = "user_permissions_cache"

    # --------------------Content APP ----------------------

    CONTENT = "content"
    CONTENT_CATEGORY = "content_category"
    CONTENT_ROUND = "content_round"
    USER_CONTENT_REPORT = "user_content_report"
    DEMO_CONTENT = "demo_content"

    # -------------------------ADS APP-------------------------
    ADVERTISEMENT = "advertisement"

    # ------------- Location APP ------------------------------

    # COUNTRY = "country"
    # PROVINCE = "province"
    # DISTRICT = "district"
    # LOCATION = "location"
    # WARD = "ward"

    # ------------------------------APP SETTINGS--------------------------
    APP_SETTINGS = "app_settings"

    # --------------------------------------------------------API LOGS--------------------------
    API_LOGS = "api_logs"

    # ---------------------------All Model List ------------------
    ALL_MODELS_LIST = {
        "CUSTOM_USER": CUSTOM_USER,
        "USER_PROFILE": USER_PROFILE,
        "CUSTOM_PERMISSION": CUSTOM_PERMISSION,
        "PERMISSION_CATEGORY": PERMISSION_CATEGORY,
        "ROLES": ROLES,
        "CONTENT": CONTENT,
        "CONTENT_CATEGORY": CONTENT_CATEGORY,
        "CONTENT_ROUND": CONTENT_ROUND,
        "USER_CONTENT_REPORT": USER_CONTENT_REPORT,
        "DEMO_CONTENT": DEMO_CONTENT,
        "ADVERTISEMENT": ADVERTISEMENT,
        # "COUNTRY": COUNTRY,
        # "PROVINCE": PROVINCE,
        # "DISTRICT": DISTRICT,
        # "LOCATION": LOCATION,
        # "WARD": WARD,
        "API_LOGS": API_LOGS,
        "APP_SETTINGS": APP_SETTINGS,
    }


class HttpBasedPermissionActionMaps:
    CAN_CREATE = "can_create"
    CAN_VIEW = "can_view"
    CAN_UPDATE = "can_update"
    CAN_DELETE = "can_delete"


def cache_user_permissions_queryset(key, queryset: list, ttl=86400):
    """
    Using LIST Queryset because : the queryset parameter is union of two .values() querysets

    IMP : If the Redis Value(Queryset) Datastrucutre is changed here , we also have to update it in Permissions
    """
    # time to live in seconds (86400 means 24hours -- 24hours * 60min * 60sec )
    # key = f"{PermissionLists.NON_BRANCH_USER_PERMISSION_CACHE_KEY}:{user_id}"
    cache.set(key, queryset, ttl)


def get_user_permissions_util(user_obj):
    """
    This functoin is used in Permision class and User Permissions Update API for retreieving the users NON-BRANCH permissions
    """
    key = f"{PermissionLists.USER_PERMISSION_CACHE_KEY}:{user_obj.id}"
    perms = cache.get(key)
    if perms:
        return perms
    perms = user_obj.permissions.values_list("code_name", flat=True)
    roles = (
        CustomPermission.objects.filter(roles__in=user_obj.roles.all())
        .distinct()
        .values_list("code_name", flat=True)
    )
    user_permissions = perms.union(roles)
    perms = list(user_permissions)
    cache_user_permissions_queryset(key=key, queryset=list(user_permissions))
    return perms


def refresh_user_permissions_cache_queryset(user_obj):
    key = f"{PermissionLists.USER_PERMISSION_CACHE_KEY}:{user_obj.id}"
    if cache.get(key):
        cache.delete(key)
    return get_user_permissions_util(user_obj)


def refresh_permissions_cache(user_obj):
    user_permissions = refresh_user_permissions_cache_queryset(user_obj)
    return user_permissions
