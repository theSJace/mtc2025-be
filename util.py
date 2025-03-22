from main import UserDTO, JournalDTO
from datetime import datetime
import string, random

def getCurrentDt():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def getRefCode():
    allowed_characters = string.ascii_letters + string.digits
    confusing_chars = "IlO0o"
    allowed_characters = ''.join(c for c in allowed_characters if c not in confusing_chars)
    random_string = ''.join(random.choice(allowed_characters) for _ in range(length))
    return random_string

def checkUserImpl(telegram_id:str, conn):
    cursor = conn.cursor()
    CHECK_CUSTOMER = "SELECT * FROM public.\"user\" WHERE telegram_id='{}'".format(telegram_id)
    cursor.execute(CHECK_CUSTOMER)
    row_count = cursor.rowcount
    if row_count > 0:
        row = cursor.fetchone()
        cursor.close()
        print(row[0])
        return True, row
    cursor.close()
    return False, None

def createUserImpl(userDto: UserDTO, conn):
    cursor = conn.cursor()
    CREATE_CUSTOMER = "INSERT INTO public.\"user\"(user_fname, user_lname, user_email, user_dob, user_type, parent_id, ref_code, telegram_id) VALUES(\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\')".format(
        userDto.userId,
        userDto.userFname,
        userDto.userLname,
        userDto.userEmail,
        userDto.userDob,
        userDto.userType,
        userDto.parentId,
        getRefCode())
    cursor.execute(CREATE_CUSTOMER)
    rowAffected = cursor.rowcount
    conn.commit()

    if rowAffected > 0:
        # Successful committing of new user into the database
        return True
    else:
        return False

def createJournalImpl(journalDto: JournalDTO, conn):
    cursor = conn.cursor()
    CREATE_JOURNAL = "INSERT INTO public.\"journal\"(journal_entry, sentiment, justification, created_ts, updated_ts, user_id) VALUES(\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\')".format(journalDto.journalEntry, journalDto.sentiment, journalDto.justification, getCurrentDt(), getCurrentDt(), journalDto.userId)
    cursor.execute(CREATE_JOURNAL)
    rowAffected = cursor.rowcount
    conn.commit()

    if rowAffected > 0:
        # Successful committing of new user into the database
        return True
    else:
        return False

def getJournalImpl(journalDto: JournalDTO, conn):
    print("nani")