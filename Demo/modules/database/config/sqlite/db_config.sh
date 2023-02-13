#!/bin/bash

# Location of the SQLite database file
DB_FILE="CRAN.db"

# Function to handle errors
error_exit()
{
    echo "$1" 1>&2
    exit 1
}

# Create the package table
echo "Creating the packages table..."
sqlite3 $DB_FILE << EOF
CREATE TABLE packages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    version TEXT NOT NULL,
    publication_date DATE NOT NULL,
    requires_compilation INTEGER NOT NULL,
    in_cran INTEGER,
    in_bioconductor INTEGER,
    mantainer TEXT NOT NULL,
    author_data TEXT,
    license TEXT NOT NULL
);
EOF
if [ $? -ne 0 ]; then
    error_exit "Error creating the packages table"
fi

# Create the dependencies table
echo "Creating the dependencies table..."
sqlite3 $DB_FILE << EOF
CREATE TABLE dependencies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    version TEXT NOT NULL,
    type TEXT NOT NULL
);
EOF
if [ $? -ne 0 ]; then
    error_exit "Error creating the dependencies table"
fi

# Create the package_dependency table
echo "Creating the package_dependency table..."
sqlite3 $DB_FILE << EOF
CREATE TABLE package_dependency (
    package_id INTEGER NOT NULL,
    dependency_id INTEGER NOT NULL,
    PRIMARY KEY (package_id, dependency_id),
    FOREIGN KEY (package_id) REFERENCES packages(id),
    FOREIGN KEY (dependency_id) REFERENCES dependencies(id)
);
EOF
if [ $? -ne 0 ]; then
    error_exit "Error creating the package_dependency table"
fi

# Create the links table
echo "Creating the links table..."
sqlite3 $DB_FILE << EOF
CREATE TABLE links (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT NOT NULL,
    package_id INTEGER NOT NULL,
    FOREIGN KEY (package_id) REFERENCES packages(id)
);
EOF
if [ $? -ne 0 ]; then
    error_exit "Error creating the links table"
fi

# Create the package_link table
echo "Creating the package_link table..."
sqlite3 $DB_FILE << EOF
CREATE TABLE package_link (
    package_id INTEGER NOT NULL,
    url_id INTEGER NOT NULL,
    PRIMARY KEY (package_id, url_id),
    FOREIGN KEY (package_id) REFERENCES packages(id),
    FOREIGN KEY (url_id) REFERENCES links(id)
);
EOF
if [ $? -ne 0 ]; then
    error_exit "Error creating the package_link table"
fi

echo "All tables created"
