rs.initiate(
    {
       _id: "${REPLICASET_NAME}",
       version: 1,
       members: [
          { _id: 0, host : "${FIRST_IP}:27017" }
       ]
    }
)

// Commented out because that's too early: we have to wait until
// FIRST shows PRIMARY in its status.

// rs.add("${SECOND_IP}:27017")
// rs.addArb("${ARBITRER_IP}:27017")