from model.role import Role


def get_all_role(db, is_active):
    return (
        db.query(Role)
        .filter_by(
            is_active=is_active,
        )
        .all()
    )


def get_role_by_uuid(db, role_id):
    return (
        db.query(Role)
        .filter_by(
            id=role_id,
        )
        .first()
    )


def create_new_role(db, new_role):
    db_role = None
    try:
        db_role = Role(name=new_role.name)
        db.add(db_role)
        db.commit()
        db.refresh(db_role)
    except Exception as ex:
        db_role = None
        print(f"No se pudo guardar en la base de datos: {ex}")
    return db_role


def crud_update_role(db, role_id, modify_role):
    rows_updated = (
        db.query(Role)
        .filter_by(
            id=role_id,
        )
        .update(
            modify_role,
            synchronize_session="fetch",
        )
    )
    db.commit()
    return rows_updated
