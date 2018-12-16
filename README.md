# Distributed databases

This is a course project for Data-Intensive Software Systems course. 

We are using one primary Cloud SQL instance that handles writing, and we also have a read replica of the primary database. In case of failure, a failover replica is taken into use automaticly, and read replica is generated for that instance as well.
https://cloud.google.com/sql/docs/mysql/high-availability
