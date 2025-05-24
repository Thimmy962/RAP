import sqlite3
import graphene
import graphql

db = "./db.sqlite3"


# Define sub-types
class PublisherType(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()

    # article = 

class AuthorType(graphene.ObjectType):
    id = graphene.Int()
    first_name = graphene.String()
    last_name = graphene.String()

class CategoryType(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()


class ArticleType(graphene.ObjectType):
    id = graphene.Int()
    title = graphene.String()
    abstract = graphene.String()
    content_path = graphene.String()
    published_in = graphene.Int()
    created_at = graphene.String()
    doi = graphene.String()
    slug = graphene.String()
    
    publisher = graphene.Field(PublisherType)
    authors = graphene.List(AuthorType)
    categories = graphene.List(CategoryType)

    def resolve_publisher(parent, info):
        with sqlite3.connect(db) as conn:
            conn.row_factory = sqlite3.Row
            command = f"SELECT * FROM publisher WHERE id = {parent['publisher_id']}"
            row = conn.execute(command).fetchone()
            return dict(row) if row else None



    def resolve_authors(parent, info):
        with sqlite3.connect(db) as conn:
            conn.row_factory = sqlite3.Row
            command = f"SELECT a.* FROM author a JOIN article_authors aa ON a.id = aa.author_id WHERE aa.article_id = {parent['id']}"
            rows = conn.execute(command).fetchall()
            return [dict(r) for r in rows]



    def resolve_categories(parent, info):
        with sqlite3.connect(db) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute("""
                SELECT c.* FROM category c
                JOIN article_categories ac ON c.id = ac.category_id
                WHERE ac.article_id = ?
            """, (parent['id'],)).fetchall()
            return [dict(r) for r in rows]



# Query root
class Query(graphene.ObjectType):
    article = graphene.Field(ArticleType, id=graphene.Int(required=True))
    articles = graphene.List(ArticleType, limit=graphene.Int(required=False), offset=graphene.Int(required=False))

    def resolve_article(root, info, id):
        with sqlite3.connect(db) as conn:
            conn.row_factory = sqlite3.Row
            command = (f"SELECT * FROM article WHERE id = {id}")
            row = conn.execute(command).fetchone()
            
            if row is None:
                raise graphql.GraphQLError(f"Article with id {id} not found")
            return dict(row)

    def resolve_articles(root, info, limit = 0, offset = 0):
        with sqlite3.connect(db) as conn:
            conn.row_factory = sqlite3.Row
            command = f"SELECT * FROM article LIMIT {limit} OFFSET {offset}"
            rows = conn.execute(command).fetchall()
            if rows is None:
                raise graphql.GraphQLError(f"Articles not found")
            return [dict(r) for r in rows]
    
        
    
    category = graphene.Field(CategoryType, id = graphene.Int(required = True))
    categories = graphene.List(CategoryType)

    def resolve_category(root, info, id):
        with sqlite3.connect(db) as conn:
            conn.row_factory = sqlite3.Row
            command = f"SELECT * FROM category WHERE id = {id}"
            row = conn.execute(command).fetchone()
            if row is None:
                raise graphql.GraphQLError(f"Category with id of {id} not found")
            return dict(row)

    def resolve_categories(root, info):
        with sqlite3.connect(db) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute("SELECT * FROM category")
            if rows is None:
                raise graphql.GraphQLError(f"Category not found")
            return [dict(row) for row in rows]


schema = graphene.Schema(query=Query)
