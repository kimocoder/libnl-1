"""Netlink Types (netlink-private/types.h).
https://github.com/thom311/libnl/blob/libnl3_2_25/include/netlink-private/types.h

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation version 2.1
of the License.
"""

import ctypes

from libnl.linux_private.netlink import sockaddr_nl, nlmsghdr
from libnl.misc import ucred
from libnl.netlink_private.object_api import NLHDR_COMMON

NL_SOCK_BUFSIZE_SET = 1 << 0
NL_SOCK_PASSCRED = 1 << 1
NL_OWN_PORT = 1 << 2
NL_MSG_PEEK = 1 << 3
NL_NO_AUTO_ACK = 1 << 4
NL_MSG_CRED_PRESENT = 1


class nl_cb(object):  # TODO https://github.com/Robpol86/libnl/issues/4
    """Netlink callback class (C struct equivalent).
    https://github.com/thom311/libnl/blob/libnl3_2_25/include/netlink-private/types.h#L40

    Instance variables:
    cb_set -- dictionary of callback functions (values), indexed by callback type (keys).
    cb_args -- dictionary of arguments to be passed to callback functions (values), indexed by callback type (keys).
    cb_err -- error callback function.
    cb_err_arg -- argument to be passed to error callback function.
    cb_recvmsgs_ow -- TODO https://github.com/Robpol86/libnl/issues/4
    cb_recv_ow -- TODO https://github.com/Robpol86/libnl/issues/4
    cb_send_ow -- call this function instead of nl_send_iovec() in nl_send(). Args are (sk, msg).
    cb_active -- current callback type (e.g. NL_CB_MSG_OUT). Modified before every callback function call.
    """

    def __init__(self):
        self.cb_set = dict()
        self.cb_args = dict()
        self.cb_err = None
        self.cb_err_arg = None
        self.cb_recvmsgs_ow = None
        self.cb_recv_ow = None
        self.cb_send_ow = None
        self.cb_active = None


class nl_sock(object):
    """Netlink socket class (C struct equivalent).
    https://github.com/thom311/libnl/blob/libnl3_2_25/include/netlink-private/types.h#L69

    Instance variables:
    s_local -- struct sockaddr_nl.
    s_peer -- struct sockaddr_nl.
    s_fd -- returns -1 if the socket has not been opened, or the socket's file descriptor integer.
    s_proto -- int.
    s_seq_next -- unsigned int.
    s_seq_expect -- unsigned int.
    s_flags -- int.
    s_cb -- struct nl_cb.
    s_bufsize -- size_t.
    socket_instance -- the actual socket.socket() instance.
    """

    def __init__(self):
        self.s_local = sockaddr_nl()
        self.s_peer = sockaddr_nl()
        self.s_proto = 0
        self.s_seq_next = 0
        self.s_seq_expect = 0
        self.s_flags = 0
        self.s_cb = None
        self.s_bufsize = None
        self.socket_instance = None

    def __repr__(self):
        answer_base = ("<{0}.{1} s_local='{2}' s_peer='{3}' s_fd={4} s_proto={5} s_seq_next={6} s_seq_expect={7} "
                       "s_flags={8} s_cb='{9}' s_bufsize={10}>")
        answer = answer_base.format(
            self.__class__.__module__,
            self.__class__.__name__,
            self.s_local, self.s_peer, self.s_fd, self.s_proto, self.s_seq_next, self.s_seq_expect, self.s_flags,
            self.s_cb, self.s_bufsize,
        )
        return answer

    @property
    def s_fd(self):
        return -1 if self.socket_instance is None else self.socket_instance.fileno()


class nl_msg(object):
    """https://github.com/thom311/libnl/blob/libnl3_2_25/include/netlink-private/types.h#L133

    Client-side only. Never transmitted to the kernel.

    Instance variables:
    nm_protocol -- integer.
    nm_flags -- integer.
    nm_src -- sockaddr_nl class instance.
    nm_dst -- sockaddr_nl class instance.
    nm_creds -- ucred class instance.
    nm_nlh -- nlmsghdr class instance.
    nm_size -- integer.
    nm_refcnt -- integer.
    """

    def __init__(self):
        self.nm_protocol = 0
        self.nm_flags = 0
        self.nm_src = sockaddr_nl()
        self.nm_dst = sockaddr_nl()
        self.nm_creds = None
        self.nm_nlh = None
        self.nm_size = 0
        self.nm_refcnt = 1

    def __repr__(self):
        answer_base = ("<{0}.{1} nm_protocol={2} nm_flags={3} nm_src='{4}' nm_dst='{5}' nm_creds='{6}' nm_nlh='{7}' "
                       "nm_size='{8}'>")
        answer = answer_base.format(
            self.__class__.__module__,
            self.__class__.__name__,
            self.nm_protocol, self.nm_flags, self.nm_src, self.nm_dst, self.nm_creds, self.nm_nlh, self.nm_size,
        )
        return answer


class genl_family_grp(object):
    """https://github.com/thom311/libnl/blob/libnl3_2_25/include/netlink-private/types.h#L761"""

    def __init__(self, family=None, name='', id_=0):
        self.family = family
        self.name = name
        self.id_ = id_


class genl_family(NLHDR_COMMON):
    """https://github.com/thom311/libnl/blob/libnl3_2_25/include/netlink-private/types.h#L768"""
    SIZEOF = NLHDR_COMMON.SIZEOF + 48

    def __init__(self):
        super().__init__()
        self.gf_id = 0
        self.gf_name = None
        self.gf_version = 0
        self.gf_hdrsize = 0
        self.gf_maxattr = 0
        self.gf_ops = None
        self.gf_mc_grps = None
