##### upgrade #####
CREATE TABLE IF NOT EXISTS "chat_chatmessage" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "room_id" INT,
    "username" VARCHAR(50),
    "message" TEXT NOT NULL,
    "message_type" VARCHAR(50),
    "image_caption" VARCHAR(50),
    "date_created" TIMESTAMP   DEFAULT CURRENT_TIMESTAMP
) /* use to store chat history message */;
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" TEXT NOT NULL
);
