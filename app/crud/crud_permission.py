from model.permission import Permission
from utils.db import db_mapping_rows_to_dict


def get_all_permission(db, is_active):
    result = (db.query(
            Permission
        ).filter_by(
            is_active = is_active,
        )
        .all())
    return result


def get_permission_by_uuid(db,permission_id):
    return (
        db.query(
            Permission.id
        ).filter(
            Permission.role_id==permission_id
        )
        .all()
    )


def get_permissions_for_menu(db, role_id,is_admin,is_coordinator,is_employee,lang):
    return (
        db.query(
            Permission
        ).filter(
            Permission.role_id==role_id,
            Permission.is_coordinator == is_coordinator,
            Permission.is_admin == is_admin,
            Permission.is_employee == is_employee,
            Permission.language == lang
        )
        .all()
    )


def get_permissions_by_lang(db, role_id,lang):
    return (
        db.query(
            Permission
        ).filter(
            Permission.role_id == role_id,
            Permission.language == lang
        )
        .all()
    )


def create_new_permission(db, new_permission):
    db_permission = None
    try:
        db_permission = Permission(
            name=new_permission.name,
            url = new_permission.url,
            icon = new_permission.icon,
            language = new_permission.language,
            is_coordinator = new_permission.is_coordinator,
            is_admin = new_permission.is_admin,
            is_employee = new_permission.is_employee,
            target = new_permission.target,
            order = new_permission.order,
            role_id=new_permission.role_id,
            new_window=new_permission.new_window,
        )
        db.add(db_permission)
        db.commit()
        db.refresh(db_permission)
    except Exception as ex:
        db_permission = None
        print(f"No se pudo guardar en la base de datos: {ex}")
    return db_permission


def crud_update_permission(db, permission_id, modify_permission):
    rows_updated = (
        db.query(Permission)
        .filter_by(id=permission_id)
        .update(
            modify_permission,
            synchronize_session="fetch",
        )
    )
    db.commit()
    return rows_updated
