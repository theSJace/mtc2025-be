from main import UserDTO, JournalDTO, HobbyDTO
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

# START OF MAPPING FUNCTIONS
def mapUserDbToUserDTO(rowObj):
    userDto = UserDTO()
    userDto.userId = rowObj[0]
    userDto.userNickName = rowObj[1]
    userDto.userEmail = rowObj[2]
    userDto.userDob = rowObj[3]
    userDto.userType = rowObj[4]
    userDto.parentId = rowObj[5]
    userDto.refCode = rowObj[6]
    userDto.foodLikes = rowObj[7]
    userDto.foodDislikes = rowObj[8]
    userDto.hobbies = rowObj[9]
    return userDto

def mapJournalToDTO(rowObj):
    journalDto = JournalDTO()
    journalDto.journalId = rowObj[0]
    journalDto.journalEntry = rowObj[1]
    journalDto.sentiment = rowObj[2]
    journalDto.emotion = rowObj[3]
    journalDto.userId = rowObj[4]
    return journalDto
# END OF MAPPING FUNCTIONS

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
    CREATE_CUSTOMER = "INSERT INTO public.user(user_id, user_nickname, user_email, user_dob, user_type, parent_id, ref_code, food_likes, food_dislikes, hobbies) VALUES(\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\')".format(
        userDto.userId,
        userDto.userNickName,
        userDto.userEmail,
        userDto.userDob,
        userDto.userType,
        userDto.parentId,
        getRefCode(),
        userDto.foodLikes,
        userDto.foodDislikes,
        userDto.hobbies
        )
    cursor.execute(CREATE_CUSTOMER)
    rowAffected = cursor.rowcount
    conn.commit()

    if rowAffected > 0:
        # Successful committing
        return True
    else:
        return False

def updateUserImpl(userDto:UserDTO, conn):
    cursor = conn.cursor()
    CREATE_JOURNAL = "UPDATE public.user SET user_email=\'{}\', food_likes=\'{}\', food_dislikes=\'{}\', hobbies=\'{}\' WHERE user_id=\'{}\';".format(
        userDto.userEmail,
        userDto.foodLikes,
        userDto.foodDislikes,
        userDto.hobbies,
        userDto.userId)
    cursor.execute(CREATE_JOURNAL)
    rowAffected = cursor.rowcount
    conn.commit()

    if rowAffected > 0:
        # Successful committing
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
    print(CREATE_JOURNAL)
    cursor.execute(CREATE_JOURNAL)
    rowAffected = cursor.rowcount
    conn.commit()

    if rowAffected > 0:
        # Successful committing
        return True
    else:
        return False

def getJournalImpl(user_id:str, conn):
    journalList = []
    cursor = conn.cursor()
    CHECK_CUSTOMER = "SELECT journal_id, journal_entry, sentiment, emotion, user_id FROM public.journal WHERE user_id='{}'".format(user_id)
    cursor.execute(CHECK_CUSTOMER)
    row_count = cursor.rowcount
    if row_count > 0:
        rows = cursor.fetchall()
        cursor.close()
        for row in rows:
            print(row)
            journalList.append(mapJournalToDTO(row))
    cursor.close()
    return True, journalList

def updateJournalImpl(journalDto:JournalDTO, conn):
    cursor = conn.cursor()
    CREATE_JOURNAL = "UPDATE public.journal SET journal_entry=\'{}\', sentiment=\'{}\', emotion=\'{}\', justification=\'{}\', updated_ts=\'{}\' WHERE journal_id=\'{}\';".format(
        journalDto.journalEntry, 
        journalDto.sentiment, 
        journalDto.emotion,
        journalDto.justification, 
        getCurrentDt(), 
        journalDto.journalId)
    cursor.execute(CREATE_JOURNAL)
    rowAffected = cursor.rowcount
    conn.commit()

    if rowAffected > 0:
        # Successful committing
        return True
    else:
        return False

def getHobbyImpl(hobbyDto:HobbyDTO, conn):
    userArr = hobbyDto.userId.split(",")
    cursor = conn.cursor()
    hobbyList = []
    for user in userArr:
        GET_HOBBY = "SELECT hobbies FROM public.user WHERE user_id='{}'".format(user)
        cursor.execute(GET_HOBBY)
        row_count = cursor.rowcount
        if row_count > 0:
            row = cursor.fetchone()
            hobbyArr = row[0].split(",")
            for hobby in hobbyArr:
                hobbyList.append(hobby)
    cursor.close()
    return hobbyList