CREATE TABLE IF NOT EXISTS "publisher" (
    "id" INTEGER,
    "name" TEXT,
    PRIMARY KEY ("id")
);


CREATE TABLE IF NOT EXISTS "category" (
    "id" INTEGER,
    "name" TEXT NOT NULL,
    PRIMARY KEY("id")
);

CREATE TABLE IF NOT EXISTS "author" (
    "id" INTEGER,
    "first_name" TEXT NOT NULL,
    "last_name" TEXT NOT NULL,
    PRIMARY KEY("id")
);

CREATE TABLE  IF NOT EXISTS "article" (
    "id" INTEGER,
    "title" TEXT NOT NULL,
    "abstract" TEXT NOT NULL,
    "content_path" TEXT NOT NULL,
    "published_in" INTEGER NOT NULL,
    "publisher_id" INTEGER,
    "created_at" NUMERIC NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "doi" TEXT,
    "slug" TEXT,
    PRIMARY KEY("id"),
    FOREIGN KEY ("publisher_id") REFERENCES "publisher"("id") ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS "article_authors" (
    "author_id" INTEGER NOT NULL,
    "article_id" INTEGER NOT NULL,
    PRIMARY KEY ("author_id", "article_id"),
    FOREIGN KEY ("author_id") REFERENCES "author"("id") ON DELETE CASCADE,
    FOREIGN KEY ("article_id") REFERENCES "article"("id") ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS "article_categories" (
    "category_id" INTEGER NOT NULL,
    "article_id" INTEGER NOT NULL,
    PRIMARY KEY ("category_id", "article_id"),
    FOREIGN KEY ("category_id") REFERENCES "category"("id") ON DELETE CASCADE,
    FOREIGN KEY ("article_id") REFERENCES "article"("id") ON DELETE CASCADE
);