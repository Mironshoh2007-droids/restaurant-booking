class AuthManager:
    def __init__(self):
        self.users = {}
    
    def register(self, username, password):
        if username in self.users:
            return False, "Пользователь уже существует"
        self.users[username] = password
        return True, "Регистрация успешна"
    
    def login(self, username, password):
        if username in self.users and self.users[username] == password:
            return True, "Вход выполнен"
        return False, "Неверный логин или пароль"
