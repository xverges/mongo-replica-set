
admin = db.getSiblingDB("admin");

admin.createUser(
  {
    user: "xv_mongo_rw",
    pwd: "mongo_password",
    roles: [ "readWriteAnyDatabase" ]
  }
);

admin.createUser(
  {
    user: "xv_mongo_ro",
    pwd: "mongo_password",
    roles: [ "readAnyDatabase" ]
  }
);

