CREATE TABLE IF NOT EXISTS "user"(
    "user_id" VARCHAR NOT NULL PRIMARY KEY,
    "user_fname" varchar(255) NOT NULL,
    "user_lname" varchar(255) NOT NULL,
    "user_email" varchar(255) NOT NULL,
    "user_dob" varchar(10) NOT NULL,
    "user_type" varchar(6) NOT NULL,
    "parent_id" varchar(8),
	"ref_code" varchar(8) NOT NULL,
	"food_likes" text,
	"food_dislikes" text
);

CREATE TABLE IF NOT EXISTS "journal"(
    "journal_id" SERIAL NOT NULL PRIMARY KEY,
    "journal_entry" text NOT NULL,
    "sentiment" varchar(8) NOT NULL,
    "justification" text NOT NULL,
    "created_ts" timestamp NOT NULL DEFAULT NOW(),
    "updated_ts" timestamp NOT NULL DEFAULT NOW(),
    "user_id" int NOT NULL REFERENCES "user"("user_id")
);