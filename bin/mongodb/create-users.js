/**
 * Created by Javier on 07/04/2017.
 */

db = db.getSiblingDB('admin');
if (!db.getUser('bisite')) {
    db.createUser({
        user:"bisite",
        pwd:"bisite00",
        roles: [
            "root"
        ]
    });
}

db = db.getSiblingDB('innhome');
if (!db.getUser('innhome')) {
    db.createUser({
        user:"innhome",
        pwd:"innhome00",
        roles: [
            "readWrite"
        ]
    });
}

db = db.getSiblingDB('celery');
if (!db.getUser('celery')) {
    db.createUser({
        user:"celery",
        pwd:"celery00",
        roles: [
            "readWrite"
        ]
    });
}