# -*- coding: UTF-8 -*-


def replace_key_if_exists(input_dict, old_key, new_key):
    if old_key not in input_dict:
        return

    input_dict[new_key] = input_dict[old_key]
    del input_dict[old_key]


# 根据一个 request 获取用户的 bk_uid
def get_bkuid_from_request(request):
    http_cookie = str(request.META['HTTP_COOKIE'])
    bk_uid = ''

    # httpCookie 的形式为 '.......bk_uid=XXXX;....'，故 bk_uid 的第一个字母的位置为 httpCookie.index('bk_uid') + 7
    index_bk_uid = http_cookie.index('bk_uid') + 7
    while http_cookie[index_bk_uid] != ';':
        bk_uid += http_cookie[index_bk_uid]
        index_bk_uid += 1
    return bk_uid
