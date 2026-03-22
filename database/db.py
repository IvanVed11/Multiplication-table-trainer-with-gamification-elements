import aiosqlite

from mul_table_and_titles import titles

class DatabaseBot:
    def __init__(self):
        self.db = None


    async def connect_with_database(self):
        if self.db is None:
            self.db = await aiosqlite.connect("database.db")
            await self.db.execute('''CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            amount_correctly_solved_examples INTEGER NOT NULL,
            amount_solved_examples INTEGER NOT NULL,
            current_title TEXT NOT NULL)
            ''')
            await self.db.commit()


    async def add_user(self, user_id, username, first_name):
        await self.db.execute('''INSERT OR IGNORE INTO Users
            (id, username, first_name, amount_correctly_solved_examples, amount_solved_examples, current_title)
            VALUES (?, ?, ?, 0, 0, ?)''',
            (user_id, username, first_name, titles[0]))
        await self.db.commit()


    async def check_is_user_in_db(self, user_id):
        cursor = await self.db.execute("SELECT 1 FROM Users WHERE id = ?", (user_id,))
        result = await cursor.fetchone()
        return result is not None


    async def update_stats(self, user_id, is_correct_ans):
        if is_correct_ans:
            await self.db.execute('''UPDATE Users SET amount_correctly_solved_examples = amount_correctly_solved_examples + 1 
                                  WHERE id = ?''', (user_id,))
        await self.db.execute("UPDATE Users SET amount_solved_examples = amount_solved_examples + 1 WHERE id = ?", (user_id,))
        await self.db.commit()


    async def update_title(self, user_id, new_title):
        sql_update_query = "UPDATE Users SET current_title = ? WHERE id = ?"
        data = (new_title, user_id)
        await self.db.execute(sql_update_query, data)
        await self.db.commit()


    async def get_user_stats(self):
        cursor = await self.db.execute('''SELECT first_name, amount_correctly_solved_examples
                        FROM Users 
                        ORDER BY amount_correctly_solved_examples DESC
                        LIMIT 5
                        ''')
        rows = await cursor.fetchall()
        return rows
    

    async def get_profile_statistics(self, user_id):
        cursor = await self.db.execute('''SELECT amount_solved_examples,
                            amount_correctly_solved_examples, first_name,
                            current_title 
                            FROM Users WHERE id = ?''', (user_id,))
        rows = await cursor.fetchall()
        return rows


    async def get_statistics_of_all_users(self):
        cursor = await self.db.execute('''SELECT id, 
                                    first_name, amount_correctly_solved_examples 
                                    FROM Users
                                    ORDER BY amount_correctly_solved_examples DESC''')
        return await cursor.fetchall()
        

    async def check_position_of_leaderboard(self, user_id):
        rows = await self.get_statistics_of_all_users()
        user_statistics = [[place, row[1], row[2]] for place, row in enumerate(rows, start=1) if row[0] == user_id]
        place, correctly_solved_examples = user_statistics[0][0], user_statistics[0][2]
        return place, correctly_solved_examples
    

    async def close_connection(self):
        if self.db:
            await self.db.close()