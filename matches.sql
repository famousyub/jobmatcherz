 CREATE TABLE IF NOT EXISTS job_offers (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255),
        skills TEXT
 );


   CREATE TABLE IF NOT EXISTS candidate_skills (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        skills TEXT
    );