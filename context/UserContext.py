from context.MongoPosts import UserPost


class UserContext:

    def __init__(self, user_id, guild_id):
        self.guild_id = guild_id
        self.user_id = user_id
        self.user_name = None
        self.user_money = None
        self.user_games_won = None
        self.user_doc = self.get_doc()

    def get_doc(self):
        try:
            user_doc = UserPost.objects(user_name=self.user_id, guild_id=self.guild_id).first()

            if user_doc is not None:
                self.user_name = user_doc.user_name
                self.user_money = user_doc.user_money
                self.user_games_won = user_doc.user_games_won
                return user_doc
            else:
                return None

        except ConnectionError as err:
            print(f'Error at connecting to database: {err}')
        except Exception as e:
            print(f'Unexpected error: {e}')
            raise

    def retrieve_money(self, value):
        if value <= 0:
            return
        else:
            return self.user_doc.modify(dec__user_money=value)

    def receive_money(self, value):
        if value <= 0:
            return
        else:
            return self.user_doc.modify(inc__user_money=value)

    def set_games_won(self, value):
        if value <= 0:
            return
        else:
            return self.user_doc.modify(inc__user_games_won=value)

    def delete(self):
        try:
            self.user_doc.delete()

        except ConnectionError as err:
            print(f'Error at connecting to database: {err}')

        except Exception as e:
            print(f'Unexpected error: {e}')
            raise
