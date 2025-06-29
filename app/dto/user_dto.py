class userDTO:
    def __init__(self, email: str, password:str):
        self.password = password
        self.email = email


    @staticmethod
    def from_dict(data: dict):
        return userDTO(
            email=data.get('email'),
            password=data.get('password')
        )