from main import UserDTO, JournalDTO
from datetime import datetime
import string, random

def getCurrentDt():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def getRefCode():
    allowed_characters = string.ascii_letters + string.digits
    confusing_chars = "IlO0o"
    allowed_characters = ''.join(c for c in allowed_characters if c not in confusing_chars)
    random_string = ''.join(random.choice(allowed_characters) for _ in range(8))
    return random_string

def mapUserDbToUserDTO(rowObj):
    userDto = UserDTO()
    userDto.userId = rowObj[0]
    userDto.userFname = rowObj[1]
    userDto.userLname = rowObj[2]
    userDto.userEmail = rowObj[3]
    userDto.userDob = rowObj[4]
    userDto.userType = rowObj[5]
    userDto.parentId = rowObj[6]
    userDto.refCode = rowObj[7]
    userDto.foodLikes = rowObj[8]
    userDto.foodDislikes = rowObj[9]
    return userDto

def mapJournalToDTO(rowObj):
    journalDto = JournalDTO()
    journalDto.journalId = rowObj[0]
    journalDto.journalEntry = rowObj[1]
    journalDto.sentiment = rowObj[2]
    journalDto.emotion = rowObj[3]
    journalDto.userId = rowObj[4]
    return journalDto

def checkUserImpl(telegram_id:str, conn):
    cursor = conn.cursor()
    CHECK_CUSTOMER = "SELECT * FROM public.user WHERE user_id='{}'".format(telegram_id)
    cursor.execute(CHECK_CUSTOMER)
    row_count = cursor.rowcount
    if row_count > 0:
        row = cursor.fetchone()
        cursor.close()
        userData = mapUserDbToUserDTO(row)
        return True, userData
    cursor.close()
    return False, None

def createUserImpl(userDto: UserDTO, conn):
    cursor = conn.cursor()
    CREATE_CUSTOMER = "INSERT INTO public.user(user_id, user_fname, user_lname, user_email, user_dob, user_type, parent_id, ref_code) VALUES(\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\')".format(
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
    CREATE_JOURNAL = "INSERT INTO public.journal(journal_entry, sentiment, emotion, justification, created_ts, updated_ts, user_id) VALUES(\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\')".format(
        journalDto.journalEntry, 
        journalDto.sentiment, 
        journalDto.emotion,
        journalDto.justification, 
        getCurrentDt(), 
        getCurrentDt(), 
        journalDto.userId)
    cursor.execute(CREATE_JOURNAL)
    rowAffected = cursor.rowcount
    conn.commit()

    if rowAffected > 0:
        # Successful committing of new user into the database
        return True
    else:
        return False

def getJournalImpl(user_id:str, conn):
    cursor = conn.cursor()
    CHECK_CUSTOMER = "SELECT journal_id, journal_entry, sentiment, emotion, user_id FROM public.journal WHERE user_id='{}'".format(user_id)
    cursor.execute(CHECK_CUSTOMER)
    row_count = cursor.rowcount
    if row_count > 0:
        rows = cursor.fetchall()
        cursor.close()
        journalList = []
        for row in rows:
            print(row)
            journalList.append(mapJournalToDTO(row))
        return True, journalList
    cursor.close()
    return False, None

