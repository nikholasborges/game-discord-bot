from context.MongoPosts import UserPost


class UserContext:

    def __init__(self, user_id):
        self.user_id = user_id
        self.user_obj = self.retrieve_obj()

    def retrieve_obj(self):
        try:
            user_obj = None

            for user in UserPost.objects():
                if user.user_name == self.user_id:
                    user_obj = user

            return user_obj

        except ConnectionError as err:
            print(f'Error at connecting to database: {err}')
        except Exception as e:
            print(f'Unexpected error: {e}')
            raise

    def retrieve_money(self, value):
        if value <= 0:
            return
        else:
            return self.user_obj.modify(dec__user_money=value)

    def receive_money(self, value):
        if value <= 0:
            return
        else:
            return self.user_obj.modify(inc__user_money=value)

    def set_games_won(self, value):
        if value <= 0:
            return
        else:
            return self.user_obj.modify(inc__user_games_won=value)
