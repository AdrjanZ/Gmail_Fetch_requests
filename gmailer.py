import requests
import threading
import ast
import sqlite3

class EmailManager:
    def __init__(self, database_name):
        self.conn = sqlite3.connect(database_name)
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS emails (title TEXT, email TEXT)''')

    def gmail_load(self, cookies, headers):
        params = {
            'hl': 'en',
            'c': '0',
            'rt': 'r',
            'pt': 'ji',
        }
        json_data = [
            [1, None, None, 0, ],
            None,
            [1, None, None, None, [None, 25, ], None, 1, ],
            [None, 0, None, 0, ],
            1,
        ]
        response = requests.post('https://mail.google.com/sync/u/0/i/s', params=params, cookies=cookies, headers=headers, json=json_data)
        glowna = response.json()
        return glowna

    def send_telegram_message(self, message):
        requests.post(
            'https://api.telegram.org/BOTID/sendMessage',
            data={
                'chat_id': 'chatid',
                'text': message,
                'parse_mode': 'Markdown'
            }
        )

    def catch_emails(self, email_name, glowna):
        emails = {}
        for i in range(len(glowna[1][5])):
            email = (glowna[1][5][i][0][2][6][0][0])
            sender = (glowna[1][5][i][0][2][6][0][4][0][1][1])
            content = (glowna[1][5][i][0][2][6][0][4][0][9])
            emails[i] = [sender, content, email_name]

        for email in emails.values():
            sender, content, email_name = email
            self.c.execute("SELECT * FROM emails WHERE title=? AND email=?", (content, email_name))
            if self.c.fetchone() is None:
                self.c.execute("INSERT INTO emails VALUES (?,?)", (content, email_name))
                self.conn.commit()
                self.send_telegram_message(
                    f"*Nowa wiadomość e-mail!*\n\n"
                    f"*Od:* {sender}\n"
                    f"*Do:* {email_name}\n"
                    f"*Treść:* {content}"
                )

    def process_account(self, email_name, account_file):
        with open(account_file, 'r') as file:
            account_data = ast.literal_eval(file.read())
            cookies = account_data['cookies']
            headers = account_data['headers']
            glowna = self.gmail_load(cookies, headers)
            self.catch_emails(email_name, glowna)

    def run(self, accounts):
        threads = []
        for email_name, account_file in accounts.items():
            thread = threading.Thread(target=self.process_account, args=(email_name, account_file,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        self.conn.close()

if __name__ == '__main__':
    email_manager = EmailManager('emails.db')
    accounts = {
        "accname1": "Konta/account1.txt",
        "accname2": "Konta/account2.txt",
    }
    email_manager.run(accounts)