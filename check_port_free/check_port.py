"""
Copied from https://github.com/google/python_portpicker.
Uses for my current project to check if a specify port is available.
"""
import socket

_PROTOS = [(socket.SOCK_STREAM, socket.IPPROTO_TCP),
           (socket.SOCK_DGRAM, socket.IPPROTO_UDP)]

def bind(port, socket_type, socket_proto):
    """Try to bind to a socket of the specified type, protocol, and port.
    This is primarily a helper function for PickUnusedPort, used to see
    if a particular port number is available.
    For the port to be considered available, the kernel must support at least
    one of (IPv6, IPv4), and the port must be available on each supported
    family.
    Args:
      port: The port number to bind to, or 0 to have the OS pick a free port.
      socket_type: The type of the socket (ex: socket.SOCK_STREAM).
      socket_proto: The protocol of the socket (ex: socket.IPPROTO_TCP).
    Returns:
      The port number on success or None on failure.
    """
    got_socket = False
    for family in (socket.AF_INET6, socket.AF_INET):
        try:
            sock = socket.socket(family, socket_type, socket_proto)
            got_socket = True
        except socket.error:
            continue
        try:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(('', port))
            if socket_type == socket.SOCK_STREAM:
                sock.listen(1)
            port = sock.getsockname()[1]
        except socket.error:
            return None
        finally:
            sock.close()
    return port if got_socket else None

def is_port_free(port):
    """Check if specified port is free.
    Args:
      port: integer, port to check
    Returns:
      boolean, whether it is free to use for both TCP and UDP
    """
    return bind(port, *_PROTOS[0]) and bind(port, *_PROTOS[1])