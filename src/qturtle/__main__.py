from transpyler import get_transpyler


def start_application():
    transpyler = get_transpyler()
    transpyler.start_qturtle()


if __name__ == '__main__':
    start_application()
