from math import ceil


def pagination(form, page, limit):
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page yoki limit 0 dan kichik kiritilmasligi kerak")
    elif page and limit:
        return {"current_page": page, "limit": limit, "pages": ceil(form.count() / limit),
            "data": form.offset((page - 1) * limit).limit(limit).all()}
    else:
        return {"data": form.all()}


"""
created -> payment -> land_preparation -> overheads -> upload_products -> reception -> rules -> planting -> control -> warranty
"""
status_dict={
    'created': "payment",
    "payment": "land_preparation",
    "land_preparation": "overheads",
    "overheads": "upload_products",
    "upload_products": "reception",
    "reception": "rules",
    "rules": "planting",
    "planting": "control",
    "control": "warranty",
    "warranty": "warranty"

}
