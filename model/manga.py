from flask_restx import fields, Model

manga = Model(
    "Manga",
    {
        "name": fields.String(required=True, description="Name of the manga book"),
        "img": fields.String(required=True, description="Image of the manga book"),
        "link": fields.String(required=True, description="Link of the manga book"),
        "publisher": fields.String(
            required=True, description="Publisher of the manga book"
        ),
    },
)
