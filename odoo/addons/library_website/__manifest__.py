{
    "name": "Library Website",
    "description": "Create and check book checkout requests.",
    "author": "GwyddionGames",
    "depends": ["library_checkout", "website"],
    "data": [
        "security/ir.model.access.csv",
        "security/library_security.xml",
        "views/library_member.xml",
        "views/website_assets.xml",
        "views/checkout_template.xml",
    ],
}
