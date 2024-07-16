CREATE TABLE post (
  id INTEGER NOT NULL AUTO_INCREMENT,
  title VARCHAR(255) NOT NULL,
  content TEXT NOT NULL,
  description VARCHAR(255) NOT NULL,
  created_at DATETIME NOT NULL,
  PRIMARY KEY (id)
);

ALTER TABLE post ADD author VARCHAR(50) NOT NULL DEFAULT 0;
use  blog;
ALTER TABLE post ADD deleted_at datetime default NULL ;
#UPDATE post SET deleted_at = NULL WHERE deleted_at = '0000-00-00T00:00:00';
SELECT * FROM post;
ALTER TABLE post ADD updated_at datetime default NULL ;
DELETE FROM post;
UPDATE post SET author = 'Nguyễn Anh Thư' where id = 11

CREATE TABLE log_deleted (
  id INT AUTO_INCREMENT PRIMARY KEY,
  post_id INT NOT NULL,
  action ENUM('deleted', 'restored') NOT NULL,
  deleted_at DATETIME NOT NULL,
  restored_at DATETIME DEFAULT NULL,
  deleted_by VARCHAR(45),
  restored_by VARCHAR(45) DEFAULT NULL,
  FOREIGN KEY (post_id) REFERENCES post(id)
);
CREATE TABLE log_updated (
  id INT AUTO_INCREMENT PRIMARY KEY,
  post_id INT NOT NULL,
  updated_fields TEXT NOT NULL,
  updated_at DATETIME NOT NULL,
  updated_by VARCHAR(45),
  FOREIGN KEY (post_id) REFERENCES post(id)
);
CREATE TABLE post (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    content TEXT,
    description VARCHAR(255),
    created_at Datetime  NOT NULL ,
    updated_at TIMESTAMP NOT NULL ,
    author VARCHAR(50),
    deleted_at datetime not  NULL,
    is_published BOOLEAN DEFAULT FALSE
);
ALTER TABLE deleted_log
ADD CONSTRAINT fk_deleted_log_post FOREIGN KEY (blog_id) REFERENCES post(id);
ALTER TABLE log MODIFY COLUMN action VARCHAR(100);