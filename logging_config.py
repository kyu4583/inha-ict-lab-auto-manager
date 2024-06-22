# logging_config.py
import logging


class SocketIOHandler(logging.Handler):
    def __init__(self, socketio):
        super().__init__()
        self.socketio = socketio

    def emit(self, record):
        log_entry = self.format(record)
        self.socketio.emit('log_message', {'message': log_entry})


def setup_logging():
    # 포매터 설정
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # 콘솔 핸들러 설정
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # 파일 핸들러 설정
    file_handler = logging.FileHandler('app.log')
    file_handler.setFormatter(formatter)

    # 콘솔 출력 로거
    console_logger = logging.getLogger('console_logger')
    console_logger.setLevel(logging.DEBUG)
    console_logger.addHandler(console_handler)
    console_logger.addHandler(file_handler)
    console_logger.propagate = False  # 부모 로거로 전파하지 않음

    # 기본 로거
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.WARNING)
    # 기존 핸들러 제거
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)


def setup_socket_logging(socketio):
    # 포매터 설정
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # 웹소켓 핸들러 설정
    socketio_handler = SocketIOHandler(socketio)
    socketio_handler.setFormatter(formatter)

    # 사용자 피드백 로거 (웹소켓용)
    feedback_logger = logging.getLogger('feedback_logger')
    feedback_logger.setLevel(logging.INFO)
    feedback_logger.addHandler(socketio_handler)
    feedback_logger.propagate = False  # 부모 로거로 전파하지 않음


setup_logging()